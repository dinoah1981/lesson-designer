"""
Tests for sequence_manager.py

Tests multi-lesson sequence session management including:
- Sequence creation with multiple competencies
- Competency assignment to lesson ranges
- Lesson directory access
- Lesson completion tracking
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from sequence_manager import (
    create_sequence_session,
    get_sequence_metadata,
    save_sequence_metadata,
    get_lesson_directory,
    assign_competency_to_lessons,
    mark_lesson_complete
)
from parse_competency import get_sessions_dir


@pytest.fixture
def test_sequence():
    """
    Create a test sequence and clean it up after test.

    Yields:
        str: The sequence_id of the test sequence
    """
    # Create test sequence
    sequence_id = create_sequence_session(
        competencies=[
            "Analyze primary sources to evaluate historical claims",
            "Compare multiple perspectives on historical events",
            "Synthesize evidence to construct historical arguments"
        ],
        grade_level="8th grade",
        total_lessons=4,
        lesson_duration=55
    )

    yield sequence_id

    # Cleanup after test
    sequence_dir = get_sessions_dir() / sequence_id
    if sequence_dir.exists():
        shutil.rmtree(sequence_dir)


def test_create_sequence_session(test_sequence):
    """
    Test that create_sequence_session creates proper directory structure and metadata.
    """
    sequence_id = test_sequence

    # Verify sequence_id format (UUID)
    assert len(sequence_id) == 36  # UUID format: 8-4-4-4-12
    assert sequence_id.count('-') == 4

    # Verify session directory exists
    sequence_dir = get_sessions_dir() / sequence_id
    assert sequence_dir.exists(), f"Sequence directory not found: {sequence_dir}"

    # Verify lesson subdirectories exist
    for lesson_num in range(1, 5):
        lesson_dir = sequence_dir / f"lesson_{lesson_num:02d}"
        assert lesson_dir.exists(), f"Lesson directory not found: {lesson_dir}"

    # Verify metadata file exists
    metadata_file = sequence_dir / 'sequence_metadata.json'
    assert metadata_file.exists(), f"Metadata file not found: {metadata_file}"

    # Load and verify metadata content
    metadata = get_sequence_metadata(sequence_id)

    assert metadata['sequence_id'] == sequence_id
    assert metadata['grade_level'] == "8th grade"
    assert metadata['total_lessons'] == 4
    assert metadata['lesson_duration'] == 55
    assert len(metadata['competencies']) == 3
    assert metadata['lessons_complete'] == 0
    assert 'created_at' in metadata
    assert 'vocabulary_progression' in metadata

    # Verify competency structure
    comp1 = metadata['competencies'][0]
    assert comp1['id'] == "comp-01"
    assert comp1['statement'] == "Analyze primary sources to evaluate historical claims"
    assert comp1['lesson_range'] is None
    assert comp1['prerequisites'] == []


def test_assign_competency_to_lessons(test_sequence):
    """
    Test that competencies can be assigned to lesson ranges.
    """
    sequence_id = test_sequence

    # Assign first competency to lessons 1-2
    assign_competency_to_lessons(sequence_id, "comp-01", 1, 2)

    # Verify assignment
    metadata = get_sequence_metadata(sequence_id)
    comp1 = metadata['competencies'][0]
    assert comp1['lesson_range'] == [1, 2]

    # Assign second competency to lessons 3-4
    assign_competency_to_lessons(sequence_id, "comp-02", 3, 4)

    # Verify assignment
    metadata = get_sequence_metadata(sequence_id)
    comp2 = metadata['competencies'][1]
    assert comp2['lesson_range'] == [3, 4]

    # Test invalid lesson numbers
    with pytest.raises(ValueError, match="out of valid range"):
        assign_competency_to_lessons(sequence_id, "comp-01", 0, 2)

    with pytest.raises(ValueError, match="out of valid range"):
        assign_competency_to_lessons(sequence_id, "comp-01", 1, 5)

    with pytest.raises(ValueError, match="cannot be greater than"):
        assign_competency_to_lessons(sequence_id, "comp-01", 3, 1)

    # Test invalid competency ID
    with pytest.raises(ValueError, match="not found"):
        assign_competency_to_lessons(sequence_id, "comp-99", 1, 2)


def test_get_lesson_directory(test_sequence):
    """
    Test that lesson directories can be accessed correctly.
    """
    sequence_id = test_sequence

    # Test valid lesson numbers
    for lesson_num in range(1, 5):
        lesson_dir = get_lesson_directory(sequence_id, lesson_num)

        # Verify path format
        assert lesson_dir.name == f"lesson_{lesson_num:02d}"
        assert lesson_dir.parent == get_sessions_dir() / sequence_id

        # Verify directory exists
        assert lesson_dir.exists()

    # Test invalid lesson numbers
    with pytest.raises(ValueError, match="out of range"):
        get_lesson_directory(sequence_id, 0)

    with pytest.raises(ValueError, match="out of range"):
        get_lesson_directory(sequence_id, 5)

    with pytest.raises(ValueError, match="out of range"):
        get_lesson_directory(sequence_id, -1)


def test_mark_lesson_complete(test_sequence):
    """
    Test that lessons can be marked complete with proper validation.
    """
    sequence_id = test_sequence

    # Initial state
    metadata = get_sequence_metadata(sequence_id)
    assert metadata['lessons_complete'] == 0

    # Mark lesson 1 complete
    mark_lesson_complete(sequence_id, 1)
    metadata = get_sequence_metadata(sequence_id)
    assert metadata['lessons_complete'] == 1

    # Mark lesson 2 complete
    mark_lesson_complete(sequence_id, 2)
    metadata = get_sequence_metadata(sequence_id)
    assert metadata['lessons_complete'] == 2

    # Test double-marking same lesson
    with pytest.raises(ValueError, match="already been marked complete"):
        mark_lesson_complete(sequence_id, 1)

    with pytest.raises(ValueError, match="already been marked complete"):
        mark_lesson_complete(sequence_id, 2)

    # Test invalid lesson numbers
    with pytest.raises(ValueError, match="out of range"):
        mark_lesson_complete(sequence_id, 0)

    with pytest.raises(ValueError, match="out of range"):
        mark_lesson_complete(sequence_id, 5)


def test_save_and_load_metadata(test_sequence):
    """
    Test that metadata can be saved and loaded correctly.
    """
    sequence_id = test_sequence

    # Load original metadata
    metadata = get_sequence_metadata(sequence_id)
    original_lessons_complete = metadata['lessons_complete']

    # Modify metadata
    metadata['lessons_complete'] = 3
    metadata['vocabulary_progression'] = {
        "tier_2": ["analyze", "evaluate", "synthesize"],
        "tier_3": ["primary source", "perspective", "evidence"]
    }

    # Save modified metadata
    saved_path = save_sequence_metadata(sequence_id, metadata)
    assert saved_path.exists()

    # Reload and verify changes
    reloaded_metadata = get_sequence_metadata(sequence_id)
    assert reloaded_metadata['lessons_complete'] == 3
    assert 'tier_2' in reloaded_metadata['vocabulary_progression']
    assert len(reloaded_metadata['vocabulary_progression']['tier_2']) == 3


def test_metadata_persistence(test_sequence):
    """
    Test that metadata changes persist across function calls.
    """
    sequence_id = test_sequence

    # Make multiple changes
    assign_competency_to_lessons(sequence_id, "comp-01", 1, 2)
    mark_lesson_complete(sequence_id, 1)

    # Reload metadata and verify all changes persisted
    metadata = get_sequence_metadata(sequence_id)
    assert metadata['competencies'][0]['lesson_range'] == [1, 2]
    assert metadata['lessons_complete'] == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
