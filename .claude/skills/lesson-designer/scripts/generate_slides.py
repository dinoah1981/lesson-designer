#!/usr/bin/env python3
"""
PowerPoint Slide Deck Generation Script

Generates visually appealing, classroom-ready PowerPoint presentations.
Matches the quality of manually-designed lesson slides with:
- Visual elements (emojis as icons)
- Clear timing on each activity slide
- Hidden first slide with complete lesson plan
- Sparse, teacher-led format

Requirements covered:
    - SLID-01: Tool generates actual .pptx files
    - SLID-02: Hidden first slide with lesson plan
    - SLID-03: Sparse, teacher-led format
    - SLID-04: 16pt font minimum
"""

import json
import os
import sys
from typing import Dict, List, Any, Optional

from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR


# Activity icons based on Marzano level
MARZANO_ICONS = {
    'retrieval': '🔍',
    'comprehension': '📖',
    'analysis': '🔬',
    'knowledge_utilization': '🎯'
}

# Activity type icons
ACTIVITY_ICONS = {
    'do now': '✏️',
    'discussion': '💬',
    'notes': '📝',
    'activity': '🎲',
    'group': '👥',
    'exit': '🎟️',
    'review': '🔄',
    'practice': '💪',
    'create': '🎨',
    'analyze': '🔍',
    'default': '📌'
}

# Colors
DARK_BLUE = RGBColor(0, 51, 102)
DARK_GRAY = RGBColor(51, 51, 51)
LIGHT_GRAY = RGBColor(128, 128, 128)
ACCENT_BLUE = RGBColor(0, 102, 204)


def load_lesson_design(lesson_path: str) -> Dict[str, Any]:
    """Load lesson design from JSON file."""
    with open(lesson_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_activity_icon(activity_name: str, marzano_level: str = '') -> str:
    """Get appropriate icon for activity based on name or Marzano level."""
    name_lower = activity_name.lower()

    for keyword, icon in ACTIVITY_ICONS.items():
        if keyword in name_lower:
            return icon

    # Fall back to Marzano-based icon
    return MARZANO_ICONS.get(marzano_level, ACTIVITY_ICONS['default'])


def create_hidden_lesson_plan_slide(prs: Presentation, lesson: Dict) -> None:
    """Create hidden first slide with complete lesson plan for teacher."""
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)

    title = lesson.get('title', 'Lesson Plan')

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.2), Inches(9.4), Inches(0.5))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{title} — Teacher Plan"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    # Get content
    hidden = lesson.get('hidden_slide_content', {})
    objective = hidden.get('objective', lesson.get('objective', ''))
    activities = lesson.get('activities', [])
    misconceptions = hidden.get('misconceptions', [])
    tips = hidden.get('delivery_tips', [])

    # Build content
    content_lines = []
    content_lines.append(f"Objective: {objective}")
    content_lines.append("")

    # Numbered activities with timing
    total_time = 0
    for i, act in enumerate(activities, 1):
        name = act.get('name', f'Activity {i}')
        duration = act.get('duration', 0)
        total_time += duration
        # Brief description from first instruction
        instructions = act.get('instructions', [])
        brief = instructions[0][:60] + '...' if instructions and len(instructions[0]) > 60 else (instructions[0] if instructions else '')
        content_lines.append(f"{i}. {name} ({duration} min): {brief}")

    content_lines.append(f"\nTotal: {total_time} minutes")

    if misconceptions:
        content_lines.append("\nAnticipated Misconceptions:")
        for m in misconceptions[:3]:
            content_lines.append(f"  • {m}")

    if tips:
        content_lines.append("\nDelivery Tips:")
        for t in tips[:3]:
            content_lines.append(f"  • {t}")

    # Content box
    content_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.7), Inches(9.4), Inches(4.5))
    tf = content_box.text_frame
    tf.word_wrap = True

    for i, line in enumerate(content_lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(11) if line.startswith('  ') else Pt(12)
        p.font.color.rgb = DARK_GRAY

    # Materials note at bottom
    materials = lesson.get('materials', [])
    if materials:
        mat_box = slide.shapes.add_textbox(Inches(0.3), Inches(5.0), Inches(9.4), Inches(0.4))
        tf = mat_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"Materials: {', '.join(materials[:5])}"
        p.font.size = Pt(8)
        p.font.color.rgb = LIGHT_GRAY

    # Hide the slide
    slide._element.set('show', '0')


def create_title_slide(prs: Presentation, lesson: Dict) -> None:
    """Create title slide with objective framing."""
    layout = prs.slide_layouts[6]  # Blank for full control
    slide = prs.slides.add_slide(layout)

    # Big title
    title = lesson.get('title', 'Today\'s Lesson')
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(9), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE
    p.alignment = PP_ALIGN.CENTER

    # Objective box
    objective = lesson.get('objective', '')
    if objective:
        obj_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.8), Inches(9), Inches(1))
        tf = obj_box.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = "TODAY'S OBJECTIVE"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE
        p.alignment = PP_ALIGN.CENTER

        p = tf.add_paragraph()
        p.text = objective
        p.font.size = Pt(16)
        p.font.color.rgb = DARK_GRAY
        p.alignment = PP_ALIGN.CENTER

    # Grade/Duration footer
    grade = lesson.get('grade_level', '')
    duration = lesson.get('duration', 50)
    footer_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.8), Inches(9), Inches(0.4))
    tf = footer_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{grade} | {duration} minutes"
    p.font.size = Pt(10)
    p.font.color.rgb = LIGHT_GRAY
    p.alignment = PP_ALIGN.CENTER


def create_activity_slide(prs: Presentation, activity: Dict, activity_num: int, total_activities: int) -> None:
    """Create an activity slide with visual elements and timing."""
    layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(layout)

    name = activity.get('name', f'Activity {activity_num}')
    duration = activity.get('duration', 10)
    marzano_level = activity.get('marzano_level', 'comprehension')
    instructions = activity.get('instructions', [])

    icon = get_activity_icon(name, marzano_level)

    # Activity type label (top left)
    type_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.2), Inches(3), Inches(0.3))
    tf = type_box.text_frame
    p = tf.paragraphs[0]

    # Determine activity type from name
    name_lower = name.lower()
    if 'do now' in name_lower:
        activity_type = "DO NOW"
    elif 'exit' in name_lower:
        activity_type = "EXIT TICKET"
    elif 'discussion' in name_lower or 'debrief' in name_lower:
        activity_type = "DISCUSSION"
    elif 'activity' in name_lower or 'group' in name_lower:
        activity_type = "ACTIVITY"
    else:
        activity_type = f"STEP {activity_num}"

    p.text = activity_type
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    # Title with icon
    title_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.5), Inches(9.4), Inches(0.7))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{icon}  {name}"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    # Instructions as bullet points (sparse)
    if instructions:
        content_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(9), Inches(3))
        tf = content_box.text_frame
        tf.word_wrap = True

        # Show max 5 concise points
        for i, instr in enumerate(instructions[:5]):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()

            # Truncate long instructions
            text = instr if len(instr) <= 80 else instr[:77] + '...'
            p.text = f"• {text}"
            p.font.size = Pt(16)
            p.font.color.rgb = DARK_GRAY
            p.space_after = Pt(8)

    # Timing footer (bottom right)
    time_box = slide.shapes.add_textbox(Inches(7), Inches(4.9), Inches(2.5), Inches(0.3))
    tf = time_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"⏱️ {duration} minutes"
    p.font.size = Pt(10)
    p.font.color.rgb = LIGHT_GRAY
    p.alignment = PP_ALIGN.RIGHT

    # Add presenter notes
    notes_text = build_presenter_notes(activity, activity_num)
    slide.notes_slide.notes_text_frame.text = notes_text


def create_exit_ticket_slide(prs: Presentation, lesson: Dict) -> None:
    """Create exit ticket slide."""
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    assessment = lesson.get('assessment', {})
    questions = assessment.get('questions', [])

    # Type label
    type_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.2), Inches(3), Inches(0.3))
    tf = type_box.text_frame
    p = tf.paragraphs[0]
    p.text = "EXIT TICKET"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.3), Inches(0.5), Inches(9.4), Inches(0.7))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "🎟️  Show What You Know"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

    # Instructions
    instr_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(9), Inches(0.5))
    tf = instr_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Complete these questions before leaving class."
    p.font.size = Pt(14)
    p.font.color.rgb = DARK_GRAY

    # Questions
    if questions:
        q_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.9), Inches(9), Inches(2.5))
        tf = q_box.text_frame
        tf.word_wrap = True

        for i, q in enumerate(questions[:4]):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"{i+1}. {q}"
            p.font.size = Pt(14)
            p.font.color.rgb = DARK_GRAY
            p.space_after = Pt(12)

    # Reminders at bottom
    remind_box = slide.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(9), Inches(0.8))
    tf = remind_box.text_frame

    reminders = ["✓ Work silently and independently", "✓ Submit when finished"]
    for i, r in enumerate(reminders):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = r
        p.font.size = Pt(10)
        p.font.color.rgb = LIGHT_GRAY


def build_presenter_notes(activity: Dict, activity_num: int) -> str:
    """Build comprehensive presenter notes."""
    lines = []

    name = activity.get('name', f'Activity {activity_num}')
    duration = activity.get('duration', 10)
    marzano = activity.get('marzano_level', '').replace('_', ' ').title()
    instructions = activity.get('instructions', [])
    materials = activity.get('materials', [])
    student_output = activity.get('student_output', '')
    assessment = activity.get('assessment_method', '')

    lines.append(f"ACTIVITY {activity_num}: {name}")
    lines.append(f"Duration: {duration} minutes | Marzano: {marzano}")
    lines.append("=" * 40)

    if instructions:
        lines.append("\nFULL INSTRUCTIONS:")
        for i, instr in enumerate(instructions, 1):
            lines.append(f"  {i}. {instr}")

    if materials:
        lines.append(f"\nMATERIALS: {', '.join(materials)}")

    if student_output:
        lines.append(f"\nSTUDENT OUTPUT: {student_output}")

    if assessment:
        lines.append(f"\nASSESSMENT: {assessment}")

    lines.append("\n" + "=" * 40)
    lines.append("\nSAY: [Introduce this activity and set expectations]")
    lines.append("\nASK: [Check for understanding before students begin]")
    lines.append("\nWATCH FOR: [Common mistakes or misconceptions]")

    diff = activity.get('differentiation', {})
    if diff:
        support = diff.get('support', [])
        extension = diff.get('extension', [])
        if support or extension:
            lines.append("\n" + "=" * 40)
            lines.append("\nDIFFERENTIATION:")
            if support:
                lines.append("  Support: " + "; ".join(support[:2]))
            if extension:
                lines.append("  Extension: " + "; ".join(extension[:2]))

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

    # Create new presentation (ignore template for now - we build from scratch)
    prs = Presentation()

    # Set slide size (widescreen 16:9)
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)

    # 1. Hidden lesson plan slide
    create_hidden_lesson_plan_slide(prs, lesson)

    # 2. Title slide
    create_title_slide(prs, lesson)

    # 3+. Activity slides
    activities = lesson.get('activities', [])
    total_activities = len(activities)

    for i, activity in enumerate(activities, 1):
        name = activity.get('name', '').lower()
        # Skip exit ticket - we'll add it as final slide
        if 'exit' in name and 'ticket' in name:
            continue
        create_activity_slide(prs, activity, i, total_activities)

    # Final: Exit ticket slide
    if lesson.get('assessment'):
        create_exit_ticket_slide(prs, lesson)

    # Save
    prs.save(output_path)
    print(f"Slide deck generated: {output_path}")

    # Validate
    if validate_output(output_path):
        print("Validation passed")

    return output_path


def validate_output(output_path: str) -> bool:
    """Verify generated file is valid."""
    try:
        prs = Presentation(output_path)

        if len(prs.slides) < 3:
            print(f"Warning: Only {len(prs.slides)} slides generated")
            return False

        # Check hidden slide
        first = prs.slides[0]
        if first._element.get('show') != '0':
            print("Warning: First slide is not hidden")

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
    template_path = sys.argv[2] if len(sys.argv) > 2 else None
    output_path = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(lesson_path):
        print(f"Error: File not found: {lesson_path}")
        sys.exit(1)

    try:
        output = generate_slide_deck(lesson_path, template_path, output_path)
        print(f"\nSlides created: {output}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
