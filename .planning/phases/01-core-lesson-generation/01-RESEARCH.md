# Phase 1: Core Lesson Generation - Research

**Researched:** 2026-01-25
**Domain:** Office file generation (PowerPoint, Word) + Educational pedagogy (Marzano framework)
**Confidence:** HIGH

## Summary

Phase 1 requires generating classroom-ready .pptx and .docx files from teacher competency input using Claude's built-in code execution environment. The critical technical finding is that **python-pptx and python-docx are pre-installed** in Claude's execution environment, eliminating the need for dependency management. The major pedagogical challenge is preventing the AI from generating low-cognitive-demand "recall-only" content—research shows 90% of AI-generated lessons promote only basic-level thinking, directly violating the Marzano framework's emphasis on higher-order cognition.

The implementation pattern is: **template-based generation with explicit cognitive rigor enforcement**. Teacher-led slides must be sparse (talking points, not paragraphs) with a hidden first slide containing the lesson plan. Student materials must use proper spacing for handwritten responses. The Marzano framework (retrieval → comprehension → analysis → knowledge utilization) must be encoded as validation criteria, not suggestions.

**Primary recommendation:** Build Phase 1 as a single-skill sequential workflow using filesystem-based state management, python-pptx for template-driven PowerPoint generation, and docxtpl for Jinja2-powered Word document templating. Implement Marzano framework validation as a Python script that blocks progression if cognitive demand is insufficient.

---

## Standard Stack

### Core Libraries (Pre-installed in Claude Environment)

| Library | Version | Purpose | Why Standard | Availability |
|---------|---------|---------|-------------|--------------|
| **python-pptx** | 1.0.0+ | PowerPoint generation | Industry standard; template support; reads existing .pptx files | ✅ Pre-installed in Claude execution environment |
| **python-docx** | 1.2.0+ | Word document generation | Mature library; programmatic document creation | ✅ Pre-installed in Claude execution environment |
| **docxtpl** | 0.20.x+ | Word template rendering | Jinja2 templating for Word; separates content from formatting | ✅ Pre-installed in Claude execution environment |

**Installation:** None required. These libraries are available in Claude's code execution sandbox (version `code_execution_20250825`).

### Supporting Tools

| Tool | Purpose | When to Use | Source |
|------|---------|-------------|--------|
| **JSON files** | State management between workflow stages | All intermediate outputs (lesson design, feedback) | Python stdlib |
| **Markdown files** | Human-readable versions of lesson plans | Teacher review and documentation | Python stdlib |
| **Validation scripts** | Structural checks before generation | Every stage transition | Custom Python |

### Alternatives Considered

| Instead of | Could Use | Tradeoff | Decision |
|------------|-----------|----------|----------|
| **python-pptx** | PptxGenJS (JavaScript) | No template loading; requires Node.js | **Use python-pptx** (native Python execution, template support) |
| **docxtpl** | python-docx only | More verbose code; no templating | **Use docxtpl** (Jinja2 integration critical for teacher customization) |
| **Local generation** | Microsoft Graph API | Full Office features but requires network, OAuth, latency | **Use local generation** (self-contained, fast, no dependencies) |
| **Multiple skills** | Single skill with stages | Better isolation but poor UX | **Single skill** (unified workflow, better state flow) |

---

## Architecture Patterns

### Pattern 1: Template-Based File Generation

**What:** Pre-create .pptx and .docx templates with placeholders; Claude populates them with generated content.

**Why:** Separates formatting (teacher/designer responsibility) from content (AI responsibility). Templates preserve branding, styles, and professional appearance. Far more maintainable than programmatic positioning.

**When to use:** All file generation tasks in Phase 1.

**Example:**

```python
# PowerPoint generation
from pptx import Presentation

# Load template (created once by teacher/designer)
prs = Presentation("templates/lesson_slide_deck.pptx")

# Use existing layout from template
title_layout = prs.slide_layouts[0]
content_layout = prs.slide_layouts[1]

# Add title slide
slide = prs.slides.add_slide(title_layout)
slide.shapes.title.text = lesson['title']
slide.placeholders[1].text = f"Grade {lesson['grade_level']} | {lesson['duration']} min"

# Add content slides
for objective in lesson['objectives']:
    slide = prs.slides.add_slide(content_layout)
    slide.shapes.title.text = "Learning Objectives"
    text_frame = slide.placeholders[1].text_frame
    p = text_frame.add_paragraph()
    p.text = objective

prs.save("output/lesson.pptx")
```

**Source:** [python-pptx documentation](https://python-pptx.readthedocs.io/en/latest/user/slides.html)

**Example: Word document with Jinja2 templates**

```python
from docxtpl import DocxTemplate

# Load template with Jinja2 placeholders
doc = DocxTemplate("templates/student_worksheet.docx")

# Render with structured context
context = {
    'title': lesson['title'],
    'activities': lesson['activities'],
    'vocabulary': lesson['vocabulary']
}

doc.render(context)
doc.save("output/worksheet.docx")
```

**Template syntax (inside .docx):**
```
Lesson: {{ title }}

Activities:
{% for activity in activities %}
  Activity {{ loop.index }}: {{ activity.name }}
  Duration: {{ activity.duration }} minutes

  Instructions:
  {% for step in activity.instructions %}
    {{ loop.index }}. {{ step }}
  {% endfor %}
{% endfor %}
```

**Source:** [docxtpl documentation](https://docxtpl.readthedocs.io/)

---

### Pattern 2: Hidden First Slide for Lesson Plan

**What:** Generate PowerPoint with first slide hidden, containing complete lesson plan for teacher reference.

**Why:** Requirement SLID-02 specifies "hidden first slide with lesson plan (objective, agenda with timing, anticipated misconceptions, delivery tips)." Teachers need this info but students shouldn't see it during presentation.

**When to use:** All .pptx generation in Phase 1.

**Implementation:**

```python
from pptx import Presentation

prs = Presentation("templates/lesson_slide_deck.pptx")

# Create first slide with lesson plan
lesson_plan_layout = prs.slide_layouts[5]  # Blank or custom layout
slide = prs.slides.add_slide(lesson_plan_layout)

# Add lesson plan content
title_shape = slide.shapes.title
title_shape.text = "Lesson Plan - For Teacher Only"

# Add detailed plan to slide body
textbox = slide.shapes.add_textbox(...)
frame = textbox.text_frame
frame.text = f"""
Objective: {lesson['objective']}

Agenda with Timing:
{format_agenda(lesson['activities'])}

Anticipated Misconceptions:
{format_misconceptions(lesson['misconceptions'])}

Delivery Tips:
{format_tips(lesson['tips'])}
"""

# Hide the first slide (workaround - no official API)
sld = slide._element
sld.set('show', '0')  # '0' = hidden, '1' or None = visible

# Continue with remaining slides...
```

**Checking if slide is hidden:**
```python
show_value = slide._element.get('show')
is_hidden = show_value == '0'
```

**Source:** [GitHub Issue #319 - python-pptx hidden slide support](https://github.com/scanny/python-pptx/issues/319)

**Confidence:** MEDIUM - This is a workaround using internal XML manipulation. It works in production but is not part of the official python-pptx API. Risk of breaking in future versions is low but non-zero.

---

### Pattern 3: Sparse Teacher-Led Slide Format

**What:** Slides contain minimal text (talking points, not paragraphs), 16pt minimum font, visual prompts.

**Why:** Critical pitfall from existing research: AI generates "slides written for self-study instead of teacher-led instruction." Teacher needs slides as conversation scaffolding, not reading material. Requirement SLID-03 specifies "sparse, teacher-led format (talking points and visual prompts, not dense self-study text)."

**When to use:** All slide content generation.

**Anti-pattern (AVOID):**
```python
# Dense paragraph on slide
slide.shapes.title.text = "Photosynthesis Overview"
slide.placeholders[1].text = """
Photosynthesis is the process by which green plants and some other
organisms use sunlight to synthesize foods from carbon dioxide and water.
Photosynthesis in plants generally involves the green pigment chlorophyll
and generates oxygen as a byproduct. The process can be summarized by
the chemical equation: 6CO2 + 6H2O + light energy → C6H12O6 + 6O2.
"""
```

**Correct pattern:**
```python
# Sparse talking points
slide.shapes.title.text = "What is Photosynthesis?"
text_frame = slide.placeholders[1].text_frame

# Bullet points, not paragraphs
bullets = [
    "Process: Light → Energy",
    "Location: Chloroplasts",
    "Products: Glucose + Oxygen",
    "Equation: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂"
]

for bullet in bullets:
    p = text_frame.add_paragraph()
    p.text = bullet
    p.level = 0
    p.font.size = Pt(20)  # Meets 16pt minimum (requirement SLID-04)

# Add presenter notes (what teacher says)
slide.notes_slide.notes_text_frame.text = """
SAY: "Today we're exploring photosynthesis - the amazing process
plants use to make food from sunlight."

ASK: "Who can tell me what chloroplasts are?"

DEMO: Show plant diagram, point to chloroplast location.

WATCH FOR: Common misconception - students think plants "eat" soil.
"""
```

**Font size requirements:**
- Minimum 16pt for all slide text (SLID-04)
- Recommended 20-24pt for body text, 36-40pt for titles
- Rationale: Classroom readability from back row

**Sources:**
- [Presentation Design Trends 2026](https://www.sketchbubble.com/blog/presentation-design-trends-2026-the-ultimate-guide-to-future-ready-slides/)
- [Teacher-Led vs Self-Study Slides Research](https://ctl.columbia.edu/faculty/sapp/slide-design/)
- [PowerPoint Minimum Font Size Best Practices](https://autoppt.com/blog/powerpoint-minimum-font-size-best-practices/)

---

### Pattern 4: Student Materials Formatting

**What:** Word documents formatted for handwritten student responses (1.5-2x line spacing, adequate margins).

**Why:** Known pitfall from user's existing tool: "Worksheets not formatted for writing (single-spaced)." Students need physical space to write answers.

**When to use:** All student-facing .docx generation.

**Implementation:**

```python
from docxtpl import DocxTemplate
from docx.shared import Pt, Inches

doc = DocxTemplate("templates/student_worksheet.docx")

# Template must use these styles
context = {
    'question_spacing': '1.5',  # Line height for questions
    'answer_spacing': '2.0',    # Line height for answer areas
    'answer_lines': 4,          # Number of blank lines per answer
}

# Template contains:
# {% for question in questions %}
# {{ loop.index }}. {{ question.text }}
#
# Answer: _____________________________________________
#
# ________________________________________________________
#
# ________________________________________________________
# {% endfor %}

doc.render(context)
doc.save("output/worksheet.docx")
```

**Formatting requirements:**
- 1.5 or 2.0 line spacing for all text
- Minimum 1-inch margins (0.75" acceptable for content-heavy pages)
- Adequate blank lines for written responses
- Clear section breaks between activities
- Space for name/date at top

**Source:** [Creating Effective Worksheets - Great Resources For Teachers](https://greatresourcesforteachers.com/creating-fun-and-effective-worksheets-tips-for-teachers/)

---

### Pattern 5: Filesystem-Based State Management

**What:** Each workflow stage writes outputs to files; next stage reads from files. No reliance on conversation history for state.

**Why:**
- Token efficiency (stages don't need full conversation context)
- Resumability (can pause/resume without context loss)
- Debugging (inspect intermediate files)
- Survives context compaction
- Enables validation at stage boundaries

**When to use:** All Phase 1 workflow stages.

**Example structure:**

```
.lesson-designer/
└── sessions/
    └── {session_id}/
        ├── 01_input.json              # Teacher requirements
        ├── 02_competency_breakdown.json  # Skills + knowledge decomposition
        ├── 03_lesson_design_v1.json   # Initial Marzano-based design
        ├── 03_lesson_design_v1.md     # Human-readable version
        ├── 04_validation_report.txt   # Cognitive rigor check
        ├── 05_lesson_final.json       # Validated design
        ├── 06_slides.pptx             # Generated PowerPoint
        ├── 07_worksheet.docx          # Generated student materials
        └── 08_generation_log.txt      # Audit trail
```

**State access pattern:**

```python
import json
import os

SESSION_DIR = f".lesson-designer/sessions/{session_id}"

# Stage N writes output
def complete_stage_2():
    breakdown = {
        'skills': ['skill1', 'skill2'],
        'knowledge': ['fact1', 'fact2']
    }
    with open(f"{SESSION_DIR}/02_competency_breakdown.json", 'w') as f:
        json.dump(breakdown, f, indent=2)

# Stage N+1 reads input
def start_stage_3():
    with open(f"{SESSION_DIR}/02_competency_breakdown.json") as f:
        breakdown = json.load(f)
    # Use breakdown to generate lesson design...
```

**Critical note:** Claude Code environment resets working directory between bash calls. Always use **absolute paths**, never relative paths.

**Source:** [Architecture Patterns research](C:/Users/david/OneDrive/Desktop/lesson-designer/.planning/research/ARCHITECTURE.md)

---

### Anti-Patterns to Avoid

#### Anti-Pattern 1: Installing Dependencies at Runtime

**Don't do this:**
```python
import subprocess
subprocess.run(["pip", "install", "python-pptx"])
```

**Why it fails:** Claude API has no network access; installation wastes time; breaks reproducibility.

**Do this instead:** Assume python-pptx, python-docx, docxtpl are pre-installed (they are).

---

#### Anti-Pattern 2: Generating Office Files from Scratch

**Don't do this:**
```python
# Positioning text boxes manually
textbox = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(0.5))
textbox.text = "Title"
font = textbox.text_frame.paragraphs[0].font
font.name = 'Calibri'
font.size = Pt(28)
font.bold = True
font.color.rgb = RGBColor(0, 51, 102)
# ... 50 more lines of positioning
```

**Why it fails:** Fragile; time-consuming; hard to maintain; looks generic.

**Do this instead:** Use template-based generation (Pattern 1).

---

#### Anti-Pattern 3: Using LLM for Validation

**Don't do this:**
```markdown
Stage 5: Review the lesson and check if it's good. Think carefully about
whether it meets Marzano framework requirements.
```

**Why it fails:** Subjective; Claude might hallucinate success; wastes tokens.

**Do this instead:** Use validation scripts (Pattern 6 below).

---

### Pattern 6: Marzano Framework Validation Script

**What:** Python script that analyzes lesson design JSON and verifies cognitive rigor distribution.

**Why:** Critical pitfall: "90% of AI-generated lessons promote only basic-level thinking." Must enforce Marzano framework requirements programmatically, not through prompting alone.

**When to use:** After initial lesson generation (Stage 3), before file generation (Stage 6).

**Implementation:**

```python
# scripts/validate_marzano.py

import json
import sys

MARZANO_LEVELS = {
    'retrieval': ['recall', 'recognize', 'identify', 'list', 'define'],
    'comprehension': ['summarize', 'explain', 'interpret', 'classify'],
    'analysis': ['compare', 'analyze', 'differentiate', 'investigate'],
    'knowledge_utilization': ['hypothesize', 'design', 'create', 'evaluate']
}

def validate_lesson(lesson_path):
    with open(lesson_path) as f:
        lesson = json.load(f)

    errors = []
    warnings = []

    # Check required Marzano components
    if 'activities' not in lesson:
        errors.append("Missing activities array")
        return errors, warnings

    # Analyze cognitive demand distribution
    level_counts = {'retrieval': 0, 'comprehension': 0,
                    'analysis': 0, 'knowledge_utilization': 0}

    for activity in lesson['activities']:
        if 'marzano_level' not in activity:
            errors.append(f"Activity '{activity['name']}': Missing marzano_level")
            continue

        level = activity['marzano_level']
        if level not in level_counts:
            errors.append(f"Activity '{activity['name']}': Invalid level '{level}'")
            continue

        level_counts[level] += 1

    total_activities = sum(level_counts.values())
    if total_activities == 0:
        errors.append("No valid activities with Marzano levels")
        return errors, warnings

    # Calculate percentages
    percentages = {k: (v / total_activities) * 100
                   for k, v in level_counts.items()}

    # CRITICAL VALIDATION: Prevent recall-only lessons
    # Requirement: Minimum 40% higher-order thinking (analysis + knowledge utilization)
    higher_order = percentages['analysis'] + percentages['knowledge_utilization']

    if higher_order < 40:
        errors.append(
            f"Insufficient higher-order thinking: {higher_order:.1f}% "
            f"(minimum 40% required). "
            f"Current distribution: {percentages}"
        )

    # WARNING: Too much lower-order thinking
    if percentages['retrieval'] > 30:
        warnings.append(
            f"High retrieval focus: {percentages['retrieval']:.1f}% "
            f"(recommended <30%)"
        )

    # Check progression (should generally increase in complexity)
    if 'activities' in lesson:
        prev_level_rank = 0
        level_rank = {'retrieval': 1, 'comprehension': 2,
                      'analysis': 3, 'knowledge_utilization': 4}

        for i, activity in enumerate(lesson['activities']):
            if 'marzano_level' in activity:
                rank = level_rank.get(activity['marzano_level'], 0)
                if i > 0 and rank < prev_level_rank - 1:
                    warnings.append(
                        f"Activity {i+1} '{activity['name']}': "
                        f"Cognitive level drops from previous activity "
                        f"(consider gradual progression)"
                    )
                prev_level_rank = rank

    return errors, warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_marzano.py <lesson.json>")
        sys.exit(1)

    lesson_path = sys.argv[1]
    errors, warnings = validate_lesson(lesson_path)

    if errors:
        print("❌ VALIDATION FAILED\n")
        for error in errors:
            print(f"  ERROR: {error}")
        print()

    if warnings:
        print("⚠️  WARNINGS\n")
        for warning in warnings:
            print(f"  WARNING: {warning}")
        print()

    if errors:
        sys.exit(2)  # Exit code 2 blocks execution
    elif warnings:
        print("✓ Validation passed with warnings")
        sys.exit(0)
    else:
        print("✅ Validation passed")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

**Usage in workflow:**

```markdown
## Stage 3b: Validate Cognitive Rigor

After generating initial lesson design:

```bash
python scripts/validate_marzano.py .lesson-designer/sessions/{session_id}/03_lesson_design_v1.json
```

If validation fails:
- Review error messages
- Increase higher-order thinking activities
- Reduce recall-only tasks
- Regenerate lesson design

ONLY proceed to file generation when validation passes.
```

**Validation thresholds:**
- **Minimum 40% higher-order thinking** (analysis + knowledge utilization)
- **Maximum 30% retrieval** (prevent recall-only lessons)
- **Recommended distribution:** 15% retrieval, 25% comprehension, 30% analysis, 30% knowledge utilization

**Sources:**
- [AI-Generated Lesson Plans Fall Short Research](https://theconversation.com/ai-generated-lesson-plans-fall-short-on-inspiring-students-and-promoting-critical-thinking-265355)
- [Marzano's New Taxonomy Framework](https://files.eric.ed.gov/fulltext/EJ1263740.pdf)

---

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| **PowerPoint slide positioning** | Manual coordinate calculation | Template-based layouts (`prs.slide_layouts[N]`) | Templates handle positioning, branding, master slides automatically |
| **Word document styling** | Programmatic font/color/spacing | docxtpl with pre-styled templates | Separates content from formatting; teachers can edit templates |
| **Validation of lesson structure** | LLM self-review ("Is this good?") | Validation scripts with objective criteria | Scripts don't hallucinate; consistent standards; clear errors |
| **Hidden slide implementation** | Custom PowerPoint XML manipulation | `slide._element.set('show', '0')` workaround | Battle-tested solution from GitHub issue #319 |
| **Cognitive rigor analysis** | Prompt engineering alone | Validation script with distribution thresholds | Prevents 90% recall-only problem; enforces minimums |

**Key insight:** AI excels at content generation but needs programmatic guardrails for structural/pedagogical requirements. Use scripts for "hard" constraints (format, cognitive distribution), prompts for "soft" constraints (creativity, relevance).

---

## Common Pitfalls

### Pitfall 1: AI Generates Recall-Only Content

**What goes wrong:** Generated lessons consist of 90% retrieval activities (list, define, recall) with insufficient higher-order thinking.

**Why it happens:** LLMs default to formulaic patterns emphasizing simple recall over analysis/evaluation. Training data skews toward basic cognitive tasks.

**How to avoid:**
- Implement Marzano validation script (Pattern 6) with 40% minimum higher-order thinking
- Use example-based prompting showing high-cognitive-demand lessons
- Include explicit Marzano level markers in prompts
- Block progression if validation fails

**Warning signs:**
- Activities dominated by "list," "define," "recall" verbs
- Questions asking for factual recall vs. analysis
- Validation script fails with "insufficient higher-order thinking"
- Teacher feedback mentions "dumbed down" lessons

**Source:** [AI-Generated Lesson Plans Research](https://theconversation.com/ai-generated-lesson-plans-fall-short-on-inspiring-students-and-promoting-critical-thinking-265355)

---

### Pitfall 2: Self-Study Slides Instead of Teacher-Led

**What goes wrong:** Slides contain dense paragraphs as if students will read independently, not sparse talking points for teacher-led instruction.

**Why it happens:** LLMs trained on textbooks/websites designed for self-study. No explicit distinction in prompts between instructional modes.

**How to avoid:**
- Separate generation templates for teacher materials vs. student materials
- Enforce bullet points, not paragraphs (max 15 words per bullet)
- Require presenter notes with what teacher says/asks/demonstrates
- Validate slide text density (max N characters per slide)

**Warning signs:**
- Slides with full paragraphs
- No presenter notes or discussion prompts
- Materials explain concepts completely (no room for teacher elaboration)
- Classroom engagement drops (teachers report slides are "too wordy")

**Source:** [Teacher-Led vs Self-Study Slides](https://www.sketchbubble.com/blog/presentation-design-trends-2026-the-ultimate-guide-to-future-ready-slides/)

---

### Pitfall 3: Worksheets Formatted for Screen, Not Print

**What goes wrong:** Single-spaced worksheets with insufficient room for handwritten responses; looks good on screen but terrible when printed.

**Why it happens:** LLMs optimize for visual density (screen reading) not physical writing requirements.

**How to avoid:**
- Use docxtpl templates with 1.5-2x line spacing
- Specify "formatted for handwritten student responses"
- Include minimum blank lines for answers (3-4 lines per short answer)
- Test print preview before finalizing templates

**Warning signs:**
- Teacher feedback about "cramped" or "single-spaced" worksheets
- Support requests about formatting
- Users manually editing every generated worksheet

**Source:** Known issue from user's existing tool (PITFALLS.md line 207)

---

### Pitfall 4: Hidden Slide Implementation Breaks

**What goes wrong:** Using `slide._element.set('show', '0')` to hide slides works now but could break if python-pptx changes internal XML handling.

**Why it happens:** This is an unofficial workaround, not part of python-pptx's public API.

**How to avoid:**
- Document the workaround clearly in code comments
- Include fallback: if hiding fails, generate lesson plan as slide 2 with "TEACHER NOTES" title
- Monitor python-pptx releases for official hidden slide support
- Test after any python-pptx version updates

**Warning signs:**
- AttributeError when accessing `_element`
- Slides not hiding despite `show='0'` being set
- XML structure changes in newer PowerPoint versions

**Source:** [GitHub Issue #319](https://github.com/scanny/python-pptx/issues/319)

---

### Pitfall 5: Context Window Bloat in Multi-Lesson Sequences

**What goes wrong:** Performance degrades as context accumulates across multiple lessons (quality drops for lesson 5 vs. lesson 1).

**Why it happens:** "Context rot" - models drop below 50% performance at 32k tokens; claimed 200k context is unreliable around 130k tokens.

**How to avoid:**
- Phase 1 focuses on single lessons only (defer sequences to Phase 6)
- Use filesystem state, not conversation history
- Compress completed lesson outputs to summaries (1-2 paragraphs)
- Set hard token budgets per stage

**Warning signs:**
- Token usage grows exponentially
- Later lessons noticeably worse than earlier ones
- Agent repeats information from earlier context
- Generic responses that miss specific requirements

**Source:** [Context Rot Research](https://research.trychroma.com/context-rot)

---

## Code Examples

### Example 1: Complete PowerPoint Generation

```python
# generate_slides.py
from pptx import Presentation
from pptx.util import Pt, Inches
import json
import sys

def generate_slide_deck(lesson_path, template_path, output_path):
    """Generate PowerPoint slides from lesson design JSON"""

    # Load template and lesson data
    prs = Presentation(template_path)
    with open(lesson_path) as f:
        lesson = json.load(f)

    # Get slide layouts from template
    title_layout = prs.slide_layouts[0]
    content_layout = prs.slide_layouts[1]
    blank_layout = prs.slide_layouts[6]

    # SLIDE 1: Hidden lesson plan (teacher reference)
    slide = prs.slides.add_slide(blank_layout)

    # Add title
    title_shape = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(9), Inches(0.75)
    )
    title_frame = title_shape.text_frame
    title_frame.text = "LESSON PLAN - For Teacher Only"
    p = title_frame.paragraphs[0]
    p.font.size = Pt(24)
    p.font.bold = True

    # Add lesson plan content
    content_shape = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.5), Inches(9), Inches(5.5)
    )
    content_frame = content_shape.text_frame
    content_frame.text = f"""
OBJECTIVE:
{lesson['objective']}

AGENDA WITH TIMING:
{format_agenda(lesson['activities'])}

ANTICIPATED MISCONCEPTIONS:
{format_misconceptions(lesson.get('misconceptions', []))}

DELIVERY TIPS:
{format_tips(lesson.get('tips', []))}
"""
    content_frame.paragraphs[0].font.size = Pt(16)

    # Hide the first slide
    sld = slide._element
    sld.set('show', '0')

    # SLIDE 2: Title slide
    slide = prs.slides.add_slide(title_layout)
    slide.shapes.title.text = lesson['title']
    slide.placeholders[1].text = f"Grade {lesson['grade_level']} | {lesson['duration']} min"

    # SLIDE 3: Learning objectives
    slide = prs.slides.add_slide(content_layout)
    slide.shapes.title.text = "Learning Objectives"
    text_frame = slide.placeholders[1].text_frame
    text_frame.clear()  # Remove default placeholder text

    for objective in lesson['objectives']:
        p = text_frame.add_paragraph()
        p.text = objective
        p.level = 0
        p.font.size = Pt(20)  # Meets 16pt minimum (SLID-04)

    # Add presenter notes
    slide.notes_slide.notes_text_frame.text = (
        "SAY: Introduce the learning goals for today's lesson.\n"
        "ASK: What do you already know about this topic?\n"
        "CHECK: Students understand what they'll be able to do by the end."
    )

    # SLIDES 4+: Activity slides
    for i, activity in enumerate(lesson['activities'], 1):
        slide = prs.slides.add_slide(content_layout)
        slide.shapes.title.text = f"Activity {i}: {activity['name']}"

        # Sparse talking points (not paragraphs)
        text_frame = slide.placeholders[1].text_frame
        text_frame.clear()

        # Duration
        p = text_frame.add_paragraph()
        p.text = f"⏱ {activity['duration']} minutes"
        p.font.size = Pt(18)
        p.space_after = Pt(12)

        # Key points only (max 4-5 bullets)
        for point in activity.get('key_points', [])[:5]:
            p = text_frame.add_paragraph()
            p.text = point
            p.level = 0
            p.font.size = Pt(20)

        # Presenter notes (what teacher does)
        notes = []
        notes.append(f"Marzano Level: {activity['marzano_level']}")
        notes.append(f"\nInstructions:\n{chr(10).join(activity['instructions'])}")
        if 'teacher_tips' in activity:
            notes.append(f"\nTips:\n{activity['teacher_tips']}")

        slide.notes_slide.notes_text_frame.text = "\n".join(notes)

    # Save presentation
    prs.save(output_path)
    print(f"✅ Slide deck generated: {output_path}")

def format_agenda(activities):
    """Format activity list with timing"""
    lines = []
    total_time = 0
    for i, act in enumerate(activities, 1):
        lines.append(f"{i}. {act['name']} ({act['duration']} min)")
        total_time += act['duration']
    lines.append(f"\nTotal: {total_time} minutes")
    return "\n".join(lines)

def format_misconceptions(misconceptions):
    """Format common misconceptions"""
    if not misconceptions:
        return "None specified"
    return "\n".join(f"• {m}" for m in misconceptions)

def format_tips(tips):
    """Format teaching tips"""
    if not tips:
        return "None specified"
    return "\n".join(f"• {t}" for t in tips)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_slides.py <lesson.json> <template.pptx> <output.pptx>")
        sys.exit(1)

    generate_slide_deck(sys.argv[1], sys.argv[2], sys.argv[3])
```

**Source:** [python-pptx documentation](https://python-pptx.readthedocs.io/)

---

### Example 2: Word Document Generation with docxtpl

```python
# generate_worksheet.py
from docxtpl import DocxTemplate
import json
import sys

def generate_worksheet(lesson_path, template_path, output_path):
    """Generate student worksheet from lesson design JSON"""

    # Load template and lesson data
    doc = DocxTemplate(template_path)
    with open(lesson_path) as f:
        lesson = json.load(f)

    # Prepare context for template
    context = {
        'title': lesson['title'],
        'grade_level': lesson['grade_level'],
        'date': '_______________',
        'student_name': '_______________',
        'objectives': lesson['objectives'],
        'activities': [],
        'vocabulary': lesson.get('vocabulary', [])
    }

    # Format activities for worksheet
    for i, activity in enumerate(lesson['activities'], 1):
        # Only include activities suitable for student worksheets
        if activity.get('student_worksheet', True):
            activity_context = {
                'number': i,
                'name': activity['name'],
                'duration': activity['duration'],
                'instructions': activity.get('student_instructions',
                                            activity['instructions']),
                'questions': activity.get('reflection_questions', []),
                'answer_lines': 4  # Blank lines per answer
            }
            context['activities'].append(activity_context)

    # Render template
    doc.render(context)

    # Save output
    doc.save(output_path)
    print(f"✅ Worksheet generated: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_worksheet.py <lesson.json> <template.docx> <output.docx>")
        sys.exit(1)

    generate_worksheet(sys.argv[1], sys.argv[2], sys.argv[3])
```

**Template file (templates/student_worksheet.docx):**

The teacher creates this once in Microsoft Word:

```
[Header with logo/branding]

STUDENT WORKSHEET

Lesson: {{ title }}
Grade {{ grade_level }}

Name: {{ student_name }}        Date: {{ date }}

═══════════════════════════════════════════

LEARNING OBJECTIVES

{% for objective in objectives %}
{{ loop.index }}. {{ objective }}
{% endfor %}

═══════════════════════════════════════════

ACTIVITIES

{% for activity in activities %}

Activity {{ activity.number }}: {{ activity.name }}
Time: {{ activity.duration }} minutes

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

_________________________________________________________

_________________________________________________________

{% endfor %}
{% endif %}

───────────────────────────────────────────

{% endfor %}

VOCABULARY

{% for term in vocabulary %}
{{ term.word }}: {{ term.definition }}

{% endfor %}

[Footer]
```

**Formatting notes:**
- Use 1.5 line spacing for instructions
- Use 2.0 line spacing for answer areas
- Minimum 1-inch margins
- Use styles (Heading 1, Body Text) for easy template editing

**Source:** [docxtpl documentation](https://docxtpl.readthedocs.io/)

---

### Example 3: Complete Validation Script

```python
# validate_outputs.py
import os
import sys
from pptx import Presentation
from docx import Document

def validate_outputs(output_dir):
    """Validate all generated files exist and are valid"""

    errors = []
    warnings = []

    required_files = {
        'slides.pptx': 'PowerPoint slide deck',
        'worksheet.docx': 'Student worksheet',
    }

    for filename, description in required_files.items():
        filepath = os.path.join(output_dir, filename)

        # Check file exists
        if not os.path.exists(filepath):
            errors.append(f"Missing file: {description} ({filename})")
            continue

        # Check file size (not empty)
        size = os.path.getsize(filepath)
        if size < 1000:  # Less than 1KB likely corrupt
            errors.append(f"{description}: File too small ({size} bytes), likely corrupt")
            continue

        # Validate PPTX structure
        if filename.endswith('.pptx'):
            try:
                prs = Presentation(filepath)

                # Check minimum slides
                if len(prs.slides) < 3:
                    errors.append(f"{description}: Too few slides ({len(prs.slides)}), need at least 3")

                # Check title slide
                if len(prs.slides) > 0:
                    title_slide = prs.slides[0]
                    # Skip if first slide is hidden lesson plan
                    if title_slide._element.get('show') != '0':
                        if not title_slide.shapes.title or not title_slide.shapes.title.text:
                            errors.append(f"{description}: Missing title on first visible slide")

                # Check for hidden lesson plan
                has_hidden_slide = False
                for slide in prs.slides:
                    if slide._element.get('show') == '0':
                        has_hidden_slide = True
                        break

                if not has_hidden_slide:
                    warnings.append(f"{description}: No hidden lesson plan slide found (SLID-02)")

                # Check font sizes (sample first 3 slides)
                for i, slide in enumerate(prs.slides[:3]):
                    for shape in slide.shapes:
                        if hasattr(shape, "text_frame"):
                            for paragraph in shape.text_frame.paragraphs:
                                for run in paragraph.runs:
                                    if run.font.size and run.font.size < Pt(16):
                                        warnings.append(
                                            f"{description} slide {i+1}: "
                                            f"Font size {run.font.size.pt}pt below "
                                            f"16pt minimum (SLID-04)"
                                        )

            except Exception as e:
                errors.append(f"{description}: Invalid PowerPoint file - {e}")

        # Validate DOCX structure
        if filename.endswith('.docx'):
            try:
                doc = Document(filepath)

                # Check not too short
                if len(doc.paragraphs) < 5:
                    warnings.append(f"{description}: Document very short ({len(doc.paragraphs)} paragraphs)")

                # Check for unrendered template tags
                text = '\n'.join(p.text for p in doc.paragraphs)
                if '{{' in text or '{%' in text:
                    errors.append(f"{description}: Unrendered Jinja2 template tags found")

                # Check for proper spacing (sample first 10 paragraphs)
                for i, para in enumerate(doc.paragraphs[:10]):
                    if para.paragraph_format.line_spacing:
                        spacing = para.paragraph_format.line_spacing
                        if spacing < 1.5:
                            warnings.append(
                                f"{description} paragraph {i+1}: "
                                f"Line spacing {spacing} below 1.5 recommendation"
                            )

            except Exception as e:
                errors.append(f"{description}: Invalid Word document - {e}")

    # Generate report
    report_path = os.path.join(output_dir, 'validation_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        if errors:
            f.write("❌ VALIDATION FAILED\n\n")
            f.write("ERRORS:\n")
            for error in errors:
                f.write(f"  • {error}\n")
        else:
            f.write("✅ VALIDATION PASSED\n\n")

        if warnings:
            f.write("\n⚠️  WARNINGS:\n")
            for warning in warnings:
                f.write(f"  • {warning}\n")

        if not errors and not warnings:
            f.write("All files generated successfully:\n")
            for filename, description in required_files.items():
                filepath = os.path.join(output_dir, filename)
                size = os.path.getsize(filepath)
                f.write(f"  ✓ {description}: {filename} ({size:,} bytes)\n")

    print(f"Validation report: {report_path}")

    # Print summary
    if errors:
        print(f"\n❌ VALIDATION FAILED: {len(errors)} error(s)")
        for error in errors:
            print(f"  • {error}")
        return False
    elif warnings:
        print(f"\n⚠️  VALIDATION PASSED WITH WARNINGS: {len(warnings)} warning(s)")
        for warning in warnings:
            print(f"  • {warning}")
        return True
    else:
        print("\n✅ VALIDATION PASSED")
        return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_outputs.py <output_directory>")
        sys.exit(1)

    output_dir = sys.argv[1]
    success = validate_outputs(output_dir)
    sys.exit(0 if success else 2)
```

---

## State of the Art

| Old Approach | Current Approach (2026) | When Changed | Impact |
|--------------|-------------------------|--------------|--------|
| Generic AI lesson generators | Marzano/Bloom's validation enforcement | 2025-2026 | Addresses "90% recall-only" problem |
| Self-study slide format | Teacher-led sparse format + presenter notes | 2025 | Prevents "dense paragraph slides" pitfall |
| Single-spaced worksheets | Print-optimized formatting (1.5-2x spacing) | Ongoing issue | Enables actual classroom use |
| Prompt-based validation | Programmatic validation scripts | 2026 best practice | Prevents AI hallucination of quality |
| Multiple separate skills | Single skill with progressive disclosure | 2025-2026 | Better UX, clearer state flow |
| External orchestration | Filesystem-based state in skill | 2026 Claude pattern | Self-contained, resumable |

**Deprecated/outdated:**
- **Dynamic pip install:** Claude environment has pre-installed libraries
- **Manual XML manipulation for most features:** Use python-pptx API (except hidden slides)
- **LLM self-review:** Use validation scripts instead
- **Conversation history for state:** Use filesystem instead

---

## Open Questions

Questions that couldn't be fully resolved in this research phase:

### 1. **Hidden Slide API Stability**
- **What we know:** `slide._element.set('show', '0')` works currently
- **What's unclear:** Will this break in future python-pptx versions?
- **Recommendation:** Implement with fallback; monitor python-pptx releases

### 2. **Optimal Cognitive Distribution**
- **What we know:** Minimum 40% higher-order thinking prevents recall-only problem
- **What's unclear:** Optimal distribution varies by grade level, subject, lesson type
- **Recommendation:** Start with 40% minimum; refine based on teacher feedback in testing

### 3. **Template Customization Scope**
- **What we know:** Teachers want to customize branding/formatting
- **What's unclear:** How much template variety to support (subject-specific? grade-specific?)
- **Recommendation:** Start with single general template; add variants based on demand

### 4. **Competency Decomposition Prompts**
- **What we know:** Competency should be broken into skills + knowledge
- **What's unclear:** Best prompt structure for accurate decomposition
- **Recommendation:** Research recent "decomposed prompting" papers; test with real competencies in Phase 1

---

## Sources

### Primary (HIGH confidence)

**Claude Execution Environment:**
- [Code execution tool - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool) - Pre-installed libraries list
- Confirmed: python-pptx, python-docx, docxtpl available in `code_execution_20250825`

**python-pptx:**
- [python-pptx documentation](https://python-pptx.readthedocs.io/) - Official API docs
- [python-pptx Introduction](https://python-pptx.readthedocs.io/en/latest/user/intro.html) - Capabilities and limitations
- [GitHub Issue #319 - Hidden slides](https://github.com/scanny/python-pptx/issues/319) - Hidden slide workaround

**docxtpl:**
- [docxtpl documentation](https://docxtpl.readthedocs.io/) - Official Jinja2 templating guide
- [GitHub - python-docx-template](https://github.com/elapouya/python-docx-template) - Source and examples

**Marzano Framework:**
- [Marzano's New Taxonomy (PDF)](https://files.eric.ed.gov/fulltext/EJ1263740.pdf) - Academic framework paper
- [Marzano's Taxonomy Framework](https://www.funblocks.net/thinking-matters/classic-mental-models/marzanos-taxonomy) - Practical application guide
- [Comprehension Level Questions - Marzano](https://msgeorgesclass.com/2019/10/16/use-marzanos-taxonomy-to-improve-your-questioning-comprehension-level/) - Implementation examples

### Secondary (MEDIUM confidence)

**Educational AI Research:**
- [AI-Generated Lesson Plans Fall Short](https://theconversation.com/ai-generated-lesson-plans-fall-short-on-inspiring-students-and-promoting-critical-thinking-265355) - 90% recall-only finding
- [AI in Education 2026 Trends](https://www.npr.org/2026/01/14/nx-s1-5674741/ai-schools-education) - Current challenges
- [Bloom's Taxonomy in AI Age](https://journals.sagepub.com/doi/10.1177/02734753241305980) - Cognitive rigor concerns

**Presentation Design:**
- [Presentation Design Trends 2026](https://www.sketchbubble.com/blog/presentation-design-trends-2026-the-ultimate-guide-to-future-ready-slides/) - Teacher-led vs self-study
- [PowerPoint Font Size Best Practices](https://autoppt.com/blog/powerpoint-minimum-font-size-best-practices/) - 16pt minimum rationale
- [Slide Design for Learning](https://ctl.columbia.edu/faculty/sapp/slide-design/) - Educational research

**Claude Skills Architecture:**
- [Skills Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) - Progressive disclosure pattern
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) - Filesystem state management

### Tertiary (LOW confidence)

**General Education:**
- [Creating Effective Worksheets](https://greatresourcesforteachers.com/creating-fun-and-effective-worksheets-tips-for-teachers/) - Formatting guidelines
- [Hidden Slides in PowerPoint](https://support.microsoft.com/en-us/office/hide-or-show-a-slide-8313e1ec-3e20-4464-952f-387931554d69) - Microsoft support

---

## Metadata

**Confidence breakdown:**
- **Standard stack:** HIGH - Official docs confirm python-pptx/docxtpl availability in Claude environment
- **Architecture patterns:** HIGH - Template-based generation is industry standard; filesystem state is documented Claude pattern
- **Marzano validation:** MEDIUM-HIGH - Framework well-documented but optimal thresholds need empirical testing
- **Hidden slide workaround:** MEDIUM - Works currently but not official API; monitor for changes
- **Pitfalls:** HIGH - Based on 2026 research + user's known issues + Claude development patterns

**Research date:** 2026-01-25
**Valid until:** ~60 days (stable stack; Marzano framework timeless; AI pedagogy fast-moving)

---

## Next Steps for Planning

Use this research to inform Phase 1 planning:

### What Phase 1 Must Build:

1. **Competency intake workflow**
   - Teacher specifies: competency, grade level, lesson duration, prior knowledge
   - Decomposition into skills + knowledge (implementation TBD - research decomposed prompting)

2. **Marzano-based lesson design**
   - Generate activities across 4 cognitive levels
   - Ensure minimum 40% higher-order thinking
   - Include timing, materials, instructions

3. **Validation before generation**
   - `validate_marzano.py` script checks cognitive distribution
   - Block progression if validation fails

4. **Template-based file generation**
   - PowerPoint: Hidden lesson plan + sparse teacher-led slides (16pt+ font)
   - Word: Print-formatted student worksheets (1.5-2x spacing)

5. **Output validation**
   - `validate_outputs.py` confirms files exist, are valid, meet requirements

### What Phase 1 Defers:

- Multi-lesson sequences (Phase 6)
- Student persona feedback loops (Phase 2-4)
- Teacher customization UI (Phase 5)
- Subject-specific enhancements (Phase 5)
- Assessment alignment deep-dive (Phase 8)

### Critical Dependencies:

**Before Phase 1 implementation:**
1. Create base templates (slide_deck.pptx, worksheet.docx)
2. Write Marzano framework reference doc (for prompt engineering)
3. Test python-pptx/docxtpl in Claude environment (validation gate)

**Success criteria for Phase 1:**
- Teacher inputs competency → receives .pptx + .docx
- Hidden lesson plan on slide 1
- Minimum 40% higher-order thinking validated
- Sparse slides (talking points, not paragraphs)
- Print-ready worksheets (proper spacing)
- All files open correctly in Office apps
