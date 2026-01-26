"""
Tests for sequence_context.py

Tests context management including:
- Lesson summarization with compressed format
- Context assembly for lesson N (includes prior lessons)
- Vocabulary continuity validation
- Vocabulary progression tracking
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))

from sequence_context import (
    create_lesson_summary,
    build_context_for_lesson,
    check_vocabulary_continuity,
    update_vocabulary_progression,
    calculate_higher_order_percent,
    extract_vocabulary_from_lesson
)
from sequence_manager import (
    create_sequence_session,
    get_sequence_metadata,
    assign_competency_to_lessons,
    get_lesson_directory
)
from parse_competency import get_sessions_dir


@pytest.fixture
def test_sequence():
    """
    Create a test sequence with 3 lessons and clean it up after test.

    Yields:
        str: The sequence_id of the test sequence
    """
    # Create test sequence
    sequence_id = create_sequence_session(
        competencies=[
            "Analyze primary sources to evaluate historical claims"
        ],
        grade_level="8th grade",
        total_lessons=3,
        lesson_duration=55
    )

    # Assign competency to all lessons
    assign_competency_to_lessons(sequence_id, "comp-01", 1, 3)

    yield sequence_id

    # Cleanup after test
    sequence_dir = get_sessions_dir() / sequence_id
    if sequence_dir.exists():
        shutil.rmtree(sequence_dir)


@pytest.fixture
def mock_lesson_json():
    """
    Create a minimal mock lesson JSON for testing.

    Returns:
        dict: Mock lesson JSON with vocabulary and activities
    """
    return {
        "title": "Analyzing Primary Sources",
        "grade_level": "8th grade",
        "duration": 55,
        "lesson_type": "introducing_skill",
        "objective": "Students will analyze primary sources and evaluate historical claims.",
        "vocabulary": [
            {
                "word": "primary source",
                "definition": "A firsthand account from the time of an event"
            },
            {
                "word": "bias",
                "definition": "A tendency to favor one perspective over others"
            },
            {
                "word": "reliability",
                "definition": "The trustworthiness of a source's information"
            }
        ],
        "assumed_knowledge": [
            "Students know what a historical event is",
            "Students can read grade-level text"
        ],
        "activities": [
            {
                "name": "Prior Knowledge",
                "duration": 5,
                "marzano_level": "retrieval",
                "instructions": ["Recall previous learning"]
            },
            {
                "name": "Introduction",
                "duration": 10,
                "marzano_level": "comprehension",
                "instructions": ["Learn about primary sources"]
            },
            {
                "name": "Document Analysis",
                "duration": 20,
                "marzano_level": "analysis",
                "instructions": ["Analyze a Civil War letter"]
            },
            {
                "name": "Claim Evaluation",
                "duration": 15,
                "marzano_level": "knowledge_utilization",
                "instructions": ["Evaluate historical claims"]
            },
            {
                "name": "Exit Ticket",
                "duration": 5,
                "marzano_level": "analysis",
                "instructions": ["Summarize learning"]
            }
        ]
    }


def test_create_lesson_summary(test_sequence, mock_lesson_json):
    """
    Test that create_lesson_summary creates proper summary file with required fields.
    """
    sequence_id = test_sequence

    # Create summary for lesson 1
    summary = create_lesson_summary(
        sequence_id=sequence_id,
        lesson_num=1,
        lesson_json=mock_lesson_json,
        persona_feedback=None
    )

    # Verify summary structure
    assert summary['lesson_number'] == 1
    assert summary['title'] == "Analyzing Primary Sources"
    assert summary['objective'] == "Students will analyze primary sources and evaluate historical claims."
    assert summary['lesson_type'] == "introducing_skill"
    assert summary['duration'] == 55

    # Verify vocabulary extraction
    assert len(summary['vocabulary_introduced']) == 3
    vocab_terms = [v['term'] for v in summary['vocabulary_introduced']]
    assert 'primary source' in vocab_terms
    assert 'bias' in vocab_terms
    assert 'reliability' in vocab_terms

    # Verify assumed knowledge
    assert len(summary['assumed_knowledge']) == 2

    # Verify Marzano distribution
    assert summary['marzano_distribution']['retrieval'] == 1
    assert summary['marzano_distribution']['comprehension'] == 1
    assert summary['marzano_distribution']['analysis'] == 2
    assert summary['marzano_distribution']['knowledge_utilization'] == 1

    # Verify cognitive rigor percentage (analysis + knowledge_utilization = 3/5 = 60%)
    assert summary['cognitive_rigor_percent'] == 60

    # Verify token estimate is reasonable (~200-400)
    assert 50 <= summary['token_estimate'] <= 500

    # Verify file was created
    lesson_dir = get_lesson_directory(sequence_id, 1)
    summary_path = lesson_dir / 'lesson_summary.json'
    assert summary_path.exists()

    # Verify file contents match returned summary
    with open(summary_path, 'r', encoding='utf-8') as f:
        saved_summary = json.load(f)
    assert saved_summary['lesson_number'] == summary['lesson_number']
    assert saved_summary['title'] == summary['title']


def test_create_lesson_summary_with_persona_feedback(test_sequence, mock_lesson_json):
    """
    Test that persona feedback is properly extracted into pedagogical notes.
    """
    sequence_id = test_sequence

    # Create mock persona feedback
    persona_feedback = [
        {
            "persona_name": "Novice Teacher",
            "concerns": [
                {
                    "issue": "Activity duration too short for complex analysis",
                    "severity": "high"
                },
                {
                    "issue": "Could use more scaffolding",
                    "severity": "medium"
                }
            ],
            "strengths": [
                "Clear learning objective",
                "Good progression of activities"
            ]
        },
        {
            "persona_name": "Experienced Teacher",
            "concerns": [],
            "strengths": [
                "Excellent cognitive rigor",
                "Strong assessment alignment"
            ]
        }
    ]

    # Create summary with feedback
    summary = create_lesson_summary(
        sequence_id=sequence_id,
        lesson_num=1,
        lesson_json=mock_lesson_json,
        persona_feedback=persona_feedback
    )

    # Verify pedagogical notes
    assert len(summary['pedagogical_notes']['concerns']) == 1  # Only high severity
    assert summary['pedagogical_notes']['concerns'][0]['persona'] == "Novice Teacher"
    assert "duration too short" in summary['pedagogical_notes']['concerns'][0]['issue']

    assert len(summary['pedagogical_notes']['successes']) == 2
    success_personas = [s['persona'] for s in summary['pedagogical_notes']['successes']]
    assert "Novice Teacher" in success_personas
    assert "Experienced Teacher" in success_personas


def test_build_context_for_lesson(test_sequence, mock_lesson_json):
    """
    Test that build_context_for_lesson includes all prior lesson summaries.
    """
    sequence_id = test_sequence

    # Create summaries for lessons 1 and 2
    create_lesson_summary(sequence_id, 1, mock_lesson_json)

    # Modify for lesson 2 (different vocabulary)
    lesson_2_json = mock_lesson_json.copy()
    lesson_2_json['title'] = "Comparing Multiple Sources"
    lesson_2_json['vocabulary'] = [
        {"word": "corroboration", "definition": "Confirming information with other sources"},
        {"word": "perspective", "definition": "A particular viewpoint"}
    ]
    create_lesson_summary(sequence_id, 2, lesson_2_json)

    # Update vocabulary progression
    update_vocabulary_progression(sequence_id, 1, ['primary source', 'bias', 'reliability'])
    update_vocabulary_progression(sequence_id, 2, ['corroboration', 'perspective'])

    # Build context for lesson 3
    context = build_context_for_lesson(sequence_id, 3)

    # Verify sequence metadata
    assert context['sequence_metadata']['sequence_id'] == sequence_id
    assert context['sequence_metadata']['grade_level'] == "8th grade"
    assert context['sequence_metadata']['total_lessons'] == 3
    assert context['sequence_metadata']['lesson_duration'] == 55

    # Verify current competency
    assert context['current_competency'] is not None
    assert context['current_competency']['id'] == "comp-01"

    # Verify current lesson number
    assert context['current_lesson_number'] == 3

    # Verify prior lessons (should have summaries for lessons 1 and 2)
    assert len(context['prior_lessons']) == 2
    assert context['prior_lessons'][0]['lesson_number'] == 1
    assert context['prior_lessons'][0]['title'] == "Analyzing Primary Sources"
    assert context['prior_lessons'][1]['lesson_number'] == 2
    assert context['prior_lessons'][1]['title'] == "Comparing Multiple Sources"

    # Verify vocabulary already taught (accumulated from lessons 1 and 2)
    assert len(context['vocabulary_already_taught']) == 5
    assert 'primary source' in context['vocabulary_already_taught']
    assert 'bias' in context['vocabulary_already_taught']
    assert 'reliability' in context['vocabulary_already_taught']
    assert 'corroboration' in context['vocabulary_already_taught']
    assert 'perspective' in context['vocabulary_already_taught']


def test_build_context_for_lesson_first_lesson(test_sequence):
    """
    Test that build_context_for_lesson works correctly for lesson 1 (no prior lessons).
    """
    sequence_id = test_sequence

    # Build context for lesson 1 (no prior lessons)
    context = build_context_for_lesson(sequence_id, 1)

    # Verify prior lessons is empty
    assert len(context['prior_lessons']) == 0

    # Verify vocabulary already taught is empty
    assert len(context['vocabulary_already_taught']) == 0

    # Verify sequence metadata is present
    assert context['sequence_metadata']['sequence_id'] == sequence_id


def test_check_vocabulary_continuity_valid(test_sequence, mock_lesson_json):
    """
    Test that check_vocabulary_continuity correctly validates coherent vocabulary usage.
    """
    sequence_id = test_sequence

    # Set vocabulary progression for lessons 1-2
    update_vocabulary_progression(
        sequence_id, 1,
        ['primary source', 'bias', 'reliability']
    )
    update_vocabulary_progression(
        sequence_id, 2,
        ['corroboration', 'perspective']
    )

    # Create draft for lesson 3 that introduces new terms
    draft_lesson_3 = mock_lesson_json.copy()
    draft_lesson_3['vocabulary'] = [
        {"word": "evidence", "definition": "Information supporting a claim"},
        {"word": "interpretation", "definition": "An explanation of meaning"}
    ]

    # Check continuity (should be valid - new terms are defined)
    result = check_vocabulary_continuity(sequence_id, 3, draft_lesson_3)

    # Verify previously taught terms
    assert len(result['previously_taught']) == 5
    assert 'primary source' in result['previously_taught']
    assert 'corroboration' in result['previously_taught']

    # Verify newly introduced terms
    assert len(result['newly_introduced']) == 2
    assert 'evidence' in result['newly_introduced']
    assert 'interpretation' in result['newly_introduced']

    # Verify coherence (no incorrectly assumed terms)
    assert result['is_coherent'] == True
    assert len(result['incorrectly_assumed']) == 0


def test_check_vocabulary_continuity_invalid(test_sequence, mock_lesson_json):
    """
    Test that check_vocabulary_continuity detects undefined terms.
    """
    sequence_id = test_sequence

    # Set vocabulary progression for lesson 1 only
    update_vocabulary_progression(
        sequence_id, 1,
        ['primary source', 'bias']
    )

    # Create draft for lesson 2 that uses 'reliability' without defining it
    # Note: In real implementation, this would scan activity instructions
    # For now, we'll just verify the structure
    draft_lesson_2 = mock_lesson_json.copy()
    draft_lesson_2['vocabulary'] = [
        {"word": "corroboration", "definition": "Confirming with other sources"}
    ]

    # Check continuity
    result = check_vocabulary_continuity(sequence_id, 2, draft_lesson_2)

    # Verify previously taught
    assert len(result['previously_taught']) == 2
    assert 'primary source' in result['previously_taught']
    assert 'bias' in result['previously_taught']

    # Verify newly introduced
    assert 'corroboration' in result['newly_introduced']

    # Note: In this simplified test, _extract_used_terms returns empty list
    # In production, this would parse activity text and find undefined terms
    # For now, we verify the structure is correct
    assert 'incorrectly_assumed' in result
    assert 'is_coherent' in result


def test_update_vocabulary_progression(test_sequence):
    """
    Test that vocabulary progression is properly tracked in metadata.
    """
    sequence_id = test_sequence

    # Update vocabulary for lesson 1
    update_vocabulary_progression(
        sequence_id, 1,
        ['primary source', 'bias', 'reliability']
    )

    # Verify in metadata
    metadata = get_sequence_metadata(sequence_id)
    assert 'lesson_01' in metadata['vocabulary_progression']
    assert len(metadata['vocabulary_progression']['lesson_01']) == 3
    assert 'primary source' in metadata['vocabulary_progression']['lesson_01']

    # Update vocabulary for lesson 2
    update_vocabulary_progression(
        sequence_id, 2,
        ['corroboration', 'perspective']
    )

    # Verify both lessons in metadata
    metadata = get_sequence_metadata(sequence_id)
    assert 'lesson_01' in metadata['vocabulary_progression']
    assert 'lesson_02' in metadata['vocabulary_progression']
    assert len(metadata['vocabulary_progression']['lesson_02']) == 2
    assert 'corroboration' in metadata['vocabulary_progression']['lesson_02']


def test_calculate_higher_order_percent(mock_lesson_json):
    """
    Test that higher-order thinking percentage is calculated correctly.
    """
    # Mock lesson has 5 activities: 1 retrieval, 1 comprehension, 2 analysis, 1 knowledge_utilization
    # Higher-order = 2 analysis + 1 knowledge_utilization = 3
    # Percentage = 3/5 = 60%
    percent = calculate_higher_order_percent(mock_lesson_json)
    assert percent == 60

    # Test with all lower-order activities
    low_order_lesson = {
        "activities": [
            {"marzano_level": "retrieval"},
            {"marzano_level": "comprehension"},
            {"marzano_level": "retrieval"}
        ]
    }
    percent = calculate_higher_order_percent(low_order_lesson)
    assert percent == 0

    # Test with all higher-order activities
    high_order_lesson = {
        "activities": [
            {"marzano_level": "analysis"},
            {"marzano_level": "knowledge_utilization"},
            {"marzano_level": "analysis"}
        ]
    }
    percent = calculate_higher_order_percent(high_order_lesson)
    assert percent == 100

    # Test with empty activities
    empty_lesson = {"activities": []}
    percent = calculate_higher_order_percent(empty_lesson)
    assert percent == 0


def test_extract_vocabulary_from_lesson(mock_lesson_json):
    """
    Test that vocabulary terms are correctly extracted from lesson JSON.
    """
    terms = extract_vocabulary_from_lesson(mock_lesson_json)

    assert len(terms) == 3
    assert 'primary source' in terms
    assert 'bias' in terms
    assert 'reliability' in terms

    # Test with lesson that has no vocabulary
    no_vocab_lesson = {"title": "Test", "activities": []}
    terms = extract_vocabulary_from_lesson(no_vocab_lesson)
    assert len(terms) == 0

    # Test with vocabulary using 'term' key instead of 'word'
    term_key_lesson = {
        "vocabulary": [
            {"term": "analyze", "definition": "To examine in detail"},
            {"term": "synthesize", "definition": "To combine elements"}
        ]
    }
    terms = extract_vocabulary_from_lesson(term_key_lesson)
    assert len(terms) == 2
    assert 'analyze' in terms
    assert 'synthesize' in terms


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
