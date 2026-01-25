"""
Competency parsing and session management utilities for the Lesson Designer skill.

This module provides functions for:
- Creating and managing lesson design sessions
- Saving and loading input data (Stage 1)
- Saving and loading competency breakdowns (Stage 2)

All functions use absolute paths to work correctly in the Claude environment
where the working directory may reset between bash calls.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path


def get_project_root() -> Path:
    """
    Get the project root directory.

    Walks up from the script location to find the project root
    (directory containing .claude or .lesson-designer).

    Returns:
        Path: Absolute path to project root
    """
    # Start from this script's directory
    current = Path(__file__).resolve().parent

    # Walk up to find project root (contains .claude or .lesson-designer)
    for _ in range(10):  # Max 10 levels up
        if (current / '.claude').exists() or (current / '.lesson-designer').exists():
            return current
        if (current / '.git').exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent

    # Fallback: assume 4 levels up from scripts directory
    # scripts -> lesson-designer -> skills -> .claude -> project_root
    return Path(__file__).resolve().parent.parent.parent.parent.parent


def get_sessions_dir() -> Path:
    """
    Get the absolute path to the sessions directory.

    Returns:
        Path: Absolute path to .lesson-designer/sessions/
    """
    return get_project_root() / '.lesson-designer' / 'sessions'


def generate_session_id() -> str:
    """
    Generate a unique session ID.

    Format: UUID v4 string (e.g., "550e8400-e29b-41d4-a716-446655440000")

    Returns:
        str: A new UUID string for the session

    Example:
        >>> session_id = generate_session_id()
        >>> print(session_id)
        "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
    """
    return str(uuid.uuid4())


def create_session_directory(session_id: str) -> Path:
    """
    Create the session directory for a new lesson design session.

    Creates the directory structure:
        .lesson-designer/sessions/{session_id}/

    Args:
        session_id: The unique session identifier

    Returns:
        Path: Absolute path to the created session directory

    Example:
        >>> session_id = generate_session_id()
        >>> session_dir = create_session_directory(session_id)
        >>> print(session_dir)
        Path('/path/to/project/.lesson-designer/sessions/abc123...')
    """
    session_dir = get_sessions_dir() / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def get_session_directory(session_id: str) -> Path:
    """
    Get the absolute path to an existing session directory.

    Args:
        session_id: The unique session identifier

    Returns:
        Path: Absolute path to the session directory

    Raises:
        FileNotFoundError: If the session directory doesn't exist
    """
    session_dir = get_sessions_dir() / session_id
    if not session_dir.exists():
        raise FileNotFoundError(f"Session directory not found: {session_dir}")
    return session_dir


def save_input(session_id: str, input_data: dict) -> Path:
    """
    Save teacher input to 01_input.json.

    Adds created_at timestamp if not present.

    Args:
        session_id: The unique session identifier
        input_data: Dictionary containing:
            - competency: str (skill statement)
            - grade_level: str
            - lesson_count: int
            - lesson_duration: int (minutes)
            - constraints: str or None

    Returns:
        Path: Absolute path to the saved file

    Example:
        >>> input_data = {
        ...     "competency": "Students will analyze primary sources",
        ...     "grade_level": "8th grade",
        ...     "lesson_count": 2,
        ...     "lesson_duration": 55,
        ...     "constraints": None
        ... }
        >>> filepath = save_input(session_id, input_data)
    """
    session_dir = get_session_directory(session_id)

    # Ensure session_id is in the data
    input_data['session_id'] = session_id

    # Add timestamp if not present
    if 'created_at' not in input_data:
        input_data['created_at'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

    filepath = session_dir / '01_input.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(input_data, f, indent=2, ensure_ascii=False)

    return filepath


def load_input(session_id: str) -> dict:
    """
    Load teacher input from 01_input.json.

    Args:
        session_id: The unique session identifier

    Returns:
        dict: The input data dictionary

    Raises:
        FileNotFoundError: If 01_input.json doesn't exist

    Example:
        >>> input_data = load_input(session_id)
        >>> print(input_data['competency'])
        "Students will analyze primary sources"
    """
    session_dir = get_session_directory(session_id)
    filepath = session_dir / '01_input.json'

    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_breakdown(session_id: str, breakdown_data: dict) -> Path:
    """
    Save competency breakdown to 02_competency_breakdown.json.

    Args:
        session_id: The unique session identifier
        breakdown_data: Dictionary containing:
            - skill: dict with verb, object, full_statement
            - required_knowledge: list of knowledge items

    Returns:
        Path: Absolute path to the saved file

    Example:
        >>> breakdown = {
        ...     "skill": {
        ...         "verb": "analyze",
        ...         "object": "primary sources",
        ...         "full_statement": "Analyze primary sources to evaluate claims"
        ...     },
        ...     "required_knowledge": [
        ...         {"id": "K1", "item": "What primary sources are", "classification": None}
        ...     ]
        ... }
        >>> filepath = save_breakdown(session_id, breakdown)
    """
    session_dir = get_session_directory(session_id)

    filepath = session_dir / '02_competency_breakdown.json'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(breakdown_data, f, indent=2, ensure_ascii=False)

    return filepath


def load_breakdown(session_id: str) -> dict:
    """
    Load competency breakdown from 02_competency_breakdown.json.

    Args:
        session_id: The unique session identifier

    Returns:
        dict: The breakdown data dictionary

    Raises:
        FileNotFoundError: If 02_competency_breakdown.json doesn't exist

    Example:
        >>> breakdown = load_breakdown(session_id)
        >>> print(breakdown['skill']['verb'])
        "analyze"
    """
    session_dir = get_session_directory(session_id)
    filepath = session_dir / '02_competency_breakdown.json'

    if not filepath.exists():
        raise FileNotFoundError(f"Breakdown file not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def update_breakdown_with_classifications(
    session_id: str,
    classifications: dict,
    target_proficiency: str
) -> Path:
    """
    Update competency breakdown with teacher classifications and proficiency target.

    Args:
        session_id: The unique session identifier
        classifications: Dictionary mapping knowledge item IDs to classifications
            e.g., {"K1": "needs_teaching", "K2": "already_assumed"}
        target_proficiency: One of "novice", "developing", "proficient", "advanced"

    Returns:
        Path: Absolute path to the updated file

    Example:
        >>> classifications = {"K1": "needs_teaching", "K2": "already_assumed"}
        >>> filepath = update_breakdown_with_classifications(
        ...     session_id, classifications, "proficient"
        ... )
    """
    breakdown = load_breakdown(session_id)

    # Update classifications for each knowledge item
    for item in breakdown.get('required_knowledge', []):
        item_id = item.get('id')
        if item_id in classifications:
            item['classification'] = classifications[item_id]

    # Add target proficiency
    breakdown['target_proficiency'] = target_proficiency

    return save_breakdown(session_id, breakdown)


# For convenience when testing
if __name__ == '__main__':
    # Test basic functionality
    print("Testing parse_competency.py...")

    # Generate session
    session_id = generate_session_id()
    print(f"Generated session ID: {session_id}")

    # Create directory
    session_dir = create_session_directory(session_id)
    print(f"Created session directory: {session_dir}")

    # Save input
    test_input = {
        "competency": "Students will analyze primary sources to evaluate historical claims",
        "grade_level": "8th grade",
        "lesson_count": 2,
        "lesson_duration": 55,
        "constraints": "Limited printing budget"
    }
    input_path = save_input(session_id, test_input)
    print(f"Saved input to: {input_path}")

    # Load input
    loaded_input = load_input(session_id)
    print(f"Loaded input competency: {loaded_input['competency']}")

    # Save breakdown
    test_breakdown = {
        "skill": {
            "verb": "analyze",
            "object": "primary sources",
            "full_statement": "Analyze primary sources to evaluate historical claims"
        },
        "required_knowledge": [
            {"id": "K1", "item": "What primary sources are (definition, types)", "classification": None},
            {"id": "K2", "item": "How to identify bias in sources", "classification": None}
        ]
    }
    breakdown_path = save_breakdown(session_id, test_breakdown)
    print(f"Saved breakdown to: {breakdown_path}")

    # Load breakdown
    loaded_breakdown = load_breakdown(session_id)
    print(f"Loaded breakdown skill: {loaded_breakdown['skill']['full_statement']}")

    print("\nAll tests passed!")
