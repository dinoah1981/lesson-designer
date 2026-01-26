#!/usr/bin/env python3
"""
Generate revision plan from persona feedback.

Usage:
    python generate_revision_plan.py <feedback_json> <output_json> [--markdown <output_md>]

Example:
    python generate_revision_plan.py \
        .lesson-designer/sessions/{session_id}/03_feedback_struggling_learner.json \
        .lesson-designer/sessions/{session_id}/03_revision_plan.json \
        --markdown .lesson-designer/sessions/{session_id}/03_revision_plan.md
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


def aggregate_feedback(feedback_files: List[str]) -> Dict[str, Any]:
    """
    Combine feedback from all personas (Phase 3: just 1, Phase 4: N personas).

    Args:
        feedback_files: List of feedback JSON file paths

    Returns:
        Aggregated feedback structure with all concerns and personas consulted
    """
    all_concerns = []
    personas_consulted = []

    for fb_path in feedback_files:
        with open(fb_path, 'r') as f:
            feedback = json.load(f)

        personas_consulted.append({
            'persona_id': feedback['persona'],
            'persona_name': feedback['persona_name']
        })

        # Extract concerns from feedback
        for concern in feedback.get('concerns', []):
            all_concerns.append({
                **concern,
                'persona_id': feedback['persona'],
                'persona_name': feedback['persona_name']
            })

    return {
        'all_concerns': all_concerns,
        'personas_consulted': personas_consulted
    }


def prioritize_revisions(concerns: List[Dict]) -> List[Dict]:
    """
    Organize by severity, group by element.

    Args:
        concerns: List of concern dictionaries from persona feedback

    Returns:
        Prioritized list sorted by severity (high > medium > low)
    """
    # Define severity ordering
    severity_order = {'high': 0, 'medium': 1, 'low': 2}

    # Sort by severity
    prioritized = sorted(
        concerns,
        key=lambda c: severity_order.get(c.get('severity', 'medium'), 1)
    )

    return prioritized


def detect_conflicts(all_concerns: List[Dict]) -> List[Dict]:
    """
    Identify conflicting recommendations across personas.

    Conflicts occur when:
    - Same element gets opposite recommendations (add scaffolding vs reduce scaffolding)
    - Persona needs are inherently opposing (struggling needs support, high-achieving needs less)

    Returns:
        List of conflict objects with resolution strategies
    """
    conflicts = []

    # Group concerns by element
    by_element = {}
    for concern in all_concerns:
        element = concern['element']
        if element not in by_element:
            by_element[element] = []
        by_element[element].append(concern)

    # Check each element for conflicts
    for element, concerns in by_element.items():
        if len(concerns) < 2:
            continue

        # Check for scaffolding vs. challenge conflict
        struggling_concerns = [c for c in concerns if c.get('persona_id') == 'struggling_learner_ell']
        high_achieving_concerns = [c for c in concerns if c.get('persona_id') == 'high_achieving']

        has_add_scaffold = any(
            'add' in c.get('recommendation', {}).get('change', '').lower() and
            ('scaffold' in c.get('recommendation', {}).get('change', '').lower() or
             'support' in c.get('recommendation', {}).get('change', '').lower())
            for c in struggling_concerns
        )

        has_reduce_complexity = any(
            any(word in c.get('recommendation', {}).get('change', '').lower()
                for word in ['reduce', 'remove', 'simplify', 'less'])
            for c in high_achieving_concerns
        )

        if has_add_scaffold and has_reduce_complexity:
            conflicts.append({
                'element': element,
                'type': 'scaffolding_vs_challenge',
                'personas_involved': ['struggling_learner_ell', 'high_achieving'],
                'struggling_recommendation': struggling_concerns[0] if struggling_concerns else None,
                'high_achieving_recommendation': high_achieving_concerns[0] if high_achieving_concerns else None,
                'resolution_strategy': 'tiered_support',
                'teacher_note': 'Provide scaffolded version for struggling learners, challenge version for advanced students. Both groups maintain same learning objective.'
            })

    return conflicts


def find_agreements(all_concerns: List[Dict], threshold: int = 3) -> List[Dict]:
    """
    Find recommendations where multiple personas agree.

    Args:
        all_concerns: All concerns from all personas
        threshold: Minimum number of personas that must agree (default: 3 of 4)

    Returns:
        List of concerns that are universally supported
    """
    # Group by element and similar recommendation patterns
    similar_groups = {}

    for concern in all_concerns:
        element = concern['element']
        change_text = concern.get('recommendation', {}).get('change', '')

        # Create grouping key from element and recommendation type (first 50 chars)
        key = f"{element}:{change_text[:50]}"

        if key not in similar_groups:
            similar_groups[key] = []
        similar_groups[key].append(concern)

    # Find groups meeting threshold
    agreements = []
    for key, group in similar_groups.items():
        persona_ids = set(c.get('persona_id', '') for c in group)
        if len(persona_ids) >= threshold:
            # Create synthesized concern
            agreements.append({
                'element': group[0]['element'],
                'severity': max((c.get('severity', 'medium') for c in group),
                               key=lambda s: {'high': 3, 'medium': 2, 'low': 1}.get(s, 0)),
                'issue': group[0]['issue'],
                'recommendation': group[0]['recommendation'],
                'personas_agreeing': [c.get('persona_name', '') for c in group],
                'agreement_count': len(persona_ids),
                'priority': 'universal'
            })

    return agreements


def synthesize_feedback(all_concerns: List[Dict]) -> Dict[str, Any]:
    """
    Combine concerns from all personas into categorized revision plan.

    Categories:
    - universal_improvements: 3+ personas agree (highest priority)
    - accessibility_critical: Struggling learner high severity concerns
    - engagement_enhancements: Unmotivated/interested persona recommendations
    - challenge_extensions: High-achieving persona recommendations
    - conflicting_recommendations: Require teacher decision with resolution strategies

    Returns:
        Categorized feedback dictionary
    """
    universal = find_agreements(all_concerns, threshold=3)
    conflicts = detect_conflicts(all_concerns)

    # Filter by persona for non-universal concerns
    def filter_by_persona(concerns, persona_ids, severity=None):
        if isinstance(persona_ids, str):
            persona_ids = [persona_ids]
        filtered = [c for c in concerns if c.get('persona_id') in persona_ids]
        if severity:
            filtered = [c for c in filtered if c.get('severity') == severity]
        return filtered

    # Get concerns already handled by universal or conflicts
    universal_elements = set(c['element'] for c in universal)
    conflict_elements = set(c['element'] for c in conflicts)
    handled = universal_elements | conflict_elements

    # Filter remaining concerns
    remaining = [c for c in all_concerns if c['element'] not in handled]

    return {
        'universal_improvements': universal,
        'accessibility_critical': filter_by_persona(remaining, 'struggling_learner_ell', 'high'),
        'engagement_enhancements': filter_by_persona(remaining, ['unmotivated_capable', 'interested_capable']),
        'challenge_extensions': filter_by_persona(remaining, 'high_achieving'),
        'conflicting_recommendations': conflicts,
        'metadata': {
            'total_concerns': len(all_concerns),
            'universal_count': len(universal),
            'conflicts_count': len(conflicts),
            'personas_analyzed': list(set(c.get('persona_id', '') for c in all_concerns))
        }
    }


def generate_revision_plan(lesson_path: str, feedback_paths: List[str], output_path: str) -> Dict[str, Any]:
    """
    Create structured revision plan with specific changes.

    Args:
        lesson_path: Path to lesson JSON (not used yet, but will be in Phase 4)
        feedback_paths: List of feedback JSON file paths
        output_path: Path to write revision plan JSON

    Returns:
        Revision plan dictionary
    """
    # Load lesson (for future use)
    with open(lesson_path, 'r') as f:
        lesson = json.load(f)

    # Aggregate concerns from all personas
    aggregated = aggregate_feedback(feedback_paths)
    all_concerns = aggregated['all_concerns']
    personas_consulted = aggregated['personas_consulted']

    # Prioritize by severity
    prioritized = prioritize_revisions(all_concerns)

    # Multi-persona mode vs single-persona mode
    if len(feedback_paths) > 1:
        # Multi-persona mode: Use synthesis categories
        synthesis = synthesize_feedback(all_concerns)

        # Build revision plan with synthesis structure
        revision_plan = {
            'lesson_title': lesson.get('title', 'Untitled Lesson'),
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'personas_consulted': [p['persona_name'] for p in personas_consulted],
            'mode': 'multi_persona',
            'synthesis': synthesis,
            'metadata': synthesis['metadata']
        }
    else:
        # Single-persona mode: Keep existing severity-based categorization
        # Structure into categories
        critical_changes = []
        optional_improvements = []
        requires_teacher_decision = []

        change_id_counter = 1

        for concern in prioritized:
            # Create change object with implementation details
            change = {
                'id': f"change_{change_id_counter:03d}",
                'element': concern['element'],
                'severity': concern['severity'],
                'status': 'pending',
                'current_state': concern['issue'],
                'proposed_change': concern['recommendation']['change'],
                'rationale': concern['recommendation']['rationale'],
                'impact_if_not_addressed': concern.get('impact', ''),
                'persona_source': concern['persona_name'],
                'implementation': _generate_implementation_object(concern),
                'teacher_notes': ''
            }

            # Categorize by severity
            if concern['severity'] == 'high':
                critical_changes.append(change)
            elif concern['severity'] == 'medium':
                optional_improvements.append(change)
            else:
                requires_teacher_decision.append(change)

            change_id_counter += 1

        # Build revision plan
        revision_plan = {
            'lesson_title': lesson.get('title', 'Untitled Lesson'),
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'personas_consulted': [p['persona_name'] for p in personas_consulted],
            'critical_changes': critical_changes,
            'optional_improvements': optional_improvements,
            'requires_teacher_decision': requires_teacher_decision,
            'metadata': {
                'total_changes': len(critical_changes) + len(optional_improvements) + len(requires_teacher_decision),
                'critical_count': len(critical_changes),
                'optional_count': len(optional_improvements),
                'low_priority_count': len(requires_teacher_decision)
            }
        }

    # Save revision plan JSON
    with open(output_path, 'w') as f:
        json.dump(revision_plan, f, indent=2)

    return revision_plan


def _generate_implementation_object(concern: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate implementation object based on concern element type.

    Args:
        concern: Concern dictionary from persona feedback

    Returns:
        Implementation object specific to the element type
    """
    element = concern['element']
    recommendation = concern.get('recommendation', {})

    if element == 'vocabulary':
        # Extract terms from evidence or issue
        evidence = concern.get('evidence', [])
        if isinstance(evidence, list) and len(evidence) > 0:
            terms = evidence
        else:
            # Parse terms from issue string if needed
            terms = []

        return {
            'add_definitions': True,
            'definitions': {term: {'definition': '', 'example': '', 'visual': ''} for term in terms},
            'add_pre_teaching_activity': True,
            'pre_teaching_duration': 5,
            'terms_to_define': terms
        }

    elif element == 'scaffolding':
        # Parse activity name from issue
        issue = concern.get('issue', '')
        activity_name = ''
        if 'Activity' in issue:
            # Extract activity name from issue string
            parts = issue.split("'")
            if len(parts) >= 2:
                activity_name = parts[1]

        return {
            'add_sentence_frames': True,
            'sentence_frames': [],
            'add_worked_example': False,
            'worked_example': {},
            'add_graphic_organizer': False,
            'graphic_organizer': {}
        }

    elif element == 'pacing':
        # Parse activity name and duration from issue
        issue = concern.get('issue', '')
        activity_name = ''
        duration = 0

        if 'Activity' in issue:
            parts = issue.split("'")
            if len(parts) >= 2:
                activity_name = parts[1]

        # Extract duration if present
        if 'min' in issue:
            import re
            match = re.search(r'(\d+)\s*min', issue)
            if match:
                duration = int(match.group(1))

        return {
            'add_break_point': True,
            'break_point': {
                'at_minute': duration // 2 if duration > 0 else 12,
                'type': 'turn_and_talk',
                'prompt': 'Share one thing you noticed with your partner'
            },
            'split_activity': False
        }

    elif element == 'instruction_clarity':
        # Parse activity name from issue
        issue = concern.get('issue', '')
        activity_name = ''
        if 'Activity' in issue:
            parts = issue.split("'")
            if len(parts) >= 2:
                activity_name = parts[1]

        return {
            'add_numbered_steps': True,
            'numbered_steps': [],
            'add_checklist': True,
            'checklist': []
        }

    else:
        # Generic implementation for unknown element types
        return {
            'manual_review_required': True,
            'recommendation_text': recommendation.get('implementation', '')
        }


def render_revision_markdown(revision_plan: Dict[str, Any], lesson: Dict[str, Any], output_md_path: str):
    """
    Generate teacher-readable Markdown from revision plan.

    Args:
        revision_plan: Revision plan dictionary
        lesson: Lesson design dictionary
        output_md_path: Path to write Markdown file
    """
    md_lines = []

    # Header
    md_lines.append(f"# Revision Plan: {revision_plan['lesson_title']}")
    md_lines.append('')
    md_lines.append(f"**Lesson:** {revision_plan['lesson_title']}")
    md_lines.append(f"**Generated:** {revision_plan['generated_date']}")
    md_lines.append(f"**Personas consulted:** {', '.join(revision_plan['personas_consulted'])}")
    md_lines.append('')

    # Summary
    metadata = revision_plan['metadata']
    md_lines.append('## Summary')
    md_lines.append('')

    # Check for multi-persona synthesis mode
    if 'synthesis' in revision_plan:
        synthesis = revision_plan['synthesis']
        md_lines.append(f"{metadata['total_concerns']} concerns identified across {len(metadata['personas_analyzed'])} personas")
        md_lines.append('')

        # Universal Improvements (highest priority - 3+ personas agree)
        if synthesis.get('universal_improvements'):
            md_lines.append('## Universal Improvements (3+ PERSONAS AGREE)')
            md_lines.append('')
            md_lines.append('*These changes are recommended by multiple personas and should be prioritized.*')
            md_lines.append('')

            for i, change in enumerate(synthesis['universal_improvements'], 1):
                md_lines.append(f"### {i}. {change['element']}")
                md_lines.append('')
                md_lines.append(f"**Issue:** {change['issue']}")
                md_lines.append(f"**Proposed Change:** {change['recommendation']['change']}")
                md_lines.append(f"**Personas Agreeing:** {', '.join(change['personas_agreeing'])}")
                md_lines.append('')
                md_lines.append('- [ ] Approve')
                md_lines.append('- [ ] Skip')
                md_lines.append('')

        # Accessibility Critical (struggling learner high severity)
        if synthesis.get('accessibility_critical'):
            md_lines.append('## Accessibility Critical (BARRIERS FOR STRUGGLING LEARNERS)')
            md_lines.append('')

            for i, change in enumerate(synthesis['accessibility_critical'], 1):
                md_lines.append(f"### {i}. {change['element']}")
                md_lines.append('')
                md_lines.append(f"**Issue:** {change['issue']}")
                md_lines.append(f"**Proposed Change:** {change['recommendation']['change']}")
                md_lines.append(f"**Rationale:** {change['recommendation']['rationale']}")
                md_lines.append('')
                md_lines.append('- [ ] Approve')
                md_lines.append('- [ ] Skip')
                md_lines.append('')

        # Engagement Enhancements
        if synthesis.get('engagement_enhancements'):
            md_lines.append('## Engagement Enhancements (MOTIVATION/INTEREST)')
            md_lines.append('')

            for i, change in enumerate(synthesis['engagement_enhancements'], 1):
                md_lines.append(f"### {i}. {change['element']}")
                md_lines.append('')
                md_lines.append(f"**Issue:** {change['issue']}")
                md_lines.append(f"**Proposed Change:** {change['recommendation']['change']}")
                md_lines.append(f"**Persona:** {change['persona_name']}")
                md_lines.append('')
                md_lines.append('- [ ] Approve')
                md_lines.append('- [ ] Skip')
                md_lines.append('')

        # Challenge Extensions
        if synthesis.get('challenge_extensions'):
            md_lines.append('## Challenge Extensions (HIGH-ACHIEVING NEEDS)')
            md_lines.append('')

            for i, change in enumerate(synthesis['challenge_extensions'], 1):
                md_lines.append(f"### {i}. {change['element']}")
                md_lines.append('')
                md_lines.append(f"**Issue:** {change['issue']}")
                md_lines.append(f"**Proposed Change:** {change['recommendation']['change']}")
                md_lines.append('')
                md_lines.append('- [ ] Approve')
                md_lines.append('- [ ] Skip')
                md_lines.append('')

        # Conflicting Recommendations (require teacher decision)
        if synthesis.get('conflicting_recommendations'):
            md_lines.append('## Conflicting Recommendations (REQUIRE TEACHER DECISION)')
            md_lines.append('')
            md_lines.append('*These recommendations conflict across personas. Review resolution strategies.*')
            md_lines.append('')

            for i, conflict in enumerate(synthesis['conflicting_recommendations'], 1):
                md_lines.append(f"### Conflict {i}: {conflict['element']}")
                md_lines.append('')
                md_lines.append(f"**Type:** {conflict['type']}")
                md_lines.append(f"**Personas Involved:** {', '.join(conflict['personas_involved'])}")
                md_lines.append('')
                if conflict.get('struggling_recommendation'):
                    md_lines.append(f"**Struggling Learner Says:** {conflict['struggling_recommendation'].get('recommendation', {}).get('change', 'N/A')}")
                if conflict.get('high_achieving_recommendation'):
                    md_lines.append(f"**High Achiever Says:** {conflict['high_achieving_recommendation'].get('recommendation', {}).get('change', 'N/A')}")
                md_lines.append('')
                md_lines.append(f"**Resolution Strategy:** `{conflict['resolution_strategy']}`")
                md_lines.append(f"**Teacher Note:** {conflict['teacher_note']}")
                md_lines.append('')
                md_lines.append('**Teacher Decision:**')
                md_lines.append('- [ ] Use tiered support (scaffolded + challenge versions)')
                md_lines.append('- [ ] Use core + extension model')
                md_lines.append('- [ ] Create optional paths')
                md_lines.append('- [ ] Other: ___')
                md_lines.append('')
    else:
        # Single-persona mode: Use existing severity-based rendering
        md_lines.append(f"{metadata['total_changes']} concerns identified, {metadata['critical_count']} critical")
        md_lines.append('')

    # Critical Changes (only for single-persona mode)
    if 'synthesis' not in revision_plan and revision_plan['critical_changes']:
        md_lines.append('## Critical Changes (RECOMMENDED)')
        md_lines.append('')

        for i, change in enumerate(revision_plan['critical_changes'], 1):
            md_lines.append(f"### Change {i}: {change['proposed_change']}")
            md_lines.append('')
            md_lines.append(f"**Element:** {change['element']}")
            md_lines.append(f"**Severity:** {change['severity'].upper()}")
            md_lines.append(f"**Persona:** {change['persona_source']}")
            md_lines.append('')
            md_lines.append(f"**Current State:** {change['current_state']}")
            md_lines.append('')
            md_lines.append(f"**Proposed Change:** {change['proposed_change']}")
            md_lines.append('')
            md_lines.append(f"**Rationale:** {change['rationale']}")
            md_lines.append('')
            md_lines.append(f"**Impact if not addressed:** {change['impact_if_not_addressed']}")
            md_lines.append('')
            md_lines.append('**Teacher decision:**')
            md_lines.append('- [ ] Approve as written')
            md_lines.append('- [ ] Approve with modifications: ___')
            md_lines.append('- [ ] Reject (reason: ___)')
            md_lines.append('')

    # Optional Improvements (only for single-persona mode)
    if 'synthesis' not in revision_plan and revision_plan['optional_improvements']:
        md_lines.append('## Optional Improvements (CONSIDER)')
        md_lines.append('')

        for i, change in enumerate(revision_plan['optional_improvements'], 1):
            md_lines.append(f"### Change {i}: {change['proposed_change']}")
            md_lines.append('')
            md_lines.append(f"**Element:** {change['element']}")
            md_lines.append(f"**Severity:** {change['severity'].upper()}")
            md_lines.append(f"**Persona:** {change['persona_source']}")
            md_lines.append('')
            md_lines.append(f"**Current State:** {change['current_state']}")
            md_lines.append('')
            md_lines.append(f"**Proposed Change:** {change['proposed_change']}")
            md_lines.append('')
            md_lines.append(f"**Rationale:** {change['rationale']}")
            md_lines.append('')
            md_lines.append('**Teacher decision:**')
            md_lines.append('- [ ] Approve')
            md_lines.append('- [ ] Skip')
            md_lines.append('')

    # Requires Teacher Context (only for single-persona mode)
    if 'synthesis' not in revision_plan and revision_plan['requires_teacher_decision']:
        md_lines.append('## Requires Teacher Context (LOW PRIORITY)')
        md_lines.append('')

        for i, change in enumerate(revision_plan['requires_teacher_decision'], 1):
            md_lines.append(f"### Change {i}: {change['proposed_change']}")
            md_lines.append('')
            md_lines.append(f"**Element:** {change['element']}")
            md_lines.append(f"**Persona:** {change['persona_source']}")
            md_lines.append('')
            md_lines.append(f"**Issue:** {change['current_state']}")
            md_lines.append('')
            md_lines.append(f"**Suggestion:** {change['proposed_change']}")
            md_lines.append('')

    # Approval Summary
    md_lines.append('## Approval Summary')
    md_lines.append('')

    if 'synthesis' in revision_plan:
        # Multi-persona summary
        synthesis = revision_plan['synthesis']
        total_changes = (len(synthesis.get('universal_improvements', [])) +
                        len(synthesis.get('accessibility_critical', [])) +
                        len(synthesis.get('engagement_enhancements', [])) +
                        len(synthesis.get('challenge_extensions', [])))
        md_lines.append(f"**Total changes requiring review:** {total_changes}")
        md_lines.append(f"**Conflicts requiring teacher decision:** {len(synthesis.get('conflicting_recommendations', []))}")
    else:
        # Single-persona summary
        md_lines.append(f"**Critical changes requiring approval:** {metadata['critical_count']}")
        # Estimate time impact
        time_estimate = metadata['critical_count'] * 3 + metadata['optional_count'] * 2
        md_lines.append(f"**Estimated time impact:** +{time_estimate} minutes")

    md_lines.append('')

    # Write to file
    with open(output_md_path, 'w') as f:
        f.write('\n'.join(md_lines))


def apply_revisions(lesson_path: str, revision_plan_path: str, output_path: str) -> Dict[str, Any]:
    """
    Apply teacher-approved revisions to lesson JSON.

    Args:
        lesson_path: Path to 04_lesson_final.json
        revision_plan_path: Path to 03_revision_plan.json with teacher decisions
        output_path: Path to write revised lesson (can be same as lesson_path)

    Returns:
        Dictionary with 'applied' and 'skipped' change IDs
    """
    # Load files
    with open(lesson_path, 'r') as f:
        lesson = json.load(f)

    with open(revision_plan_path, 'r') as f:
        revision_plan = json.load(f)

    # Track what was applied
    applied = []
    skipped = []

    # Process each change category
    all_changes = (
        revision_plan.get('critical_changes', []) +
        revision_plan.get('optional_improvements', [])
    )

    for change in all_changes:
        # Skip non-approved changes
        if change.get('status') not in ['approved', 'approved_with_modifications']:
            skipped.append(change['id'])
            continue

        # Route to appropriate handler based on element type
        element = change['element']

        try:
            if element == 'vocabulary':
                _apply_vocabulary_change(lesson, change)
            elif element == 'scaffolding':
                _apply_scaffolding_change(lesson, change)
            elif element == 'pacing':
                _apply_pacing_change(lesson, change)
            elif element == 'instruction_clarity':
                _apply_instructions_change(lesson, change)
            else:
                # Generic change - store in lesson metadata for manual handling
                _apply_generic_change(lesson, change)

            applied.append(change['id'])
        except Exception as e:
            # If application fails, skip and log
            skipped.append(change['id'])
            print(f"Warning: Failed to apply {change['id']}: {e}")

    # Add revision metadata
    lesson['_revision_applied'] = {
        'date': datetime.now().isoformat(),
        'revision_plan': str(revision_plan_path),
        'changes_applied': applied,
        'changes_skipped': skipped
    }

    # Write output
    with open(output_path, 'w') as f:
        json.dump(lesson, f, indent=2)

    return {'applied': applied, 'skipped': skipped}


def _apply_vocabulary_change(lesson: Dict[str, Any], change: Dict[str, Any]):
    """
    Add vocabulary definitions to lesson.

    Change structure expected:
    {
        "element": "vocabulary",
        "terms_to_define": ["bias", "reliability", "perspective"],
        "implementation": {
            "add_definitions": true,
            "definitions": {
                "bias": {"definition": "...", "example": "...", "visual": "..."},
                ...
            }
        }
    }

    Modifies lesson:
    - lesson['vocabulary'] list: adds 'definition', 'example', 'visual' fields to each term
    - lesson['activities']: adds pre-teaching activity if not present
    """
    impl = change.get('implementation', {})

    # Ensure vocabulary section exists
    if 'vocabulary' not in lesson:
        lesson['vocabulary'] = []

    # Add definitions to existing vocabulary items
    if impl.get('add_definitions'):
        definitions = impl.get('definitions', {})
        for vocab_item in lesson['vocabulary']:
            term = vocab_item.get('word', vocab_item.get('term', ''))
            if term in definitions:
                vocab_item['definition'] = definitions[term].get('definition', '')
                vocab_item['example'] = definitions[term].get('example', '')
                vocab_item['visual'] = definitions[term].get('visual', '')

    # Add pre-teaching activity if specified
    if impl.get('add_pre_teaching_activity'):
        pre_teach = {
            'name': 'Vocabulary Pre-Teaching',
            'duration': impl.get('pre_teaching_duration', 5),
            'description': 'Review key vocabulary before main lesson',
            'type': 'vocabulary_introduction',
            'marzano_level': 'retrieval',
            'instructions': [
                'Review each vocabulary term',
                'Read definition and example',
                'View visual representation'
            ],
            'student_output': 'Vocabulary notes',
            'assessment_method': 'Quick check for understanding',
            'terms': impl.get('terms_to_define', [])
        }
        # Insert at beginning of activities
        if 'activities' in lesson:
            lesson['activities'].insert(0, pre_teach)


def _apply_scaffolding_change(lesson: Dict[str, Any], change: Dict[str, Any]):
    """
    Add scaffolding elements (sentence frames, worked examples, graphic organizers).

    Change structure expected:
    {
        "element": "scaffolding",
        "target_activity": "SOAP Analysis",  # Activity name to modify
        "implementation": {
            "add_sentence_frames": true,
            "sentence_frames": [
                "The speaker is ___ because ___.",
                "This source was created to ___."
            ],
            "add_worked_example": true,
            "worked_example": {
                "description": "Model SOAP analysis of Declaration of Independence",
                "content": "..."
            },
            "add_graphic_organizer": true,
            "graphic_organizer": {
                "type": "SOAP_chart",
                "template": "..."
            }
        }
    }

    Modifies lesson:
    - lesson['activities'][target]: adds 'sentence_frames', 'worked_example', 'graphic_organizer' fields
    - lesson['materials']: adds new handout if graphic organizer specified
    """
    impl = change.get('implementation', {})

    # Try to extract target activity from issue or use a pattern match
    issue = change.get('current_state', '')
    target_name = ''
    if 'Activity' in issue:
        parts = issue.split("'")
        if len(parts) >= 2:
            target_name = parts[1]

    # Find target activity
    for activity in lesson.get('activities', []):
        if target_name and (activity.get('name') == target_name or target_name in activity.get('name', '')):
            # Add sentence frames
            if impl.get('add_sentence_frames'):
                activity['sentence_frames'] = impl.get('sentence_frames', [])
                activity['include_sentence_frames'] = True

            # Add worked example
            if impl.get('add_worked_example'):
                activity['worked_example'] = impl.get('worked_example', {})
                activity['include_worked_example'] = True

            # Add graphic organizer
            if impl.get('add_graphic_organizer'):
                activity['graphic_organizer'] = impl.get('graphic_organizer', {})

            break

    # Add to materials list if graphic organizer added
    if impl.get('add_graphic_organizer'):
        if 'materials' not in lesson:
            lesson['materials'] = []
        lesson['materials'].append({
            'name': f"{impl['graphic_organizer'].get('type', 'Graphic Organizer')} Handout",
            'type': 'handout',
            'for_activity': target_name
        })


def _apply_pacing_change(lesson: Dict[str, Any], change: Dict[str, Any]):
    """
    Add break points or split activities for better pacing.

    Change structure expected:
    {
        "element": "pacing",
        "target_activity": "Document Analysis",
        "implementation": {
            "add_break_point": true,
            "break_point": {
                "at_minute": 12,
                "type": "turn_and_talk",
                "prompt": "Share one thing you noticed with your partner"
            },
            "split_activity": false  # Alternative: split into two activities
        }
    }

    Modifies lesson:
    - lesson['activities'][target]: adds 'break_points' array
    - OR splits activity into two separate activities
    """
    impl = change.get('implementation', {})

    # Extract target activity name from issue
    issue = change.get('current_state', '')
    target_name = ''
    if 'Activity' in issue:
        parts = issue.split("'")
        if len(parts) >= 2:
            target_name = parts[1]

    for i, activity in enumerate(lesson.get('activities', [])):
        if target_name and (activity.get('name') == target_name or target_name in activity.get('name', '')):
            if impl.get('add_break_point'):
                # Add break point within activity
                if 'break_points' not in activity:
                    activity['break_points'] = []
                activity['break_points'].append(impl.get('break_point', {}))

            elif impl.get('split_activity'):
                # Split into two activities
                split_config = impl.get('split_config', {})
                original_duration = activity.get('duration', 20)

                # First half
                activity['duration'] = split_config.get('first_duration', original_duration // 2)
                activity['name'] = f"{activity['name']} - Part 1"

                # Second half (insert after)
                second_half = {
                    'name': f"{target_name} - Part 2",
                    'duration': split_config.get('second_duration', original_duration // 2),
                    'description': split_config.get('second_description', 'Continue activity'),
                    'type': activity.get('type', 'activity'),
                    'marzano_level': activity.get('marzano_level', 'comprehension')
                }
                lesson['activities'].insert(i + 1, second_half)

            break


def _apply_instructions_change(lesson: Dict[str, Any], change: Dict[str, Any]):
    """
    Modify instruction clarity (numbered steps, simplify language).

    Change structure expected:
    {
        "element": "instructions",
        "target_activity": "Activity Name",
        "implementation": {
            "add_numbered_steps": true,
            "numbered_steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
            "add_checklist": true,
            "checklist": ["Did you...?", "Did you...?"]
        }
    }
    """
    impl = change.get('implementation', {})

    # Extract target activity name from issue
    issue = change.get('current_state', '')
    target_name = ''
    if 'Activity' in issue:
        parts = issue.split("'")
        if len(parts) >= 2:
            target_name = parts[1]

    for activity in lesson.get('activities', []):
        if target_name and (activity.get('name') == target_name or target_name in activity.get('name', '')):
            if impl.get('add_numbered_steps'):
                activity['instructions'] = impl.get('numbered_steps', [])
                activity['instruction_format'] = 'numbered'

            if impl.get('add_checklist'):
                activity['completion_checklist'] = impl.get('checklist', [])

            break


def _apply_generic_change(lesson: Dict[str, Any], change: Dict[str, Any]):
    """
    Store unhandled change types in lesson metadata for manual review.
    """
    if '_pending_manual_changes' not in lesson:
        lesson['_pending_manual_changes'] = []

    lesson['_pending_manual_changes'].append({
        'id': change.get('id'),
        'element': change.get('element'),
        'description': change.get('proposed_change'),
        'rationale': change.get('rationale')
    })


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate revision plan from persona feedback'
    )
    parser.add_argument('feedback', help='Path to feedback JSON file (or comma-separated list for multiple)')
    parser.add_argument('output', help='Path to output revision plan JSON')
    parser.add_argument('--markdown', help='Path to output Markdown file (optional)')
    parser.add_argument('--lesson', help='Path to lesson JSON file (optional, for context)')

    args = parser.parse_args()

    try:
        # Parse feedback file paths (support comma-separated list for Phase 4)
        feedback_paths = [f.strip() for f in args.feedback.split(',')]

        # Generate revision plan
        # For now, use empty lesson if not provided
        lesson_path = args.lesson if args.lesson else feedback_paths[0]  # Fallback

        revision_plan = generate_revision_plan(
            lesson_path=lesson_path,
            feedback_paths=feedback_paths,
            output_path=args.output
        )

        print(f"\n{'='*60}")
        print(f"Revision Plan Generated")
        print(f"{'='*60}")
        print(f"Lesson: {revision_plan['lesson_title']}")
        print(f"Date: {revision_plan['generated_date']}")
        print(f"Personas: {', '.join(revision_plan['personas_consulted'])}")
        print(f"\nChanges:")
        print(f"  Critical: {revision_plan['metadata']['critical_count']}")
        print(f"  Optional: {revision_plan['metadata']['optional_count']}")
        print(f"  Low priority: {revision_plan['metadata']['low_priority_count']}")
        print(f"\nRevision plan saved to: {args.output}")

        # Generate Markdown if requested
        if args.markdown:
            # Load lesson for Markdown generation
            lesson = {}
            if args.lesson:
                with open(args.lesson, 'r') as f:
                    lesson = json.load(f)

            render_revision_markdown(revision_plan, lesson, args.markdown)
            print(f"Markdown version saved to: {args.markdown}")

        print(f"{'='*60}\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == '__main__':
    import sys
    main()
