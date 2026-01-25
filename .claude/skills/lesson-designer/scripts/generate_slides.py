#!/usr/bin/env python3
"""
PowerPoint Slide Deck Generation Script

Generates professionally-designed, classroom-ready PowerPoint presentations.
Uses a coordinated color palette and typography matching high-quality lesson slides.

Design principles:
- Coordinated color palette (blue headers, dark body, red accents)
- Italic titles for visual interest
- Color-coded elements
- Gray italic for hints/tips
- Numbered steps with visual indicators
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional

from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn


# Professional color palette
COLORS = {
    'primary_blue': RGBColor(0x2D, 0x5A, 0x87),     # #2D5A87 - Headers, titles
    'dark_body': RGBColor(0x2C, 0x3E, 0x50),        # #2C3E50 - Main body text
    'secondary_gray': RGBColor(0x34, 0x49, 0x5E),   # #34495E - Secondary text
    'accent_red': RGBColor(0xE7, 0x4C, 0x3C),       # #E74C3C - Emphasis, key points
    'hint_gray': RGBColor(0x7F, 0x8C, 0x8D),        # #7F8C8D - Hints, tips, timing
    'white': RGBColor(0xFF, 0xFF, 0xFF),            # White for contrast
    'timer_yellow': RGBColor(0xF4, 0xD0, 0x3F),     # #F4D03F - Timer display
    'vocab_blue': RGBColor(0x1E, 0x40, 0xAF),       # #1E40AF - Vocabulary terms
    'vocab_green': RGBColor(0x06, 0x5F, 0x46),      # #065F46 - Definitions
}

# Activity icons
ACTIVITY_ICONS = {
    'do now': '✏️',
    'entrance': '✏️',
    'discussion': '💬',
    'debrief': '💬',
    'notes': '📝',
    'vocabulary': '📚',
    'activity': '🎮',
    'simulation': '🎮',
    'group': '👥',
    'exit': '🎯',
    'review': '🔄',
    'practice': '💪',
    'analyze': '🔍',
    'predict': '🔮',
    'question': '❓',
    'default': '📌'
}


def load_lesson_design(lesson_path: str) -> Dict[str, Any]:
    """Load lesson design from JSON file."""
    with open(lesson_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_activity_icon(activity_name: str) -> str:
    """Get appropriate icon for activity based on name."""
    name_lower = activity_name.lower()
    for keyword, icon in ACTIVITY_ICONS.items():
        if keyword in name_lower:
            return icon
    return ACTIVITY_ICONS['default']


def set_shape_fill(shape, color: RGBColor):
    """Set solid fill color for a shape."""
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def add_rounded_rectangle(slide, left, top, width, height, color: RGBColor):
    """Add a rounded rectangle shape with solid fill."""
    from pptx.enum.shapes import MSO_SHAPE
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()  # No border
    return shape


def create_hidden_lesson_plan_slide(prs: Presentation, lesson: Dict) -> None:
    """Create hidden first slide with complete lesson plan for teacher."""
    layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(layout)

    title = lesson.get('title', 'Lesson Plan')
    objective = lesson.get('objective', '')
    activities = lesson.get('activities', [])
    hidden = lesson.get('hidden_slide_content', {})
    misconceptions = hidden.get('misconceptions', [])
    tips = hidden.get('delivery_tips', [])

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.15), Inches(9.4), Inches(0.4))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Lesson Agenda with Notes/Materials"
    p.font.size = Pt(21)
    p.font.color.rgb = COLORS['primary_blue']

    # Objectives box (top right area)
    obj_box = slide.shapes.add_textbox(Inches(6.5), Inches(0.5), Inches(3.3), Inches(1.2))
    tf = obj_box.text_frame
    tf.word_wrap = True

    # Split objective into parts for formatting
    obj_text = objective[:150] if objective else 'Complete lesson objectives'
    p = tf.paragraphs[0]
    p.text = obj_text
    p.font.size = Pt(9.75)
    p.font.color.rgb = COLORS['secondary_gray']

    # Activities list (main content)
    y_pos = Inches(0.7)
    total_time = 0

    for i, act in enumerate(activities, 1):
        name = act.get('name', f'Activity {i}')
        duration = act.get('duration', 5)
        total_time += duration
        instructions = act.get('instructions', [])
        brief = instructions[0][:50] if instructions else ''

        # Number and name
        act_box = slide.shapes.add_textbox(Inches(0.3), y_pos, Inches(6), Inches(0.4))
        tf = act_box.text_frame

        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = f"{i}. {name} "
        run.font.size = Pt(15)
        run.font.bold = True
        run.font.color.rgb = COLORS['primary_blue']

        run = p.add_run()
        run.text = f"({duration} mins): {brief}"
        run.font.size = Pt(15)
        run.font.color.rgb = COLORS['dark_body']

        y_pos += Inches(0.35)

    # Hide the slide
    slide._element.set('show', '0')


def create_title_slide(prs: Presentation, lesson: Dict) -> None:
    """Create title slide with objective framing."""
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    title = lesson.get('title', 'Today\'s Lesson')
    objective = lesson.get('objective', '')
    grade = lesson.get('grade_level', '')
    duration = lesson.get('duration', 50)

    # Main title - large and italic
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.italic = True
    p.font.color.rgb = COLORS['primary_blue']
    p.alignment = PP_ALIGN.CENTER

    # Objective section
    if objective:
        # Label
        obj_label = slide.shapes.add_textbox(Inches(0.5), Inches(2.7), Inches(9), Inches(0.3))
        tf = obj_label.text_frame
        p = tf.paragraphs[0]
        p.text = "TODAY'S OBJECTIVE"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLORS['primary_blue']
        p.alignment = PP_ALIGN.CENTER

        # Objective text
        obj_box = slide.shapes.add_textbox(Inches(0.5), Inches(3.0), Inches(9), Inches(1))
        tf = obj_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = objective
        p.font.size = Pt(16)
        p.font.color.rgb = COLORS['dark_body']
        p.alignment = PP_ALIGN.CENTER

    # Footer
    footer_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.9), Inches(9), Inches(0.3))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{grade} | {duration} minutes"
    p.font.size = Pt(10)
    p.font.color.rgb = COLORS['hint_gray']
    p.alignment = PP_ALIGN.CENTER


def create_agenda_slide(prs: Presentation, lesson: Dict) -> None:
    """Create agenda overview slide."""
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    activities = lesson.get('activities', [])

    # Title - italic
    title_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.3), Inches(4), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "AGENDA"
    p.font.size = Pt(28)
    p.font.italic = True
    p.font.color.rgb = COLORS['primary_blue']

    # Agenda items
    y_pos = Inches(1.0)
    for i, act in enumerate(activities, 1):
        name = act.get('name', f'Activity {i}')

        item_box = slide.shapes.add_textbox(Inches(0.5), y_pos, Inches(4), Inches(0.35))
        tf = item_box.text_frame
        p = tf.paragraphs[0]

        # Check mark + name
        run = p.add_run()
        run.text = "▢ "
        run.font.size = Pt(14)
        run.font.color.rgb = COLORS['secondary_gray']

        run = p.add_run()
        run.text = name
        run.font.size = Pt(14)
        run.font.color.rgb = COLORS['secondary_gray']

        y_pos += Inches(0.35)


def create_activity_slide(prs: Presentation, activity: Dict, activity_num: int) -> None:
    """Create an activity slide with professional design."""
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    name = activity.get('name', f'Activity {activity_num}')
    duration = activity.get('duration', 10)
    instructions = activity.get('instructions', [])
    marzano = activity.get('marzano_level', 'comprehension')

    icon = get_activity_icon(name)

    # Title - italic with icon
    title_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.3), Inches(8), Inches(0.7))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{icon} {name}"
    p.font.size = Pt(26)
    p.font.italic = True
    p.font.color.rgb = COLORS['primary_blue']

    # Timer (top right)
    timer_box = slide.shapes.add_textbox(Inches(8.5), Inches(0.3), Inches(1.2), Inches(0.4))
    tf = timer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{duration:02d}:00"
    p.font.size = Pt(15)
    p.font.color.rgb = COLORS['timer_yellow']
    p.alignment = PP_ALIGN.RIGHT

    # Instructions
    if instructions:
        y_pos = Inches(1.1)
        for i, instr in enumerate(instructions[:5]):
            instr_box = slide.shapes.add_textbox(Inches(0.5), y_pos, Inches(9), Inches(0.5))
            tf = instr_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]

            # Truncate if too long
            text = instr if len(instr) <= 80 else instr[:77] + '...'
            p.text = f"• {text}"
            p.font.size = Pt(16)
            p.font.color.rgb = COLORS['dark_body']

            y_pos += Inches(0.45)

    # Hint/tip at bottom (if available)
    student_output = activity.get('student_output', '')
    if student_output:
        hint_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.8), Inches(9), Inches(0.4))
        tf = hint_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"Output: {student_output}"
        p.font.size = Pt(10)
        p.font.italic = True
        p.font.color.rgb = COLORS['hint_gray']

    # Add presenter notes
    notes = build_presenter_notes(activity, activity_num)
    slide.notes_slide.notes_text_frame.text = notes


def create_vocabulary_slide(prs: Presentation, lesson: Dict) -> None:
    """Create vocabulary slide with color-coded terms."""
    vocab = lesson.get('vocabulary', [])
    if not vocab:
        return

    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.3), Inches(9), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "📚 Key Vocabulary"
    p.font.size = Pt(26)
    p.font.italic = True
    p.font.color.rgb = COLORS['primary_blue']

    # Vocabulary terms - color coded
    term_colors = [
        RGBColor(0x1E, 0x40, 0xAF),  # Blue
        RGBColor(0x06, 0x5F, 0x46),  # Green
        RGBColor(0x92, 0x40, 0x0E),  # Orange
        RGBColor(0x99, 0x1B, 0x1B),  # Red
        RGBColor(0x5B, 0x21, 0xB6),  # Purple
    ]

    y_pos = Inches(1.0)
    for i, term in enumerate(vocab[:5]):
        word = term.get('word', term.get('term', ''))
        definition = term.get('definition', '')
        color = term_colors[i % len(term_colors)]

        # Term (bold, colored)
        term_box = slide.shapes.add_textbox(Inches(0.5), y_pos, Inches(9), Inches(0.3))
        tf = term_box.text_frame
        p = tf.paragraphs[0]
        p.text = word.upper()
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color

        # Definition
        def_box = slide.shapes.add_textbox(Inches(0.5), y_pos + Inches(0.25), Inches(9), Inches(0.5))
        tf = def_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = definition
        p.font.size = Pt(10)
        p.font.color.rgb = COLORS['secondary_gray']

        y_pos += Inches(0.7)


def create_exit_ticket_slide(prs: Presentation, lesson: Dict) -> None:
    """Create exit ticket slide."""
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    assessment = lesson.get('assessment', {})
    questions = assessment.get('questions', [])

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.4), Inches(0.3), Inches(9), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "🎯 Complete the Exit Ticket"
    p.font.size = Pt(26)
    p.font.italic = True
    p.font.color.rgb = COLORS['primary_blue']

    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.9), Inches(9), Inches(0.4))
    tf = subtitle_box.text_frame
    p = tf.paragraphs[0]
    p.text = lesson.get('title', 'Exit Ticket')
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLORS['dark_body']

    # Questions
    y_pos = Inches(1.5)
    for i, q in enumerate(questions[:4], 1):
        q_box = slide.shapes.add_textbox(Inches(0.5), y_pos, Inches(9), Inches(0.6))
        tf = q_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]

        # Number
        run = p.add_run()
        run.text = f"{i}. "
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLORS['secondary_gray']

        # Question
        run = p.add_run()
        run.text = q
        run.font.size = Pt(11)
        run.font.color.rgb = COLORS['secondary_gray']

        y_pos += Inches(0.6)


def build_presenter_notes(activity: Dict, activity_num: int) -> str:
    """Build comprehensive presenter notes."""
    lines = []

    name = activity.get('name', f'Activity {activity_num}')
    duration = activity.get('duration', 10)
    marzano = activity.get('marzano_level', '').replace('_', ' ').title()
    instructions = activity.get('instructions', [])
    materials = activity.get('materials', [])

    lines.append(f"ACTIVITY {activity_num}: {name}")
    lines.append(f"Duration: {duration} minutes | Marzano Level: {marzano}")
    lines.append("=" * 40)

    if instructions:
        lines.append("\nFULL INSTRUCTIONS:")
        for i, instr in enumerate(instructions, 1):
            lines.append(f"  {i}. {instr}")

    if materials:
        lines.append(f"\nMATERIALS: {', '.join(materials)}")

    lines.append("\n" + "=" * 40)
    lines.append("\nSAY: [Introduce this activity]")
    lines.append("ASK: [Check for understanding]")
    lines.append("WATCH FOR: [Common mistakes]")

    return "\n".join(lines)


def generate_slide_deck(
    lesson_path: str,
    template_path: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """Generate complete slide deck from lesson design."""

    lesson = load_lesson_design(lesson_path)

    if output_path is None:
        input_dir = os.path.dirname(os.path.abspath(lesson_path))
        output_path = os.path.join(input_dir, '05_slides.pptx')

    # Create presentation
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    # 1. Hidden lesson plan slide
    create_hidden_lesson_plan_slide(prs, lesson)

    # 2. Title slide
    create_title_slide(prs, lesson)

    # 3. Agenda slide (if more than 2 activities)
    activities = lesson.get('activities', [])
    if len(activities) > 2:
        create_agenda_slide(prs, lesson)

    # 4. Vocabulary slide (if vocabulary exists)
    if lesson.get('vocabulary'):
        create_vocabulary_slide(prs, lesson)

    # 5+. Activity slides
    for i, activity in enumerate(activities, 1):
        name = activity.get('name', '').lower()
        if 'exit' in name and 'ticket' in name:
            continue
        create_activity_slide(prs, activity, i)

    # Final: Exit ticket
    if lesson.get('assessment'):
        create_exit_ticket_slide(prs, lesson)

    # Save
    prs.save(output_path)
    print(f"Slide deck generated: {output_path}")

    if validate_output(output_path):
        print("Validation passed")

    return output_path


def validate_output(output_path: str) -> bool:
    """Verify generated file is valid."""
    try:
        prs = Presentation(output_path)
        if len(prs.slides) < 3:
            print(f"Warning: Only {len(prs.slides)} slides")
            return False
        if prs.slides[0]._element.get('show') != '0':
            print("Warning: First slide not hidden")
        return True
    except Exception as e:
        print(f"Validation error: {e}")
        return False


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_slides.py <lesson.json> [template.pptx] [output.pptx]")
        sys.exit(1)

    lesson_path = sys.argv[1]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(lesson_path):
        print(f"Error: File not found: {lesson_path}")
        sys.exit(1)

    try:
        generate_slide_deck(lesson_path, None, output_path)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
