# Phase 2: Material Quality & Formatting - Research

**Researched:** 2026-01-25
**Domain:** Document generation, educational materials formatting, assessment design
**Confidence:** HIGH

## Summary

This phase enhances the existing python-docx and python-pptx generators to produce pedagogically complete, properly formatted materials. Research covered five key domains: (1) worksheet formatting with double-spacing and adequate writing space, (2) discussion activity structure with time allocations and facilitation guidance, (3) HTML/JS simulation generation for interactive learning, (4) dedicated assessment lesson types including quizzes and rubrics, and (5) formatting standards for diverse material types.

The standard approach uses the existing python-docx and python-pptx libraries, which already support all required formatting features. Line spacing in python-docx is controlled via `paragraph_format.line_spacing = 2.0` for double-spacing, while python-pptx supports rich teacher notes via `slide.notes_slide.notes_text_frame`. For simulations, p5.js emerges as the recommended library due to its educational focus and extensive STEM curriculum support. Performance task rubrics follow a standard grid structure with criteria, performance levels, scores, and descriptors.

**Primary recommendation:** Extend existing generators with format configuration parameters rather than creating new generator scripts. Use python-docx's line_spacing property for student worksheets, add structured facilitation notes to python-pptx slides, generate standalone HTML files with embedded p5.js for simulations, and create dedicated assessment document generators following established pedagogical patterns.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| python-docx | 1.2.0 | Word document generation with formatting control | Industry standard for programmatic .docx creation; supports line spacing, margins, tables, and all Office formatting features |
| python-pptx | 1.0.0 | PowerPoint generation with notes slides | De facto standard for .pptx generation; supports teacher notes, complex layouts, and full slide design |
| p5.js | Latest (CDN) | Interactive educational simulations | Processing Foundation-backed library designed specifically for education; extensive STEM curriculum support and beginner-friendly API |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Jinja2 | 3.x | HTML template rendering | For generating standalone simulation HTML files with embedded JavaScript |
| docx.shared | (part of python-docx) | Unit measurements (Pt, Inches) | For precise formatting control in worksheets and documents |
| docx.enum.text | (part of python-docx) | Text formatting enums (WD_LINE_SPACING, WD_ALIGN_PARAGRAPH) | For setting line spacing rules and text alignment |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| p5.js | HTML5 Canvas + vanilla JS | More control but requires building animation framework from scratch; p5.js abstracts complexity for educators |
| p5.js | Three.js for 3D simulations | Better for complex 3D but steeper learning curve; p5.js has WebGL mode for basic 3D |
| Embedded JS in HTML | Separate .js files | Cleaner separation but requires multi-file distribution; embedded simplifies deployment for single-file simulations |

**Installation:**
```bash
# Python dependencies already in requirements.txt from Phase 1
pip install python-docx==1.2.0 python-pptx==1.0.0 jinja2

# p5.js via CDN (no installation needed)
# Include in HTML: <script src="https://cdn.jsdelivr.net/npm/p5@latest/lib/p5.min.js"></script>
```

## Architecture Patterns

### Recommended Project Structure
```
.claude/skills/lesson-designer/
├── scripts/
│   ├── generate_worksheet.py      # Enhanced with line spacing control
│   ├── generate_slides.py          # Enhanced with facilitation notes
│   ├── generate_assessment.py      # NEW: Quizzes, tests, rubrics
│   ├── generate_simulation.py      # NEW: HTML/JS simulation files
│   └── validate_outputs.py         # Enhanced with format validation
├── templates/
│   ├── simulation_template.html    # Jinja2 template for p5.js simulations
│   ├── rubric_template.docx        # Optional: Rubric document structure
│   └── discussion_guide_template.pptx  # Optional: Discussion slide structure
└── formatters/
    ├── worksheet_formatter.py      # Line spacing, margins, answer space
    ├── discussion_formatter.py     # Time allocations, structure, facilitation notes
    ├── assessment_formatter.py     # Quiz/test layouts, rubric grids
    └── simulation_formatter.py     # p5.js code generation helpers
```

### Pattern 1: Line Spacing Configuration
**What:** Control line spacing in worksheets to provide adequate student writing space
**When to use:** For all student worksheets, especially those requiring written responses
**Example:**
```python
# Source: https://python-docx.readthedocs.io/en/latest/user/text.html
from docx import Document
from docx.shared import Pt, Inches

doc = Document()

# Set margins for student worksheets
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Add paragraph with double spacing
paragraph = doc.add_paragraph("Student writes answer here:")
para_format = paragraph.paragraph_format
para_format.line_spacing = 2.0  # Double-spaced
para_format.space_after = Pt(12)  # Additional space after paragraph
para_format.space_before = Pt(6)

# Alternative: Use WD_LINE_SPACING enum
from docx.enum.text import WD_LINE_SPACING
paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
```

### Pattern 2: Discussion Activity Structure
**What:** Structured discussion slides with opening, prompts, closing, and teacher facilitation notes
**When to use:** For all discussion activities requiring student-to-student or student-teacher dialogue
**Example:**
```python
# Source: https://python-pptx.readthedocs.io/en/latest/user/notes.html
from pptx import Presentation
from pptx.util import Pt

def create_discussion_slide(prs, slide, activity):
    # Slide visible content
    add_header_bar(prs, slide, f"Discussion: {activity['name']}",
                   timer_text=f"⏱️ {activity['duration']}m")

    # Opening question
    add_content_box(prs, slide, "Opening (2 min):", activity['opening'])

    # Main prompts
    add_content_box(prs, slide, "Discussion Prompts (10 min):",
                    activity['prompts'])

    # Closing
    add_content_box(prs, slide, "Closing (3 min):", activity['closing'])

    # Teacher facilitation notes (hidden from students)
    notes_slide = slide.notes_slide
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = f"FACILITATION GUIDE:\n\n"
    notes_tf.text += f"TIME ALLOCATION:\n"
    notes_tf.text += f"  • Opening: 2 min\n"
    notes_tf.text += f"  • Pair discussion: 5 min\n"
    notes_tf.text += f"  • Group share: 5 min\n"
    notes_tf.text += f"  • Closing: 3 min\n\n"
    notes_tf.text += f"WATCH FOR:\n"
    notes_tf.text += f"  • Students dominating airtime\n"
    notes_tf.text += f"  • Off-task conversations\n"
    notes_tf.text += f"  • Need for clarifying questions\n\n"
    notes_tf.text += f"PROMPTS TO USE:\n"
    notes_tf.text += f"  • 'Can you build on what [student] said?'\n"
    notes_tf.text += f"  • 'Who has a different perspective?'\n"
    notes_tf.text += f"  • 'What evidence supports that claim?'\n"
```

### Pattern 3: Standalone HTML/JS Simulation
**What:** Self-contained HTML files with embedded p5.js simulations
**When to use:** When lesson requires interactive visualization or hands-on manipulation of concepts
**Example:**
```python
# Source: Verified pattern from p5.js educational resources
# https://p5js.org/education-resources/

from jinja2 import Template

SIMULATION_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/p5@latest/lib/p5.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        #instructions {
            max-width: 600px;
            margin-bottom: 20px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 5px;
        }
        canvas {
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div id="instructions">
        <h2>{{ title }}</h2>
        <p>{{ instructions }}</p>
    </div>
    <script>
        // p5.js sketch
        {{ simulation_code }}
    </script>
</body>
</html>
"""

def generate_simulation(competency, lesson_type):
    """Generate educational simulation based on competency."""
    template = Template(SIMULATION_TEMPLATE)

    # Example: Physics velocity simulation
    if 'velocity' in competency.lower():
        simulation_code = """
        let position, velocity;

        function setup() {
            createCanvas(600, 400);
            position = createVector(50, height/2);
            velocity = createVector(2, 0);
        }

        function draw() {
            background(240);

            // Update position
            position.add(velocity);

            // Wrap around
            if (position.x > width) position.x = 0;

            // Draw object
            fill(0, 100, 200);
            circle(position.x, position.y, 30);

            // Draw velocity vector
            stroke(200, 0, 0);
            strokeWeight(2);
            line(position.x, position.y,
                 position.x + velocity.x * 20,
                 position.y + velocity.y * 20);
        }
        """

        return template.render(
            title="Understanding Velocity",
            instructions="Watch the blue circle move. The red arrow shows its velocity vector. Click to change direction.",
            simulation_code=simulation_code
        )
```

### Pattern 4: Performance Task Rubric Structure
**What:** Grid-based rubric with criteria, performance levels, and descriptors
**When to use:** For performance tasks and complex assessments requiring multi-dimensional evaluation
**Example:**
```python
# Source: https://www.niu.edu/citl/resources/guides/instructional-guide/rubrics-for-assessment.shtml
from docx import Document
from docx.shared import Inches, RGBColor

def create_performance_rubric(doc, task_name, criteria_list):
    """
    Create analytical rubric with separate scores per criterion.

    Structure: Criteria x Performance Levels grid
    """
    # Rubric header
    doc.add_heading(f"Performance Task Rubric: {task_name}", level=1)

    # Performance levels: Advanced, Proficient, Developing, Beginning
    levels = ["Advanced (4)", "Proficient (3)", "Developing (2)", "Beginning (1)"]

    # Create table: criteria rows + 1 header row, levels columns + 1 criteria column
    num_rows = len(criteria_list) + 1
    num_cols = len(levels) + 1
    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.style = 'Table Grid'

    # Header row
    header_cells = table.rows[0].cells
    header_cells[0].text = "Criteria"
    for i, level in enumerate(levels):
        header_cells[i + 1].text = level
        # Style header
        for paragraph in header_cells[i + 1].paragraphs:
            paragraph.runs[0].bold = True

    # Criteria rows
    for row_idx, criterion in enumerate(criteria_list):
        cells = table.rows[row_idx + 1].cells

        # Criterion name
        cells[0].text = criterion['name']
        cells[0].paragraphs[0].runs[0].bold = True

        # Descriptors for each level
        for level_idx, descriptor in enumerate(criterion['descriptors']):
            cells[level_idx + 1].text = descriptor

    return table

# Example usage
criteria = [
    {
        'name': 'Content Understanding',
        'descriptors': [
            'Demonstrates deep, nuanced understanding with connections to broader concepts',
            'Shows clear understanding of core concepts with accurate explanations',
            'Demonstrates partial understanding with some gaps or misconceptions',
            'Shows minimal understanding with significant gaps or errors'
        ]
    },
    {
        'name': 'Evidence & Reasoning',
        'descriptors': [
            'Provides compelling evidence with sophisticated analysis',
            'Supports claims with relevant evidence and clear reasoning',
            'Provides some evidence but reasoning is incomplete',
            'Little to no evidence provided to support claims'
        ]
    }
]
```

### Pattern 5: Quiz/Test Generation
**What:** Formatted assessment documents with multiple question types
**When to use:** For dedicated assessment lessons (quizzes, tests)
**Example:**
```python
from docx import Document
from docx.shared import Pt, Inches

def generate_quiz(doc, assessment_data):
    """Generate formatted quiz with multiple question types."""

    # Header
    doc.add_heading(assessment_data['title'], level=1)
    info = doc.add_paragraph()
    info.add_run(f"Name: ________________  Date: __________  Score: ____/{assessment_data['total_points']}")

    question_num = 1

    # Multiple choice section
    if assessment_data.get('multiple_choice'):
        doc.add_heading("Part 1: Multiple Choice", level=2)
        doc.add_paragraph("Circle the best answer.")

        for mc in assessment_data['multiple_choice']:
            # Question
            q_para = doc.add_paragraph()
            q_para.add_run(f"{question_num}. {mc['question']}").bold = True

            # Choices
            for choice in mc['choices']:
                doc.add_paragraph(f"    {choice}", style='List Bullet')

            doc.add_paragraph()  # Spacing
            question_num += 1

    # Short answer section
    if assessment_data.get('short_answer'):
        doc.add_heading("Part 2: Short Answer", level=2)
        doc.add_paragraph("Write your answer in the space provided.")

        for sa in assessment_data['short_answer']:
            # Question
            q_para = doc.add_paragraph()
            q_para.add_run(f"{question_num}. {sa['question']}").bold = True

            # Answer space with double spacing
            for _ in range(sa.get('lines', 4)):
                answer_para = doc.add_paragraph("_" * 80)
                answer_para.paragraph_format.line_spacing = 2.0

            doc.add_paragraph()  # Spacing
            question_num += 1
```

### Anti-Patterns to Avoid
- **Hard-coded line heights:** Don't use fixed Pt values for line spacing; use multipliers (2.0) so spacing scales with font size
- **Ignoring accessibility:** Simulations must include keyboard controls and ARIA labels, not just mouse/touch interaction
- **Vague rubric descriptors:** Avoid qualifiers like "sometimes" or "usually"; use concrete observable behaviors
- **Single-file monoliths:** Don't stuff all generation logic in one script; separate formatters by material type
- **Template files for simple layouts:** For dynamic content like worksheets, programmatic generation is cleaner than template manipulation

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Line spacing in Word docs | Custom XML manipulation | python-docx `paragraph_format.line_spacing` | Line spacing rules are complex (EXACTLY, AT_LEAST, MULTIPLE modes); library handles all edge cases |
| Interactive animations | Custom canvas rendering loop | p5.js `setup()` and `draw()` functions | Animation timing, event handling, and cross-browser compatibility are solved problems; p5.js is battle-tested in education |
| Rubric grid layouts | Manual table cell positioning | python-docx `add_table()` with style | Table formatting, cell merging, and borders are error-prone; library provides consistent layouts |
| Teacher notes in presentations | Custom slide shapes | python-pptx `slide.notes_slide.notes_text_frame` | Notes slides have specific XML structure and master relationships; library manages this correctly |
| HTML template rendering | String concatenation or f-strings | Jinja2 Template engine | Proper escaping, inheritance, and maintainability require template engine; string concat leads to injection vulnerabilities |
| Discussion time tracking | Custom timer JavaScript | p5.js `millis()` or native browser timer | Cross-browser timing accuracy and pause/resume logic are non-trivial; use proven solutions |

**Key insight:** Document generation and educational simulations have mature, well-tested libraries. Custom solutions introduce bugs, maintenance burden, and compatibility issues. The existing python-docx/python-pptx foundation from Phase 1 already handles 80% of requirements; Phase 2 should extend, not replace.

## Common Pitfalls

### Pitfall 1: Line Spacing Confusion (line_spacing vs line_spacing_rule)
**What goes wrong:** Developers set `line_spacing = Pt(24)` expecting double-spacing, but get fixed 24pt spacing regardless of font size
**Why it happens:** python-docx has two related properties: `line_spacing` (value) and `line_spacing_rule` (mode). Setting Length value (Pt) triggers EXACTLY mode; setting float triggers MULTIPLE mode
**How to avoid:** Always use float multipliers for proportional spacing: `paragraph_format.line_spacing = 2.0` for double-spacing
**Warning signs:** Students with larger fonts have tighter-looking spacing than students with smaller fonts; spacing looks inconsistent across different worksheet sections

### Pitfall 2: Simulation Accessibility Failure
**What goes wrong:** Simulations only work with mouse/touch, excluding keyboard-only users and screen reader users
**Why it happens:** Canvas-based simulations don't have native accessibility; developers forget to add keyboard event handlers and semantic HTML
**How to avoid:** (1) Add keyboard controls for all interactions, (2) Include text instructions outside canvas, (3) Provide alternative text description of simulation behavior, (4) Test with keyboard-only navigation
**Warning signs:** Simulation requires mouse dragging with no keyboard alternative; no instructions visible to screen readers; focus trap in canvas element

### Pitfall 3: Vague Rubric Language
**What goes wrong:** Rubric descriptors like "shows good understanding" or "usually provides evidence" lead to inconsistent grading
**Why it happens:** Rubric writers copy generic templates without tailoring to specific task; avoid concrete examples to stay "flexible"
**How to avoid:** Use observable behaviors and concrete criteria: "Cites at least 3 specific examples from text" instead of "provides good evidence"
**Warning signs:** Two teachers give different scores for same work; students don't understand why they lost points; appeals/challenges are frequent

### Pitfall 4: Missing Facilitation Guidance
**What goes wrong:** Discussion slides show prompts but teachers don't know how to structure time or handle common issues
**Why it happens:** Slide content focuses on student-facing material; teacher notes are afterthought or omitted
**How to avoid:** Always populate `slide.notes_slide` with (1) time allocations, (2) facilitation moves, (3) common student misconceptions, (4) example probing questions
**Warning signs:** Teachers skip discussion activities because they're unclear; discussions run over time or end too early; some students dominate while others don't participate

### Pitfall 5: Simulation Complexity Overload
**What goes wrong:** Simulations become too complex, distracting from learning objective or requiring excessive debugging
**Why it happens:** Developer excitement about features; scope creep from "wouldn't it be cool if..."; trying to replicate professional simulations
**How to avoid:** Limit scope to direct mapping to competency; start with minimal viable simulation; test with target grade level; follow p5.js educational examples, not game dev tutorials
**Warning signs:** Simulation has 5+ interactive controls; simulation code exceeds 200 lines; students spend more time figuring out controls than learning concept

### Pitfall 6: Hard-Coded Formatting Values
**What goes wrong:** Worksheets use fixed margin/spacing values that don't adapt to different content or page sizes
**Why it happens:** Copy-paste from one generator to all others; testing only with standard 8.5x11 Letter size
**How to avoid:** Use configuration parameters for margins, line spacing, font sizes; test with different page sizes; use relative units (multipliers) over absolute units (Pt) where possible
**Warning signs:** Content gets cut off when printed; worksheets look cramped or overly sparse; foreign language text (longer words) breaks layouts

### Pitfall 7: No Answer Key Generation
**What goes wrong:** Teachers receive quizzes/tests but no answer keys, requiring manual creation
**Why it happens:** Generator focuses on student-facing document; answer key treated as separate concern
**How to avoid:** Generate paired documents (assessment + answer key) from same data; answer key should show correct answers highlighted and include rubric/scoring guide
**Warning signs:** Teachers request answer keys after generation; inconsistencies between assessment and grading criteria

## Code Examples

Verified patterns from official sources:

### Setting Double-Spaced Lines for Student Worksheets
```python
# Source: https://python-docx.readthedocs.io/en/latest/user/text.html
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_LINE_SPACING

doc = Document()

# Method 1: Float multiplier (RECOMMENDED)
paragraph = doc.add_paragraph("Question 1: Explain the water cycle.")
paragraph.paragraph_format.line_spacing = 2.0  # Double-spaced

# Method 2: Using enum
paragraph2 = doc.add_paragraph("Question 2: What causes seasons?")
paragraph2.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

# Add adequate answer space
for _ in range(5):
    answer_line = doc.add_paragraph("_" * 80)
    answer_line.paragraph_format.line_spacing = 2.0
    answer_line.paragraph_format.space_after = Pt(6)
```

### Adding Teacher Facilitation Notes to Slides
```python
# Source: https://python-pptx.readthedocs.io/en/latest/user/notes.html
from pptx import Presentation

prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[1])

# Student-facing content
title = slide.shapes.title
title.text = "Discussion: What is Democracy?"

# Teacher facilitation notes
notes_slide = slide.notes_slide
text_frame = notes_slide.notes_text_frame
text_frame.text = """FACILITATION GUIDE (15 min total):

OPENING (2 min):
- Ask: "What does democracy mean to you?"
- Record 3-4 initial ideas on board

PAIR DISCUSSION (5 min):
- Students discuss with partner: "What are key features of democracy?"
- Walk around, listen for misconceptions

WHOLE GROUP (6 min):
- Chart responses, group similar ideas
- Push for evidence: "Where do you see that in our community?"

CLOSING (2 min):
- Exit question: "What's one way you participate in democracy?"

WATCH FOR:
- Students confusing democracy with voting only
- Need to define "citizen" for clarity
"""

prs.save('discussion_slides.pptx')
```

### Generating HTML/JS Simulation with p5.js
```python
# Source: https://p5js.org/education-resources/
from jinja2 import Template

def generate_physics_simulation(title, instructions, sketch_code):
    template = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/p5@latest/lib/p5.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        #instructions {
            max-width: 600px;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        canvas { border: 2px solid #333; }
    </style>
</head>
<body>
    <div id="instructions">
        <h2>{{ title }}</h2>
        <p>{{ instructions }}</p>
        <p><strong>Controls:</strong> Click to reset | Spacebar to pause</p>
    </div>
    <script>
{{ sketch_code | indent(8) }}
    </script>
</body>
</html>
    """)

    return template.render(
        title=title,
        instructions=instructions,
        sketch_code=sketch_code
    )

# Example: Projectile motion
sketch = """
let projectile, velocity, gravity;
let paused = false;

function setup() {
    createCanvas(600, 400);
    resetSimulation();
}

function draw() {
    background(220);

    if (!paused) {
        // Apply gravity
        velocity.add(gravity);
        projectile.add(velocity);

        // Bounce off ground
        if (projectile.y > height - 20) {
            projectile.y = height - 20;
            velocity.y *= -0.8;
        }
    }

    // Draw ground
    stroke(0);
    strokeWeight(2);
    line(0, height - 20, width, height - 20);

    // Draw projectile
    fill(255, 0, 0);
    noStroke();
    circle(projectile.x, projectile.y, 20);

    // Show velocity vector
    stroke(0, 0, 255);
    strokeWeight(2);
    line(projectile.x, projectile.y,
         projectile.x + velocity.x * 10,
         projectile.y + velocity.y * 10);
}

function resetSimulation() {
    projectile = createVector(50, 50);
    velocity = createVector(5, 0);
    gravity = createVector(0, 0.2);
}

function mousePressed() {
    resetSimulation();
}

function keyPressed() {
    if (key === ' ') paused = !paused;
}
"""

html_output = generate_physics_simulation(
    "Projectile Motion",
    "Watch how gravity affects the projectile's path. Notice the velocity vector (blue arrow) changes as gravity pulls down.",
    sketch
)
```

### Creating Performance Task Rubric
```python
# Source: https://www.niu.edu/citl/resources/guides/instructional-guide/rubrics-for-assessment.shtml
from docx import Document
from docx.shared import Inches, Pt, RGBColor

def create_analytical_rubric(task_name, criteria):
    doc = Document()

    # Title
    doc.add_heading(f"Performance Task Rubric: {task_name}", level=1)

    # Rubric table
    levels = ["Advanced (4)", "Proficient (3)", "Developing (2)", "Beginning (1)"]
    table = doc.add_table(rows=len(criteria) + 1, cols=len(levels) + 1)
    table.style = 'Table Grid'

    # Header row
    header = table.rows[0].cells
    header[0].text = "Criteria"
    for i, level in enumerate(levels):
        header[i + 1].text = level
        header[i + 1].paragraphs[0].runs[0].bold = True

    # Criteria rows
    for row_idx, criterion in enumerate(criteria):
        cells = table.rows[row_idx + 1].cells
        cells[0].text = criterion['name']
        cells[0].paragraphs[0].runs[0].bold = True

        for level_idx, descriptor in enumerate(criterion['descriptors']):
            cells[level_idx + 1].text = descriptor
            cells[level_idx + 1].paragraphs[0].runs[0].font.size = Pt(10)

    # Set column widths
    table.columns[0].width = Inches(1.5)
    for col in table.columns[1:]:
        col.width = Inches(2.0)

    return doc

# Example usage
criteria = [
    {
        'name': 'Content Knowledge',
        'descriptors': [
            'Demonstrates comprehensive understanding with nuanced analysis and connections to broader concepts',
            'Shows clear understanding of key concepts with accurate explanations',
            'Demonstrates partial understanding with minor gaps or misconceptions',
            'Shows minimal understanding with significant gaps or errors'
        ]
    },
    {
        'name': 'Use of Evidence',
        'descriptors': [
            'Integrates 4+ specific, relevant examples with sophisticated analysis',
            'Cites 3+ relevant examples with clear explanation of how they support claims',
            'Provides 1-2 examples with limited connection to claims',
            'Provides no evidence or irrelevant examples'
        ]
    }
]

rubric_doc = create_analytical_rubric("Historical Analysis Essay", criteria)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Template-based document generation (.docx templates) | Programmatic generation with python-docx | Phase 1 decision (2024) | More maintainable, version-controllable, consistent formatting |
| Flash/Java applets for simulations | HTML5 + p5.js | ~2015-2018 | Universal browser support, mobile-friendly, no plugins required |
| Generic "good, better, best" rubrics | Task-specific analytical rubrics with observable criteria | Current best practice (2020s) | More reliable grading, clearer expectations, better student outcomes |
| Teacher-created facilitation notes (external docs) | Embedded notes in presentation files | python-pptx capability (long-standing) | Single file distribution, notes visible in presenter view |
| Fixed line spacing in worksheets | Proportional line spacing (multipliers) | Current python-docx standard | Scales with font size, accessible for vision-impaired students |

**Deprecated/outdated:**
- **Flash-based simulations:** No longer supported in browsers; replaced by HTML5 Canvas and p5.js
- **Java applets:** Deprecated; replaced by JavaScript-based solutions
- **Hard-coded templates:** For dynamic content, programmatic generation is more maintainable than template manipulation

## Open Questions

Things that couldn't be fully resolved:

1. **Simulation complexity thresholds**
   - What we know: p5.js is appropriate for STEM visualizations; educational examples exist
   - What's unclear: Exact competency-to-simulation mapping; when simulation adds value vs. when static diagram suffices
   - Recommendation: Start conservative—only generate simulations for explicitly interactive competencies (e.g., "manipulate variables," "observe patterns"). Expand based on teacher feedback in later phases.

2. **Rubric granularity**
   - What we know: 4-level rubrics (Advanced, Proficient, Developing, Beginning) are standard; 3-5 criteria recommended
   - What's unclear: How to auto-generate criteria from competency without human review; risk of too-generic or too-specific criteria
   - Recommendation: Use competency + Bloom's level to generate initial criteria, but mark for teacher review. Include examples in descriptors for clarity.

3. **Discussion timing variations**
   - What we know: Standard structure is Opening (2-3 min), Main (10-12 min), Closing (2-3 min)
   - What's unclear: How timing scales with grade level, class size, and discussion complexity
   - Recommendation: Use baseline timings with notes field explaining: "Adjust timing based on class needs. Younger students may need shorter turns; complex topics may need extended time."

4. **Answer key generation for open-ended assessments**
   - What we know: Multiple choice and short answer can have clear answer keys
   - What's unclear: How to generate useful "answer keys" for performance tasks with rubrics (sample responses? Just the rubric?)
   - Recommendation: For performance tasks, "answer key" is the rubric itself plus 1-2 annotated sample responses showing different performance levels.

## Sources

### Primary (HIGH confidence)
- [python-docx official documentation - Working with Text](https://python-docx.readthedocs.io/en/latest/user/text.html) - Line spacing methods and paragraph formatting
- [python-docx official documentation - WD_LINE_SPACING enum](https://python-docx.readthedocs.io/en/latest/api/enum/WdLineSpacing.html) - Line spacing modes
- [python-pptx official documentation - Working with Notes](https://python-pptx.readthedocs.io/en/latest/user/notes.html) - Notes slides and teacher guidance
- [NIU Center for Innovative Teaching and Learning - Rubrics for Assessment](https://www.niu.edu/citl/resources/guides/instructional-guide/rubrics-for-assessment.shtml) - Rubric design best practices

### Secondary (MEDIUM confidence)
- [p5.js Education Resources](https://p5js.org/education-resources/) - Educational simulation framework and curriculum examples
- [Processing Foundation - Improving Science and Math Education using p5.js](https://medium.com/processing-foundation/improving-science-and-math-education-using-p5-js-d434beea465c) - STEM education use cases
- [Facing History - Socratic Seminar Strategy](https://www.facinghistory.org/resource-library/socratic-seminar) - Discussion facilitation structure (403 error on fetch, but verified via WebSearch)
- [Read Write Think - Socratic Seminars](https://www.readwritethink.org/professional-development/strategy-guides/socratic-seminars) - Teacher facilitation guidance
- [MDN Web Docs - CSS and JavaScript Accessibility Best Practices](https://developer.mozilla.org/en/docs/Learn_web_development/Core/Accessibility/CSS_and_JavaScript) - Simulation accessibility standards

### Tertiary (LOW confidence)
- [WebAIM 2026 Predictions](https://webaim.org/blog/2026-predictions/) - Future trends in web accessibility (predictions, not established practice)
- Various WebSearch results on student worksheet spacing - No single authoritative source; triangulated common standards (1-inch margins, double-spacing)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - python-docx and python-pptx are verified via official docs; p5.js is Processing Foundation-backed and widely used in education
- Architecture: HIGH - Patterns verified via official documentation and existing Phase 1 generators
- Pitfalls: MEDIUM - Based on common issues in python-docx GitHub issues, accessibility guidelines, and pedagogical best practices (some from indirect sources)
- Simulation details: MEDIUM - p5.js is verified as educational standard, but specific competency-to-simulation mapping requires domain expertise
- Rubric design: HIGH - Based on authoritative educational assessment sources (NIU CITL, multiple university teaching centers)

**Research date:** 2026-01-25
**Valid until:** 2026-03-25 (60 days for stable libraries; python-docx and python-pptx are mature with infrequent breaking changes)
