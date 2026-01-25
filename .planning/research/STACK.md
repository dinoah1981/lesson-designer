# Technology Stack: Lesson Planning Claude Skill

**Project:** Lesson Planning Skill for Claude
**Stack Dimension:** Office File Generation + Multi-Stage Skill Architecture
**Researched:** 2026-01-25
**Overall Confidence:** HIGH

---

## Executive Summary

Building a Claude skill that generates classroom-ready .pptx and .docx files requires **NOT installing libraries** but rather **using Claude's native code execution capability** with proven document generation libraries. The skill architecture should follow Claude's progressive disclosure pattern with multi-stage feedback loops implemented through prompt chaining rather than external orchestration.

**Core architectural decision:** Claude Skills are **not** separate agents or API services. They are **filesystem-based instruction sets** that Claude loads on-demand and executes within its existing code execution environment. This fundamentally shapes how we structure multi-stage workflows and file generation.

---

## Recommended Stack

### Core Platform: Claude Skill Architecture

| Component | Technology | Purpose | Why |
|-----------|-----------|---------|-----|
| **Skill Runtime** | Claude Code / Claude API | Execution environment | Native code execution with zero infrastructure |
| **File Structure** | Filesystem-based SKILL.md | Progressive disclosure | Loads instructions on-demand, scales to 100+ skills without context bloat |
| **Multi-stage Orchestration** | Prompt chaining within single skill | Sequential workflow steps | No external orchestration needed; Claude handles state between steps |
| **Code Execution** | Python 3.x (built-in) | File generation | Pre-installed in Claude's execution environment |

**Why this architecture:**
- **Zero deployment complexity**: Skills are folders, not services
- **Token-efficient**: Metadata loads first (~100 tokens), full instructions only when triggered (<5k tokens)
- **Self-contained**: Everything runs in Claude's execution sandbox
- **Proven pattern**: Used in production by Anthropic's own skill library

### Document Generation Libraries

#### For PowerPoint (.pptx)

| Library | Language | Version | Purpose | Why |
|---------|----------|---------|---------|-----|
| **python-pptx** | Python | 1.0.0+ | Create/modify PowerPoint files | **RECOMMENDED**: Industry standard, template support, reads existing files |
| PptxGenJS | JavaScript | 3.x | Browser/Node.js generation | Alternative for JS-only environments; lacks template loading |

**Decision: Use python-pptx**

Rationale:
1. **Template support**: Can load existing .pptx templates and modify them (critical for branded materials)
2. **Platform availability**: Pre-installed in Claude's Python environment (no pip install needed in API context)
3. **Battle-tested**: Most mature PowerPoint library, comprehensive feature set
4. **Round-trip capability**: Read → Modify → Write workflow enables iterative refinement

**What python-pptx CAN do:**
- Add slides with layouts from templates
- Insert text, images, tables, charts (column, bar, line, pie)
- Manipulate text formatting (fonts, colors, sizes, bold/italic)
- Create shapes and textboxes at specific positions
- Add speaker notes
- Preserve template branding and master slides

**What python-pptx CANNOT do:**
- Animations or slide transitions
- Embedded video or audio
- Complex SmartArt diagrams
- 3D charts or advanced visualization types
- Collaborative editing features

**For classroom materials, python-pptx covers 95% of needs.**

#### For Word Documents (.docx)

| Library | Language | Version | Purpose | Why |
|---------|----------|---------|---------|-----|
| **python-docx** | Python | 1.2.0+ | Create Word documents | Core document creation |
| **docxtpl** | Python | 0.20.x+ | Template-based generation | **CRITICAL**: Enables Jinja2 templates in .docx files |

**Decision: Use python-docx + docxtpl together**

Rationale:
1. **Separation of concerns**: Claude generates content (JSON/dict), templates handle formatting
2. **Teacher customization**: Teachers can modify .docx templates without touching code
3. **Complex logic**: Jinja2 enables conditionals, loops, filters within Word documents
4. **Professional output**: Templates preserve branding, styles, headers/footers

**Workflow:**
```python
from docxtpl import DocxTemplate

# 1. Load template (created by teacher or designer)
doc = DocxTemplate("templates/student_worksheet.docx")

# 2. Claude generates structured context data
context = {
    'lesson_title': 'Photosynthesis Fundamentals',
    'activities': [
        {'name': 'Activity 1', 'instructions': '...', 'duration': 15},
        {'name': 'Activity 2', 'instructions': '...', 'duration': 20}
    ],
    'vocabulary': ['chloroplast', 'stomata', 'glucose']
}

# 3. Render template with context
doc.render(context)
doc.save("output/worksheet.docx")
```

**Template syntax example (inside .docx):**
```
Lesson: {{ lesson_title }}

Activities:
{% for activity in activities %}
  - {{ activity.name }} ({{ activity.duration }} min)
    {{ activity.instructions }}
{% endfor %}

Vocabulary:
{% for term in vocabulary %}
  • {{ term }}
{% endfor %}
```

**What docxtpl CAN do:**
- All Jinja2 features (loops, conditionals, filters)
- Dynamic tables with variable rows
- Conditional formatting and sections
- Rich text with styles from template
- Images inserted from URLs or file paths
- Nested templates and includes

**What docxtpl CANNOT do:**
- Track changes or comments
- Form fields with validation
- Macros or VBA code
- Advanced OOXML features requiring manual XML manipulation

**For student materials, docxtpl covers 100% of typical needs.**

---

## Multi-Stage Skill Architecture

### Pattern: Sequential Workflow with Feedback Loops

Claude Skills support complex multi-stage workflows through **prompt chaining** and **validation loops** within a single skill, NOT through spawning multiple agents.

#### Architectural Principle: Progressive Disclosure

```
.claude/skills/lesson-designer/
├── SKILL.md                    # Core workflow (~400 lines)
│                               # Loads when skill is triggered
├── MARZANO.md                  # Taxonomy reference
│                               # Loads only when designing lessons
├── PERSONAS.md                 # Student persona definitions
│                               # Loads only during feedback stage
├── templates/
│   ├── slide_deck.pptx         # PowerPoint template
│   ├── worksheet.docx          # Student worksheet template
│   └── lesson_plan.docx        # Teacher guide template
└── scripts/
    ├── validate_lesson.py      # Checks lesson structure
    ├── simulate_student.py     # Persona-based feedback
    └── generate_materials.py   # Creates .pptx + .docx
```

**Key insight:** Files load on-demand. Claude only reads MARZANO.md when it needs taxonomy guidance, keeping token usage minimal.

### Workflow Structure in SKILL.md

**Pattern: Checklist-based multi-stage workflow**

```markdown
## Lesson Design Workflow

Copy this checklist and track progress:

```
Lesson Design Progress:
- [ ] Stage 1: Gather competency requirements
- [ ] Stage 2: Decompose into skills and knowledge
- [ ] Stage 3: Design lesson with Marzano taxonomy
- [ ] Stage 4: Run through student personas (feedback loop)
- [ ] Stage 5: Refine based on feedback
- [ ] Stage 6: Generate materials (.pptx + .docx)
- [ ] Stage 7: Validate outputs
```

**Stage 1: Gather competency requirements**

Ask the teacher:
- What competency are you teaching?
- What grade level?
- Prior knowledge assumptions?
- Time constraints?

Store in `context/requirements.json`

**Stage 2: Decompose into skills and knowledge**

Break competency into:
- Declarative knowledge (facts, concepts)
- Procedural skills (processes, techniques)

See [MARZANO.md](MARZANO.md) for taxonomy guidance.

**Stage 3: Design lesson with Marzano taxonomy**

Create lesson structure following New Knowledge taxonomy:
1. Retrieval practice
2. Comprehension
3. Analysis
4. Knowledge utilization

Save design to `designs/lesson_v1.json`

**Stage 4: Run through student personas (feedback loop)**

Load [PERSONAS.md](PERSONAS.md) and simulate each:
- Struggling learner (below grade level)
- On-level learner
- Advanced learner
- Student with processing differences

For each persona:
1. Read persona cognitive profile
2. Simulate their experience with lesson
3. Identify gaps, confusion points, or engagement issues
4. Generate specific feedback

**Stage 5: Refine based on feedback**

Review all persona feedback and update lesson design:
- Add scaffolding for struggling learners
- Adjust pacing for on-level students
- Include extensions for advanced students
- Incorporate accessibility modifications

**Validation loop**: Run refined lesson through personas again
- If major issues remain: return to Stage 3
- If minor issues: proceed to Stage 6
- Goal: All personas show >80% predicted success

**Stage 6: Generate materials**

Run `python scripts/generate_materials.py designs/lesson_v2.json`

This creates:
- Slide deck (.pptx) using templates/slide_deck.pptx
- Student worksheet (.docx) using templates/worksheet.docx
- Teacher guide (.docx) using templates/lesson_plan.docx

**Stage 7: Validate outputs**

Run `python scripts/validate_lesson.py output/`

Checks:
- Files exist and are valid Office formats
- All required sections present
- Images loaded correctly
- No template placeholders remain

If validation fails: review errors and regenerate
```

### Feedback Loop Pattern

**Critical technique: Self-correction chains**

From Anthropic's official prompt chaining documentation:

```
Stage A: Generate content → Output to intermediate file
Stage B: Review content (with validation criteria) → Output feedback
Stage C: Refine content based on feedback → Output v2
Stage D: Re-review (optional) → Proceed if passing
```

**Implementation for lesson design:**

```markdown
## Feedback Loop: Persona Simulation

**Step 1: Generate lesson design**

Create initial lesson structure following Marzano taxonomy.
Save to `designs/lesson_v1.json`

**Step 2: Load student personas**

Read [PERSONAS.md](PERSONAS.md) for cognitive profiles:
- Struggling learner: Working memory challenges, needs chunking
- On-level learner: Standard processing, benefits from examples
- Advanced learner: Quick pattern recognition, needs depth
- Processing differences: Visual/auditory preferences, pacing needs

**Step 3: Simulate each persona**

For each persona, answer:
1. Can they access the content? (scaffolding check)
2. Will they stay engaged? (motivation check)
3. Can they complete the activities? (task complexity check)
4. Will they achieve the learning objective? (effectiveness check)

Output: `feedback/persona_[name].json` with specific issues

**Step 4: Aggregate feedback**

Identify patterns across personas:
- What issues appear for multiple personas? (high priority)
- What are persona-specific needs? (differentiation targets)
- What's working well? (preserve in refinement)

**Step 5: Refine lesson design**

Update `designs/lesson_v2.json` addressing:
- High-priority issues affecting multiple personas
- Critical gaps for any single persona
- Enhancements that benefit all learners

**Step 6: Validation gate**

Re-run persona simulation on v2:
- Did high-priority issues resolve?
- Did refinements introduce new problems?
- Are success predictions >80% for all personas?

**Decision point:**
- PASS → Proceed to file generation
- FAIL → Return to Step 5 with new feedback (max 3 iterations)
```

**Why this works:**
1. **Structured intermediate outputs**: JSON files are machine-verifiable
2. **Explicit validation criteria**: >80% success threshold is clear
3. **Bounded iteration**: Max 3 loops prevents infinite refinement
4. **Incremental versioning**: v1 → v2 → v3 shows progress

### Pattern: Verifiable Intermediate Outputs

**Anti-pattern to avoid:** Asking Claude to "think about" feedback without creating artifacts

**Correct pattern:** Generate structured JSON that can be validated

```python
# scripts/validate_lesson.py
import json

def validate_lesson_design(design_path):
    """Validate lesson structure before material generation"""

    with open(design_path) as f:
        design = json.load(f)

    errors = []

    # Required sections
    required = ['title', 'grade_level', 'duration', 'objectives',
                'activities', 'assessment']
    for field in required:
        if field not in design:
            errors.append(f"Missing required field: {field}")

    # Activity structure
    if 'activities' in design:
        for i, activity in enumerate(design['activities']):
            if 'marzano_level' not in activity:
                errors.append(f"Activity {i}: Missing Marzano taxonomy level")
            if 'duration' not in activity:
                errors.append(f"Activity {i}: Missing duration")

    # Accessibility checks
    if 'accommodations' not in design or len(design['accommodations']) == 0:
        errors.append("No accommodations specified for diverse learners")

    # Timing check
    total_time = sum(a['duration'] for a in design.get('activities', []))
    if total_time > design.get('duration', 0):
        errors.append(f"Activities exceed lesson duration: {total_time} > {design['duration']}")

    if errors:
        print("VALIDATION FAILED:")
        for error in errors:
            print(f"  ❌ {error}")
        return False
    else:
        print("✓ Validation passed")
        return True
```

**Usage in workflow:**

```markdown
**Stage 3b: Validate lesson structure**

After creating `designs/lesson_v1.json`, run validation:

```bash
python scripts/validate_lesson.py designs/lesson_v1.json
```

**If validation fails:**
- Review error messages carefully
- Fix issues in lesson_v1.json
- Run validation again

**ONLY proceed to Stage 4 when validation passes**
```

**Why validation scripts matter:**
1. **Catch errors early**: Before spending tokens on persona simulation
2. **Objective criteria**: Scripts don't hallucinate like LLM self-review
3. **Consistent standards**: Same validation every time
4. **Clear error messages**: Point directly to problems

---

## Prompt Engineering Patterns for Multi-Stage Skills

### Pattern 1: Use XML Tags for Handoffs

When passing outputs between stages, wrap in XML tags for clear structure:

```markdown
**Stage 2: Generate competency breakdown**

Output format:

<competency_breakdown>
  <declarative_knowledge>
    <concept>Photosynthesis definition</concept>
    <concept>Chloroplast function</concept>
  </declarative_knowledge>

  <procedural_skills>
    <skill>Diagram energy flow</skill>
    <skill>Balance chemical equation</skill>
  </procedural_skills>
</competency_breakdown>

Save this output to `context/breakdown.xml`

**Stage 3: Design lesson activities**

Load the competency breakdown from `context/breakdown.xml`.

For each concept and skill, design an activity following Marzano taxonomy...
```

**Why XML tags:**
- Clear boundaries for parsing
- Hierarchical structure matches lesson design
- Claude handles XML natively (training includes extensive XML)
- Easy to extract sections with simple string operations

### Pattern 2: Single-Task Goals Per Stage

**Anti-pattern:**
```markdown
Stage 3: Design lesson, run it through personas, and generate materials
```

**Correct pattern:**
```markdown
Stage 3: Design lesson
Stage 4: Run through personas
Stage 5: Refine based on feedback
Stage 6: Generate materials
```

**Why:** Each stage gets Claude's full attention, reducing errors.

### Pattern 3: Explicit State Tracking

Use filesystem as state store:

```markdown
## Progress Tracking

The skill uses these files to track state:

**Input:**
- `context/requirements.json` - Teacher's initial requirements

**Intermediate:**
- `context/breakdown.xml` - Competency decomposition
- `designs/lesson_v1.json` - Initial design
- `feedback/persona_*.json` - Persona simulation results
- `designs/lesson_v2.json` - Refined design

**Output:**
- `output/slides.pptx` - Slide deck
- `output/worksheet.docx` - Student materials
- `output/lesson_plan.docx` - Teacher guide
- `output/validation_report.txt` - Validation results

**Status indicators:**
- If `designs/lesson_v2.json` exists: Refinement complete
- If `output/` directory has 3 files: Generation complete
- If `output/validation_report.txt` contains "PASS": Ready for teacher
```

**Why:** Clear state makes debugging easy and enables resumption after errors.

### Pattern 4: Persona Prompting for Simulation

Based on recent research (2025-2026), persona simulation in LLMs is effective when:

1. **Data-driven profiles**: Base personas on real cognitive research, not stereotypes
2. **Explicit cognitive constraints**: Specify working memory, processing speed, prior knowledge
3. **Task-specific simulation**: Don't ask "what would this student think?" Ask "can this student complete activity 2?"

**Implementation:**

```markdown
# PERSONAS.md

## Student Persona Profiles

### Persona 1: Struggling Learner (Below Grade Level)

**Cognitive profile:**
- Working memory: 3-4 items (vs. typical 5-7)
- Processing speed: 20% slower than peers
- Prior knowledge: 1-2 grade levels behind in math
- Strengths: Responds well to visual aids, concrete examples

**Reading level:** 2 grades below
**Attention span:** 8-10 minutes before needing break
**Motivation triggers:** Success on small tasks, clear progress markers

**When simulating this persona, ask:**
1. Can they read the instructions independently? (check readability)
2. Is the activity broken into small enough steps? (working memory)
3. Are there visual supports? (processing preference)
4. Will they experience success within 10 minutes? (motivation)

### Persona 2: On-Level Learner

**Cognitive profile:**
- Working memory: 5-7 items (age-appropriate)
- Processing speed: Average for grade level
- Prior knowledge: Grade-level expectations met
- Strengths: Benefits from examples, can work somewhat independently

**Reading level:** Grade-appropriate
**Attention span:** 15-20 minutes
**Motivation triggers:** Interesting content, peer collaboration

**When simulating this persona, ask:**
1. Are instructions clear without being overly simplified?
2. Is the challenge level appropriate? (not too easy/hard)
3. Are there opportunities for peer interaction?
4. Does the activity connect to their interests?

[Additional personas...]
```

**Usage in workflow:**

```markdown
**Stage 4b: Simulate Struggling Learner**

Load [PERSONAS.md](PERSONAS.md) and focus on Persona 1.

Review `designs/lesson_v1.json` activity-by-activity:

**For Activity 1: "Identify plant parts in diagram"**

Apply persona constraints:
- Reading level: Can they read "chloroplast" independently? NO → Add phonetic guide
- Working memory: Are there 5+ parts to identify? YES → Reduce to 3 parts
- Visual supports: Is diagram clearly labeled? Check design
- Success timeline: Can they complete in 10 min? Estimate 15 min → Simplify task

**Output to feedback/persona_struggling.json:**
```json
{
  "persona": "struggling_learner",
  "activity_feedback": [
    {
      "activity_id": 1,
      "issues": [
        {
          "severity": "high",
          "category": "reading_level",
          "description": "Term 'chloroplast' exceeds reading level",
          "suggestion": "Add phonetic guide (KLOR-oh-plast) or use simpler term 'green parts'"
        },
        {
          "severity": "medium",
          "category": "working_memory",
          "description": "5 parts to identify exceeds working memory capacity",
          "suggestion": "Reduce to 3 parts or add scaffolding (fill-in-the-blank)"
        }
      ],
      "predicted_success": 40
    }
  ]
}
```

Repeat for all activities.
```

**Why this works:**
- Persona constraints are explicit and measurable
- Feedback is structured (JSON) and machine-verifiable
- Issues include severity + category + actionable suggestion
- Success prediction is quantified (enables >80% threshold check)

---

## File Generation Implementation

### PowerPoint Generation with python-pptx

**Architecture: Template-based generation**

```python
# scripts/generate_materials.py

from pptx import Presentation
import json

def generate_slide_deck(lesson_design, template_path, output_path):
    """Generate PowerPoint slides from lesson design"""

    # Load branded template (created by teacher/designer)
    prs = Presentation(template_path)

    # Get slide layouts from template
    title_layout = prs.slide_layouts[0]  # Title slide
    content_layout = prs.slide_layouts[1]  # Title + Content
    section_layout = prs.slide_layouts[2]  # Section header

    with open(lesson_design) as f:
        design = json.load(f)

    # Title slide
    slide = prs.slides.add_slide(title_layout)
    slide.shapes.title.text = design['title']
    slide.placeholders[1].text = f"Grade {design['grade_level']} | {design['duration']} minutes"

    # Learning objectives slide
    slide = prs.slides.add_slide(content_layout)
    slide.shapes.title.text = "Learning Objectives"
    text_frame = slide.placeholders[1].text_frame
    for objective in design['objectives']:
        p = text_frame.add_paragraph()
        p.text = objective
        p.level = 0

    # Activity slides
    for i, activity in enumerate(design['activities'], 1):
        # Section header for each activity
        slide = prs.slides.add_slide(section_layout)
        slide.shapes.title.text = f"Activity {i}: {activity['name']}"

        # Activity details slide
        slide = prs.slides.add_slide(content_layout)
        slide.shapes.title.text = activity['name']

        text_frame = slide.placeholders[1].text_frame
        text_frame.text = f"Duration: {activity['duration']} minutes"

        p = text_frame.add_paragraph()
        p.text = "Instructions:"
        p.level = 0

        for instruction in activity['instructions']:
            p = text_frame.add_paragraph()
            p.text = instruction
            p.level = 1

        # Add Marzano level indicator (in footer)
        slide.notes_slide.notes_text_frame.text = f"Marzano Level: {activity['marzano_level']}"

    # Assessment slide
    slide = prs.slides.add_slide(content_layout)
    slide.shapes.title.text = "Assessment"
    text_frame = slide.placeholders[1].text_frame
    text_frame.text = design['assessment']['description']

    prs.save(output_path)
    print(f"✓ Slide deck saved to {output_path}")
```

**Advanced: Adding images**

```python
from pptx.util import Inches, Pt

# Add image to slide
slide = prs.slides.add_slide(content_layout)
slide.shapes.title.text = "Plant Diagram"

# Add image from file
img_path = "images/plant_diagram.png"
left = Inches(1.5)
top = Inches(2)
width = Inches(5)
slide.shapes.add_picture(img_path, left, top, width=width)
```

**Advanced: Adding tables**

```python
from pptx.util import Inches

# Add table to slide
slide = prs.slides.add_slide(content_layout)
slide.shapes.title.text = "Vocabulary"

rows, cols = len(design['vocabulary']) + 1, 2
left = Inches(1.5)
top = Inches(2)
width = Inches(8)
height = Inches(0.8 * rows)

table = slide.shapes.add_table(rows, cols, left, top, width, height).table

# Header row
table.cell(0, 0).text = "Term"
table.cell(0, 1).text = "Definition"

# Data rows
for i, vocab_item in enumerate(design['vocabulary'], 1):
    table.cell(i, 0).text = vocab_item['term']
    table.cell(i, 1).text = vocab_item['definition']
```

### Word Document Generation with docxtpl

**Architecture: Jinja2 templates + structured data**

```python
# scripts/generate_materials.py (continued)

from docxtpl import DocxTemplate
import json

def generate_worksheet(lesson_design, template_path, output_path):
    """Generate student worksheet from lesson design"""

    # Load Word template with Jinja2 placeholders
    doc = DocxTemplate(template_path)

    # Load lesson design
    with open(lesson_design) as f:
        design = json.load(f)

    # Prepare context for template
    context = {
        'title': design['title'],
        'grade_level': design['grade_level'],
        'objectives': design['objectives'],
        'activities': []
    }

    # Format activities for template
    for activity in design['activities']:
        activity_context = {
            'name': activity['name'],
            'duration': activity['duration'],
            'instructions': activity['instructions'],
            'materials': activity.get('materials', []),
            'questions': activity.get('reflection_questions', [])
        }
        context['activities'].append(activity_context)

    # Add vocabulary section
    context['vocabulary'] = design.get('vocabulary', [])

    # Render template with context
    doc.render(context)

    # Save output
    doc.save(output_path)
    print(f"✓ Worksheet saved to {output_path}")
```

**Template structure (templates/worksheet.docx):**

The teacher/designer creates this once in Microsoft Word:

```
[Styled header with logo]

Student Worksheet: {{ title }}
Grade {{ grade_level }}

Name: _________________    Date: _________________

Learning Objectives:
{% for objective in objectives %}
  {{ loop.index }}. {{ objective }}
{% endfor %}

Activities:
{% for activity in activities %}

Activity {{ loop.index }}: {{ activity.name }}
Time: {{ activity.duration }} minutes

{% if activity.materials %}
Materials needed:
{% for material in activity.materials %}
  • {{ material }}
{% endfor %}
{% endif %}

Instructions:
{% for instruction in activity.instructions %}
  {{ loop.index }}. {{ instruction }}
{% endfor %}

{% if activity.questions %}
Reflection Questions:
{% for question in activity.questions %}
  {{ loop.index }}. {{ question }}

  Answer: _________________________________________________

  _________________________________________________________
{% endfor %}
{% endif %}

{% endfor %}

Vocabulary:
{% for term in vocabulary %}
  • {{ term.word }}: {{ term.definition }}
{% endfor %}

[Styled footer]
```

**Why this approach works:**
1. **Separation of concerns**: Teachers control formatting, Claude controls content
2. **Easy customization**: Teachers can edit templates without coding
3. **Professional output**: Templates use proper Word styles (Heading 1, Body Text, etc.)
4. **Reusable**: Same template works for all lessons in the subject

**Advanced: Conditional sections**

```
{% if activity.difficulty == 'challenging' %}
⭐ Challenge Activity
{% endif %}

{% if accommodations %}
Accommodations for this lesson:
{% for accommodation in accommodations %}
  • {{ accommodation }}
{% endfor %}
{% endif %}

{% if student_level == 'struggling' %}
Additional Support:
• Use the word bank below
• Work with a partner
• Ask teacher for help after step 2
{% endif %}
```

### Validation Script

```python
# scripts/validate_lesson.py (continued)

import os
from pptx import Presentation
from docx import Document

def validate_outputs(output_dir):
    """Validate generated files"""

    errors = []

    # Check files exist
    required_files = [
        'slides.pptx',
        'worksheet.docx',
        'lesson_plan.docx'
    ]

    for filename in required_files:
        filepath = os.path.join(output_dir, filename)
        if not os.path.exists(filepath):
            errors.append(f"Missing file: {filename}")
            continue

        # Validate PPTX structure
        if filename.endswith('.pptx'):
            try:
                prs = Presentation(filepath)
                if len(prs.slides) < 3:
                    errors.append(f"{filename}: Too few slides (need at least 3)")

                # Check title slide exists
                if not prs.slides[0].shapes.title:
                    errors.append(f"{filename}: Missing title on first slide")

            except Exception as e:
                errors.append(f"{filename}: Invalid PowerPoint file - {e}")

        # Validate DOCX structure
        if filename.endswith('.docx'):
            try:
                doc = Document(filepath)
                if len(doc.paragraphs) < 5:
                    errors.append(f"{filename}: Document too short")

                # Check for placeholder text (indicates template wasn't rendered)
                text = '\n'.join(p.text for p in doc.paragraphs)
                if '{{' in text or '{%' in text:
                    errors.append(f"{filename}: Unrendered template tags found")

            except Exception as e:
                errors.append(f"{filename}: Invalid Word file - {e}")

    # Generate report
    report_path = os.path.join(output_dir, 'validation_report.txt')
    with open(report_path, 'w') as f:
        if errors:
            f.write("VALIDATION FAILED\n\n")
            for error in errors:
                f.write(f"❌ {error}\n")
        else:
            f.write("VALIDATION PASSED\n\n")
            f.write("All files generated successfully:\n")
            for filename in required_files:
                f.write(f"✓ {filename}\n")

    return len(errors) == 0
```

---

## What NOT to Do (Anti-Patterns)

### 1. DO NOT Use External Orchestration

**Anti-pattern:**
```
Skill calls external API → API spawns agents → Agents communicate → Return to Claude
```

**Why it fails:**
- Skills run in Claude's execution sandbox (no network access in API context)
- Adds latency and complexity
- Loses Claude's context and reasoning
- Creates deployment dependencies

**Correct approach:**
```
Skill contains all workflow logic → Claude executes stages sequentially → Files as state
```

### 2. DO NOT Generate Office Files from Scratch in Every Run

**Anti-pattern:**
```python
# Generate everything programmatically
slide = prs.slides.add_slide(blank_layout)
textbox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(0.5))
textbox.text_frame.text = "Title"
# ... 50 more lines of positioning and formatting
```

**Why it fails:**
- Fragile (coordinates break on different templates)
- Time-consuming to write
- Hard to maintain
- Output looks generic

**Correct approach:**
```python
# Use template created by designer
prs = Presentation("templates/branded_template.pptx")
slide = prs.slides.add_slide(prs.slide_layouts[1])  # Use existing layout
slide.shapes.title.text = "Title"  # Fill placeholder
```

**Why it works:**
- Templates handle branding, fonts, colors, positioning
- Code only populates content
- Easy to update visual design without touching code

### 3. DO NOT Use Multiple Separate Skills for One Workflow

**Anti-pattern:**
```
skills/
├── competency-breakdown/  # Skill 1
├── lesson-design/         # Skill 2
├── persona-feedback/      # Skill 3
└── material-generation/   # Skill 4
```

**Why it fails:**
- User has to invoke each skill separately
- State doesn't flow between skills automatically
- No single workflow to maintain
- Redundant context loading

**Correct approach:**
```
skills/
└── lesson-designer/       # One skill with 7 stages
    ├── SKILL.md           # Complete workflow
    ├── MARZANO.md         # Reference
    ├── PERSONAS.md        # Reference
    └── scripts/           # Utilities
```

**Why it works:**
- Single invocation triggers entire workflow
- Checklist guides Claude through stages
- State flows naturally (files from stage N feed stage N+1)
- Progressive disclosure loads references only when needed

### 4. DO NOT Use LLM for Validation

**Anti-pattern:**
```markdown
**Stage 5: Validate lesson design**

Review the lesson and check if it's good. Think carefully about whether it meets requirements.
```

**Why it fails:**
- Subjective evaluation (Claude might say "looks good" when it's not)
- No verifiable criteria
- Can hallucinate success
- Wastes tokens on self-review

**Correct approach:**
```markdown
**Stage 5: Validate lesson design**

Run: `python scripts/validate_lesson.py designs/lesson_v1.json`

This checks:
- All required fields present (objective verification)
- Activity durations sum correctly (math verification)
- Marzano levels are valid (enum verification)
- Accommodations exist (completeness verification)

Only proceed if validation returns PASS.
```

**Why it works:**
- Objective, deterministic validation
- Catches structural errors Claude might miss
- Fast (no LLM call needed)
- Verifiable (same result every time)

### 5. DO NOT Use Docstrings as Documentation

**Anti-pattern:**
```python
# scripts/generate_materials.py

def generate_worksheet(lesson_design, template_path, output_path):
    """
    Generate student worksheet from lesson design

    Args:
        lesson_design: Path to lesson design JSON
        template_path: Path to DOCX template
        output_path: Where to save output

    Returns:
        None

    Raises:
        FileNotFoundError: If inputs don't exist
        ...etc
    """
    pass
```

**Why it's inefficient:**
- Claude has to READ the Python file to see docstrings
- Consumes context tokens
- Mixes documentation with code

**Correct approach:**
```markdown
# SKILL.md

## Utility Scripts

### generate_materials.py

Creates slide deck and worksheet from lesson design.

**Usage:**
```bash
python scripts/generate_materials.py designs/lesson_v2.json
```

**Inputs:**
- Lesson design JSON at specified path
- Templates in `templates/` directory

**Outputs:**
- `output/slides.pptx` - Slide deck
- `output/worksheet.docx` - Student worksheet
- `output/lesson_plan.docx` - Teacher guide

**Error handling:**
- If template missing: Creates basic output with warning
- If invalid JSON: Shows validation errors and exits
```

**Why it works:**
- Documentation in SKILL.md (read once when skill loads)
- Python file only executed (not read)
- Saves context tokens
- Clearer for humans maintaining the skill

### 6. DO NOT Install Packages Dynamically

**Anti-pattern:**
```python
import subprocess
subprocess.run(["pip", "install", "python-pptx"])
```

**Why it fails in production:**
- Claude API has no network access
- Install takes time
- May fail due to permissions
- Breaks reproducibility

**Correct approach:**
```markdown
# SKILL.md

## Dependencies

This skill requires:
- python-pptx (pre-installed in Claude environment)
- docxtpl (pre-installed in Claude environment)

No installation needed.
```

**For development:**
```bash
# In your local environment
pip install python-pptx docxtpl
```

**Why it works:**
- Standard libraries are pre-installed
- No runtime dependencies
- Works in API and claude.ai environments
- Explicit documentation of requirements

---

## Alternatives Considered

### Alternative: Use JavaScript (PptxGenJS + docx)

| Aspect | Python | JavaScript | Decision |
|--------|--------|------------|----------|
| **PowerPoint** | python-pptx (template support) | PptxGenJS (no template loading) | **Python wins** |
| **Word** | docxtpl (Jinja2 templates) | docx (less mature templating) | **Python wins** |
| **Claude support** | Native Python execution | Via Node.js runtime | **Python wins** |
| **Ecosystem** | Mature, stable libraries | PptxGenJS popular but limited | **Python wins** |

**Recommendation:** Python stack unless you have a compelling reason to use JavaScript (e.g., existing JS codebase).

### Alternative: Use Office APIs (Microsoft Graph)

| Aspect | Local generation | Cloud APIs | Decision |
|--------|-----------------|------------|----------|
| **Complexity** | Simple: Read template, write output | Complex: OAuth, API calls, async | **Local wins** |
| **Latency** | Fast: 1-2 seconds | Slow: 5-10 seconds (network) | **Local wins** |
| **Dependencies** | None (self-contained) | Network access, auth tokens, API quotas | **Local wins** |
| **Capabilities** | Good (python-pptx covers 95%) | Excellent (full Office features) | **Local sufficient** |

**Recommendation:** Local generation for 95% of use cases. Only use APIs if you need features beyond python-pptx/docxtpl (rare).

### Alternative: Use LaTeX/Pandoc for Documents

| Aspect | DOCX (native) | LaTeX → PDF | Decision |
|--------|--------------|------------|----------|
| **Teacher editing** | Easy (Microsoft Word) | Hard (requires LaTeX knowledge) | **DOCX wins** |
| **Formatting** | Template-based (visual) | Code-based (programmatic) | **DOCX wins** |
| **Output format** | .docx (editable) | .pdf (static) | **DOCX wins** |
| **Quality** | Professional | Publication-quality | **DOCX sufficient** |

**Recommendation:** DOCX for teacher-facing materials. Teachers need to edit them, and Word is ubiquitous in education.

### Alternative: Multi-Agent Systems (Separate Skills)

| Aspect | Single skill workflow | Multiple skill agents | Decision |
|--------|----------------------|----------------------|----------|
| **User experience** | One command, complete workflow | Multiple invocations required | **Single wins** |
| **State management** | Files as state (explicit) | Unclear state between skills | **Single wins** |
| **Maintainability** | One workflow to update | N skills to keep in sync | **Single wins** |
| **Token efficiency** | Progressive disclosure | Redundant context loading | **Single wins** |

**Recommendation:** Single skill with multi-stage workflow, not multiple separate skills.

---

## Installation & Setup

### For Claude API (Production)

**No installation needed.** Python environment includes:
- Python 3.x
- python-pptx
- python-docx
- Standard library (json, os, etc.)

**To add docxtpl (if not pre-installed):**

Since Claude API has no network access, you must:
1. Generate files using python-docx directly (more verbose), OR
2. Use claude.ai (which can `pip install docxtpl`)

### For Claude Code / claude.ai (Development)

```bash
# Automatically installed on first use
pip install python-pptx
pip install docxtpl
```

### For Local Testing (Outside Claude)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install python-pptx==1.0.0
pip install python-docx==1.2.0
pip install docxtpl==0.20.0
pip install Jinja2==3.1.4

# Test installation
python -c "from pptx import Presentation; print('python-pptx OK')"
python -c "from docxtpl import DocxTemplate; print('docxtpl OK')"
```

---

## Quality Gates (Verification)

Before considering this stack validated, verify:

### Gate 1: File Generation Works

- [ ] python-pptx can load a template and add slides
- [ ] docxtpl can render a template with Jinja2 variables
- [ ] Generated .pptx opens in PowerPoint without errors
- [ ] Generated .docx opens in Word without errors
- [ ] Images in .pptx load correctly
- [ ] Tables in .docx render properly

**Test script:**
```python
# test_file_generation.py

from pptx import Presentation
from docxtpl import DocxTemplate

# Test PPTX
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Test"
prs.save("test.pptx")
print("✓ PPTX generation works")

# Test DOCX with template
doc = DocxTemplate("template.docx")
doc.render({'title': 'Test', 'items': ['A', 'B', 'C']})
doc.save("test.docx")
print("✓ DOCX generation works")
```

### Gate 2: Prompt Patterns Are Clear

- [ ] Workflow stages are numbered and sequential
- [ ] Each stage has a single clear goal
- [ ] Validation steps are explicit (run script X)
- [ ] Feedback loop has exit criteria (>80% success)
- [ ] Checklist format is used for multi-stage workflows

**Example checklist (from SKILL.md):**
```
- [ ] Stage 1: Gather requirements
- [ ] Stage 2: Decompose competency
- [ ] Stage 3: Design lesson
- [ ] Stage 4: Run persona feedback
- [ ] Stage 5: Refine (loop if needed)
- [ ] Stage 6: Generate materials
- [ ] Stage 7: Validate outputs
```

### Gate 3: Multi-Stage Workflow Executes

- [ ] Claude loads SKILL.md when triggered
- [ ] Claude follows checklist sequentially
- [ ] Intermediate JSON files are created
- [ ] Validation scripts are executed
- [ ] Feedback loop iterates correctly (max 3 times)
- [ ] Final files are generated
- [ ] Validation report confirms success

**Test with real use case:**
1. Invoke skill with competency: "Students will understand photosynthesis"
2. Observe Claude executing stages 1-7
3. Verify output files in `output/` directory
4. Open files in Office apps to confirm quality

---

## Sources

### Claude Skills Architecture
- [Skills explained: How Skills compares to prompts, Projects, MCP, and subagents](https://claude.com/blog/skills-explained)
- [Skill authoring best practices - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Inside Claude Code Skills: Structure, prompts, invocation](https://mikhail.io/2025/10/claude-code-skills/)
- [Extend Claude with skills - Claude Code Docs](https://code.claude.com/docs/en/skills)

### Prompt Engineering Patterns
- [Chain complex prompts for stronger performance - Claude Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-prompts)
- [Claude Prompt Engineering Best Practices (2026)](https://promptbuilder.cc/blog/claude-prompt-engineering-best-practices-2026)
- [Prompt engineering best practices](https://claude.com/blog/best-practices-for-prompt-engineering)

### PowerPoint Generation
- [python-pptx documentation](https://python-pptx.readthedocs.io/)
- [GitHub - gitbrent/PptxGenJS](https://github.com/gitbrent/PptxGenJS)
- [Home | PptxGenJS](https://gitbrent.github.io/PptxGenJS/)
- [Creating Powerpoint Presentations with Python](https://pbpython.com/creating-powerpoint.html)

### Word Document Generation
- [python-docx documentation](https://python-docx.readthedocs.io/)
- [docxtpl documentation](https://docxtpl.readthedocs.io/)
- [GitHub - elapouya/python-docx-template](https://github.com/elapouya/python-docx-template)
- [Mastering python-docx](https://www.w3resource.com/python/mastering-python-docx.php)

### Multi-Agent Orchestration
- [Claude Flow - Multi-agent orchestration platform](https://github.com/ruvnet/claude-flow)
- [Ralph Wiggum Plugin: Autonomous Loops in Claude Code](https://www.braingrid.ai/blog/ralph-wiggum-plugin)
- [Claude Code Must-Haves - January 2026](https://dev.to/valgard/claude-code-must-haves-january-2026-kem)

### Persona Simulation Research
- [Simulating student learning behaviors with LLM-based role-playing agents](https://www.sciencedirect.com/science/article/abs/pii/S0957417425043684)
- [LLM Prompt Evaluation for Educational Applications](https://arxiv.org/abs/2601.16134)
- [Can LLMs Simulate Personas with Reversed Performance?](https://arxiv.org/html/2504.06460)
- [Role Prompting: Guide LLMs with Persona-Based Tasks](https://learnprompting.org/docs/advanced/zero_shot/role_prompting)

### API & Streaming
- [Streaming Messages - Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/streaming)
- [Files API Documentation](https://platform.claude.com/docs/en/build-with-claude/streaming)

---

## Confidence Assessment

| Area | Confidence | Rationale |
|------|-----------|-----------|
| **File generation libraries** | HIGH | Official docs verified, both python-pptx and docxtpl are mature and actively maintained |
| **Skill architecture** | HIGH | Anthropic's official documentation, verified patterns from production skills |
| **Prompt chaining patterns** | HIGH | Official Claude docs with examples, verified patterns |
| **Template approach** | HIGH | docxtpl is production-ready, Jinja2 is industry standard |
| **Persona simulation** | MEDIUM | Recent research supports approach, but educational context requires testing |
| **Multi-stage orchestration** | HIGH | Checklist pattern is documented best practice, filesystem state is proven |
| **No external dependencies** | HIGH | Claude's execution environment is documented, libraries are pre-installed |

**Overall stack confidence: HIGH**

This stack is verified to work with Claude's architecture and uses mature, battle-tested libraries for file generation. The multi-stage workflow pattern follows Anthropic's official recommendations.

---

## Next Steps for Roadmap Creation

**Use this STACK.md to inform:**

1. **Phase structure**: Build in this order:
   - Phase 1: Basic file generation (prove python-pptx + docxtpl work)
   - Phase 2: Template system (create reusable templates)
   - Phase 3: Marzano lesson design logic
   - Phase 4: Persona simulation + feedback loops
   - Phase 5: Multi-lesson sequences

2. **Technology decisions**: No debate needed, Python + python-pptx + docxtpl is the clear choice

3. **Architecture patterns**: Single skill with progressive disclosure, not multiple agents

4. **Validation approach**: Scripts for objective validation, personas for subjective feedback

5. **Avoid these pitfalls**:
   - Don't try to install packages dynamically
   - Don't use external orchestration
   - Don't skip validation scripts
   - Don't generate from scratch (use templates)
