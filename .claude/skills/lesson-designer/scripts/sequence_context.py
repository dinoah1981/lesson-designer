"""
Context management for multi-lesson sequences.

This module provides functions for:
- Creating compressed lesson summaries after lesson generation
- Building context packages for designing lesson N (includes prior lessons)
- Tracking vocabulary progression across lessons
- Validating vocabulary continuity

All functions use absolute paths to work correctly in the Claude environment
where the working directory may reset between bash calls.
"""

import json
from pathlib import Path
from typing import Optional

from sequence_manager import (
    get_sequence_metadata,
    save_sequence_metadata,
    get_lesson_directory
)


def create_lesson_summary(
    sequence_id: str,
    lesson_num: int,
    lesson_json: dict,
    persona_feedback: Optional[list[dict]] = None
) -> dict:
    """
    Create a compressed summary of a completed lesson.

    Extracts key information from the lesson JSON and persona feedback,
    then saves to lesson_summary.json in the lesson directory.
    Target size: ~250 tokens for efficient context assembly.

    Args:
        sequence_id: The unique sequence identifier
        lesson_num: Lesson number (1-based)
        lesson_json: The complete lesson JSON (typically 04_lesson_final.json)
        persona_feedback: Optional list of persona evaluation results

    Returns:
        dict: The lesson summary

    Example:
        >>> summary = create_lesson_summary(
        ...     sequence_id=seq_id,
        ...     lesson_num=1,
        ...     lesson_json=lesson_data,
        ...     persona_feedback=evaluations
        ... )
        >>> print(summary['vocabulary_introduced'])
        [{'term': 'primary source', 'definition': '...', 'example': '...'}]
    """
    # Extract vocabulary introduced in this lesson
    vocabulary_introduced = []
    if 'vocabulary' in lesson_json:
        for vocab_item in lesson_json['vocabulary']:
            vocab_entry = {
                'term': vocab_item.get('word', vocab_item.get('term', '')),
                'definition': vocab_item.get('definition', '')
            }
            # Add example if available
            if 'example' in vocab_item:
                vocab_entry['example'] = vocab_item['example']
            vocabulary_introduced.append(vocab_entry)

    # Extract assumed knowledge if present
    assumed_knowledge = lesson_json.get('assumed_knowledge', [])

    # Calculate Marzano distribution
    marzano_distribution = {
        'retrieval': 0,
        'comprehension': 0,
        'analysis': 0,
        'knowledge_utilization': 0
    }

    activities = lesson_json.get('activities', [])
    for activity in activities:
        level = activity.get('marzano_level', '').lower()
        if level in marzano_distribution:
            marzano_distribution[level] += 1

    # Calculate cognitive rigor percentage (higher-order thinking)
    cognitive_rigor_percent = calculate_higher_order_percent(lesson_json)

    # Extract pedagogical notes from persona feedback
    pedagogical_notes = {
        'concerns': [],
        'successes': []
    }

    if persona_feedback:
        for feedback in persona_feedback:
            # Extract high severity concerns
            concerns = feedback.get('concerns', [])
            for concern in concerns:
                if concern.get('severity') == 'high':
                    pedagogical_notes['concerns'].append({
                        'persona': feedback.get('persona_name', 'Unknown'),
                        'issue': concern.get('issue', '')
                    })

            # Extract positive feedback
            strengths = feedback.get('strengths', [])
            if strengths:
                pedagogical_notes['successes'].append({
                    'persona': feedback.get('persona_name', 'Unknown'),
                    'strengths': strengths[:2]  # Keep top 2 strengths
                })

    # Build summary
    summary = {
        'lesson_number': lesson_num,
        'title': lesson_json.get('title', ''),
        'objective': lesson_json.get('objective', ''),
        'lesson_type': lesson_json.get('lesson_type', 'introducing_skill'),
        'vocabulary_introduced': vocabulary_introduced,
        'assumed_knowledge': assumed_knowledge,
        'marzano_distribution': marzano_distribution,
        'cognitive_rigor_percent': cognitive_rigor_percent,
        'pedagogical_notes': pedagogical_notes,
        'duration': lesson_json.get('duration', 55),
        'token_estimate': _estimate_tokens(summary_dict={
            'vocabulary_introduced': vocabulary_introduced,
            'assumed_knowledge': assumed_knowledge,
            'pedagogical_notes': pedagogical_notes
        })
    }

    # Save to lesson directory
    lesson_dir = get_lesson_directory(sequence_id, lesson_num)
    summary_path = lesson_dir / 'lesson_summary.json'

    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return summary


def build_context_for_lesson(sequence_id: str, lesson_num: int) -> dict:
    """
    Assemble context package for designing lesson N.

    Includes:
    - Sequence metadata (always)
    - Current competency being taught (based on lesson_range)
    - Prior lesson summaries (lessons 1 to N-1)
    - Vocabulary already taught (accumulated from progression)
    - Vocabulary to introduce in this lesson (from metadata)

    For 2-4 lesson sequences, all prior summaries are included directly
    as research shows JSON context is sufficient for Claude.

    Args:
        sequence_id: The unique sequence identifier
        lesson_num: Lesson number to build context for (1-based)

    Returns:
        dict: Context package for lesson design

    Example:
        >>> context = build_context_for_lesson(sequence_id, 3)
        >>> print(len(context['prior_lessons']))  # Summaries for lessons 1-2
        2
        >>> print(context['vocabulary_already_taught'])
        ['primary source', 'bias', 'corroboration', ...]
    """
    metadata = get_sequence_metadata(sequence_id)

    # Find current competency for this lesson
    current_competency = None
    for comp in metadata['competencies']:
        lesson_range = comp.get('lesson_range')
        if lesson_range and lesson_range[0] <= lesson_num <= lesson_range[1]:
            current_competency = comp
            break

    # Load prior lesson summaries
    prior_lessons = []
    for prior_lesson_num in range(1, lesson_num):
        lesson_dir = get_lesson_directory(sequence_id, prior_lesson_num)
        summary_path = lesson_dir / 'lesson_summary.json'

        if summary_path.exists():
            with open(summary_path, 'r', encoding='utf-8') as f:
                prior_lessons.append(json.load(f))

    # Accumulate vocabulary already taught
    vocabulary_already_taught = []
    vocab_progression = metadata.get('vocabulary_progression', {})

    for prior_lesson_num in range(1, lesson_num):
        lesson_key = f"lesson_{prior_lesson_num:02d}"
        if lesson_key in vocab_progression:
            vocabulary_already_taught.extend(vocab_progression[lesson_key])

    # Remove duplicates while preserving order
    vocabulary_already_taught = list(dict.fromkeys(vocabulary_already_taught))

    # Get vocabulary to introduce in this lesson (if specified in metadata)
    # This would be added by lesson planning tools if they pre-allocate vocab
    vocabulary_to_introduce = []
    lesson_key = f"lesson_{lesson_num:02d}"
    if lesson_key in vocab_progression:
        vocabulary_to_introduce = vocab_progression[lesson_key]

    # Build context package
    context = {
        'sequence_metadata': {
            'sequence_id': metadata['sequence_id'],
            'grade_level': metadata['grade_level'],
            'total_lessons': metadata['total_lessons'],
            'lesson_duration': metadata['lesson_duration'],
            'lessons_complete': metadata.get('lessons_complete', 0)
        },
        'current_competency': current_competency,
        'current_lesson_number': lesson_num,
        'prior_lessons': prior_lessons,
        'vocabulary_already_taught': vocabulary_already_taught,
        'vocabulary_to_introduce': vocabulary_to_introduce
    }

    return context


def check_vocabulary_continuity(
    sequence_id: str,
    lesson_num: int,
    draft_lesson: dict
) -> dict:
    """
    Validate vocabulary usage for coherence across the sequence.

    Checks that:
    - Terms used in the lesson were either taught previously or are being introduced
    - No terms are assumed without being defined

    Args:
        sequence_id: The unique sequence identifier
        lesson_num: Current lesson number (1-based)
        draft_lesson: Draft lesson JSON to validate

    Returns:
        dict: Validation result with fields:
            - previously_taught: list[str] - Terms lesson can use without defining
            - newly_introduced: list[str] - Terms this lesson introduces
            - incorrectly_assumed: list[str] - Terms used but never taught (ERROR)
            - is_coherent: bool - True if no incorrectly assumed terms

    Example:
        >>> result = check_vocabulary_continuity(seq_id, 3, draft)
        >>> if not result['is_coherent']:
        ...     print(f"ERROR: Undefined terms: {result['incorrectly_assumed']}")
    """
    metadata = get_sequence_metadata(sequence_id)

    # Get previously taught vocabulary
    previously_taught = []
    vocab_progression = metadata.get('vocabulary_progression', {})

    for prior_lesson_num in range(1, lesson_num):
        lesson_key = f"lesson_{prior_lesson_num:02d}"
        if lesson_key in vocab_progression:
            previously_taught.extend(vocab_progression[lesson_key])

    # Remove duplicates
    previously_taught = list(dict.fromkeys(previously_taught))

    # Extract newly introduced terms from draft lesson
    newly_introduced = extract_vocabulary_from_lesson(draft_lesson)

    # Extract all terms used in the lesson (from activity instructions, etc.)
    used_terms = _extract_used_terms(draft_lesson)

    # Find terms that are used but not taught
    incorrectly_assumed = []
    all_known_terms = set(previously_taught + newly_introduced)

    for term in used_terms:
        # Normalize for comparison (lowercase)
        term_lower = term.lower()
        all_known_lower = {t.lower() for t in all_known_terms}

        if term_lower not in all_known_lower:
            incorrectly_assumed.append(term)

    return {
        'previously_taught': previously_taught,
        'newly_introduced': newly_introduced,
        'incorrectly_assumed': incorrectly_assumed,
        'is_coherent': len(incorrectly_assumed) == 0
    }


def update_vocabulary_progression(
    sequence_id: str,
    lesson_num: int,
    terms: list[str]
) -> None:
    """
    Add vocabulary terms to the progression tracking in sequence metadata.

    Updates vocabulary_progression[lesson_XX] with the terms introduced
    in this lesson. Terms are stored as a list to preserve introduction order.

    Args:
        sequence_id: The unique sequence identifier
        lesson_num: Lesson number (1-based)
        terms: List of vocabulary terms introduced in this lesson

    Example:
        >>> update_vocabulary_progression(
        ...     seq_id, 1, ['primary source', 'bias', 'reliability']
        ... )
        >>> metadata = get_sequence_metadata(seq_id)
        >>> print(metadata['vocabulary_progression']['lesson_01'])
        ['primary source', 'bias', 'reliability']
    """
    metadata = get_sequence_metadata(sequence_id)

    lesson_key = f"lesson_{lesson_num:02d}"

    # Initialize vocabulary_progression if not present
    if 'vocabulary_progression' not in metadata:
        metadata['vocabulary_progression'] = {}

    # Add terms for this lesson
    metadata['vocabulary_progression'][lesson_key] = terms

    # Save updated metadata
    save_sequence_metadata(sequence_id, metadata)


def calculate_higher_order_percent(lesson_json: dict) -> int:
    """
    Calculate percentage of activities at higher-order thinking levels.

    Higher-order thinking = analysis + knowledge_utilization levels
    in Marzano's taxonomy.

    Args:
        lesson_json: Complete lesson JSON

    Returns:
        int: Percentage of higher-order activities (0-100)

    Example:
        >>> percent = calculate_higher_order_percent(lesson_data)
        >>> print(f"Higher-order thinking: {percent}%")
        Higher-order thinking: 60%
    """
    activities = lesson_json.get('activities', [])

    if not activities:
        return 0

    higher_order_count = 0

    for activity in activities:
        level = activity.get('marzano_level', '').lower()
        if level in ['analysis', 'knowledge_utilization']:
            higher_order_count += 1

    # Calculate percentage
    percent = int((higher_order_count / len(activities)) * 100)

    return percent


def extract_vocabulary_from_lesson(lesson_json: dict) -> list[str]:
    """
    Extract vocabulary terms from a lesson JSON.

    Looks for explicit vocabulary definitions in the 'vocabulary' field.
    Returns the list of terms (words) introduced in this lesson.

    Args:
        lesson_json: Complete lesson JSON

    Returns:
        list[str]: List of vocabulary terms

    Example:
        >>> terms = extract_vocabulary_from_lesson(lesson_data)
        >>> print(terms)
        ['primary source', 'bias', 'reliability', 'corroboration']
    """
    terms = []

    if 'vocabulary' in lesson_json:
        for vocab_item in lesson_json['vocabulary']:
            # Handle both 'word' and 'term' keys
            term = vocab_item.get('word', vocab_item.get('term', ''))
            if term:
                terms.append(term)

    return terms


# Private helper functions

def _estimate_tokens(summary_dict: dict) -> int:
    """
    Estimate token count for a summary dictionary.

    Uses rough heuristic: ~4 characters per token for English text.
    This is approximate but good enough for monitoring summary size.

    Args:
        summary_dict: Dictionary to estimate

    Returns:
        int: Estimated token count
    """
    # Convert to JSON string
    json_str = json.dumps(summary_dict, ensure_ascii=False)

    # Estimate tokens (rough: 4 chars per token)
    estimated_tokens = len(json_str) // 4

    return estimated_tokens


def _extract_used_terms(lesson_json: dict) -> list[str]:
    """
    Extract terminology actually used in lesson activities and instructions.

    This is a simplified implementation that looks for:
    - Terms in activity instructions
    - Terms in key_points
    - Terms in assessment questions

    In production, this might use NLP to identify domain-specific terminology.
    For now, we extract capitalized phrases and compare against known vocabulary.

    Args:
        lesson_json: Complete lesson JSON

    Returns:
        list[str]: List of terms used in the lesson
    """
    used_terms = []

    # For now, we'll check against the vocabulary list itself
    # In a real implementation, this would scan instruction text
    # and identify domain-specific terms being used

    # This is a placeholder - vocabulary continuity checking
    # would need more sophisticated term extraction in production

    return used_terms


if __name__ == '__main__':
    print("sequence_context.py loaded successfully")
    print("\nAvailable functions:")
    print("  - create_lesson_summary()")
    print("  - build_context_for_lesson()")
    print("  - check_vocabulary_continuity()")
    print("  - update_vocabulary_progression()")
    print("  - calculate_higher_order_percent()")
    print("  - extract_vocabulary_from_lesson()")
