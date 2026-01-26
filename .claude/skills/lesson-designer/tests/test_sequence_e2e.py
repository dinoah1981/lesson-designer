#!/usr/bin/env python3
"""
End-to-End Integration Test for Multi-Lesson Sequences

Tests the complete workflow from sequence creation through assessment generation:
1. Create sequence session (Stage 0.5)
2. Generate lessons 1-3 with context awareness (Stages 1-7)
3. Generate sequence-level assessment (Stage 8)

This test proves all sequence components work together correctly.
"""

import json
import pytest
import shutil
import sys
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(script_dir))

from sequence_manager import (
    create_sequence_session,
    assign_competency_to_lessons,
    get_sequence_metadata,
    get_lesson_directory,
    mark_lesson_complete
)
from sequence_context import (
    create_lesson_summary,
    build_context_for_lesson,
    check_vocabulary_continuity,
    update_vocabulary_progression
)
from generate_sequence_assessment import (
    generate_sequence_assessment,
    SequenceAssessmentConfig
)


@pytest.fixture
def test_sequence():
    """
    Create a test sequence session and clean up after test.

    Yields sequence_id for use in tests.
    """
    # Create sequence with 1 competency, 3 lessons
    sequence_id = create_sequence_session(
        competencies=["Analyze primary sources to evaluate historical claims"],
        grade_level="8th grade",
        total_lessons=3,
        lesson_duration=55
    )

    # Assign competency to all lessons
    assign_competency_to_lessons(sequence_id, "comp-01", start_lesson=1, end_lesson=3)

    # Set vocabulary progression
    metadata = get_sequence_metadata(sequence_id)
    metadata['vocabulary_progression'] = {
        'lesson_01': ['primary source', 'bias', 'reliability'],
        'lesson_02': ['corroboration', 'perspective', 'context'],
        'lesson_03': ['historiography', 'interpretation', 'synthesis']
    }

    from sequence_manager import save_sequence_metadata
    save_sequence_metadata(sequence_id, metadata)

    yield sequence_id

    # Cleanup: Remove test sequence directory
    from parse_competency import get_sessions_dir
    sequence_dir = get_sessions_dir() / sequence_id
    if sequence_dir.exists():
        shutil.rmtree(sequence_dir)


def create_mock_lesson(lesson_num: int, vocabulary_terms: list) -> dict:
    """
    Create a mock lesson JSON for testing.

    Args:
        lesson_num: Lesson number (1-based)
        vocabulary_terms: List of vocabulary terms to include

    Returns:
        dict: Mock lesson JSON
    """
    return {
        "title": f"Lesson {lesson_num}: Analyzing Primary Sources",
        "grade_level": "8th grade",
        "duration": 55,
        "lesson_type": "introducing_skill" if lesson_num == 1 else "practicing_skill",
        "objective": f"Students will analyze primary sources to evaluate claims (Lesson {lesson_num})",
        "activities": [
            {
                "name": "Retrieval Activity",
                "duration": 10,
                "marzano_level": "retrieval",
                "instructions": ["Review key concepts"],
                "materials": ["Worksheet"],
                "student_output": "Completed warmup",
                "assessment_method": "Teacher observation"
            },
            {
                "name": "Analysis Activity",
                "duration": 25,
                "marzano_level": "analysis",
                "instructions": ["Compare primary sources", "Identify bias"],
                "materials": ["Primary source documents"],
                "student_output": "Source comparison chart",
                "assessment_method": "Chart completion"
            },
            {
                "name": "Application Activity",
                "duration": 15,
                "marzano_level": "knowledge_utilization",
                "instructions": ["Apply analysis to new source"],
                "materials": ["New document"],
                "student_output": "Written evaluation",
                "assessment_method": "Exit ticket"
            }
        ],
        "vocabulary": [
            {"word": term, "definition": f"Definition of {term}"}
            for term in vocabulary_terms
        ],
        "assessment": {
            "type": "exit_ticket",
            "description": "Quick assessment",
            "questions": ["Question 1", "Question 2"]
        }
    }


def create_mock_persona_feedback(lesson_num: int) -> list:
    """
    Create mock persona feedback for testing.

    Args:
        lesson_num: Lesson number

    Returns:
        list: List of persona feedback dictionaries
    """
    return [
        {
            "persona_name": "Alex (Struggling Learner)",
            "rating": 4,
            "concerns": [
                {
                    "issue": "Vocabulary may be challenging",
                    "severity": "high"
                }
            ],
            "strengths": ["Clear structure", "Good scaffolding"]
        }
    ]


@pytest.mark.integration
def test_full_sequence_workflow(test_sequence):
    """
    Test complete sequence workflow from creation through assessment.

    This integration test exercises:
    - Sequence session creation
    - Lesson generation with context awareness
    - Vocabulary progression tracking
    - Sequence assessment generation
    """
    sequence_id = test_sequence

    # =========================================================================
    # STEP 1: Verify sequence creation
    # =========================================================================
    metadata = get_sequence_metadata(sequence_id)

    assert metadata['total_lessons'] == 3
    assert metadata['grade_level'] == "8th grade"
    assert len(metadata['competencies']) == 1
    assert metadata['competencies'][0]['id'] == "comp-01"
    assert metadata['competencies'][0]['lesson_range'] == [1, 3]

    # Verify lesson directories exist
    for lesson_num in range(1, 4):
        lesson_dir = get_lesson_directory(sequence_id, lesson_num)
        assert lesson_dir.exists()

    # =========================================================================
    # STEP 2: Generate Lesson 1 (no prior context)
    # =========================================================================
    print("\nGenerating Lesson 1...")

    lesson_1_vocab = ['primary source', 'bias', 'reliability']
    lesson_1_json = create_mock_lesson(1, lesson_1_vocab)

    # Create lesson summary
    summary_1 = create_lesson_summary(
        sequence_id, 1, lesson_1_json,
        persona_feedback=create_mock_persona_feedback(1)
    )

    # Verify summary created
    lesson_1_dir = get_lesson_directory(sequence_id, 1)
    summary_path_1 = lesson_1_dir / 'lesson_summary.json'
    assert summary_path_1.exists()

    # Verify summary structure
    assert summary_1['lesson_number'] == 1
    assert summary_1['title'] == "Lesson 1: Analyzing Primary Sources"
    assert len(summary_1['vocabulary_introduced']) == 3
    assert summary_1['vocabulary_introduced'][0]['term'] == 'primary source'

    # Update vocabulary progression
    update_vocabulary_progression(sequence_id, 1, lesson_1_vocab)

    # =========================================================================
    # STEP 3: Generate Lesson 2 with context from Lesson 1
    # =========================================================================
    print("\nGenerating Lesson 2 with context...")

    # Build context
    context_2 = build_context_for_lesson(sequence_id, 2)

    # Verify context includes lesson 1
    assert context_2['current_lesson_number'] == 2
    assert len(context_2['prior_lessons']) == 1
    assert context_2['prior_lessons'][0]['lesson_number'] == 1

    # Verify vocabulary already taught
    assert len(context_2['vocabulary_already_taught']) == 3
    assert 'primary source' in context_2['vocabulary_already_taught']
    assert 'bias' in context_2['vocabulary_already_taught']
    assert 'reliability' in context_2['vocabulary_already_taught']

    # Generate lesson 2
    lesson_2_vocab = ['corroboration', 'perspective', 'context']
    lesson_2_json = create_mock_lesson(2, lesson_2_vocab)

    # Create lesson summary
    summary_2 = create_lesson_summary(
        sequence_id, 2, lesson_2_json,
        persona_feedback=create_mock_persona_feedback(2)
    )

    # Verify summary created
    lesson_2_dir = get_lesson_directory(sequence_id, 2)
    summary_path_2 = lesson_2_dir / 'lesson_summary.json'
    assert summary_path_2.exists()

    # Update vocabulary progression
    update_vocabulary_progression(sequence_id, 2, lesson_2_vocab)

    # =========================================================================
    # STEP 4: Generate Lesson 3 with context from Lessons 1-2
    # =========================================================================
    print("\nGenerating Lesson 3 with context...")

    # Build context
    context_3 = build_context_for_lesson(sequence_id, 3)

    # Verify context includes lessons 1 and 2
    assert context_3['current_lesson_number'] == 3
    assert len(context_3['prior_lessons']) == 2
    assert context_3['prior_lessons'][0]['lesson_number'] == 1
    assert context_3['prior_lessons'][1]['lesson_number'] == 2

    # Verify vocabulary accumulation
    assert len(context_3['vocabulary_already_taught']) == 6  # 3 from L1 + 3 from L2
    assert 'primary source' in context_3['vocabulary_already_taught']
    assert 'corroboration' in context_3['vocabulary_already_taught']

    # Generate lesson 3 using terms from lessons 1-2
    lesson_3_vocab = ['historiography', 'interpretation', 'synthesis']
    lesson_3_json = create_mock_lesson(3, lesson_3_vocab)

    # Check vocabulary continuity
    continuity = check_vocabulary_continuity(sequence_id, 3, lesson_3_json)

    # Verify continuity (should be coherent since we're not using undefined terms)
    assert continuity['is_coherent'] == True
    assert len(continuity['previously_taught']) == 6
    assert len(continuity['newly_introduced']) == 3
    assert len(continuity['incorrectly_assumed']) == 0

    # Create lesson summary
    summary_3 = create_lesson_summary(
        sequence_id, 3, lesson_3_json,
        persona_feedback=create_mock_persona_feedback(3)
    )

    # Verify summary created
    lesson_3_dir = get_lesson_directory(sequence_id, 3)
    summary_path_3 = lesson_3_dir / 'lesson_summary.json'
    assert summary_path_3.exists()

    # Update vocabulary progression
    update_vocabulary_progression(sequence_id, 3, lesson_3_vocab)

    # =========================================================================
    # STEP 5: Generate sequence assessment (cumulative test)
    # =========================================================================
    print("\nGenerating sequence assessment...")

    config = SequenceAssessmentConfig(
        assessment_type="cumulative_test",
        title="Unit Assessment: Primary Source Analysis",
        time_limit=50
    )

    assessment = generate_sequence_assessment(sequence_id, config)

    # Verify assessment structure
    assert assessment['title'] == "Unit Assessment: Primary Source Analysis"
    assert assessment['type'] == 'test'
    assert 'multiple_choice' in assessment
    assert 'short_answer' in assessment
    assert 'essay' in assessment

    # Verify assessment references vocabulary from all 3 lessons
    # (In real implementation, this would check question content)
    assert assessment['metadata']['sequence_id'] == sequence_id
    assert assessment['metadata']['lessons_covered'] == [1, 2, 3]

    # Verify Marzano level distribution
    mc_questions = assessment['multiple_choice']
    assert any(q['marzano_level'] == 'retrieval' for q in mc_questions)
    assert any(q['marzano_level'] == 'comprehension' for q in mc_questions)

    sa_questions = assessment['short_answer']
    assert any(q['marzano_level'] == 'analysis' for q in sa_questions)

    essay_questions = assessment['essay']
    assert any(q['marzano_level'] == 'knowledge_utilization' for q in essay_questions)

    print("\n✓ All sequence workflow steps verified successfully!")


@pytest.mark.integration
def test_vocabulary_progression_tracking(test_sequence):
    """
    Test that vocabulary progression is tracked correctly across lessons.
    """
    sequence_id = test_sequence

    # Update vocabulary for lessons 1-3
    update_vocabulary_progression(sequence_id, 1, ['term1', 'term2'])
    update_vocabulary_progression(sequence_id, 2, ['term3', 'term4'])
    update_vocabulary_progression(sequence_id, 3, ['term5', 'term6'])

    # Verify progression in metadata
    metadata = get_sequence_metadata(sequence_id)
    vocab_prog = metadata['vocabulary_progression']

    assert 'lesson_01' in vocab_prog
    assert 'lesson_02' in vocab_prog
    assert 'lesson_03' in vocab_prog

    assert vocab_prog['lesson_01'] == ['term1', 'term2']
    assert vocab_prog['lesson_02'] == ['term3', 'term4']
    assert vocab_prog['lesson_03'] == ['term5', 'term6']

    # Build context for lesson 3
    context = build_context_for_lesson(sequence_id, 3)

    # Verify vocabulary_already_taught includes terms from lessons 1-2
    assert 'term1' in context['vocabulary_already_taught']
    assert 'term2' in context['vocabulary_already_taught']
    assert 'term3' in context['vocabulary_already_taught']
    assert 'term4' in context['vocabulary_already_taught']
    assert 'term5' not in context['vocabulary_already_taught']  # Not taught yet


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '-s'])
