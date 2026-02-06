"""
Claude-Direct Material Generation

This module generates lesson materials by asking Claude to write python-pptx
and python-docx code, then executing that code. This mirrors how Claude works
when used directly.

One API call per lesson generates ALL materials for that lesson together,
keeping everything coherent and aligned.
"""

import json
import traceback
from pathlib import Path
from typing import Dict, List, Any
import anthropic


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

**Slide 2:** Objective in Context
- Show the day's objective
- Connect to the unit theme/topic
- Frame how today fits with what students have been learning

**Remaining slides:** Teaching slides supporting lesson execution

**Formatting:**
- Helvetica font throughout
- Minimum 16pt font size for body, larger for titles
- Clean, appealing visual style
- Sparse content - talking points, not paragraphs (3-5 bullets max)
- Include discussion prompts, activity instructions, key content
- NO TEXT CUTOFF - ensure all text fits within slide boundaries
- Include presenter notes with SAY/ASK/WATCH FOR guidance

### Student Worksheet (DOCX)

**Formatting:** Helvetica font throughout, double-spaced answer lines

**The worksheet must match what the activities actually require:**
- If an activity uses a graphic organizer → include that graphic organizer
- If an activity needs data tables → include actual data tables
- If an activity has discussion questions → include those specific questions
- If an activity references "investigation sheets" or "station cards" → those go in supplementary materials

**Structure:**
1. Header with title, name, date, period fields
2. Clear sections matching lesson activities
3. Appropriate response formats (tables, organizers, answer lines)
4. Adequate writing space (more for complex thinking tasks)
5. Exit Ticket at the end

### Supplementary Materials (Station Cards, Data Sheets, etc.)

When lessons include group activities, stations, or investigations that reference specific materials, create those materials.

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
- ALL materials for a lesson should be coherent and aligned with each other
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
    Generate all materials for a lesson in a single Claude call.

    This keeps everything coherent - slides, worksheet, and supplementary
    materials are all created together with full awareness of each other.

    Returns dict with paths to generated files.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    result = {}

    # Determine what materials are needed
    needs_supplementary = _check_needs_supplementary(lesson)

    # Build paths
    slides_path = output_dir / "slides.pptx"
    worksheet_path = output_dir / "worksheet.docx"
    supplementary_path = output_dir / "supplementary_materials.docx" if needs_supplementary else None
    modified_path = output_dir / "worksheet_modified.docx" if generate_modified else None
    extension_path = output_dir / "worksheet_extension.docx" if generate_extension else None

    # Generate all materials in one call
    try:
        success = _generate_lesson_materials(
            client=client,
            lesson=lesson,
            persona_feedback=persona_feedback,
            selected_concerns=selected_concerns,
            slides_path=str(slides_path),
            worksheet_path=str(worksheet_path),
            supplementary_path=str(supplementary_path) if supplementary_path else None,
            modified_path=str(modified_path) if modified_path else None,
            extension_path=str(extension_path) if extension_path else None
        )

        if success:
            if slides_path.exists():
                result['slides_path'] = str(slides_path)
            if worksheet_path.exists():
                result['worksheet_path'] = str(worksheet_path)
            if supplementary_path and supplementary_path.exists():
                result['supplementary_paths'] = [str(supplementary_path)]
            if modified_path and modified_path.exists():
                result['modified_worksheet_path'] = str(modified_path)
            if extension_path and extension_path.exists():
                result['extension_worksheet_path'] = str(extension_path)

    except Exception as e:
        print(f"Error generating materials: {e}")
        traceback.print_exc()

    return result


def _check_needs_supplementary(lesson: Dict) -> bool:
    """Check if any activities reference materials that need to be created."""
    for activity in lesson.get('activities', []):
        materials = activity.get('materials', [])
        if isinstance(materials, str):
            materials = [materials]

        for mat in materials:
            mat_lower = mat.lower() if isinstance(mat, str) else ''
            if any(keyword in mat_lower for keyword in [
                'card', 'sheet', 'handout', 'packet', 'brief', 'data',
                'organizer', 'template', 'station', 'investigation'
            ]):
                return True
    return False


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
        context += "\n## Selected Concerns to Address in Materials:\n"
        for c in selected_concerns:
            context += f"- [{c.get('from_persona', '')}] {c.get('element', '')}: {c.get('issue', '')}\n"
            if c.get('recommendation'):
                context += f"  Recommendation: {c['recommendation']}\n"

    return context


def _execute_generated_code(code: str, context_vars: Dict[str, str]) -> bool:
    """Execute Claude-generated code to create files."""

    # Create execution environment with necessary imports and path variables
    exec_globals = {
        '__builtins__': __builtins__,
        **context_vars  # Add all the path variables
    }

    # Setup code with all imports Claude's code will need
    setup_code = '''
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

from docx import Document
from docx.shared import Pt as DocxPt, Inches as DocxInches, Twips, RGBColor as DocxRGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn as docx_qn
from docx.oxml import OxmlElement

def set_cell_shading(cell, color):
    """Helper to set table cell background color."""
    shading = OxmlElement('w:shd')
    shading.set(docx_qn('w:fill'), color)
    cell._tc.get_or_add_tcPr().append(shading)
'''

    full_code = setup_code + "\n" + code

    try:
        exec(full_code, exec_globals)
        return True
    except Exception as e:
        print(f"Error executing generated code: {e}")
        print(f"Code snippet:\n{code[:1000]}...")
        traceback.print_exc()
        return False


def _generate_lesson_materials(
    client: anthropic.Anthropic,
    lesson: Dict,
    persona_feedback: List[Dict],
    selected_concerns: List[Dict],
    slides_path: str,
    worksheet_path: str,
    supplementary_path: str = None,
    modified_path: str = None,
    extension_path: str = None
) -> bool:
    """Generate all materials for a lesson in a single Claude call."""

    context = _build_context(lesson, persona_feedback, selected_concerns)

    # Build the list of files to create
    files_to_create = f"""
## Files to Create

You will write Python code that creates ALL of the following files:

1. **Slide Deck:** `slides_path` = "{slides_path}"
2. **Student Worksheet:** `worksheet_path` = "{worksheet_path}"
"""

    if supplementary_path:
        files_to_create += f'3. **Supplementary Materials:** `supplementary_path` = "{supplementary_path}"\n'

    if modified_path:
        files_to_create += f'''
**Modified Worksheet (for struggling learners):** `modified_path` = "{modified_path}"
   - Same objectives as main worksheet
   - Add word banks, sentence starters, visual supports
   - Simplify language where appropriate
   - Chunk complex instructions into steps
'''

    if extension_path:
        files_to_create += f'''
**Extension Worksheet (for advanced learners):** `extension_path` = "{extension_path}"
   - Same core objectives as main worksheet
   - Add more complex analytical questions
   - Include research/inquiry prompts
   - Add open-ended challenges
'''

    prompt = f"""You are creating classroom materials for a teacher. Write Python code that creates ALL the materials for this lesson in one coherent set.

{context}

{files_to_create}

{MATERIAL_GENERATION_INSTRUCTIONS}

## Instructions

Write Python code that creates ALL the files listed above. The code should:

1. **Create the slide deck** using python-pptx:
   - Professional, visually appealing design
   - Hidden first slide with lesson plan
   - Sparse, teacher-led format (talking points, not paragraphs)
   - Presenter notes with teaching guidance
   - No text cutoff - all content fits within boundaries

2. **Create the student worksheet** using python-docx:
   - Sections that MATCH what activities actually require
   - If activity needs a graphic organizer, include it
   - If activity needs data tables, include them
   - Proper formatting with adequate answer space
   - Exit ticket at the end

3. **Create supplementary materials** (if supplementary_path is provided):
   - Station cards, data sheets, etc. referenced in activities
   - Follow the Discovery Principle - provide data, not conclusions
   - 1-2 analysis questions per card

4. **Create modified worksheet** (if modified_path is provided):
   - Same objectives with scaffolds for struggling learners

5. **Create extension worksheet** (if extension_path is provided):
   - Same objectives with added depth for advanced learners

**IMPORTANT:** All materials should be coherent and aligned. The worksheet should match what the slides describe. The supplementary materials should contain what the activities reference.

Write ONLY the Python code. No explanations. The code will be executed directly.
Use the variable names exactly as shown (slides_path, worksheet_path, etc.).

```python
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )

    code = response.content[0].text

    # Extract code from markdown if present
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    elif "```" in code:
        code = code.split("```")[1].split("```")[0]

    # Build context variables for code execution
    context_vars = {
        'slides_path': slides_path,
        'worksheet_path': worksheet_path,
    }
    if supplementary_path:
        context_vars['supplementary_path'] = supplementary_path
    if modified_path:
        context_vars['modified_path'] = modified_path
    if extension_path:
        context_vars['extension_path'] = extension_path

    return _execute_generated_code(code, context_vars)
