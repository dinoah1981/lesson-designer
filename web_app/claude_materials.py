"""
Claude-Direct Material Generation

This module generates lesson materials by asking Claude to write python-pptx
and python-docx code, then executing that code. This mirrors how Claude works
when used directly - it writes the code, we run it.

No JSON intermediaries. No dumb rendering. Just Claude creating materials
the way it would if you were chatting with it directly.
"""

import json
import os
import tempfile
import traceback
from pathlib import Path
from typing import Dict, List, Any
import anthropic

# These imports are made available to Claude's generated code
import sys


MATERIAL_GENERATION_INSTRUCTIONS = '''
## Material Creation Guidelines

### Slide Deck (PPTX)

**Slide 1 (Hidden):** Lesson plan in this format:
```
Lesson Agenda with Notes/Materials
Objective: [Student-friendly daily objective]
1. Do Now (5-7 mins): [Activity + notes]
2. Framing (3 mins): [Hook + key concept]
3. Notes/Discussion (10 mins): [Content + discussion prompts]
4. Practice/Application (20 mins): [Activity + materials reference]
5. Exit Ticket (7 mins): [Assessment task]
```

**Slide 2 (After Do Now):** Objective in Context
- Show the day's objective
- Connect to the unit theme/topic
- Frame how today fits with what students have been learning

**Remaining slides:** Teaching slides supporting lesson execution

**Formatting:**
- Helvetica font throughout
- Minimum 16pt font size for body, larger for titles
- Clean, appealing visual style
- Sparse content - talking points, not paragraphs
- Include discussion prompts, activity instructions, key content
- NO TEXT CUTOFF - ensure all text fits within slide boundaries

### Student Worksheet (DOCX)

**Formatting:** Helvetica font throughout, double-spaced answer lines

**The worksheet must match what the activities actually require:**
- If an activity uses a graphic organizer → include that graphic organizer
- If an activity needs data tables → include actual data tables
- If an activity has discussion questions → include those specific questions
- If an activity references "investigation sheets" or "station cards" → those go in supplementary materials

**Structure varies by lesson type but always includes:**
1. Clear sections matching lesson activities
2. Appropriate response formats (tables, organizers, answer lines)
3. Adequate writing space
4. Exit Ticket at the end

### Supplementary Materials (Station Cards, Data Sheets, etc.)

When lessons include group activities, stations, or investigations that reference specific materials, create those materials in a separate document.

**CRITICAL — Follow the Discovery Principle:**

- **DO NOT give away answers.** Cards should provide raw information, data, scenarios, or primary-source-style context that students must analyze to arrive at conclusions themselves.
- **Limit to 1–2 thought-provoking questions per card.** Questions should require synthesis, not fact-finding.
- **Provide enough information for students to figure it out through discussion** — not so much that the answer is obvious, and not so little that they're guessing.
- **Avoid leading language.** Don't say "This shows X because…" — provide the data and let students draw conclusions.

**Good card structure:**
1. Topic/region title
2. Context paragraph (scene-setting, not answer-giving)
3. 3–5 data points, statistics, or real-world examples
4. 1–2 discussion questions requiring analysis
5. Space for students to record key takeaway

### Design Principles

- Exit tickets assess mastery of the daily objective
- Discussion prompts should be accessible and promote thinking
- Group materials should make students do the thinking — provide evidence, not conclusions
- Materials should be classroom-ready, not drafts
'''


def generate_all_materials(
    client: anthropic.Anthropic,
    lesson: Dict[str, Any],
    output_dir: str,
    persona_feedback: List[Dict] = None,
    selected_concerns: List[Dict] = None,
    generate_modified: bool = False,
    generate_extension: bool = False
) -> Dict[str, str]:
    """
    Generate all materials by having Claude write the code to create them.

    Returns dict with paths to generated files.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {}

    # Generate slides
    slides_path = output_dir / "slides.pptx"
    try:
        _generate_slides_with_claude(client, lesson, persona_feedback, selected_concerns, str(slides_path))
        if slides_path.exists():
            result['slides_path'] = str(slides_path)
    except Exception as e:
        print(f"Error generating slides: {e}")
        traceback.print_exc()

    # Generate worksheet
    worksheet_path = output_dir / "worksheet.docx"
    try:
        _generate_worksheet_with_claude(client, lesson, persona_feedback, selected_concerns, str(worksheet_path))
        if worksheet_path.exists():
            result['worksheet_path'] = str(worksheet_path)
    except Exception as e:
        print(f"Error generating worksheet: {e}")
        traceback.print_exc()

    # Generate supplementary materials if the lesson has activities that need them
    supplementary_paths = []
    try:
        supp_path = output_dir / "supplementary_materials.docx"
        if _generate_supplementary_with_claude(client, lesson, persona_feedback, selected_concerns, str(supp_path)):
            if supp_path.exists():
                supplementary_paths.append(str(supp_path))
    except Exception as e:
        print(f"Error generating supplementary: {e}")
        traceback.print_exc()

    if supplementary_paths:
        result['supplementary_paths'] = supplementary_paths

    # Generate modified worksheet if requested
    if generate_modified and persona_feedback:
        modified_path = output_dir / "worksheet_modified.docx"
        try:
            _generate_modified_worksheet_with_claude(client, lesson, persona_feedback, selected_concerns, str(modified_path))
            if modified_path.exists():
                result['modified_worksheet_path'] = str(modified_path)
        except Exception as e:
            print(f"Error generating modified worksheet: {e}")
            traceback.print_exc()

    # Generate extension worksheet if requested
    if generate_extension and persona_feedback:
        extension_path = output_dir / "worksheet_extension.docx"
        try:
            _generate_extension_worksheet_with_claude(client, lesson, persona_feedback, selected_concerns, str(extension_path))
            if extension_path.exists():
                result['extension_worksheet_path'] = str(extension_path)
        except Exception as e:
            print(f"Error generating extension worksheet: {e}")
            traceback.print_exc()

    return result


def _build_context(lesson: Dict, persona_feedback: List[Dict] = None, selected_concerns: List[Dict] = None) -> str:
    """Build the context section of the prompt with lesson and feedback info."""

    context = f"""
## Lesson Information

**Title:** {lesson.get('title', 'Untitled Lesson')}
**Grade Level:** {lesson.get('grade_level', 'Not specified')}
**Duration:** {lesson.get('duration', 50)} minutes
**Objective:** {lesson.get('objective', 'Not specified')}
**Lesson Type:** {lesson.get('lesson_type', 'introducing')}

### Activities:
"""

    for i, activity in enumerate(lesson.get('activities', []), 1):
        context += f"""
**Activity {i}: {activity.get('name', 'Untitled')}**
- Duration: {activity.get('duration', '?')} minutes
- Type: {activity.get('marzano_level', 'Not specified')}
- Instructions: {activity.get('instructions', activity.get('student_directions', 'None'))}
- Materials: {activity.get('materials', 'None')}
- Student Output: {activity.get('student_output', 'Not specified')}
"""
        if activity.get('differentiation'):
            diff = activity['differentiation']
            if diff.get('support'):
                context += f"- Support: {diff['support']}\n"
            if diff.get('extension'):
                context += f"- Extension: {diff['extension']}\n"

    # Add vocabulary if present
    vocab = lesson.get('vocabulary', [])
    if vocab:
        context += "\n### Key Vocabulary:\n"
        for term in vocab:
            if isinstance(term, dict):
                context += f"- **{term.get('word', term.get('term', ''))}**: {term.get('definition', '')}\n"
            else:
                context += f"- {term}\n"

    # Add assessment info
    assessment = lesson.get('assessment', {})
    if assessment:
        context += f"\n### Assessment:\n"
        context += f"- Type: {assessment.get('type', 'exit_ticket')}\n"
        context += f"- Description: {assessment.get('description', '')}\n"
        if assessment.get('questions'):
            context += "- Questions:\n"
            for q in assessment['questions']:
                context += f"  - {q}\n"

    # Add persona feedback if provided
    if persona_feedback:
        context += "\n## Persona Feedback Received:\n"
        for fb in persona_feedback:
            context += f"\n**{fb.get('persona_name', 'Persona')}** (Rating: {fb.get('overall_rating', '?')}/5)\n"
            context += f"Reaction: {fb.get('reaction', 'No reaction')}\n"
            if fb.get('concerns'):
                context += "Key Concerns:\n"
                for c in fb['concerns'][:5]:
                    context += f"- {c.get('element', '')}: {c.get('issue', '')}\n"

    # Add selected concerns to address
    if selected_concerns:
        context += "\n## Selected Concerns to Address:\n"
        for c in selected_concerns:
            context += f"- [{c.get('from_persona', '')}] {c.get('element', '')}: {c.get('issue', '')}\n"
            if c.get('recommendation'):
                context += f"  Recommendation: {c['recommendation']}\n"

    return context


def _execute_generated_code(code: str, output_path: str) -> bool:
    """Execute Claude-generated code to create a file."""

    # Create a safe execution environment with necessary imports
    exec_globals = {
        '__builtins__': __builtins__,
        'output_path': output_path,
    }

    # Add common imports that Claude's code will need
    setup_code = '''
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

from docx import Document
from docx.shared import Pt as DocxPt, Inches as DocxInches, Twips, RGBColor as DocxRGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn as docx_qn
from docx.oxml import OxmlElement

import os
'''

    full_code = setup_code + "\n" + code

    try:
        exec(full_code, exec_globals)
        return True
    except Exception as e:
        print(f"Error executing generated code: {e}")
        print(f"Code was:\n{code[:500]}...")
        traceback.print_exc()
        return False


def _generate_slides_with_claude(
    client: anthropic.Anthropic,
    lesson: Dict,
    persona_feedback: List[Dict],
    selected_concerns: List[Dict],
    output_path: str
) -> bool:
    """Have Claude write python-pptx code to create slides, then execute it."""

    context = _build_context(lesson, persona_feedback, selected_concerns)

    prompt = f"""You are creating a PowerPoint slide deck for a teacher. Write python-pptx code that creates professional, classroom-ready slides.

{context}

{MATERIAL_GENERATION_INSTRUCTIONS}

Write Python code using python-pptx that:
1. Creates a professional slide deck for this lesson
2. Slide 1 should be HIDDEN and contain the full lesson plan for the teacher
3. Slide 2 shows the objective and connects to prior learning
4. Remaining slides support each activity with clean, sparse content
5. Uses good visual design - colored headers, proper spacing, readable fonts
6. All text must fit within slide boundaries (no cutoff)
7. Includes presenter notes with teaching guidance

The output file path is stored in the variable `output_path`.

Write ONLY the Python code, no explanations. The code will be executed directly.
Start with creating the Presentation object and end with prs.save(output_path).

```python
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.content[0].text

    # Extract code from markdown if present
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]

    return _execute_generated_code(code, output_path)


def _generate_worksheet_with_claude(
    client: anthropic.Anthropic,
    lesson: Dict,
    persona_feedback: List[Dict],
    selected_concerns: List[Dict],
    output_path: str
) -> bool:
    """Have Claude write python-docx code to create worksheet, then execute it."""

    context = _build_context(lesson, persona_feedback, selected_concerns)

    prompt = f"""You are creating a student worksheet for a teacher. Write python-docx code that creates a professional, classroom-ready worksheet.

{context}

{MATERIAL_GENERATION_INSTRUCTIONS}

Write Python code using python-docx that:
1. Creates a worksheet that MATCHES what the lesson activities actually require
2. If an activity uses a graphic organizer, include that specific organizer structure
3. If an activity needs data tables, include actual tables with headers
4. If an activity has specific questions, include those questions
5. Uses proper formatting - Helvetica font, adequate spacing, clear sections
6. Includes an Exit Ticket at the end
7. Has a header with title, name, date, period fields

The output file path is stored in the variable `output_path`.

Write ONLY the Python code, no explanations. The code will be executed directly.
Start with creating the Document object and end with doc.save(output_path).

```python
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.content[0].text

    # Extract code from markdown if present
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]

    return _execute_generated_code(code, output_path)


def _generate_supplementary_with_claude(
    client: anthropic.Anthropic,
    lesson: Dict,
    persona_feedback: List[Dict],
    selected_concerns: List[Dict],
    output_path: str
) -> bool:
    """Have Claude write python-docx code for supplementary materials if needed."""

    # Check if any activities reference materials that need to be created
    needs_supplementary = False
    materials_needed = []

    for activity in lesson.get('activities', []):
        materials = activity.get('materials', [])
        if isinstance(materials, str):
            materials = [materials]

        for mat in materials:
            mat_lower = mat.lower() if isinstance(mat, str) else ''
            if any(keyword in mat_lower for keyword in ['card', 'sheet', 'handout', 'packet', 'brief', 'data', 'organizer', 'template']):
                needs_supplementary = True
                materials_needed.append(f"- {activity.get('name', 'Activity')}: {mat}")

    if not needs_supplementary:
        return False

    context = _build_context(lesson, persona_feedback, selected_concerns)

    prompt = f"""You are creating supplementary materials (station cards, data sheets, etc.) for a lesson. Write python-docx code that creates these materials.

{context}

**Materials specifically needed:**
{chr(10).join(materials_needed)}

{MATERIAL_GENERATION_INSTRUCTIONS}

**CRITICAL: Follow the Discovery Principle** - provide data and evidence for students to analyze, NOT pre-made conclusions. Cards should make students THINK, not just copy answers.

Write Python code using python-docx that creates the supplementary materials referenced in the lesson. Each card/sheet should:
1. Have a clear title
2. Provide raw information, data, or scenarios (NOT conclusions)
3. Include 1-2 analysis questions
4. Have space for students to record their takeaways

The output file path is stored in the variable `output_path`.

Write ONLY the Python code, no explanations. The code will be executed directly.
Start with creating the Document object and end with doc.save(output_path).

```python
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.content[0].text

    # Extract code from markdown if present
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]

    return _execute_generated_code(code, output_path)


def _generate_modified_worksheet_with_claude(
    client: anthropic.Anthropic,
    lesson: Dict,
    persona_feedback: List[Dict],
    selected_concerns: List[Dict],
    output_path: str
) -> bool:
    """Generate a modified worksheet with scaffolds for struggling learners."""

    context = _build_context(lesson, persona_feedback, selected_concerns)

    # Extract Alex's concerns specifically
    alex_concerns = []
    for fb in (persona_feedback or []):
        if 'alex' in fb.get('persona_name', '').lower() or 'struggling' in fb.get('persona_name', '').lower():
            alex_concerns = fb.get('concerns', [])
            break

    concerns_text = ""
    if alex_concerns:
        concerns_text = "\n**Specific concerns to address:**\n"
        for c in alex_concerns[:5]:
            concerns_text += f"- {c.get('element', '')}: {c.get('issue', '')}\n"

    prompt = f"""You are creating a MODIFIED worksheet for struggling learners and ELL students. This should have the SAME learning objectives but with added scaffolds.

{context}
{concerns_text}

Create a modified version that includes:
1. **Word banks** for vocabulary-heavy sections
2. **Sentence starters** for open-ended questions
3. **Simplified language** where appropriate (but same rigor)
4. **Visual supports** and graphic organizers
5. **Chunked instructions** - break complex tasks into steps
6. Same Exit Ticket content (this is for assessment)

The output file path is stored in the variable `output_path`.

Write ONLY the Python code using python-docx, no explanations.

```python
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.content[0].text

    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]

    return _execute_generated_code(code, output_path)


def _generate_extension_worksheet_with_claude(
    client: anthropic.Anthropic,
    lesson: Dict,
    persona_feedback: List[Dict],
    selected_concerns: List[Dict],
    output_path: str
) -> bool:
    """Generate an extension worksheet with challenges for advanced learners."""

    context = _build_context(lesson, persona_feedback, selected_concerns)

    # Extract Marcus's concerns specifically
    marcus_concerns = []
    for fb in (persona_feedback or []):
        if 'marcus' in fb.get('persona_name', '').lower() or 'high achieving' in fb.get('persona_name', '').lower():
            marcus_concerns = fb.get('concerns', [])
            break

    concerns_text = ""
    if marcus_concerns:
        concerns_text = "\n**Specific concerns to address:**\n"
        for c in marcus_concerns[:5]:
            concerns_text += f"- {c.get('element', '')}: {c.get('issue', '')}\n"

    prompt = f"""You are creating an EXTENSION worksheet for advanced/gifted learners. This should have the SAME core objectives but with added depth and challenge.

{context}
{concerns_text}

Create an extension version that includes:
1. **More complex questions** requiring deeper analysis
2. **Research prompts** for independent inquiry
3. **Open-ended challenges** without single correct answers
4. **Cross-curricular connections** where appropriate
5. **Creative application** opportunities
6. Same Exit Ticket core content, but with an extension question

The output file path is stored in the variable `output_path`.

Write ONLY the Python code using python-docx, no explanations.

```python
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.content[0].text

    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]

    return _execute_generated_code(code, output_path)
