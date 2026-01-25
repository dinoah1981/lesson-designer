#!/usr/bin/env python3
"""
Lesson Design Helper Functions

Provides utility functions for creating and managing lesson designs
following Marzano's New Taxonomy framework.

Functions:
    create_lesson_design() - Create initial lesson design structure
    get_recommended_distribution() - Get recommended Marzano level distribution
    calculate_activity_durations() - Suggest activity durations
    save_lesson_design() - Save lesson design to session directory
    load_lesson_design() - Load lesson design from session directory
    get_activity_templates() - Get activity templates for a Marzano level
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any


# Base path for lesson designer sessions
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '.lesson-designer', 'sessions'))


# Recommended cognitive distributions by lesson type
LESSON_TYPE_DISTRIBUTIONS = {
    'introducing': {
        'retrieval': 30.0,
        'comprehension': 40.0,
        'analysis': 20.0,
        'knowledge_utilization': 10.0
    },
    'practicing': {
        'retrieval': 20.0,
        'comprehension': 30.0,
        'analysis': 35.0,
        'knowledge_utilization': 15.0
    },
    'applying': {
        'retrieval': 10.0,
        'comprehension': 20.0,
        'analysis': 30.0,
        'knowledge_utilization': 40.0
    },
    'synthesizing': {
        'retrieval': 10.0,
        'comprehension': 20.0,
        'analysis': 35.0,
        'knowledge_utilization': 35.0
    },
    'novel_application': {
        'retrieval': 5.0,
        'comprehension': 15.0,
        'analysis': 30.0,
        'knowledge_utilization': 50.0
    }
}


# Activity templates by Marzano level
ACTIVITY_TEMPLATES = {
    'retrieval': [
        {
            'name_pattern': 'Vocabulary Quick-Match',
            'typical_duration': (5, 8),
            'description': 'Students match terms to definitions',
            'student_output': 'Completed matching exercise'
        },
        {
            'name_pattern': 'Fact Retrieval Sprint',
            'typical_duration': (5, 10),
            'description': 'Rapid-fire recall questions',
            'student_output': 'Written answers'
        },
        {
            'name_pattern': 'Procedure Demonstration',
            'typical_duration': (8, 12),
            'description': 'Students execute a learned procedure',
            'student_output': 'Completed procedure'
        }
    ],
    'comprehension': [
        {
            'name_pattern': 'Concept Mapping',
            'typical_duration': (10, 15),
            'description': 'Create visual diagram showing relationships',
            'student_output': 'Concept map'
        },
        {
            'name_pattern': 'Summarization Challenge',
            'typical_duration': (10, 12),
            'description': 'Write 3-5 sentence summary in own words',
            'student_output': 'Written summary'
        },
        {
            'name_pattern': 'Comparison Matrix',
            'typical_duration': (12, 15),
            'description': 'Create Venn diagram or T-chart',
            'student_output': 'Comparison diagram'
        }
    ],
    'analysis': [
        {
            'name_pattern': 'Error Analysis',
            'typical_duration': (15, 20),
            'description': 'Find and explain errors in examples',
            'student_output': 'Error identification with explanations'
        },
        {
            'name_pattern': 'Case Study Investigation',
            'typical_duration': (18, 25),
            'description': 'Analyze scenario and identify key factors',
            'student_output': 'Analysis with evidence-based conclusions'
        },
        {
            'name_pattern': 'Pattern Recognition Challenge',
            'typical_duration': (12, 18),
            'description': 'Identify patterns and formulate rules',
            'student_output': 'Pattern rule with examples'
        }
    ],
    'knowledge_utilization': [
        {
            'name_pattern': 'Design Challenge',
            'typical_duration': (25, 40),
            'description': 'Design a solution meeting constraints',
            'student_output': 'Design plan or prototype'
        },
        {
            'name_pattern': 'Investigation Project',
            'typical_duration': (30, 45),
            'description': 'Research and test a hypothesis',
            'student_output': 'Investigation report'
        },
        {
            'name_pattern': 'Real-World Problem Solving',
            'typical_duration': (20, 35),
            'description': 'Apply knowledge to authentic scenario',
            'student_output': 'Solution with justification'
        }
    ]
}


def get_session_path(session_id: str) -> str:
    """Get absolute path for session directory."""
    return os.path.join(BASE_PATH, session_id)


def create_lesson_design(
    input_data: Dict[str, Any],
    breakdown_data: Dict[str, Any],
    lesson_type: str
) -> Dict[str, Any]:
    """
    Create initial lesson design structure from input and breakdown.

    Args:
        input_data: Data from 01_input.json (competency, grade_level, etc.)
        breakdown_data: Data from 02_competency_breakdown.json (skills, knowledge)
        lesson_type: One of: introducing, practicing, applying, synthesizing, novel_application

    Returns:
        Dict with initial lesson design structure
    """
    # Get recommended distribution for this lesson type
    distribution = get_recommended_distribution(lesson_type)

    # Build initial structure
    design = {
        'title': f"Lesson: {input_data.get('competency', 'Untitled')[:50]}",
        'grade_level': input_data.get('grade_level', ''),
        'duration': input_data.get('lesson_duration', 50),
        'lesson_type': lesson_type,
        'objective': breakdown_data.get('skill', {}).get('full_statement', ''),
        'activities': [],
        'hidden_slide_content': {
            'objective': breakdown_data.get('skill', {}).get('full_statement', ''),
            'agenda': [],
            'misconceptions': [],
            'delivery_tips': []
        },
        'vocabulary': [],
        'assessment': {
            'type': 'exit_ticket',
            'description': '',
            'questions': []
        },
        'metadata': {
            'created_at': datetime.now().isoformat(),
            'version': 1,
            'recommended_distribution': distribution
        }
    }

    return design


def get_recommended_distribution(lesson_type: str) -> Dict[str, float]:
    """
    Return recommended Marzano level distribution for lesson type.

    Args:
        lesson_type: One of: introducing, practicing, applying, synthesizing, novel_application

    Returns:
        Dict with percentage for each Marzano level
    """
    if lesson_type not in LESSON_TYPE_DISTRIBUTIONS:
        # Default to balanced distribution if unknown type
        return {
            'retrieval': 15.0,
            'comprehension': 25.0,
            'analysis': 30.0,
            'knowledge_utilization': 30.0
        }

    return LESSON_TYPE_DISTRIBUTIONS[lesson_type].copy()


def calculate_activity_durations(
    total_duration: int,
    num_activities: int,
    distribution: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Suggest activity durations based on total time and distribution.

    Args:
        total_duration: Total lesson duration in minutes
        num_activities: Desired number of activities
        distribution: Target Marzano level distribution (percentages)

    Returns:
        List of suggested activity slots with level and duration
    """
    # Allocate time based on distribution
    level_minutes = {}
    for level, pct in distribution.items():
        level_minutes[level] = (pct / 100.0) * total_duration

    # Determine activities per level (simplified approach)
    # For typical 5-activity lesson: 1 retrieval, 1 comprehension, 2 analysis, 1 knowledge_utilization
    activity_slots = []

    # Order levels by typical lesson progression
    level_order = ['retrieval', 'comprehension', 'analysis', 'knowledge_utilization']

    # Calculate activities per level based on distribution weight
    total_weight = sum(distribution.values())
    remaining_activities = num_activities

    for i, level in enumerate(level_order):
        weight = distribution.get(level, 0)
        if i == len(level_order) - 1:
            # Last level gets remaining activities
            level_activities = remaining_activities
        else:
            # Proportional allocation
            level_activities = max(1, round((weight / total_weight) * num_activities))
            level_activities = min(level_activities, remaining_activities - (len(level_order) - i - 1))

        remaining_activities -= level_activities

        # Divide this level's time among its activities
        level_time = level_minutes.get(level, 0)
        time_per_activity = level_time / level_activities if level_activities > 0 else 0

        for _ in range(level_activities):
            activity_slots.append({
                'marzano_level': level,
                'suggested_duration': round(time_per_activity)
            })

    return activity_slots


def save_lesson_design(
    session_id: str,
    design_data: Dict[str, Any],
    version: int = 1
) -> str:
    """
    Save lesson design to session directory.

    Args:
        session_id: Session identifier
        design_data: Lesson design data
        version: Version number (for iteration during validation)

    Returns:
        Path to saved file
    """
    session_path = get_session_path(session_id)

    # Ensure directory exists
    os.makedirs(session_path, exist_ok=True)

    # Determine filename based on version
    if version == 1:
        filename = '03_lesson_design_v1.json'
    else:
        filename = f'03_lesson_design_v{version}.json'

    filepath = os.path.join(session_path, filename)

    # Update version in metadata
    if 'metadata' not in design_data:
        design_data['metadata'] = {}
    design_data['metadata']['version'] = version
    design_data['metadata']['saved_at'] = datetime.now().isoformat()

    # Save JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(design_data, f, indent=2, ensure_ascii=False)

    return filepath


def load_lesson_design(session_id: str, version: int = 1) -> Optional[Dict[str, Any]]:
    """
    Load lesson design from session directory.

    Args:
        session_id: Session identifier
        version: Version number to load

    Returns:
        Lesson design data or None if not found
    """
    session_path = get_session_path(session_id)

    if version == 1:
        filename = '03_lesson_design_v1.json'
    else:
        filename = f'03_lesson_design_v{version}.json'

    filepath = os.path.join(session_path, filename)

    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_activity_templates(marzano_level: str) -> List[Dict[str, Any]]:
    """
    Return activity templates for a given Marzano level.

    Args:
        marzano_level: One of: retrieval, comprehension, analysis, knowledge_utilization

    Returns:
        List of activity template dicts with:
        - name_pattern: Suggested activity name
        - typical_duration: (min, max) duration range
        - description: What students do
        - student_output: What students produce
    """
    if marzano_level not in ACTIVITY_TEMPLATES:
        return []

    return ACTIVITY_TEMPLATES[marzano_level].copy()


def save_final_design(session_id: str, design_data: Dict[str, Any]) -> str:
    """
    Save validated final lesson design.

    Called after validation passes in Stage 3b.

    Args:
        session_id: Session identifier
        design_data: Validated lesson design data

    Returns:
        Path to saved file
    """
    session_path = get_session_path(session_id)

    # Ensure directory exists
    os.makedirs(session_path, exist_ok=True)

    filepath = os.path.join(session_path, '04_lesson_final.json')

    # Update metadata
    if 'metadata' not in design_data:
        design_data['metadata'] = {}
    design_data['metadata']['validated'] = True
    design_data['metadata']['finalized_at'] = datetime.now().isoformat()

    # Save JSON
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(design_data, f, indent=2, ensure_ascii=False)

    return filepath


# Convenience function to get all lesson types
def get_lesson_types() -> List[str]:
    """Return list of valid lesson types."""
    return list(LESSON_TYPE_DISTRIBUTIONS.keys())


if __name__ == '__main__':
    # Example usage
    print("Lesson Design Helper Functions")
    print("=" * 40)
    print()

    print("Available lesson types:")
    for lt in get_lesson_types():
        dist = get_recommended_distribution(lt)
        print(f"  {lt}:")
        for level, pct in dist.items():
            print(f"    {level}: {pct}%")
    print()

    print("Activity templates for 'analysis':")
    for template in get_activity_templates('analysis'):
        print(f"  - {template['name_pattern']}")
        print(f"    Duration: {template['typical_duration'][0]}-{template['typical_duration'][1]} min")
        print(f"    Output: {template['student_output']}")
