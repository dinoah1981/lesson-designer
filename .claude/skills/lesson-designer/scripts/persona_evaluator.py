#!/usr/bin/env python3
"""
Persona-based lesson evaluator for accessibility feedback.

Usage:
    python persona_evaluator.py <lesson_json> <persona_json> <output_json>

Example:
    python persona_evaluator.py \
        .lesson-designer/sessions/{session_id}/04_lesson_final.json \
        .claude/skills/lesson-designer/personas/struggling_learner.json \
        .lesson-designer/sessions/{session_id}/03_feedback_struggling_learner.json
"""

import json
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class PersonaEvaluator:
    """Evaluates lesson designs against persona characteristics and needs."""

    def __init__(self, persona_config: Dict[str, Any]):
        """
        Initialize evaluator with persona configuration.

        Args:
            persona_config: Persona definition JSON with characteristics and evaluation criteria
        """
        self.persona = persona_config
        self.persona_id = persona_config['persona_id']
        self.persona_name = persona_config['persona_name']
        self.characteristics = persona_config['characteristics']
        self.decision_rules = persona_config.get('decision_rules', {})

        # Map evaluation criteria to methods
        self.evaluators = {
            'vocabulary_accessibility': self.evaluate_vocabulary,
            'instruction_clarity': self.evaluate_instructions,
            'scaffolding_adequacy': self.evaluate_scaffolding,
            'pacing_appropriateness': self.evaluate_pacing,
            'engagement_accessibility': self.evaluate_engagement
        }

    def evaluate_lesson(self, lesson: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run all evaluation criteria from persona config.

        Args:
            lesson: Lesson design JSON from Stage 3

        Returns:
            Structured feedback JSON with strengths, concerns, recommendations
        """
        strengths = []
        concerns = []

        # Run each evaluation criterion
        for criterion in self.persona.get('evaluation_criteria', []):
            evaluator = self.evaluators.get(criterion)
            if evaluator:
                criterion_results = evaluator(lesson)
                strengths.extend(criterion_results.get('strengths', []))
                concerns.extend(criterion_results.get('concerns', []))

        # Calculate overall accessibility rating
        rating = self.calculate_rating(concerns)

        # Generate overall assessment
        overall_assessment = {
            'accessibility_rating': f"{rating}/5",
            'summary': self._generate_summary(rating, concerns, strengths),
            'primary_concern': self._get_primary_concern(concerns)
        }

        # Build feedback structure
        feedback = {
            'persona': self.persona_id,
            'persona_name': self.persona_name,
            'evaluation_date': datetime.now().strftime('%Y-%m-%d'),
            'lesson_title': lesson.get('title', 'Untitled Lesson'),
            'overall_assessment': overall_assessment,
            'strengths': strengths,
            'concerns': concerns,
            'pedagogical_notes': self._generate_pedagogical_notes(concerns, strengths),
            'metadata': {
                'confidence': 'high',
                'persona_version': '1.0',
                'evaluator_version': '1.0'
            }
        }

        return feedback

    def evaluate_vocabulary(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check vocabulary against persona reading level and needs."""
        strengths = []
        concerns = []

        # Check vocabulary list
        vocabulary = lesson.get('vocabulary', [])

        # Identify undefined academic terms
        undefined_terms = [
            term for term in vocabulary
            if not term.get('definition') and not term.get('visual_support')
        ]

        if undefined_terms:
            severity = self._determine_severity('vocabulary', len(undefined_terms))
            concerns.append({
                'element': 'vocabulary',
                'issue': f"{len(undefined_terms)} academic term(s) lack explicit definitions or visual supports",
                'severity': severity,
                'impact': f"Alex will struggle to understand tier 2/3 vocabulary: {', '.join([t['word'] for t in undefined_terms[:3]])}",
                'evidence': [t['word'] for t in undefined_terms],
                'recommendation': {
                    'change': 'Add explicit definitions with examples or visual supports for all academic terms',
                    'rationale': 'Students reading 2-3 years below grade level need explicit vocabulary instruction with multiple representations',
                    'implementation': 'Include definition, example sentence, and visual representation (diagram, icon, or photo) for each term'
                }
            })

        # Check if definitions are provided - this is a strength
        defined_terms = [
            term for term in vocabulary
            if term.get('definition') or term.get('visual_support')
        ]

        if defined_terms and len(defined_terms) > len(undefined_terms):
            strengths.append({
                'element': 'vocabulary',
                'observation': f"{len(defined_terms)} vocabulary term(s) include explicit definitions",
                'why_helpful': 'Explicit definitions support Alex\'s vocabulary development and reduce cognitive load during new concept learning'
            })

        # Check sentence complexity in instructions and materials
        for activity in lesson.get('activities', []):
            instructions = activity.get('instructions', [])
            if instructions:
                text = ' '.join(instructions)
                words = text.split()
                avg_sentence_length = len(words) / len(instructions) if instructions else 0

                if avg_sentence_length > 20:
                    severity = self._determine_severity('sentence_complexity', avg_sentence_length)
                    concerns.append({
                        'element': 'instruction_clarity',
                        'issue': f"Activity '{activity['name']}': Complex sentences (avg {avg_sentence_length:.0f} words/sentence)",
                        'severity': severity,
                        'impact': f"Alex may struggle to process lengthy instructions while holding task requirements in working memory",
                        'evidence': f"Average sentence length: {avg_sentence_length:.1f} words (target: <15 words)",
                        'recommendation': {
                            'change': 'Break instructions into shorter sentences or bullet points',
                            'rationale': 'Shorter sentences (10-15 words) reduce cognitive load for struggling readers',
                            'implementation': 'Rewrite as step-by-step checklist with one action per bullet point'
                        }
                    })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_instructions(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check instruction clarity against persona limits."""
        strengths = []
        concerns = []

        for activity in lesson.get('activities', []):
            instructions = activity.get('instructions', [])

            # Check step count
            if len(instructions) > self.characteristics['attention']['multistep_limit']:
                severity = self._determine_severity('instructions', len(instructions))
                concerns.append({
                    'element': 'instruction_clarity',
                    'issue': f"Activity '{activity['name']}': {len(instructions)} steps exceeds Alex's multistep limit ({self.characteristics['attention']['multistep_limit']} steps)",
                    'severity': severity,
                    'impact': 'Alex may forget earlier steps or lose track of the overall task goal',
                    'evidence': f"Instructions have {len(instructions)} steps: {'; '.join(instructions[:3])}...",
                    'recommendation': {
                        'change': 'Add visual checklist or break into smaller sub-tasks',
                        'rationale': 'Struggling learners benefit from chunked tasks with visual progress tracking',
                        'implementation': 'Create a numbered checklist graphic organizer with checkbox for each step'
                    }
                })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_scaffolding(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check scaffolding against persona needs."""
        strengths = []
        concerns = []

        for activity in lesson.get('activities', []):
            student_output = activity.get('student_output', '').lower()

            # Check for production tasks without scaffolding
            if any(term in student_output for term in ['written response', 'writing', 'essay', 'paragraph', 'analysis']):
                # Look for scaffolding indicators
                has_model = 'example' in str(activity).lower() or 'model' in str(activity).lower()
                has_frames = 'sentence frame' in str(activity).lower() or 'sentence starter' in str(activity).lower()
                has_graphic_organizer = 'graphic organizer' in str(activity).lower() or 'organizer' in str(activity).lower()

                scaffolding_present = has_model or has_frames or has_graphic_organizer

                if not scaffolding_present:
                    # Determine severity based on task complexity
                    marzano_level = activity.get('marzano_level', '')
                    if marzano_level in ['analysis', 'knowledge_utilization']:
                        severity = 'high'
                    else:
                        severity = 'medium'

                    concerns.append({
                        'element': 'scaffolding',
                        'issue': f"Activity '{activity['name']}': Writing task lacks sentence frames or model responses",
                        'severity': severity,
                        'impact': 'Alex may freeze when attempting to produce academic writing without structural support',
                        'evidence': f"Output type: {student_output}, Marzano level: {marzano_level}, No visible scaffolding",
                        'recommendation': {
                            'change': 'Add sentence frames and/or worked example',
                            'rationale': 'Struggling writers need explicit models showing how to structure academic responses',
                            'implementation': 'Provide sentence frames like "The primary source shows ___ because ___" and display one completed example'
                        }
                    })
                elif has_model or has_frames:
                    strengths.append({
                        'element': 'scaffolding',
                        'observation': f"Activity '{activity['name']}' includes scaffolding for writing task",
                        'why_helpful': 'Models and sentence frames give Alex concrete starting points for academic writing'
                    })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_pacing(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check activity pacing against attention span."""
        strengths = []
        concerns = []

        sustained_focus_limit = self.characteristics['attention']['sustained_focus_minutes']

        for activity in lesson.get('activities', []):
            duration = activity.get('duration', 0)

            if duration > sustained_focus_limit:
                severity = self._determine_severity('pacing', duration)

                # Check for explicit break points
                has_breaks = any(word in str(activity).lower() for word in ['break', 'pause', 'transition', 'partner', 'turn and talk'])

                if not has_breaks:
                    concerns.append({
                        'element': 'pacing',
                        'issue': f"Activity '{activity['name']}': {duration} min exceeds Alex's sustained focus limit ({sustained_focus_limit} min) without break points",
                        'severity': severity,
                        'impact': 'Alex\'s attention may wane, leading to incomplete work or behavioral issues',
                        'evidence': f"Duration: {duration} min, no explicit breaks or transitions mentioned",
                        'recommendation': {
                            'change': 'Add explicit break point or partner interaction at 15-minute mark',
                            'rationale': 'Cognitive breaks prevent attention fatigue and allow processing time',
                            'implementation': 'Insert "Pause: Turn and share one observation with your partner" midway through activity'
                        }
                    })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_engagement(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check engagement accessibility."""
        strengths = []
        concerns = []

        # Check for multiple modalities
        activities = lesson.get('activities', [])

        modalities = {
            'visual': False,
            'verbal': False,
            'kinesthetic': False
        }

        for activity in activities:
            activity_str = str(activity).lower()

            if any(word in activity_str for word in ['diagram', 'graphic', 'visual', 'image', 'chart']):
                modalities['visual'] = True
            if any(word in activity_str for word in ['discuss', 'share', 'talk', 'present', 'explain']):
                modalities['verbal'] = True
            if any(word in activity_str for word in ['manipulative', 'hands-on', 'physical', 'movement', 'act out']):
                modalities['kinesthetic'] = True

        active_modalities = sum(modalities.values())

        if active_modalities >= 2:
            strengths.append({
                'element': 'engagement',
                'observation': f"Lesson incorporates {active_modalities} learning modalities",
                'why_helpful': 'Multiple entry points increase engagement for Alex and provide alternative pathways to understanding'
            })
        else:
            concerns.append({
                'element': 'engagement',
                'issue': 'Limited modality variety - primarily single-mode instruction',
                'severity': 'medium',
                'impact': 'Alex may disengage if instruction doesn\'t match preferred learning style',
                'evidence': f"Only {active_modalities} modality detected: {[k for k, v in modalities.items() if v]}",
                'recommendation': {
                    'change': 'Add visual or kinesthetic components to complement verbal instruction',
                    'rationale': 'UDL principles suggest multiple means of representation increase accessibility',
                    'implementation': 'Add graphic organizer (visual) or think-pair-share (kinesthetic/social)'
                }
            })

        return {'strengths': strengths, 'concerns': concerns}

    def calculate_rating(self, concerns: List[Dict]) -> int:
        """
        Calculate 1-5 accessibility rating based on concern count/severity.

        5: No high concerns, <=1 medium
        4: No high concerns, 2-3 medium
        3: 1 high concern OR 4+ medium
        2: 2-3 high concerns
        1: 4+ high concerns
        """
        high_concerns = [c for c in concerns if c.get('severity') == 'high']
        medium_concerns = [c for c in concerns if c.get('severity') == 'medium']

        high_count = len(high_concerns)
        medium_count = len(medium_concerns)

        if high_count >= 4:
            return 1
        elif high_count >= 2:
            return 2
        elif high_count == 1 or medium_count >= 4:
            return 3
        elif medium_count >= 2:
            return 4
        else:
            return 5

    def _determine_severity(self, rule_type: str, value: float) -> str:
        """Determine severity level based on decision rules."""
        thresholds = self.decision_rules.get(rule_type, {}).get('severity_thresholds', {})

        if not thresholds:
            return 'medium'  # Default if no thresholds defined

        # Custom logic per rule type
        if rule_type == 'vocabulary':
            if value >= 3:
                return 'high'
            elif value >= 1:
                return 'medium'
            else:
                return 'low'

        elif rule_type == 'pacing':
            if value >= 30:
                return 'high'
            elif value >= 20:
                return 'medium'
            else:
                return 'low'

        elif rule_type == 'instructions':
            if value >= 5:
                return 'high'
            elif value >= 4:
                return 'medium'
            else:
                return 'low'

        elif rule_type == 'sentence_complexity':
            if value >= 25:
                return 'high'
            elif value >= 20:
                return 'medium'
            else:
                return 'low'

        else:
            return 'medium'

    def _generate_summary(self, rating: int, concerns: List[Dict], strengths: List[Dict]) -> str:
        """Generate overall summary based on rating and feedback."""
        if rating >= 4:
            return f"This lesson is highly accessible for {self.persona_name}. Minor adjustments could further support engagement."
        elif rating == 3:
            return f"This lesson has moderate accessibility for {self.persona_name}. Key revisions recommended to reduce cognitive barriers."
        else:
            return f"This lesson poses significant challenges for {self.persona_name}. Major revisions needed to ensure accessibility."

    def _get_primary_concern(self, concerns: List[Dict]) -> str:
        """Identify the most critical concern."""
        if not concerns:
            return "None - lesson is accessible"

        # Prioritize high severity concerns
        high_concerns = [c for c in concerns if c.get('severity') == 'high']
        if high_concerns:
            return high_concerns[0]['issue']

        # Otherwise return first medium concern
        return concerns[0]['issue']

    def _generate_pedagogical_notes(self, concerns: List[Dict], strengths: List[Dict]) -> Dict[str, Any]:
        """Generate notes about overall difficulty and revision priorities."""
        high_concerns = [c for c in concerns if c.get('severity') == 'high']
        medium_concerns = [c for c in concerns if c.get('severity') == 'medium']

        # Determine overall difficulty
        if len(high_concerns) >= 2:
            difficulty = "Very challenging - multiple significant barriers"
        elif len(high_concerns) == 1:
            difficulty = "Moderately challenging - one significant barrier"
        elif len(medium_concerns) >= 3:
            difficulty = "Moderately accessible - several minor barriers"
        else:
            difficulty = "Highly accessible - minimal barriers"

        # Prioritize revisions
        priority_revisions = []
        if high_concerns:
            priority_revisions = [c['element'] for c in high_concerns[:2]]
        elif medium_concerns:
            priority_revisions = [c['element'] for c in medium_concerns[:2]]

        # What to defer to teacher
        deferred = [
            "Content-specific background knowledge needed",
            "Cultural relevance and student interests",
            "Specific accommodations beyond general scaffolding"
        ]

        return {
            'overall_difficulty': difficulty,
            'priority_revisions': priority_revisions,
            'deferred_to_teacher': deferred
        }


def evaluate_lesson_with_persona(lesson_path: str, persona_path: str, output_path: str) -> Dict[str, Any]:
    """
    Main entry point for evaluating a lesson with a persona.

    Args:
        lesson_path: Path to lesson JSON file
        persona_path: Path to persona definition JSON
        output_path: Path to write feedback JSON

    Returns:
        Feedback dictionary
    """
    # Load lesson and persona
    with open(lesson_path, 'r') as f:
        lesson = json.load(f)

    with open(persona_path, 'r') as f:
        persona = json.load(f)

    # Create evaluator and run evaluation
    evaluator = PersonaEvaluator(persona)
    feedback = evaluator.evaluate_lesson(lesson)

    # Write output
    with open(output_path, 'w') as f:
        json.dump(feedback, f, indent=2)

    return feedback


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Evaluate lesson accessibility using persona-based criteria'
    )
    parser.add_argument('lesson', help='Path to lesson JSON file')
    parser.add_argument('persona', help='Path to persona definition JSON')
    parser.add_argument('output', help='Path to output feedback JSON')

    args = parser.parse_args()

    try:
        feedback = evaluate_lesson_with_persona(args.lesson, args.persona, args.output)

        # Print summary
        print(f"\n{'='*60}")
        print(f"Persona Evaluation: {feedback['persona_name']}")
        print(f"{'='*60}")
        print(f"Lesson: {feedback['lesson_title']}")
        print(f"Rating: {feedback['overall_assessment']['accessibility_rating']}")
        print(f"\nSummary: {feedback['overall_assessment']['summary']}")
        print(f"\nPrimary Concern: {feedback['overall_assessment']['primary_concern']}")
        print(f"\nStrengths: {len(feedback['strengths'])}")
        print(f"Concerns: {len(feedback['concerns'])}")
        print(f"  - High severity: {len([c for c in feedback['concerns'] if c['severity'] == 'high'])}")
        print(f"  - Medium severity: {len([c for c in feedback['concerns'] if c['severity'] == 'medium'])}")
        print(f"  - Low severity: {len([c for c in feedback['concerns'] if c['severity'] == 'low'])}")
        print(f"\nFeedback written to: {args.output}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
