"""
Claude-Direct Material Generation

Generates lesson materials (slides, worksheets, supplementary) by having Claude
create detailed content specifications, then rendering them to files.

This replaces the old script-based approach with intelligent, context-aware generation.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import anthropic

# python-pptx imports
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml

# python-docx imports
from docx import Document
from docx.shared import Pt as DocxPt, Inches as DocxInches, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn as docx_qn
from docx.oxml import OxmlElement


# ============================================================================
# CLAUDE CONTENT GENERATION
# ============================================================================

def generate_materials_with_claude(
    client: anthropic.Anthropic,
    lesson: Dict[str, Any],
    persona_feedback: List[Dict] = None,
    selected_concerns: List[Dict] = None,
    generate_modified: bool = False,
    generate_extension: bool = False
) -> Dict[str, Any]:
    """
    Have Claude generate detailed content specifications for all materials.

    Returns a dict with:
    - slides: List of slide specs
    - worksheet: Worksheet content spec
    - supplementary: List of supplementary material specs
    - modified_worksheet: Optional modified version spec
    - extension_worksheet: Optional extension version spec
    """

    # Build the prompt with full context
    prompt = _build_materials_prompt(
        lesson,
        persona_feedback,
        selected_concerns,
        generate_modified,
        generate_extension
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.content[0].text

    # Parse JSON from response
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())


def _build_materials_prompt(
    lesson: Dict[str, Any],
    persona_feedback: List[Dict] = None,
    selected_concerns: List[Dict] = None,
    generate_modified: bool = False,
    generate_extension: bool = False
) -> str:
    """Build the prompt for Claude to generate material content."""

    # Format the lesson data
    lesson_json = json.dumps(lesson, indent=2)

    # Format persona feedback if present
    feedback_text = ""
    if persona_feedback:
        feedback_text = "\n\nPERSONA FEEDBACK RECEIVED:\n"
        for fb in persona_feedback:
            feedback_text += f"\n{fb.get('persona_name', 'Persona')} (Rating: {fb.get('overall_rating', '?')}/5):\n"
            feedback_text += f"Reaction: {fb.get('reaction', '')}\n"
            if fb.get('concerns'):
                feedback_text += "Concerns:\n"
                for c in fb['concerns'][:3]:
                    feedback_text += f"  - {c.get('element', '')}: {c.get('issue', '')}\n"

    # Format selected concerns to address
    concerns_text = ""
    if selected_concerns:
        concerns_text = "\n\nSELECTED CONCERNS TO ADDRESS IN MATERIALS:\n"
        for c in selected_concerns:
            concerns_text += f"- [{c.get('from_persona', '')}] {c.get('element', '')}: {c.get('issue', '')}\n"
            if c.get('recommendation'):
                concerns_text += f"  Recommendation: {c.get('recommendation', '')}\n"

    # Differentiation requests
    diff_text = ""
    if generate_modified:
        diff_text += "\n\nGENERATE MODIFIED VERSION: Yes - Create scaffolded version for struggling learners with word banks, sentence starters, visual supports.\n"
    if generate_extension:
        diff_text += "\nGENERATE EXTENSION VERSION: Yes - Create challenging version for advanced learners with deeper questions and open-ended tasks.\n"

    prompt = f"""Generate complete classroom materials for this lesson. Return a JSON object with detailed content specifications.

LESSON DATA:
{lesson_json}
{feedback_text}
{concerns_text}
{diff_text}

Generate a JSON object with this structure:

{{
    "slides": [
        {{
            "slide_number": 1,
            "is_hidden": true,
            "title": "Lesson Plan (Teacher Reference)",
            "content_type": "lesson_plan",
            "body": "Full lesson plan text with objective, agenda with times, materials list, anticipated misconceptions, delivery tips"
        }},
        {{
            "slide_number": 2,
            "is_hidden": false,
            "title": "Today's Objective",
            "content_type": "objective",
            "body": "Student-friendly objective statement",
            "subtext": "Connection to unit/prior learning"
        }},
        {{
            "slide_number": 3,
            "is_hidden": false,
            "title": "Activity Name",
            "content_type": "activity",
            "duration": "X min",
            "icon": "emoji",
            "bullets": ["Point 1", "Point 2", "Point 3"],
            "presenter_notes": "SAY: ...\\nASK: ...\\nWATCH FOR: ..."
        }}
        // ... more slides for each activity
    ],

    "worksheet": {{
        "title": "Worksheet title",
        "sections": [
            {{
                "section_number": 1,
                "title": "Section title matching activity",
                "type": "questions|table|graphic_organizer|writing|vocabulary|exit_ticket",
                "instructions": "Student-facing instructions",
                "content": {{
                    // For type "questions":
                    "questions": [
                        {{"question": "Question text", "lines": 3}},
                        {{"question": "Question text", "lines": 4}}
                    ],
                    // For type "table":
                    "headers": ["Column 1", "Column 2", "Column 3"],
                    "rows": [
                        ["Data", "Data", ""],  // Empty string = student fills in
                        ["Data", "", ""]
                    ],
                    // For type "graphic_organizer":
                    "organizer_type": "venn|tchart|concept_map|flow|comparison",
                    "labels": ["Label 1", "Label 2"],
                    "description": "What students fill in",
                    // For type "vocabulary":
                    "terms": [
                        {{"term": "Word", "definition": "Definition", "example_space": true}}
                    ],
                    // For type "exit_ticket":
                    "questions": [
                        {{"question": "Question", "lines": 3}}
                    ]
                }}
            }}
        ]
    }},

    "supplementary": [
        {{
            "filename": "station_cards.docx",
            "title": "Station Cards",
            "description": "Materials for station rotation activity",
            "cards": [
                {{
                    "card_title": "Station 1: Topic",
                    "context": "2-3 sentences of context/scene-setting",
                    "data_points": [
                        "Data point or statistic 1",
                        "Data point or statistic 2",
                        "Data point or statistic 3"
                    ],
                    "discussion_questions": [
                        "Analytical question requiring synthesis"
                    ],
                    "takeaway_prompt": "Key takeaway: _____________"
                }}
            ]
        }},
        {{
            "filename": "data_sheets.docx",
            "title": "Investigation Data Sheets",
            "description": "Data for student investigation",
            "sheets": [
                {{
                    "sheet_title": "Region/Topic Name",
                    "data_table": {{
                        "headers": ["Category", "Value", "Notes"],
                        "rows": [["Item", "123", "Context"]]
                    }},
                    "source_excerpts": ["Primary source quote or excerpt"],
                    "guiding_questions": ["Question for analysis"]
                }}
            ]
        }}
    ],

    "modified_worksheet": {{
        // Same structure as worksheet, but with added scaffolds:
        // - Word banks added to sections
        // - Sentence starters for writing
        // - Simplified language
        // - Visual supports noted
        // Only include if generate_modified was requested
    }},

    "extension_worksheet": {{
        // Same structure as worksheet, but with added challenge:
        // - More complex questions
        // - Research/inquiry prompts
        // - Open-ended extensions
        // Only include if generate_extension was requested
    }}
}}

CRITICAL GUIDELINES:

1. SLIDES:
   - Slide 1 is ALWAYS hidden with full lesson plan
   - Keep slides SPARSE - 3-5 bullet points max, 15 words max per bullet
   - Include presenter notes with SAY/ASK/WATCH FOR guidance
   - Every activity gets its own slide with duration and icon

2. WORKSHEET:
   - Sections must MATCH what activities actually ask students to do
   - If activity mentions "graphic organizer" - include the actual organizer structure
   - If activity mentions "data analysis" - include space for data and analysis
   - Include adequate writing space (more lines for complex thinking)
   - ALWAYS end with exit ticket

3. SUPPLEMENTARY MATERIALS:
   - Only generate materials that activities ACTUALLY REFERENCE
   - Follow Discovery Principle: provide data/evidence, NOT conclusions
   - 1-2 analysis questions per card/sheet, not fact-finding questions
   - Let students draw conclusions from evidence provided

4. DIFFERENTIATION:
   - Modified: ADD scaffolds, don't remove content. Same objectives.
   - Extension: ADD depth and challenge, same core objectives.

Return ONLY the JSON object, no other text."""

    return prompt


# ============================================================================
# SLIDE RENDERING
# ============================================================================

def render_slides(slides_spec: List[Dict], output_path: str) -> bool:
    """Render slide specifications to a PPTX file."""

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Brand colors
    HEADER_BLUE = RGBColor(0x2D, 0x5A, 0x87)
    DARK_GREEN = RGBColor(0x00, 0x58, 0x2C)
    LIGHT_GREEN = RGBColor(0x4D, 0xAE, 0x58)
    BODY_COLOR = RGBColor(0x2C, 0x3E, 0x50)

    for slide_spec in slides_spec:
        slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout

        # Hide slide if specified
        if slide_spec.get('is_hidden', False):
            slide._element.set('show', '0')

        content_type = slide_spec.get('content_type', 'activity')

        if content_type == 'lesson_plan':
            _render_lesson_plan_slide(slide, slide_spec, DARK_GREEN)
        elif content_type == 'objective':
            _render_objective_slide(slide, slide_spec, DARK_GREEN, LIGHT_GREEN)
        else:
            _render_activity_slide(slide, slide_spec, DARK_GREEN, LIGHT_GREEN, BODY_COLOR)

    prs.save(output_path)
    return True


def _render_lesson_plan_slide(slide, spec: Dict, header_color):
    """Render the hidden lesson plan slide."""
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = spec.get('title', 'Lesson Plan')
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = header_color

    # Body content
    body_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.33), Inches(6))
    tf = body_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = spec.get('body', '')
    p.font.size = Pt(16)
    p.font.name = 'Helvetica'


def _render_objective_slide(slide, spec: Dict, dark_color, light_color):
    """Render the objective slide."""
    # Header bar
    header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.5))
    header.fill.solid()
    header.fill.fore_color.rgb = dark_color
    header.line.fill.background()

    # Title in header
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12.33), Inches(0.7))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = spec.get('title', "Today's Objective")
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Objective text
    obj_box = slide.shapes.add_textbox(Inches(0.75), Inches(2.5), Inches(11.83), Inches(2))
    tf = obj_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = spec.get('body', '')
    p.font.size = Pt(28)
    p.font.color.rgb = dark_color
    p.alignment = PP_ALIGN.CENTER

    # Subtext
    if spec.get('subtext'):
        sub_box = slide.shapes.add_textbox(Inches(0.75), Inches(5), Inches(11.83), Inches(1))
        tf = sub_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = spec.get('subtext', '')
        p.font.size = Pt(20)
        p.font.italic = True
        p.font.color.rgb = light_color
        p.alignment = PP_ALIGN.CENTER


def _render_activity_slide(slide, spec: Dict, dark_color, light_color, body_color):
    """Render an activity slide."""
    # Header bar
    header = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.333), Inches(1.3))
    header.fill.solid()
    header.fill.fore_color.rgb = dark_color
    header.line.fill.background()

    # Icon and title
    icon = spec.get('icon', '📚')
    title = spec.get('title', 'Activity')

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.35), Inches(9), Inches(0.7))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{icon}  {title}"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Duration badge
    duration = spec.get('duration', '')
    if duration:
        dur_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.35), Inches(2.5), Inches(0.6))
        tf = dur_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"⏱️ {duration}"
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0xF4, 0xD0, 0x3F)  # Gold
        p.alignment = PP_ALIGN.RIGHT

    # Bullet points - with proper width to prevent cutoff
    bullets = spec.get('bullets', [])
    if bullets:
        # Use narrower width to prevent text cutoff
        content_box = slide.shapes.add_textbox(Inches(0.75), Inches(1.8), Inches(11.5), Inches(5))
        tf = content_box.text_frame
        tf.word_wrap = True

        for i, bullet in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"• {bullet}"
            p.font.size = Pt(24)
            p.font.color.rgb = body_color
            p.space_after = Pt(12)

    # Presenter notes
    notes = spec.get('presenter_notes', '')
    if notes:
        notes_slide = slide.notes_slide
        notes_tf = notes_slide.notes_text_frame
        notes_tf.text = notes


# ============================================================================
# WORKSHEET RENDERING
# ============================================================================

def render_worksheet(worksheet_spec: Dict, output_path: str) -> bool:
    """Render worksheet specification to a DOCX file."""

    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    style.font.name = 'Helvetica'
    style.font.size = DocxPt(11)

    # Set margins
    for section in doc.sections:
        section.top_margin = DocxInches(0.5)
        section.bottom_margin = DocxInches(0.5)
        section.left_margin = DocxInches(0.75)
        section.right_margin = DocxInches(0.75)

    # Title
    title = doc.add_paragraph()
    title_run = title.add_run(worksheet_spec.get('title', 'Student Worksheet'))
    title_run.bold = True
    title_run.font.size = DocxPt(16)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Name/Date line
    info_table = doc.add_table(rows=1, cols=3)
    cells = info_table.rows[0].cells
    cells[0].text = "Name: _________________"
    cells[1].text = "Period: ____"
    cells[2].text = "Date: ____________"
    for cell in cells:
        cell.paragraphs[0].runs[0].font.size = DocxPt(10)

    doc.add_paragraph()  # Spacing

    # Render each section
    for section in worksheet_spec.get('sections', []):
        _render_worksheet_section(doc, section)

    doc.save(output_path)
    return True


def _render_worksheet_section(doc: Document, section: Dict):
    """Render a single worksheet section."""

    # Section header
    header = doc.add_paragraph()
    section_num = section.get('section_number', '')
    section_title = section.get('title', 'Section')
    header_run = header.add_run(f"Part {section_num}: {section_title}")
    header_run.bold = True
    header_run.font.size = DocxPt(12)

    # Instructions
    instructions = section.get('instructions', '')
    if instructions:
        inst_para = doc.add_paragraph(instructions)
        inst_para.runs[0].font.size = DocxPt(10)
        inst_para.runs[0].italic = True

    # Content based on type
    section_type = section.get('type', 'questions')
    content = section.get('content', {})

    if section_type == 'questions':
        _render_questions(doc, content.get('questions', []))
    elif section_type == 'table':
        _render_table(doc, content)
    elif section_type == 'graphic_organizer':
        _render_graphic_organizer(doc, content)
    elif section_type == 'vocabulary':
        _render_vocabulary(doc, content.get('terms', []))
    elif section_type == 'writing':
        _render_writing_space(doc, content)
    elif section_type == 'exit_ticket':
        _render_exit_ticket(doc, content)

    doc.add_paragraph()  # Spacing between sections


def _render_questions(doc: Document, questions: List[Dict]):
    """Render numbered questions with answer lines."""
    for i, q in enumerate(questions, 1):
        # Question
        q_para = doc.add_paragraph()
        q_run = q_para.add_run(f"{i}. {q.get('question', '')}")
        q_run.font.size = DocxPt(11)

        # Answer lines
        lines = q.get('lines', 3)
        for _ in range(lines):
            line_para = doc.add_paragraph("_" * 80)
            line_para.paragraph_format.line_spacing = 2.0
            line_para.paragraph_format.space_before = DocxPt(6)


def _render_table(doc: Document, content: Dict):
    """Render a data table."""
    headers = content.get('headers', [])
    rows = content.get('rows', [])

    if not headers:
        return

    table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    table.style = 'Table Grid'

    # Headers
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = header
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = DocxPt(10)
        _set_cell_shading(cell, "D0D0D0")

    # Data rows
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_value in enumerate(row_data):
            cell = table.rows[row_idx + 1].cells[col_idx]
            cell.text = str(cell_value) if cell_value else ""
            if cell.paragraphs[0].runs:
                cell.paragraphs[0].runs[0].font.size = DocxPt(10)

    doc.add_paragraph()


def _render_graphic_organizer(doc: Document, content: Dict):
    """Render a graphic organizer structure."""
    org_type = content.get('organizer_type', 'comparison')
    labels = content.get('labels', [])
    description = content.get('description', '')

    if org_type == 'venn':
        # Simple Venn representation with two columns
        table = doc.add_table(rows=2, cols=3)
        table.style = 'Table Grid'

        # Headers
        if len(labels) >= 2:
            table.rows[0].cells[0].text = labels[0]
            table.rows[0].cells[1].text = "Both"
            table.rows[0].cells[2].text = labels[1]

        # Space for answers
        for cell in table.rows[1].cells:
            cell.text = "\n\n\n\n"

    elif org_type == 'tchart':
        table = doc.add_table(rows=2, cols=2)
        table.style = 'Table Grid'

        if len(labels) >= 2:
            table.rows[0].cells[0].text = labels[0]
            table.rows[0].cells[1].text = labels[1]

        for cell in table.rows[1].cells:
            cell.text = "\n\n\n\n\n"

    else:  # Generic comparison or concept map
        if labels:
            for label in labels:
                label_para = doc.add_paragraph()
                label_para.add_run(f"{label}: ").bold = True
                doc.add_paragraph("_" * 70)
                doc.add_paragraph("_" * 70)

    if description:
        desc_para = doc.add_paragraph(f"({description})")
        desc_para.runs[0].font.size = DocxPt(9)
        desc_para.runs[0].italic = True


def _render_vocabulary(doc: Document, terms: List[Dict]):
    """Render vocabulary section."""
    table = doc.add_table(rows=len(terms) + 1, cols=3 if terms and terms[0].get('example_space') else 2)
    table.style = 'Table Grid'

    # Headers
    table.rows[0].cells[0].text = "Term"
    table.rows[0].cells[1].text = "Definition"
    if len(table.columns) > 2:
        table.rows[0].cells[2].text = "Example/Visual"

    for cell in table.rows[0].cells:
        cell.paragraphs[0].runs[0].bold = True
        _set_cell_shading(cell, "D0D0D0")

    # Terms
    for i, term in enumerate(terms):
        row = table.rows[i + 1]
        row.cells[0].text = term.get('term', '')
        row.cells[0].paragraphs[0].runs[0].bold = True
        row.cells[1].text = term.get('definition', '')
        if len(row.cells) > 2:
            row.cells[2].text = ""  # Space for student example


def _render_writing_space(doc: Document, content: Dict):
    """Render writing space with optional prompts."""
    prompt = content.get('prompt', '')
    lines = content.get('lines', 6)

    if prompt:
        p = doc.add_paragraph(prompt)
        p.runs[0].font.size = DocxPt(11)

    for _ in range(lines):
        line_para = doc.add_paragraph("_" * 80)
        line_para.paragraph_format.line_spacing = 2.0


def _render_exit_ticket(doc: Document, content: Dict):
    """Render exit ticket section."""
    # Header box
    header_table = doc.add_table(rows=1, cols=1)
    header_table.style = 'Table Grid'
    cell = header_table.rows[0].cells[0]
    cell.text = "EXIT TICKET"
    cell.paragraphs[0].runs[0].bold = True
    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_cell_shading(cell, "E0E0E0")

    doc.add_paragraph()

    # Questions
    _render_questions(doc, content.get('questions', []))


def _set_cell_shading(cell, color: str):
    """Set background shading for a table cell."""
    shading = OxmlElement('w:shd')
    shading.set(docx_qn('w:fill'), color)
    cell._tc.get_or_add_tcPr().append(shading)


# ============================================================================
# SUPPLEMENTARY MATERIALS RENDERING
# ============================================================================

def render_supplementary(supplementary_spec: List[Dict], output_dir: str) -> List[str]:
    """Render supplementary materials to DOCX files. Returns list of file paths."""

    output_paths = []
    output_dir = Path(output_dir)

    for material in supplementary_spec:
        filename = material.get('filename', 'supplementary.docx')
        output_path = output_dir / filename

        doc = Document()

        # Set default font
        style = doc.styles['Normal']
        style.font.name = 'Helvetica'
        style.font.size = DocxPt(11)

        # Title
        title = doc.add_paragraph()
        title_run = title.add_run(material.get('title', 'Supplementary Materials'))
        title_run.bold = True
        title_run.font.size = DocxPt(16)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Description
        if material.get('description'):
            desc = doc.add_paragraph(material['description'])
            desc.runs[0].italic = True
            desc.alignment = WD_ALIGN_PARAGRAPH.CENTER

        doc.add_paragraph()

        # Render based on content type
        if 'cards' in material:
            _render_cards(doc, material['cards'])
        elif 'sheets' in material:
            _render_data_sheets(doc, material['sheets'])

        doc.save(str(output_path))
        output_paths.append(str(output_path))

    return output_paths


def _render_cards(doc: Document, cards: List[Dict]):
    """Render station/discussion cards."""
    for i, card in enumerate(cards):
        if i > 0:
            doc.add_page_break()

        # Card title
        title = doc.add_paragraph()
        title_run = title.add_run(card.get('card_title', f'Card {i+1}'))
        title_run.bold = True
        title_run.font.size = DocxPt(14)

        # Context
        if card.get('context'):
            ctx = doc.add_paragraph(card['context'])
            ctx.runs[0].font.size = DocxPt(11)

        doc.add_paragraph()

        # Data points
        data_points = card.get('data_points', [])
        if data_points:
            data_header = doc.add_paragraph()
            data_header.add_run("Key Information:").bold = True

            for point in data_points:
                p = doc.add_paragraph(f"• {point}")
                p.paragraph_format.left_indent = DocxInches(0.25)

        doc.add_paragraph()

        # Discussion questions
        questions = card.get('discussion_questions', [])
        if questions:
            q_header = doc.add_paragraph()
            q_header.add_run("Discussion Questions:").bold = True

            for q in questions:
                p = doc.add_paragraph(f"→ {q}")
                p.runs[0].font.size = DocxPt(11)
                p.runs[0].italic = True

        doc.add_paragraph()

        # Takeaway prompt
        if card.get('takeaway_prompt'):
            takeaway = doc.add_paragraph()
            takeaway.add_run(card['takeaway_prompt'])
            # Add line for student response
            doc.add_paragraph("_" * 60)


def _render_data_sheets(doc: Document, sheets: List[Dict]):
    """Render data/investigation sheets."""
    for i, sheet in enumerate(sheets):
        if i > 0:
            doc.add_page_break()

        # Sheet title
        title = doc.add_paragraph()
        title_run = title.add_run(sheet.get('sheet_title', f'Data Sheet {i+1}'))
        title_run.bold = True
        title_run.font.size = DocxPt(14)

        doc.add_paragraph()

        # Data table
        table_data = sheet.get('data_table', {})
        if table_data:
            headers = table_data.get('headers', [])
            rows = table_data.get('rows', [])

            if headers:
                table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
                table.style = 'Table Grid'

                # Headers
                for j, header in enumerate(headers):
                    cell = table.rows[0].cells[j]
                    cell.text = header
                    cell.paragraphs[0].runs[0].bold = True
                    _set_cell_shading(cell, "D0D0D0")

                # Data
                for row_idx, row_data in enumerate(rows):
                    for col_idx, val in enumerate(row_data):
                        table.rows[row_idx + 1].cells[col_idx].text = str(val)

        doc.add_paragraph()

        # Source excerpts
        excerpts = sheet.get('source_excerpts', [])
        if excerpts:
            exc_header = doc.add_paragraph()
            exc_header.add_run("Source Material:").bold = True

            for excerpt in excerpts:
                p = doc.add_paragraph(f'"{excerpt}"')
                p.runs[0].italic = True
                p.paragraph_format.left_indent = DocxInches(0.25)

        doc.add_paragraph()

        # Guiding questions
        questions = sheet.get('guiding_questions', [])
        if questions:
            q_header = doc.add_paragraph()
            q_header.add_run("Analysis Questions:").bold = True

            for q in questions:
                doc.add_paragraph(f"• {q}")
                doc.add_paragraph("_" * 60)
                doc.add_paragraph("_" * 60)


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

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
    Generate all materials for a lesson using Claude-direct approach.

    Returns dict with paths to generated files.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get content specs from Claude
    specs = generate_materials_with_claude(
        client=client,
        lesson=lesson,
        persona_feedback=persona_feedback,
        selected_concerns=selected_concerns,
        generate_modified=generate_modified,
        generate_extension=generate_extension
    )

    result = {}

    # Render slides
    if specs.get('slides'):
        slides_path = output_dir / "slides.pptx"
        render_slides(specs['slides'], str(slides_path))
        result['slides_path'] = str(slides_path)

    # Render worksheet
    if specs.get('worksheet'):
        worksheet_path = output_dir / "worksheet.docx"
        render_worksheet(specs['worksheet'], str(worksheet_path))
        result['worksheet_path'] = str(worksheet_path)

    # Render supplementary materials
    if specs.get('supplementary'):
        supp_paths = render_supplementary(specs['supplementary'], str(output_dir))
        result['supplementary_paths'] = supp_paths

    # Render modified worksheet
    if specs.get('modified_worksheet'):
        modified_path = output_dir / "worksheet_modified.docx"
        render_worksheet(specs['modified_worksheet'], str(modified_path))
        result['modified_worksheet_path'] = str(modified_path)

    # Render extension worksheet
    if specs.get('extension_worksheet'):
        extension_path = output_dir / "worksheet_extension.docx"
        render_worksheet(specs['extension_worksheet'], str(extension_path))
        result['extension_worksheet_path'] = str(extension_path)

    return result
