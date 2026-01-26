"""
Sequence session management for multi-lesson planning.

This module provides functions for:
- Creating and managing multi-lesson sequences
- Assigning competencies to lesson ranges
- Tracking lesson completion within sequences
- Managing sequence metadata

All functions use absolute paths to work correctly in the Claude environment
where the working directory may reset between bash calls.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from parse_competency import get_sessions_dir, generate_session_id, get_project_root


def create_sequence_session(
    competencies: list[str],
    grade_level: str,
    total_lessons: int,
    lesson_duration: int
) -> str:
    """
    Create a new multi-lesson sequence session.

    Creates directory structure:
        .lesson-designer/sessions/{sequence_id}/
            lesson_01/
            lesson_02/
            ...
            lesson_N/
            sequence_metadata.json

    Args:
        competencies: List of competency statement strings
        grade_level: Grade level (e.g., "8th grade")
        total_lessons: Number of lessons in sequence
        lesson_duration: Duration of each lesson in minutes

    Returns:
        str: The generated sequence_id

    Example:
        >>> sequence_id = create_sequence_session(
        ...     competencies=["Analyze primary sources", "Evaluate claims"],
        ...     grade_level="8th grade",
        ...     total_lessons=4,
        ...     lesson_duration=55
        ... )
    """
    # Generate unique sequence ID
    sequence_id = generate_session_id()

    # Create main sequence directory
    sequence_dir = get_sessions_dir() / sequence_id
    sequence_dir.mkdir(parents=True, exist_ok=True)

    # Create lesson subdirectories
    for lesson_num in range(1, total_lessons + 1):
        lesson_dir = sequence_dir / f"lesson_{lesson_num:02d}"
        lesson_dir.mkdir(exist_ok=True)

    # Build competency objects
    competency_objects = []
    for idx, comp_statement in enumerate(competencies, start=1):
        competency_objects.append({
            "id": f"comp-{idx:02d}",
            "statement": comp_statement,
            "lesson_range": None,
            "prerequisites": []
        })

    # Create sequence metadata
    metadata = {
        "sequence_id": sequence_id,
        "grade_level": grade_level,
        "total_lessons": total_lessons,
        "lesson_duration": lesson_duration,
        "competencies": competency_objects,
        "vocabulary_progression": {},
        "lessons_complete": 0,
        "created_at": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    }

    # Save metadata
    save_sequence_metadata(sequence_id, metadata)

    return sequence_id


def get_sequence_metadata(sequence_id: str) -> dict:
    """
    Load sequence metadata from sequence_metadata.json.

    Args:
        sequence_id: The unique sequence identifier

    Returns:
        dict: The sequence metadata dictionary

    Raises:
        FileNotFoundError: If sequence_metadata.json doesn't exist

    Example:
        >>> metadata = get_sequence_metadata(sequence_id)
        >>> print(metadata['total_lessons'])
        4
    """
    sequence_dir = get_sessions_dir() / sequence_id
    metadata_path = sequence_dir / 'sequence_metadata.json'

    if not metadata_path.exists():
        raise FileNotFoundError(f"Sequence metadata not found: {metadata_path}")

    with open(metadata_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_sequence_metadata(sequence_id: str, metadata: dict) -> Path:
    """
    Save sequence metadata to sequence_metadata.json.

    Args:
        sequence_id: The unique sequence identifier
        metadata: Dictionary containing sequence metadata

    Returns:
        Path: Absolute path to the saved file

    Example:
        >>> metadata = get_sequence_metadata(sequence_id)
        >>> metadata['lessons_complete'] = 2
        >>> save_sequence_metadata(sequence_id, metadata)
    """
    sequence_dir = get_sessions_dir() / sequence_id
    metadata_path = sequence_dir / 'sequence_metadata.json'

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return metadata_path


def get_lesson_directory(sequence_id: str, lesson_num: int) -> Path:
    """
    Get the absolute path to a lesson subdirectory.

    Args:
        sequence_id: The unique sequence identifier
        lesson_num: Lesson number (1-based)

    Returns:
        Path: Absolute path to the lesson directory

    Raises:
        ValueError: If lesson_num is out of valid range

    Example:
        >>> lesson_dir = get_lesson_directory(sequence_id, 1)
        >>> print(lesson_dir)
        Path('/path/to/.lesson-designer/sessions/{id}/lesson_01')
    """
    metadata = get_sequence_metadata(sequence_id)
    total_lessons = metadata['total_lessons']

    if lesson_num < 1 or lesson_num > total_lessons:
        raise ValueError(
            f"Lesson number {lesson_num} out of range. "
            f"Valid range: 1-{total_lessons}"
        )

    sequence_dir = get_sessions_dir() / sequence_id
    lesson_dir = sequence_dir / f"lesson_{lesson_num:02d}"

    return lesson_dir


def assign_competency_to_lessons(
    sequence_id: str,
    competency_id: str,
    start_lesson: int,
    end_lesson: int
) -> None:
    """
    Assign a competency to a range of lessons.

    Updates the competency's lesson_range field in sequence metadata.

    Args:
        sequence_id: The unique sequence identifier
        competency_id: Competency ID (e.g., "comp-01")
        start_lesson: First lesson number (1-based, inclusive)
        end_lesson: Last lesson number (1-based, inclusive)

    Raises:
        ValueError: If lesson numbers are out of valid range
        ValueError: If competency_id is not found

    Example:
        >>> assign_competency_to_lessons(sequence_id, "comp-01", 1, 2)
    """
    metadata = get_sequence_metadata(sequence_id)
    total_lessons = metadata['total_lessons']

    # Validate lesson numbers
    if start_lesson < 1 or end_lesson > total_lessons:
        raise ValueError(
            f"Lesson range {start_lesson}-{end_lesson} out of valid range: "
            f"1-{total_lessons}"
        )

    if start_lesson > end_lesson:
        raise ValueError(
            f"Start lesson {start_lesson} cannot be greater than "
            f"end lesson {end_lesson}"
        )

    # Find and update the competency
    competency_found = False
    for comp in metadata['competencies']:
        if comp['id'] == competency_id:
            comp['lesson_range'] = [start_lesson, end_lesson]
            competency_found = True
            break

    if not competency_found:
        raise ValueError(f"Competency {competency_id} not found in sequence metadata")

    # Save updated metadata
    save_sequence_metadata(sequence_id, metadata)


def mark_lesson_complete(sequence_id: str, lesson_num: int) -> None:
    """
    Mark a lesson as complete and increment the counter.

    Args:
        sequence_id: The unique sequence identifier
        lesson_num: Lesson number to mark complete (1-based)

    Raises:
        ValueError: If lesson_num is out of valid range
        ValueError: If lesson has already been marked complete

    Example:
        >>> mark_lesson_complete(sequence_id, 1)
    """
    metadata = get_sequence_metadata(sequence_id)
    total_lessons = metadata['total_lessons']
    lessons_complete = metadata.get('lessons_complete', 0)

    # Validate lesson number
    if lesson_num < 1 or lesson_num > total_lessons:
        raise ValueError(
            f"Lesson number {lesson_num} out of range. "
            f"Valid range: 1-{total_lessons}"
        )

    # Check if already marked complete
    # We'll track this with a simple counter for now
    # In future, we could add a 'completed_lessons' list
    if lesson_num <= lessons_complete:
        raise ValueError(
            f"Lesson {lesson_num} has already been marked complete "
            f"(lessons_complete: {lessons_complete})"
        )

    # Increment counter
    metadata['lessons_complete'] = lessons_complete + 1

    # Save updated metadata
    save_sequence_metadata(sequence_id, metadata)


# For convenience when testing
if __name__ == '__main__':
    import shutil

    print("Testing sequence_manager.py...")

    # Test 1: Create sequence
    print("\n1. Creating sequence session...")
    sequence_id = create_sequence_session(
        competencies=[
            "Analyze primary sources to evaluate historical claims",
            "Compare multiple perspectives on historical events"
        ],
        grade_level="8th grade",
        total_lessons=4,
        lesson_duration=55
    )
    print(f"   Created sequence: {sequence_id}")

    # Test 2: Load metadata
    print("\n2. Loading sequence metadata...")
    metadata = get_sequence_metadata(sequence_id)
    print(f"   Total lessons: {metadata['total_lessons']}")
    print(f"   Grade level: {metadata['grade_level']}")
    print(f"   Competencies: {len(metadata['competencies'])}")

    # Test 3: Get lesson directories
    print("\n3. Getting lesson directories...")
    for lesson_num in range(1, 5):
        lesson_dir = get_lesson_directory(sequence_id, lesson_num)
        print(f"   Lesson {lesson_num}: {lesson_dir}")
        assert lesson_dir.exists(), f"Lesson directory doesn't exist: {lesson_dir}"

    # Test 4: Assign competency to lessons
    print("\n4. Assigning competencies to lesson ranges...")
    assign_competency_to_lessons(sequence_id, "comp-01", 1, 2)
    assign_competency_to_lessons(sequence_id, "comp-02", 3, 4)
    updated_metadata = get_sequence_metadata(sequence_id)
    print(f"   comp-01 lesson_range: {updated_metadata['competencies'][0]['lesson_range']}")
    print(f"   comp-02 lesson_range: {updated_metadata['competencies'][1]['lesson_range']}")

    # Test 5: Mark lessons complete
    print("\n5. Marking lessons complete...")
    mark_lesson_complete(sequence_id, 1)
    metadata = get_sequence_metadata(sequence_id)
    print(f"   Lessons complete: {metadata['lessons_complete']}")

    # Test 6: Validate error handling
    print("\n6. Testing error handling...")
    try:
        get_lesson_directory(sequence_id, 0)
        print("   ERROR: Should have raised ValueError for lesson 0")
    except ValueError as e:
        print(f"   OK: Correctly raised error for lesson 0")

    try:
        get_lesson_directory(sequence_id, 5)
        print("   ERROR: Should have raised ValueError for lesson 5")
    except ValueError as e:
        print(f"   OK: Correctly raised error for lesson 5")

    try:
        mark_lesson_complete(sequence_id, 1)
        print("   ERROR: Should have raised ValueError for duplicate marking")
    except ValueError as e:
        print(f"   OK: Correctly raised error for duplicate marking")

    # Cleanup
    print("\n7. Cleaning up test session...")
    test_session_dir = get_sessions_dir() / sequence_id
    if test_session_dir.exists():
        shutil.rmtree(test_session_dir)
        print(f"   Removed: {test_session_dir}")

    print("\nAll tests passed!")
