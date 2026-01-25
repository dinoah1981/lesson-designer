#!/usr/bin/env python3
"""
Generate Student Worksheet/Materials from Lesson Design JSON

Uses docxtpl (Jinja2 templating) to create Word documents from lesson designs.
Selects appropriate material type based on lesson type and ensures formative
assessment is included in every document.

Requirements covered:
    - MATL-01: Generate actual .docx files
    - MATL-03: Material type matches lesson type
    - ASMT-01: Each lesson includes assessment of its objective

Usage:
    python generate_worksheet.py <lesson.json> [template.docx] [output.docx]

    With defaults:
    python generate_worksheet.py <lesson.json>
    (uses default template and outputs to same directory as input)
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional

from docxtpl import DocxTemplate


# Material type mapping based on lesson type
MATERIAL_TYPE_MAP = {
    'introducing': 'worksheet',       # Reading + comprehension questions
    'practicing': 'problem_set',      # Practice exercises
    'applying': 'worksheet',          # Structured application
    'synthesizing': 'activity_guide', # Project guide
    'novel_application': 'problem_set' # Challenge problems
}

# Material type descriptions for template context
MATERIAL_TYPE_DESCRIPTIONS = {
    'worksheet': {
        'title_suffix': 'Student Worksheet',
        'instruction_header': 'Instructions',
        'section_header': 'Activities'
    },
    'problem_set': {
        'title_suffix': 'Problem Set',
        'instruction_header': 'Directions',
        'section_header': 'Problems'
    },
    'activity_guide': {
        'title_suffix': 'Activity Guide',
        'instruction_header': 'Procedure',
        'section_header': 'Steps'
    }
}


def select_material_type(lesson_type: str) -> str:
    """
    Determine appropriate material format based on lesson type.

    Args:
        lesson_type: introducing|practicing|applying|synthesizing|novel_application

    Returns:
        Material type: worksheet|reading|problem_set|activity_guide
    """
    return MATERIAL_TYPE_MAP.get(lesson_type, 'worksheet')


def prepare_template_context(lesson: Dict[str, Any], material_type: str) -> Dict[str, Any]:
    """
    Prepare context dictionary for docxtpl rendering.

    Args:
        lesson: Lesson design data from JSON
        material_type: Selected material type

    Returns:
        Context dictionary for template rendering
    """
    # Get material type metadata
    type_meta = MATERIAL_TYPE_DESCRIPTIONS.get(material_type, MATERIAL_TYPE_DESCRIPTIONS['worksheet'])

    # Build base context
    context = {
        # Title and metadata
        'title': lesson.get('title', 'Untitled Lesson'),
        'title_suffix': type_meta['title_suffix'],
        'grade_level': lesson.get('grade_level', ''),
        'duration': lesson.get('duration', 0),
        'material_type': material_type,
        'instruction_header': type_meta['instruction_header'],
        'section_header': type_meta['section_header'],

        # Learning content
        'objective': lesson.get('objective', ''),
        'objectives': [lesson.get('objective', '')] if lesson.get('objective') else [],

        # Activities (formatted for material type)
        'activities': format_activities_for_worksheet(
            lesson.get('activities', []),
            material_type
        ),

        # Vocabulary
        'vocabulary': lesson.get('vocabulary', []),

        # Placeholders for student info
        'student_name': '_______________',
        'date': '_______________'
    }

    # Add assessment section
    context = add_assessment_section(context, lesson)

    return context


def format_activities_for_worksheet(
    activities: List[Dict[str, Any]],
    material_type: str
) -> List[Dict[str, Any]]:
    """
    Format activities appropriately for the material type.

    Args:
        activities: List of activity dictionaries from lesson design
        material_type: Selected material type

    Returns:
        List of formatted activity dictionaries for template
    """
    formatted = []

    for i, activity in enumerate(activities, 1):
        formatted_activity = {
            'number': i,
            'name': activity.get('name', f'Activity {i}'),
            'duration': activity.get('duration', 0),
            'marzano_level': activity.get('marzano_level', ''),
            'instructions': [],
            'questions': [],
            'answer_lines': 4,  # Default blank lines per answer
            'include_in_worksheet': True
        }

        # Get instructions - prefer student-specific if available
        instructions = activity.get('student_instructions', activity.get('instructions', []))
        if isinstance(instructions, str):
            instructions = [instructions]
        formatted_activity['instructions'] = instructions

        # Format based on material type
        if material_type == 'worksheet':
            # Worksheet: Include reflection questions after each activity
            formatted_activity['questions'] = activity.get('reflection_questions', [])
            # Add standard reflection if none provided
            if not formatted_activity['questions'] and activity.get('student_output'):
                formatted_activity['questions'] = [
                    f"What was the most important thing you learned in this activity?",
                    f"What questions do you still have?"
                ]

        elif material_type == 'problem_set':
            # Problem set: Focus on practice problems
            formatted_activity['questions'] = activity.get('practice_problems', [])
            # Add worked example indicator
            if i == 1:
                formatted_activity['is_worked_example'] = True

        elif material_type == 'activity_guide':
            # Activity guide: Step-by-step with materials checklist
            formatted_activity['materials'] = activity.get('materials', [])
            formatted_activity['recording_section'] = activity.get('student_output', 'Record your observations here.')

        # Get differentiation options
        diff = activity.get('differentiation', {})
        formatted_activity['support_options'] = diff.get('support', [])
        formatted_activity['extension_options'] = diff.get('extension', [])

        formatted.append(formatted_activity)

    return formatted


def add_assessment_section(context: Dict[str, Any], lesson: Dict[str, Any]) -> Dict[str, Any]:
    """
    Add formative assessment to materials.

    Assessment types:
        - exit_ticket: Standalone questions at end
        - embedded: Questions integrated throughout activities
        - performance: Task rubric for demonstration

    CRITICAL: Every lesson MUST include assessment of its objective.
    This is requirement ASMT-01.

    Args:
        context: Template context dictionary
        lesson: Lesson design data

    Returns:
        Updated context with assessment data
    """
    assessment = lesson.get('assessment', {})
    assessment_type = assessment.get('type', 'exit_ticket')

    # Default exit ticket questions if none provided
    default_questions = [
        'What is one thing you learned today?',
        'What is one question you still have?',
        f"How would you explain today's main concept to a classmate?"
    ]

    if assessment_type == 'exit_ticket':
        context['exit_ticket'] = {
            'title': 'Exit Ticket',
            'instructions': 'Answer these questions before leaving class.',
            'questions': assessment.get('questions', default_questions)
        }
        context['has_exit_ticket'] = True
        context['has_embedded_assessment'] = False
        context['has_performance_task'] = False

    elif assessment_type == 'embedded':
        # Assessment questions are already in activities
        context['has_embedded_assessment'] = True
        context['has_exit_ticket'] = False
        context['has_performance_task'] = False
        context['embedded_assessment_note'] = (
            'Assessment is embedded in the activities above. '
            'Your teacher will check your work as you complete each section.'
        )

    elif assessment_type == 'performance':
        context['performance_task'] = {
            'title': 'Performance Task',
            'description': assessment.get('description', 'Demonstrate your understanding.'),
            'success_criteria': assessment.get('criteria', [
                'Completed all required components',
                'Showed understanding of key concepts',
                'Used appropriate vocabulary'
            ])
        }
        context['has_performance_task'] = True
        context['has_exit_ticket'] = False
        context['has_embedded_assessment'] = False

    else:
        # Default to exit ticket if unknown type
        context['exit_ticket'] = {
            'title': 'Exit Ticket',
            'instructions': 'Answer these questions before leaving class.',
            'questions': assessment.get('questions', default_questions)
        }
        context['has_exit_ticket'] = True
        context['has_embedded_assessment'] = False
        context['has_performance_task'] = False

    return context


def render_template(template_path: str, context: Dict[str, Any], output_path: str) -> bool:
    """
    Render docxtpl template with context and save.

    Args:
        template_path: Path to Word template
        context: Context dictionary for rendering
        output_path: Where to save generated .docx

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load template
        doc = DocxTemplate(template_path)

        # Render with context
        doc.render(context)

        # Save output
        doc.save(output_path)

        return True

    except Exception as e:
        print(f"Error rendering template: {e}", file=sys.stderr)
        return False


def validate_output(output_path: str) -> tuple:
    """
    Verify generated file is valid Word document.

    Checks:
        - File exists and can be opened
        - No unrendered Jinja2 tags ({{ or {%)
        - Has minimum content

    Args:
        output_path: Path to generated .docx file

    Returns:
        Tuple of (is_valid: bool, errors: list, warnings: list)
    """
    errors = []
    warnings = []

    # Check file exists
    if not os.path.exists(output_path):
        errors.append(f"File not found: {output_path}")
        return False, errors, warnings

    # Check file size
    size = os.path.getsize(output_path)
    if size < 1000:
        errors.append(f"File too small ({size} bytes), likely corrupt or empty")
        return False, errors, warnings

    try:
        # Import python-docx for validation (not docxtpl)
        from docx import Document
        doc = Document(output_path)
    except Exception as e:
        errors.append(f"Invalid Word document: {e}")
        return False, errors, warnings

    # Check for unrendered Jinja2 tags
    text = '\n'.join(p.text for p in doc.paragraphs)
    if '{{' in text or '{%' in text:
        errors.append("Unrendered Jinja2 template tags found - template rendering failed")

    # Check for minimum content
    if len(doc.paragraphs) < 5:
        warnings.append(f"Document has only {len(doc.paragraphs)} paragraphs - may be incomplete")

    # Check for assessment content (ASMT-01)
    text_lower = text.lower()
    assessment_keywords = ['exit ticket', 'assessment', 'check your understanding', 'reflection', 'performance task']
    has_assessment = any(kw in text_lower for kw in assessment_keywords)
    if not has_assessment:
        warnings.append("May be missing explicit assessment section (check document manually)")

    is_valid = len(errors) == 0
    return is_valid, errors, warnings


def generate_worksheet(lesson_path: str, template_path: str, output_path: str) -> bool:
    """
    Generate student materials from lesson design.

    Args:
        lesson_path: Path to lesson design JSON (04_lesson_final.json)
        template_path: Path to Word template
        output_path: Where to save generated .docx

    Returns:
        True if successful, False otherwise
    """
    # Load lesson design
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            lesson = json.load(f)
    except Exception as e:
        print(f"Error loading lesson design: {e}", file=sys.stderr)
        return False

    # Determine material type from lesson type
    lesson_type = lesson.get('lesson_type', 'introducing')
    material_type = select_material_type(lesson_type)

    print(f"Lesson type: {lesson_type}")
    print(f"Material type: {material_type}")

    # Prepare template context
    context = prepare_template_context(lesson, material_type)

    # Render template
    if not render_template(template_path, context, output_path):
        return False

    # Validate output
    is_valid, errors, warnings = validate_output(output_path)

    if errors:
        print("\nValidation errors:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)

    if warnings:
        print("\nValidation warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if is_valid:
        print(f"\nWorksheet generated successfully: {output_path}")
        return True
    else:
        return False


def get_default_paths(lesson_path: str) -> tuple:
    """
    Get default template and output paths based on lesson path.

    Args:
        lesson_path: Path to lesson design JSON

    Returns:
        Tuple of (template_path, output_path)
    """
    # Get script directory for default template
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, '..', 'templates', 'student_worksheet.docx')
    template_path = os.path.normpath(template_path)

    # Output to same directory as lesson JSON
    lesson_dir = os.path.dirname(os.path.abspath(lesson_path))
    output_path = os.path.join(lesson_dir, '06_worksheet.docx')

    return template_path, output_path


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_worksheet.py <lesson.json> [template.docx] [output.docx]")
        print()
        print("Arguments:")
        print("  lesson.json    Path to lesson design JSON (e.g., 04_lesson_final.json)")
        print("  template.docx  Path to Word template (optional, uses default)")
        print("  output.docx    Output path for generated worksheet (optional)")
        print()
        print("Examples:")
        print("  python generate_worksheet.py session/04_lesson_final.json")
        print("  python generate_worksheet.py lesson.json template.docx output.docx")
        sys.exit(1)

    lesson_path = sys.argv[1]

    # Check lesson file exists
    if not os.path.exists(lesson_path):
        print(f"Error: Lesson file not found: {lesson_path}", file=sys.stderr)
        sys.exit(1)

    # Get template and output paths
    if len(sys.argv) >= 4:
        template_path = sys.argv[2]
        output_path = sys.argv[3]
    elif len(sys.argv) == 3:
        template_path = sys.argv[2]
        _, output_path = get_default_paths(lesson_path)
    else:
        template_path, output_path = get_default_paths(lesson_path)

    # Check template exists
    if not os.path.exists(template_path):
        print(f"Error: Template file not found: {template_path}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Generate worksheet
    success = generate_worksheet(lesson_path, template_path, output_path)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
