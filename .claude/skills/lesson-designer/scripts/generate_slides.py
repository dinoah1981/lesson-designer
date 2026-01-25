#!/usr/bin/env python3
"""
PowerPoint Slide Deck Generation Script

Generates classroom-ready PowerPoint presentations from lesson design JSON files.
Implements sparse teacher-led slide format with hidden lesson plan slide.

Key Features:
- Hidden first slide with complete lesson plan for teacher reference
- Sparse slide format: Max 5 bullets per slide, max 15 words per bullet
- Font sizes: 36pt+ titles, 20pt body text (exceeds 16pt minimum)
- Presenter notes with SAY/ASK/DEMO/WATCH FOR guidance

Usage:
    python generate_slides.py <lesson.json> [<template.pptx>] [<output.pptx>]

    With all arguments:
        python generate_slides.py lesson.json template.pptx output.pptx

    With defaults:
        python generate_slides.py lesson.json
        (uses default template, outputs to same directory as input)

Requirements:
    - python-pptx (pip install python-pptx)

Example lesson JSON structure:
    See validate_marzano.py for complete schema.

Output:
    PowerPoint file with:
    - Slide 1 (Hidden): Lesson plan for teacher only
    - Slide 2: Title slide with lesson metadata
    - Slide 3: Learning objectives
    - Slides 4+: Activity slides (one per activity)
    - Final slide: Assessment/exit ticket

Requirements covered:
    - SLID-01: Tool generates actual .pptx files
    - SLID-02: Hidden first slide with lesson plan
    - SLID-03: Sparse, teacher-led format
    - SLID-04: 16pt font minimum (uses 20pt)
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional

from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


# Font size constants (meets/exceeds 16pt minimum per SLID-04)
TITLE_FONT_SIZE = Pt(40)     # Titles: 40pt
SUBTITLE_FONT_SIZE = Pt(28)  # Subtitles: 28pt
BODY_FONT_SIZE = Pt(20)      # Body text: 20pt
NOTES_FONT_SIZE = Pt(12)     # Presenter notes: 12pt (not visible during presentation)

# Sparse format limits (per SLID-03)
MAX_BULLETS_PER_SLIDE = 5
MAX_WORDS_PER_BULLET = 15

# Colors
TITLE_COLOR = RGBColor(0, 51, 102)    # Dark blue
BODY_COLOR = RGBColor(51, 51, 51)     # Dark gray

# Default paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(SCRIPT_DIR, '..', 'templates', 'slide_deck.pptx')


def load_lesson_design(lesson_path: str) -> Dict[str, Any]:
    """Load lesson design from JSON file.

    Args:
        lesson_path: Path to lesson design JSON file

    Returns:
        Parsed lesson design dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    with open(lesson_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def truncate_text(text: str, max_words: int) -> str:
    """Truncate text to maximum number of words.

    Args:
        text: Input text
        max_words: Maximum words allowed

    Returns:
        Truncated text with ellipsis if needed
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    return ' '.join(words[:max_words]) + '...'


def format_agenda(activities: List[Dict]) -> str:
    """Format activity list with timing for lesson plan slide.

    Args:
        activities: List of activity dictionaries

    Returns:
        Formatted agenda string
    """
    lines = []
    total_time = 0

    for i, activity in enumerate(activities, 1):
        name = activity.get('name', f'Activity {i}')
        duration = activity.get('duration', 0)
        lines.append(f"{i}. {name} ({duration} min)")
        total_time += duration

    lines.append(f"\nTotal: {total_time} minutes")
    return "\n".join(lines)


def format_misconceptions(misconceptions: List[str]) -> str:
    """Format misconceptions list for lesson plan slide.

    Args:
        misconceptions: List of anticipated misconceptions

    Returns:
        Formatted misconceptions string
    """
    if not misconceptions:
        return "None specified"
    return "\n".join(f"- {m}" for m in misconceptions)


def format_tips(tips: List[str]) -> str:
    """Format teaching tips for lesson plan slide.

    Args:
        tips: List of delivery tips

    Returns:
        Formatted tips string
    """
    if not tips:
        return "None specified"
    return "\n".join(f"- {t}" for t in tips)


def create_hidden_lesson_plan_slide(prs: Presentation, lesson: Dict) -> None:
    """Create hidden first slide with lesson plan for teacher.

    Contains: objective, agenda with timing, misconceptions, delivery tips.
    Hidden via: slide._element.set('show', '0')

    Args:
        prs: PowerPoint presentation object
        lesson: Lesson design dictionary
    """
    # Use blank layout for full control
    blank_layout = prs.slide_layouts[6]  # Index 6 is typically blank
    slide = prs.slides.add_slide(blank_layout)

    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(9), Inches(0.7)
    )
    title_frame = title_box.text_frame
    title_frame.word_wrap = True
    p = title_frame.paragraphs[0]
    p.text = "LESSON PLAN - For Teacher Only"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TITLE_COLOR

    # Get hidden slide content
    hidden_content = lesson.get('hidden_slide_content', {})
    objective = hidden_content.get('objective', lesson.get('objective', ''))
    agenda_items = hidden_content.get('agenda', [])
    misconceptions = hidden_content.get('misconceptions', [])
    delivery_tips = hidden_content.get('delivery_tips', [])

    # If no structured agenda, build from activities
    if not agenda_items:
        activities = lesson.get('activities', [])
        agenda_text = format_agenda(activities)
    else:
        agenda_lines = []
        for item in agenda_items:
            if isinstance(item, dict):
                agenda_lines.append(f"- {item.get('activity', '')} ({item.get('duration', 0)} min)")
            else:
                agenda_lines.append(f"- {item}")
        agenda_text = "\n".join(agenda_lines)

    # Content sections
    sections = [
        ("OBJECTIVE:", objective),
        ("AGENDA WITH TIMING:", agenda_text),
        ("ANTICIPATED MISCONCEPTIONS:", format_misconceptions(misconceptions)),
        ("DELIVERY TIPS:", format_tips(delivery_tips))
    ]

    y_position = 1.1
    for section_title, section_content in sections:
        # Section title
        section_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(y_position), Inches(9), Inches(0.3)
        )
        section_frame = section_box.text_frame
        section_frame.word_wrap = True
        p = section_frame.paragraphs[0]
        p.text = section_title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR

        y_position += 0.35

        # Section content
        content_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(y_position), Inches(9), Inches(1.0)
        )
        content_frame = content_box.text_frame
        content_frame.word_wrap = True
        p = content_frame.paragraphs[0]
        p.text = section_content
        p.font.size = Pt(12)
        p.font.color.rgb = BODY_COLOR

        # Calculate approximate height based on content
        lines = section_content.count('\n') + 1
        y_position += 0.3 + (lines * 0.2)

    # CRITICAL: Hide the slide (unofficial but working workaround)
    # This sets the 'show' attribute to '0' making slide hidden during presentation
    slide._element.set('show', '0')


def create_title_slide(prs: Presentation, lesson: Dict) -> None:
    """Create visible title slide with lesson title and metadata.

    Args:
        prs: PowerPoint presentation object
        lesson: Lesson design dictionary
    """
    # Use title layout
    title_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_layout)

    # Set title
    title = lesson.get('title', 'Untitled Lesson')
    slide.shapes.title.text = title
    for paragraph in slide.shapes.title.text_frame.paragraphs:
        paragraph.font.size = TITLE_FONT_SIZE
        paragraph.font.color.rgb = TITLE_COLOR

    # Set subtitle with metadata
    grade_level = lesson.get('grade_level', '')
    duration = lesson.get('duration', 50)
    lesson_type = lesson.get('lesson_type', '').replace('_', ' ').title()

    subtitle_text = f"Grade {grade_level} | {duration} min | {lesson_type}"

    # Find subtitle placeholder
    for shape in slide.shapes:
        if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
            shape.text = subtitle_text
            for paragraph in shape.text_frame.paragraphs:
                paragraph.font.size = SUBTITLE_FONT_SIZE
                paragraph.font.color.rgb = BODY_COLOR
            break

    # Add presenter notes
    add_presenter_notes(slide,
        "SAY: Welcome everyone. Today we're going to...\n\n"
        "PREPARATION CHECK:\n"
        "- All materials ready?\n"
        "- Technology working?\n"
        "- Seating arranged appropriately?"
    )


def create_objectives_slide(prs: Presentation, lesson: Dict) -> None:
    """Create slide showing learning objectives.

    Format: Bullet points, not paragraphs.
    Font: 20pt minimum for body text.

    Args:
        prs: PowerPoint presentation object
        lesson: Lesson design dictionary
    """
    # Use content layout
    content_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(content_layout)

    # Set title
    slide.shapes.title.text = "Learning Objectives"
    for paragraph in slide.shapes.title.text_frame.paragraphs:
        paragraph.font.size = TITLE_FONT_SIZE
        paragraph.font.color.rgb = TITLE_COLOR

    # Get objectives - may be list or single string
    objectives = lesson.get('objectives', [])
    if not objectives:
        # Fall back to single objective
        single_obj = lesson.get('objective', '')
        if single_obj:
            objectives = [single_obj]

    # Find body placeholder
    body_shape = None
    for shape in slide.shapes:
        if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
            body_shape = shape
            break

    if body_shape and hasattr(body_shape, 'text_frame'):
        text_frame = body_shape.text_frame
        text_frame.clear()  # Clear default text

        for i, objective in enumerate(objectives[:MAX_BULLETS_PER_SLIDE]):
            p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
            # Truncate if too long
            p.text = truncate_text(objective, MAX_WORDS_PER_BULLET)
            p.level = 0
            p.font.size = BODY_FONT_SIZE
            p.font.color.rgb = BODY_COLOR

    # Add presenter notes
    add_presenter_notes(slide,
        "SAY: By the end of today's lesson, you'll be able to...\n\n"
        "ASK: What do you already know about this topic?\n\n"
        "CHECK: Students understand what they'll be able to do by the end."
    )


def create_activity_slide(prs: Presentation, activity: Dict, activity_num: int) -> None:
    """Create slide for single activity.

    Content: Activity name, duration, 3-5 key talking points.
    Presenter notes: Full instructions, Marzano level, tips.

    CRITICAL: Sparse format - max 5 bullets per slide, max 15 words per bullet.

    Args:
        prs: PowerPoint presentation object
        activity: Activity dictionary
        activity_num: Activity number (1-based)
    """
    # Use content layout
    content_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(content_layout)

    # Get activity details
    name = activity.get('name', f'Activity {activity_num}')
    duration = activity.get('duration', 10)
    marzano_level = activity.get('marzano_level', 'comprehension')
    instructions = activity.get('instructions', [])
    materials = activity.get('materials', [])
    student_output = activity.get('student_output', '')
    assessment_method = activity.get('assessment_method', '')
    differentiation = activity.get('differentiation', {})

    # Set title
    slide.shapes.title.text = f"Activity {activity_num}: {name}"
    for paragraph in slide.shapes.title.text_frame.paragraphs:
        paragraph.font.size = Pt(36)  # Slightly smaller for activity titles
        paragraph.font.color.rgb = TITLE_COLOR

    # Find body placeholder
    body_shape = None
    for shape in slide.shapes:
        if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
            body_shape = shape
            break

    if body_shape and hasattr(body_shape, 'text_frame'):
        text_frame = body_shape.text_frame
        text_frame.clear()

        # Duration indicator
        p = text_frame.paragraphs[0]
        p.text = f"Time: {duration} minutes"
        p.font.size = Pt(18)
        p.font.color.rgb = RGBColor(100, 100, 100)
        p.font.italic = True

        # Extract key talking points from instructions
        # Convert full instructions to sparse bullet points
        key_points = activity.get('key_points', [])
        if not key_points and instructions:
            # Generate sparse points from instructions
            key_points = []
            for instruction in instructions[:4]:  # Max 4 from instructions
                # Extract key concept from instruction
                point = truncate_text(instruction, MAX_WORDS_PER_BULLET)
                key_points.append(point)

        # Add key points (sparse format)
        for point in key_points[:MAX_BULLETS_PER_SLIDE - 1]:  # -1 for duration line
            p = text_frame.add_paragraph()
            p.text = point
            p.level = 0
            p.font.size = BODY_FONT_SIZE
            p.font.color.rgb = BODY_COLOR

    # Build comprehensive presenter notes
    notes_sections = []

    # Marzano level
    level_display = marzano_level.replace('_', ' ').title()
    notes_sections.append(f"MARZANO LEVEL: {level_display}")

    # Full instructions
    if instructions:
        notes_sections.append("\nINSTRUCTIONS:")
        for i, instruction in enumerate(instructions, 1):
            notes_sections.append(f"  {i}. {instruction}")

    # Materials
    if materials:
        notes_sections.append("\nMATERIALS NEEDED:")
        for material in materials:
            notes_sections.append(f"  - {material}")

    # Expected output
    if student_output:
        notes_sections.append(f"\nSTUDENT OUTPUT: {student_output}")

    # Assessment method
    if assessment_method:
        notes_sections.append(f"\nASSESSMENT: {assessment_method}")

    # SAY/ASK/DEMO/WATCH FOR guidance
    notes_sections.append("\n" + "=" * 40)
    notes_sections.append("\nSAY: [Introduce the activity and explain expectations]")
    notes_sections.append("\nASK: [Check for understanding before students begin]")
    notes_sections.append("\nDEMO: [Show example if applicable]")
    notes_sections.append("\nWATCH FOR: [Common issues or misconceptions to address]")

    # Differentiation
    if differentiation:
        support = differentiation.get('support', [])
        extension = differentiation.get('extension', [])
        if support or extension:
            notes_sections.append("\n" + "=" * 40)
            notes_sections.append("\nDIFFERENTIATION:")
            if support:
                notes_sections.append("  Support:")
                for s in support:
                    notes_sections.append(f"    - {s}")
            if extension:
                notes_sections.append("  Extension:")
                for e in extension:
                    notes_sections.append(f"    - {e}")

    add_presenter_notes(slide, "\n".join(notes_sections))


def create_assessment_slide(prs: Presentation, lesson: Dict) -> None:
    """Create slide for assessment/exit ticket.

    Args:
        prs: PowerPoint presentation object
        lesson: Lesson design dictionary
    """
    # Use content layout
    content_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(content_layout)

    # Get assessment details
    assessment = lesson.get('assessment', {})
    assessment_type = assessment.get('type', 'exit_ticket')
    description = assessment.get('description', '')
    questions = assessment.get('questions', [])

    # Set title based on type
    title_map = {
        'exit_ticket': 'Exit Ticket',
        'embedded': 'Check for Understanding',
        'performance': 'Performance Task'
    }
    slide.shapes.title.text = title_map.get(assessment_type, 'Assessment')
    for paragraph in slide.shapes.title.text_frame.paragraphs:
        paragraph.font.size = TITLE_FONT_SIZE
        paragraph.font.color.rgb = TITLE_COLOR

    # Find body placeholder
    body_shape = None
    for shape in slide.shapes:
        if hasattr(shape, 'placeholder_format') and shape.placeholder_format.idx == 1:
            body_shape = shape
            break

    if body_shape and hasattr(body_shape, 'text_frame'):
        text_frame = body_shape.text_frame
        text_frame.clear()

        # Add description if present
        if description:
            p = text_frame.paragraphs[0]
            p.text = truncate_text(description, MAX_WORDS_PER_BULLET)
            p.font.size = BODY_FONT_SIZE
            p.font.color.rgb = BODY_COLOR

        # Add questions
        for i, question in enumerate(questions[:MAX_BULLETS_PER_SLIDE]):
            if i == 0 and not description:
                p = text_frame.paragraphs[0]
            else:
                p = text_frame.add_paragraph()
            p.text = f"{i + 1}. {truncate_text(question, MAX_WORDS_PER_BULLET)}"
            p.level = 0
            p.font.size = BODY_FONT_SIZE
            p.font.color.rgb = BODY_COLOR

    # Add presenter notes
    add_presenter_notes(slide,
        "SAY: Before you leave, I want to check what you learned today.\n\n"
        "TIMING: Allow 3-5 minutes for completion.\n\n"
        "COLLECTION: [How will you collect responses?]\n\n"
        "FOLLOW-UP: Review responses to inform next lesson planning."
    )


def add_presenter_notes(slide, notes_text: str) -> None:
    """Add presenter notes to slide.

    Notes should include:
    - What teacher SAYS
    - What teacher ASKS
    - What to DEMO
    - What to WATCH FOR (common issues)
    - TIMING guidance

    Args:
        slide: PowerPoint slide object
        notes_text: Text content for presenter notes
    """
    notes_slide = slide.notes_slide
    notes_frame = notes_slide.notes_text_frame
    notes_frame.text = notes_text


def validate_output(output_path: str) -> bool:
    """Verify generated file is valid PowerPoint.

    Args:
        output_path: Path to generated .pptx file

    Returns:
        True if file is valid, False otherwise
    """
    try:
        # Try to open the file
        prs = Presentation(output_path)

        # Check it has slides
        if len(prs.slides) < 3:
            print(f"Warning: Generated presentation has only {len(prs.slides)} slides")
            return False

        # Check first slide is hidden
        first_slide = prs.slides[0]
        if first_slide._element.get('show') != '0':
            print("Warning: First slide is not hidden")

        return True

    except Exception as e:
        print(f"Error validating output: {e}")
        return False


def generate_slide_deck(
    lesson_path: str,
    template_path: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """Generate complete slide deck from lesson design.

    Args:
        lesson_path: Path to lesson design JSON (04_lesson_final.json)
        template_path: Path to PowerPoint template (optional)
        output_path: Where to save generated .pptx (optional)

    Returns:
        Path to generated .pptx file
    """
    # Load lesson design
    lesson = load_lesson_design(lesson_path)

    # Determine template path
    if template_path is None:
        template_path = os.path.abspath(DEFAULT_TEMPLATE)

    # Determine output path
    if output_path is None:
        # Output to same directory as input
        input_dir = os.path.dirname(os.path.abspath(lesson_path))
        output_path = os.path.join(input_dir, '05_slides.pptx')

    # Load template
    try:
        prs = Presentation(template_path)
    except Exception as e:
        print(f"Error loading template: {e}")
        print("Using blank presentation instead...")
        prs = Presentation()

    # Clear any existing slides from template
    # (keep layouts but remove sample slides)
    while len(prs.slides) > 0:
        slide = prs.slides[0]
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]

    # Create slides in order

    # 1. Hidden lesson plan slide (SLID-02)
    create_hidden_lesson_plan_slide(prs, lesson)

    # 2. Title slide
    create_title_slide(prs, lesson)

    # 3. Objectives slide
    create_objectives_slide(prs, lesson)

    # 4+. Activity slides (one per activity)
    activities = lesson.get('activities', [])
    for i, activity in enumerate(activities, 1):
        create_activity_slide(prs, activity, i)

    # Final slide: Assessment
    if lesson.get('assessment'):
        create_assessment_slide(prs, lesson)

    # Save presentation
    prs.save(output_path)
    print(f"Slide deck generated: {output_path}")

    # Validate output
    if validate_output(output_path):
        print("Validation passed")
    else:
        print("Validation completed with warnings")

    return output_path


def main():
    """CLI entry point.

    Usage: python generate_slides.py <lesson.json> [<template.pptx>] [<output.pptx>]

    Or with defaults:
    python generate_slides.py <lesson.json>
    (uses default template and outputs to same directory as input)
    """
    if len(sys.argv) < 2:
        print("Usage: python generate_slides.py <lesson.json> [<template.pptx>] [<output.pptx>]")
        print("")
        print("Generate PowerPoint slide deck from lesson design JSON.")
        print("")
        print("Arguments:")
        print("  lesson.json    - Path to lesson design JSON file")
        print("  template.pptx  - (Optional) Path to PowerPoint template")
        print("  output.pptx    - (Optional) Path for output file")
        print("")
        print("If template not specified, uses default template.")
        print("If output not specified, saves as 05_slides.pptx in same directory as input.")
        sys.exit(1)

    lesson_path = sys.argv[1]
    template_path = sys.argv[2] if len(sys.argv) > 2 else None
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    # Verify lesson file exists
    if not os.path.exists(lesson_path):
        print(f"Error: Lesson file not found: {lesson_path}")
        sys.exit(1)

    # Generate slides
    try:
        output = generate_slide_deck(lesson_path, template_path, output_path)
        print(f"\nSlide deck created successfully: {output}")
        sys.exit(0)
    except Exception as e:
        print(f"Error generating slides: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
