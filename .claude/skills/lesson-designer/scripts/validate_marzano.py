#!/usr/bin/env python3
"""
Marzano Cognitive Rigor Validation Script

Validates lesson designs against Marzano framework requirements:
- Enforces minimum 40% higher-order thinking (analysis + knowledge_utilization)
- Warns if retrieval exceeds 30%
- Checks cognitive progression across activities
- Validates timing consistency

Usage:
    python validate_marzano.py <lesson.json>

Exit codes:
    0 - Passed (all requirements met)
    1 - Passed with warnings (requirements met, but improvements suggested)
    2 - Failed (requirements not met, blocks progression)

Example lesson JSON structure:
{
  "title": "Introduction to Photosynthesis",
  "grade_level": "7th grade",
  "duration": 50,
  "lesson_type": "introducing",
  "objective": "Students will explain the process of photosynthesis",
  "activities": [
    {
      "name": "Vocabulary Quick-Match",
      "duration": 5,
      "marzano_level": "retrieval",
      "instructions": ["Match terms to definitions"],
      "materials": ["Flashcards"],
      "student_output": "Completed matching exercise",
      "assessment_method": "Accuracy check"
    },
    {
      "name": "Concept Mapping",
      "duration": 15,
      "marzano_level": "comprehension",
      "instructions": ["Create diagram showing relationships"],
      "materials": ["Paper", "Markers"],
      "student_output": "Concept map",
      "assessment_method": "Review for key relationships"
    },
    {
      "name": "Error Analysis",
      "duration": 15,
      "marzano_level": "analysis",
      "instructions": ["Find and explain errors in examples"],
      "materials": ["Worksheet with errors"],
      "student_output": "Error analysis with explanations",
      "assessment_method": "Check error identification accuracy"
    },
    {
      "name": "Design Challenge",
      "duration": 15,
      "marzano_level": "knowledge_utilization",
      "instructions": ["Design experiment to test hypothesis"],
      "materials": ["Design template"],
      "student_output": "Experimental design plan",
      "assessment_method": "Rubric evaluation"
    }
  ]
}
"""

import json
import sys
import os
from typing import Dict, List, Tuple, Any


# Valid Marzano cognitive levels in order of complexity
MARZANO_LEVELS = ['retrieval', 'comprehension', 'analysis', 'knowledge_utilization']

# Map levels to numeric ranks for progression checking
LEVEL_RANKS = {
    'retrieval': 1,
    'comprehension': 2,
    'analysis': 3,
    'knowledge_utilization': 4
}

# Thresholds (as percentages)
MIN_HIGHER_ORDER = 40.0  # Minimum combined analysis + knowledge_utilization
MAX_RETRIEVAL = 30.0     # Maximum retrieval-only activities
RECOMMENDED_DISTRIBUTION = {
    'retrieval': 15.0,
    'comprehension': 25.0,
    'analysis': 30.0,
    'knowledge_utilization': 30.0
}


def validate_required_fields(lesson: Dict) -> List[str]:
    """Check that all required top-level fields are present."""
    errors = []
    required_fields = ['title', 'grade_level', 'duration', 'activities']

    for field in required_fields:
        if field not in lesson:
            errors.append(f"Missing required field: '{field}'")

    # Check activities array
    if 'activities' in lesson:
        if not isinstance(lesson['activities'], list):
            errors.append("'activities' must be an array")
        elif len(lesson['activities']) == 0:
            errors.append("'activities' array is empty - lesson must have at least one activity")

    return errors


def validate_activity_fields(activities: List[Dict]) -> List[str]:
    """Check that each activity has required fields."""
    errors = []
    required_activity_fields = ['name', 'duration', 'marzano_level']

    for i, activity in enumerate(activities, 1):
        activity_name = activity.get('name', f'Activity {i}')

        for field in required_activity_fields:
            if field not in activity:
                errors.append(f"Activity '{activity_name}': Missing required field '{field}'")

        # Validate marzano_level value
        if 'marzano_level' in activity:
            level = activity['marzano_level']
            if level not in MARZANO_LEVELS:
                errors.append(
                    f"Activity '{activity_name}': Invalid marzano_level '{level}'. "
                    f"Must be one of: {', '.join(MARZANO_LEVELS)}"
                )

        # Validate duration is positive integer
        if 'duration' in activity:
            duration = activity['duration']
            if not isinstance(duration, (int, float)) or duration <= 0:
                errors.append(f"Activity '{activity_name}': Duration must be a positive number")

        # Check for instructions (required but can be empty array)
        if 'instructions' in activity:
            if not isinstance(activity['instructions'], list):
                errors.append(f"Activity '{activity_name}': 'instructions' must be an array")
            elif len(activity['instructions']) < 1:
                errors.append(f"Activity '{activity_name}': 'instructions' should have at least 1 step")

    return errors


def calculate_cognitive_distribution(activities: List[Dict]) -> Dict[str, float]:
    """
    Calculate percentage breakdown of time spent at each Marzano level.

    Returns dict with percentage for each level based on duration.
    """
    level_durations = {level: 0 for level in MARZANO_LEVELS}
    total_duration = 0

    for activity in activities:
        if 'duration' in activity and 'marzano_level' in activity:
            level = activity['marzano_level']
            duration = activity['duration']

            if level in level_durations:
                level_durations[level] += duration
                total_duration += duration

    if total_duration == 0:
        return {level: 0.0 for level in MARZANO_LEVELS}

    # Calculate percentages
    distribution = {}
    for level, duration in level_durations.items():
        distribution[level] = (duration / total_duration) * 100

    return distribution


def validate_cognitive_rigor(distribution: Dict[str, float]) -> Tuple[List[str], List[str]]:
    """
    Validate cognitive rigor thresholds.

    Returns tuple of (errors, warnings).
    """
    errors = []
    warnings = []

    # Calculate higher-order thinking percentage
    higher_order = distribution.get('analysis', 0) + distribution.get('knowledge_utilization', 0)

    # CRITICAL: Enforce 40% minimum higher-order thinking
    if higher_order < MIN_HIGHER_ORDER:
        errors.append(
            f"Insufficient higher-order thinking: {higher_order:.1f}% "
            f"(minimum {MIN_HIGHER_ORDER:.0f}% required). "
            f"Add more analysis or knowledge utilization activities."
        )

    # Warning: Too much retrieval
    retrieval_pct = distribution.get('retrieval', 0)
    if retrieval_pct > MAX_RETRIEVAL:
        warnings.append(
            f"High retrieval focus: {retrieval_pct:.1f}% "
            f"(recommended <{MAX_RETRIEVAL:.0f}%). "
            f"Consider converting some retrieval activities to comprehension."
        )

    return errors, warnings


def check_progression(activities: List[Dict]) -> List[str]:
    """
    Check that cognitive levels don't drop more than 1 level between activities.

    Returns list of warnings for progression issues.
    """
    warnings = []

    prev_rank = 0
    prev_name = None

    for i, activity in enumerate(activities):
        if 'marzano_level' not in activity:
            continue

        level = activity['marzano_level']
        name = activity.get('name', f'Activity {i+1}')
        rank = LEVEL_RANKS.get(level, 0)

        if i > 0 and prev_rank > 0 and rank < prev_rank - 1:
            warnings.append(
                f"Activity '{name}' drops {prev_rank - rank} cognitive level(s) from '{prev_name}'. "
                f"Consider gradual progression for better scaffolding."
            )

        prev_rank = rank
        prev_name = name

    return warnings


def check_timing(lesson: Dict) -> Tuple[List[str], List[str]]:
    """
    Validate timing consistency.

    Returns tuple of (errors, warnings).
    """
    errors = []
    warnings = []

    if 'duration' not in lesson or 'activities' not in lesson:
        return errors, warnings

    lesson_duration = lesson['duration']
    activity_total = sum(
        a.get('duration', 0) for a in lesson['activities']
        if isinstance(a.get('duration'), (int, float))
    )

    # Error if activities exceed lesson duration
    if activity_total > lesson_duration:
        errors.append(
            f"Activity durations ({activity_total} min) exceed lesson duration ({lesson_duration} min). "
            f"Remove or shorten activities."
        )

    # Warning if significant time unaccounted for
    unaccounted = lesson_duration - activity_total
    if unaccounted > 10:
        warnings.append(
            f"Unaccounted time: {unaccounted} minutes. "
            f"Consider adding transition time to activities or adding another activity."
        )

    return errors, warnings


def validate_lesson(lesson_path: str) -> Tuple[List[str], List[str], Dict[str, float]]:
    """
    Validate lesson design against Marzano framework requirements.

    Args:
        lesson_path: Path to lesson JSON file

    Returns:
        Tuple of (errors, warnings, cognitive_distribution)
    """
    errors = []
    warnings = []
    distribution = {}

    # Load lesson JSON
    try:
        with open(lesson_path, 'r', encoding='utf-8') as f:
            lesson = json.load(f)
    except FileNotFoundError:
        errors.append(f"File not found: {lesson_path}")
        return errors, warnings, distribution
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON: {e}")
        return errors, warnings, distribution

    # Validate required fields
    field_errors = validate_required_fields(lesson)
    errors.extend(field_errors)

    if 'activities' not in lesson or not isinstance(lesson['activities'], list):
        return errors, warnings, distribution

    # Validate activity fields
    activity_errors = validate_activity_fields(lesson['activities'])
    errors.extend(activity_errors)

    # Calculate cognitive distribution
    distribution = calculate_cognitive_distribution(lesson['activities'])

    # Validate cognitive rigor
    rigor_errors, rigor_warnings = validate_cognitive_rigor(distribution)
    errors.extend(rigor_errors)
    warnings.extend(rigor_warnings)

    # Check progression
    progression_warnings = check_progression(lesson['activities'])
    warnings.extend(progression_warnings)

    # Check timing
    timing_errors, timing_warnings = check_timing(lesson)
    errors.extend(timing_errors)
    warnings.extend(timing_warnings)

    return errors, warnings, distribution


def generate_report(
    errors: List[str],
    warnings: List[str],
    distribution: Dict[str, float]
) -> str:
    """Generate human-readable validation report."""
    lines = []
    lines.append("VALIDATION REPORT")
    lines.append("=================")
    lines.append("")

    # Cognitive distribution
    if distribution:
        lines.append("Cognitive Distribution:")
        for level in MARZANO_LEVELS:
            pct = distribution.get(level, 0)
            lines.append(f"  {level.replace('_', ' ').title()}: {pct:.1f}%")
        lines.append("")

        # Higher-order thinking summary
        higher_order = distribution.get('analysis', 0) + distribution.get('knowledge_utilization', 0)
        status = "PASS" if higher_order >= MIN_HIGHER_ORDER else "FAIL"
        lines.append(f"Higher-Order Thinking: {higher_order:.1f}% (minimum {MIN_HIGHER_ORDER:.0f}%) - {status}")
        lines.append("")

    # Errors
    lines.append("Errors:")
    if errors:
        for error in errors:
            lines.append(f"  - {error}")
    else:
        lines.append("  (none)")
    lines.append("")

    # Warnings
    lines.append("Warnings:")
    if warnings:
        for warning in warnings:
            lines.append(f"  - {warning}")
    else:
        lines.append("  (none)")
    lines.append("")

    # Result
    if errors:
        lines.append("RESULT: FAILED")
    elif warnings:
        lines.append("RESULT: PASSED WITH WARNINGS")
    else:
        lines.append("RESULT: PASSED")

    return "\n".join(lines)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_marzano.py <lesson.json>")
        print("")
        print("Validates lesson design against Marzano framework requirements.")
        print("")
        print("Exit codes:")
        print("  0 - Passed")
        print("  1 - Passed with warnings")
        print("  2 - Failed (blocks progression)")
        sys.exit(1)

    lesson_path = sys.argv[1]

    # Run validation
    errors, warnings, distribution = validate_lesson(lesson_path)

    # Generate and print report
    report = generate_report(errors, warnings, distribution)
    print(report)

    # Exit with appropriate code
    if errors:
        sys.exit(2)  # Failed - blocks progression
    elif warnings:
        sys.exit(1)  # Passed with warnings
    else:
        sys.exit(0)  # Passed


if __name__ == "__main__":
    main()
