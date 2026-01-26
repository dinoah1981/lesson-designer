#!/usr/bin/env python3
"""
Multi-persona lesson evaluator orchestrator.

Purpose: Run lesson evaluation through all 4 student personas for comprehensive accessibility feedback.

Usage:
    python run_multi_persona.py <lesson_json> <output_dir>

Example:
    python run_multi_persona.py \
        .lesson-designer/sessions/abc123/04_lesson_final.json \
        .lesson-designer/sessions/abc123/

Output:
    Creates 4 feedback JSON files in output_dir:
    - 03_feedback_struggling_learner.json
    - 03_feedback_unmotivated_capable.json
    - 03_feedback_interested_capable.json
    - 03_feedback_high_achieving.json

Returns:
    Exit code 0 if all personas evaluated successfully
    Exit code 1 if any persona failed to evaluate
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

from persona_evaluator import PersonaEvaluator


# Constants
PERSONA_DIR = Path(__file__).parent.parent / 'personas'
PERSONAS = [
    'struggling_learner.json',
    'unmotivated_capable.json',
    'interested_capable.json',
    'high_achieving.json'
]


def run_all_personas(lesson_path: str, output_dir: str, verbose: bool = False) -> List[str]:
    """
    Evaluate a lesson through all 4 student personas.

    Args:
        lesson_path: Path to lesson JSON file (04_lesson_final.json)
        output_dir: Directory to write feedback files
        verbose: If True, print detailed output

    Returns:
        List of feedback file paths that were created

    Raises:
        FileNotFoundError: If lesson file doesn't exist
        OSError: If output directory can't be created
    """
    # Validate lesson file exists
    lesson_file = Path(lesson_path)
    if not lesson_file.exists():
        raise FileNotFoundError(f"Lesson file not found: {lesson_path}")

    # Load lesson
    if verbose:
        print(f"Loading lesson from {lesson_path}...")
    with open(lesson_file, 'r') as f:
        lesson = json.load(f)

    # Create output directory
    output_path = Path(output_dir)
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create output directory {output_dir}: {e}")

    # Track results
    feedback_files = []
    results = []
    failed_personas = []

    # Evaluate with each persona
    for persona_file in PERSONAS:
        persona_path = PERSONA_DIR / persona_file
        persona_id = persona_file.replace('.json', '')

        # Check if persona file exists
        if not persona_path.exists():
            print(f"⚠ Warning: Persona file not found: {persona_path}")
            print(f"  Skipping {persona_id}...")
            failed_personas.append(persona_id)
            continue

        try:
            # Load persona
            if verbose:
                print(f"\nLoading persona: {persona_id}...")
            with open(persona_path, 'r') as f:
                persona_config = json.load(f)

            # Create evaluator
            evaluator = PersonaEvaluator(persona_config)

            # Evaluate lesson
            print(f"Evaluating with {persona_id}...")
            feedback = evaluator.evaluate_lesson(lesson)

            # Write feedback file
            feedback_filename = f"03_feedback_{persona_id}.json"
            feedback_path = output_path / feedback_filename
            with open(feedback_path, 'w') as f:
                json.dump(feedback, f, indent=2)

            feedback_files.append(str(feedback_path))

            # Count concerns
            concern_count = len(feedback.get('concerns', []))
            rating = feedback['overall_assessment']['accessibility_rating']

            print(f"  [OK] {concern_count} concerns identified (rating: {rating})")

            # Store results for summary
            results.append({
                'persona_id': persona_id,
                'persona_name': feedback['persona_name'],
                'rating': rating,
                'concern_count': concern_count,
                'high_severity': len([c for c in feedback['concerns'] if c.get('severity') == 'high']),
                'feedback_file': feedback_filename
            })

        except Exception as e:
            print(f"[ERROR] Error evaluating with {persona_id}: {e}")
            failed_personas.append(persona_id)
            continue

    # Print summary
    print("\n" + "="*70)
    print("MULTI-PERSONA EVALUATION SUMMARY")
    print("="*70)
    print(f"Lesson: {lesson.get('title', 'Untitled')}")
    print(f"Personas evaluated: {len(results)}/4")

    if failed_personas:
        print(f"Failed personas: {', '.join(failed_personas)}")

    if results:
        print("\nResults:")
        print(f"{'Persona':<25} {'Rating':<10} {'Concerns':<12} {'High Severity'}")
        print("-" * 70)
        for result in results:
            print(f"{result['persona_name']:<25} {result['rating']:<10} {result['concern_count']:<12} {result['high_severity']}")

        print(f"\nFeedback files created in: {output_dir}")
        for result in results:
            print(f"  - {result['feedback_file']}")

    print("="*70 + "\n")

    # Return exit code via list length
    if failed_personas:
        print(f"⚠ Warning: {len(failed_personas)} persona(s) failed to evaluate")

    return feedback_files


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Evaluate lesson through all 4 student personas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python run_multi_persona.py \\
        .lesson-designer/sessions/abc123/04_lesson_final.json \\
        .lesson-designer/sessions/abc123/

This will create 4 feedback files:
    - 03_feedback_struggling_learner.json
    - 03_feedback_unmotivated_capable.json
    - 03_feedback_interested_capable.json
    - 03_feedback_high_achieving.json
        """
    )

    parser.add_argument(
        'lesson',
        help='Path to lesson JSON file (04_lesson_final.json)'
    )
    parser.add_argument(
        'output_dir',
        help='Directory to write feedback files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed output during evaluation'
    )

    args = parser.parse_args()

    try:
        feedback_files = run_all_personas(args.lesson, args.output_dir, args.verbose)

        # Exit code 0 if all 4 personas evaluated, 1 if any failed
        if len(feedback_files) == 4:
            sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
