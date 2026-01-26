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
        # Alex (struggling learner) criteria
        self.evaluators = {
            'vocabulary_accessibility': self.evaluate_vocabulary,
            'instruction_clarity': self.evaluate_instructions,
            'scaffolding_adequacy': self.evaluate_scaffolding,
            'pacing_appropriateness': self.evaluate_pacing,
            'engagement_accessibility': self.evaluate_engagement,
            # Jordan (unmotivated capable) criteria
            'task_relevance': self.evaluate_task_relevance,
            'cognitive_challenge': self.evaluate_cognitive_challenge,
            'student_choice': self.evaluate_student_choice,
            'real_world_connection': self.evaluate_real_world_connection,
            'autonomy_opportunities': self.evaluate_autonomy,
            # Maya (interested capable) criteria
            'depth_opportunities': self.evaluate_depth_opportunities,
            'inquiry_support': self.evaluate_inquiry_support,
            'discussion_quality': self.evaluate_discussion_quality,
            'extension_availability': self.evaluate_extension_availability,
            'intellectual_rigor': self.evaluate_intellectual_rigor,
            # Marcus (high achieving) criteria
            'challenge_level': self.evaluate_challenge_level,
            'pacing_flexibility': self.evaluate_pacing_flexibility,
            'abstract_complexity': self.evaluate_abstract_complexity,
            'ceiling_removal': self.evaluate_ceiling_removal,
            'meaningful_work': self.evaluate_meaningful_work
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

    # ============================================================================
    # JORDAN (unmotivated capable) EVALUATION METHODS
    # ============================================================================

    def evaluate_task_relevance(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if activities have clear real-world relevance explanations."""
        strengths = []
        concerns = []

        activities = lesson.get('activities', [])
        relevance_keywords = ['why', 'because', 'real world', 'application', 'career',
                              'life', 'matters', 'important', 'relevant', 'used in',
                              'professionals', 'scientists', 'historians', 'engineers']

        activities_with_relevance = 0
        activities_without_relevance = []

        for activity in activities:
            activity_text = str(activity).lower()
            objective = lesson.get('objective', '').lower()

            has_relevance = any(kw in activity_text or kw in objective for kw in relevance_keywords)

            if has_relevance:
                activities_with_relevance += 1
            else:
                activities_without_relevance.append(activity.get('name', 'Unnamed'))

        # Check objective for test-prep framing (high severity)
        objective = lesson.get('objective', '').lower()
        test_prep_indicators = ['memorize', 'quiz', 'test', 'exam', 'recall', 'remember']
        is_test_prep = any(ind in objective for ind in test_prep_indicators)

        if is_test_prep and activities_with_relevance == 0:
            concerns.append({
                'element': 'task_relevance',
                'issue': 'Lesson framed as test prep with no real-world relevance explanation',
                'severity': 'high',
                'impact': 'Jordan will disengage immediately from work perceived as pointless drill',
                'evidence': f"Objective: '{lesson.get('objective', '')}' - no relevance to student life/future",
                'recommendation': {
                    'change': 'Reframe objective around authentic purpose and add "why this matters" context',
                    'rationale': 'Unmotivated capable students need to see purpose before they invest effort',
                    'implementation': 'Begin lesson with compelling hook showing real-world application of skill'
                }
            })
        elif len(activities_without_relevance) > len(activities) / 2:
            concerns.append({
                'element': 'task_relevance',
                'issue': f'{len(activities_without_relevance)} of {len(activities)} activities lack clear relevance',
                'severity': 'medium',
                'impact': 'Jordan may complete work minimally without understanding why it matters',
                'evidence': f"Activities without clear relevance: {', '.join(activities_without_relevance[:3])}",
                'recommendation': {
                    'change': 'Add explicit "why this matters" explanation to each activity',
                    'rationale': 'Capable but unmotivated students respond to clear purpose statements',
                    'implementation': 'Include 1-2 sentences connecting each task to authentic use or student interests'
                }
            })
        elif activities_with_relevance == len(activities):
            strengths.append({
                'element': 'task_relevance',
                'observation': 'All activities include relevance context',
                'why_helpful': 'Jordan can see the purpose behind each task, maintaining engagement'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_cognitive_challenge(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if activities include higher-order thinking tasks."""
        strengths = []
        concerns = []

        activities = lesson.get('activities', [])
        higher_order_levels = ['analysis', 'knowledge_utilization']
        lower_order_levels = ['retrieval', 'comprehension']

        higher_order_count = 0
        all_retrieval = True

        for activity in activities:
            marzano_level = activity.get('marzano_level', '').lower()
            if marzano_level in higher_order_levels:
                higher_order_count += 1
                all_retrieval = False
            elif marzano_level not in lower_order_levels:
                all_retrieval = False

        if all_retrieval and len(activities) > 0:
            concerns.append({
                'element': 'cognitive_challenge',
                'issue': 'All activities are retrieval/comprehension level - no higher-order thinking required',
                'severity': 'high',
                'impact': 'Jordan will find this intellectually boring and disengage; capable of much more',
                'evidence': f"Marzano levels: {[a.get('marzano_level', 'unknown') for a in activities]}",
                'recommendation': {
                    'change': 'Add analysis or knowledge utilization tasks that challenge capable students',
                    'rationale': 'Above-grade-level students need cognitive challenge to stay engaged',
                    'implementation': 'Replace at least one drill activity with analysis, evaluation, or creation task'
                }
            })
        elif higher_order_count == 0 and len(activities) > 0:
            concerns.append({
                'element': 'cognitive_challenge',
                'issue': 'No analysis or knowledge utilization activities present',
                'severity': 'medium',
                'impact': 'Capable student may coast through without genuine intellectual engagement',
                'evidence': f"All activities at basic levels: {[a.get('marzano_level', 'unknown') for a in activities]}",
                'recommendation': {
                    'change': 'Include at least one higher-order thinking activity',
                    'rationale': 'Capable students need opportunities for deeper cognitive work',
                    'implementation': 'Add activity requiring analysis, synthesis, or application to new contexts'
                }
            })
        elif higher_order_count >= len(activities) / 2:
            strengths.append({
                'element': 'cognitive_challenge',
                'observation': f'{higher_order_count} of {len(activities)} activities require higher-order thinking',
                'why_helpful': 'Jordan has opportunities for genuine intellectual challenge'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_student_choice(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if students have meaningful choices in approach, method, or product."""
        strengths = []
        concerns = []

        choice_keywords = ['choose', 'select', 'option', 'preference', 'decide',
                          'pick', 'alternative', 'or', 'either', 'choice']
        product_choice_keywords = ['presentation', 'poster', 'essay', 'video',
                                   'creative', 'format of your choice']

        lesson_text = str(lesson).lower()

        has_choice = any(kw in lesson_text for kw in choice_keywords)
        has_product_choice = any(kw in lesson_text for kw in product_choice_keywords)

        # Count activities - check if any mention choice
        activities = lesson.get('activities', [])
        activities_with_choice = 0

        for activity in activities:
            activity_text = str(activity).lower()
            if any(kw in activity_text for kw in choice_keywords):
                activities_with_choice += 1

        if not has_choice and not has_product_choice:
            concerns.append({
                'element': 'student_choice',
                'issue': 'No student choice offered in approach, method, or product format',
                'severity': 'high',
                'impact': 'Jordan feels controlled and powerless, reducing motivation to invest effort',
                'evidence': 'Lesson is entirely teacher-directed with single prescribed path',
                'recommendation': {
                    'change': 'Add meaningful choices at one or more points in the lesson',
                    'rationale': 'Choice increases ownership and motivation for capable but resistant learners',
                    'implementation': 'Offer choice in: which text to analyze, how to demonstrate learning, or work grouping'
                }
            })
        elif activities_with_choice == 0 and len(activities) > 1:
            concerns.append({
                'element': 'student_choice',
                'issue': 'Limited choice opportunities within activities',
                'severity': 'medium',
                'impact': 'Student autonomy is constrained; may feel like going through the motions',
                'evidence': 'Activities prescribe single approach without alternatives',
                'recommendation': {
                    'change': 'Embed choice options within individual activities',
                    'rationale': 'Even small choices (which problem to start with, partner vs. solo) increase ownership',
                    'implementation': 'Add "you may choose to..." options or provide 2-3 paths through activities'
                }
            })
        elif has_choice or has_product_choice:
            strengths.append({
                'element': 'student_choice',
                'observation': 'Lesson includes student choice opportunities',
                'why_helpful': 'Jordan can exercise autonomy and approach work in preferred way'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_real_world_connection(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check for authentic contexts and real-world applications."""
        strengths = []
        concerns = []

        real_world_indicators = ['real world', 'authentic', 'professional', 'career',
                                 'workplace', 'scientist', 'historian', 'engineer',
                                 'actual', 'current events', 'news', 'contemporary',
                                 'application', 'scenario', 'case study', 'simulation']

        academic_only_indicators = ['practice', 'drill', 'worksheet', 'textbook',
                                    'exercise', 'problems 1-10', 'complete the']

        lesson_text = str(lesson).lower()

        has_real_world = any(ind in lesson_text for ind in real_world_indicators)
        is_purely_academic = all(ind in lesson_text for ind in academic_only_indicators[:2])

        if not has_real_world and is_purely_academic:
            concerns.append({
                'element': 'real_world_connection',
                'issue': 'Pure academic exercise with no connection to authentic contexts',
                'severity': 'high',
                'impact': 'Jordan sees no point in work disconnected from reality; effort will be minimal',
                'evidence': 'Activities focus on abstract practice without application context',
                'recommendation': {
                    'change': 'Frame activities within authentic scenario or real-world problem',
                    'rationale': 'Capable students engage when they see skills used in actual contexts',
                    'implementation': 'Use case study, simulation, or current events as context for skills practice'
                }
            })
        elif not has_real_world:
            concerns.append({
                'element': 'real_world_connection',
                'issue': 'Weak or missing connection to real-world application',
                'severity': 'medium',
                'impact': 'Student may question relevance; reduced intrinsic motivation',
                'evidence': 'No explicit real-world framing in activities',
                'recommendation': {
                    'change': 'Add explicit connection showing how skills are used outside classroom',
                    'rationale': 'Even brief real-world context increases perceived value',
                    'implementation': 'Include example of professional using this skill or current issue requiring it'
                }
            })
        else:
            strengths.append({
                'element': 'real_world_connection',
                'observation': 'Activities connected to authentic real-world contexts',
                'why_helpful': 'Jordan can see practical value and purpose behind the learning'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_autonomy(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check for flexibility in how and when students work."""
        strengths = []
        concerns = []

        autonomy_indicators = ['self-paced', 'at your own pace', 'when ready',
                               'flexible', 'choose when', 'independent', 'self-directed']
        rigid_indicators = ['everyone', 'all together', 'at the same time', 'wait',
                            'do not move on', 'as a class', 'together we will']

        lesson_text = str(lesson).lower()

        has_autonomy = any(ind in lesson_text for ind in autonomy_indicators)
        is_rigid = any(ind in lesson_text for ind in rigid_indicators)

        # Check instructions for rigidity
        activities = lesson.get('activities', [])
        lockstep_activities = 0

        for activity in activities:
            instructions = activity.get('instructions', [])
            instr_text = ' '.join(instructions).lower()

            if any(ind in instr_text for ind in rigid_indicators):
                lockstep_activities += 1
            elif 'silently' in instr_text and 'independently' in instr_text:
                # Rigid work style but not autonomy per se
                pass

        if lockstep_activities == len(activities) and len(activities) > 0:
            concerns.append({
                'element': 'autonomy_opportunities',
                'issue': 'Rigid lock-step instruction throughout - no flexibility in pacing or approach',
                'severity': 'high',
                'impact': 'Jordan feels controlled; resentment builds when forced to wait or comply',
                'evidence': f'All {len(activities)} activities require uniform pacing and approach',
                'recommendation': {
                    'change': 'Allow flexible pacing and approach within activity boundaries',
                    'rationale': 'Capable students resent being held to pace of whole class',
                    'implementation': 'Provide clear goals but allow students to determine how/when to complete'
                }
            })
        elif not has_autonomy and is_rigid:
            concerns.append({
                'element': 'autonomy_opportunities',
                'issue': 'Limited autonomy - mostly teacher-controlled pacing and structure',
                'severity': 'medium',
                'impact': 'Student agency restricted; may comply minimally without investment',
                'evidence': 'Instructions emphasize whole-class timing and uniform approach',
                'recommendation': {
                    'change': 'Build in opportunities for student control over work process',
                    'rationale': 'Autonomy increases ownership and reduces resistance',
                    'implementation': 'Offer choice in work order, grouping, or timing within activity'
                }
            })
        elif has_autonomy:
            strengths.append({
                'element': 'autonomy_opportunities',
                'observation': 'Lesson includes opportunities for student autonomy',
                'why_helpful': 'Jordan can exercise agency over learning process'
            })

        return {'strengths': strengths, 'concerns': concerns}

    # ============================================================================
    # MAYA (interested capable) EVALUATION METHODS
    # ============================================================================

    def evaluate_depth_opportunities(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check for opportunities to explore content more deeply."""
        strengths = []
        concerns = []

        depth_indicators = ['explore', 'investigate', 'deeper', 'further', 'extend',
                            'beyond', 'additional', 'multiple perspectives', 'complexity',
                            'nuance', 'implications', 'connections', 'why might']

        single_answer_indicators = ['correct answer', 'the answer is', 'right answer',
                                    'match each', 'fill in', 'complete the blank']

        lesson_text = str(lesson).lower()

        has_depth = any(ind in lesson_text for ind in depth_indicators)
        is_single_answer = any(ind in lesson_text for ind in single_answer_indicators)

        # Check activities for open-ended vs. closed tasks
        activities = lesson.get('activities', [])
        closed_tasks = 0

        for activity in activities:
            output = activity.get('student_output', '').lower()
            if any(term in output for term in ['matching', 'filled worksheet', 'completed worksheet', 'copied']):
                closed_tasks += 1

        if closed_tasks == len(activities) and len(activities) > 0:
            concerns.append({
                'element': 'depth_opportunities',
                'issue': 'All tasks are closed-ended with single correct answers - no room for depth',
                'severity': 'high',
                'impact': 'Maya will be frustrated by lack of intellectual exploration opportunities',
                'evidence': f'All {len(activities)} outputs are closed tasks: {[a.get("student_output", "") for a in activities]}',
                'recommendation': {
                    'change': 'Add at least one open-ended task allowing deeper exploration',
                    'rationale': 'Curious, capable students need outlets for genuine inquiry',
                    'implementation': 'Include analysis, comparison, or "what if" exploration task'
                }
            })
        elif not has_depth and is_single_answer:
            concerns.append({
                'element': 'depth_opportunities',
                'issue': 'Limited opportunities for deeper exploration beyond basic content',
                'severity': 'medium',
                'impact': 'Maya may complete work quickly but feel intellectually unsatisfied',
                'evidence': 'Tasks focus on correct answers without paths to deeper understanding',
                'recommendation': {
                    'change': 'Add explicit "go deeper" options or extension questions',
                    'rationale': 'Interested students benefit from structured paths to deeper content',
                    'implementation': 'Include "for further exploration" questions or resources'
                }
            })
        elif has_depth:
            strengths.append({
                'element': 'depth_opportunities',
                'observation': 'Lesson includes opportunities for deeper exploration',
                'why_helpful': 'Maya can pursue genuine intellectual curiosity within the lesson'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_inquiry_support(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if student-generated questions are encouraged and structured."""
        strengths = []
        concerns = []

        inquiry_indicators = ['what questions', 'wonder', 'curious', 'your questions',
                              'generate questions', 'inquiry', 'investigate', 'research question',
                              'what would you like to know', 'what do you wonder']

        lesson_text = str(lesson).lower()

        has_inquiry = any(ind in lesson_text for ind in inquiry_indicators)

        # Check activities for question opportunities
        activities = lesson.get('activities', [])
        question_activities = 0

        for activity in activities:
            activity_text = str(activity).lower()
            if any(ind in activity_text for ind in inquiry_indicators):
                question_activities += 1

        if not has_inquiry and question_activities == 0:
            concerns.append({
                'element': 'inquiry_support',
                'issue': 'No opportunities for student-generated questions or inquiry',
                'severity': 'high',
                'impact': 'Maya\'s natural curiosity has no outlet; learning feels passive and receptive',
                'evidence': 'Lesson is entirely teacher-directed with no question generation',
                'recommendation': {
                    'change': 'Add structured opportunity for students to generate their own questions',
                    'rationale': 'Curious students learn better when pursuing their own questions',
                    'implementation': 'Include QFT (Question Formulation Technique) or "What do you wonder?" protocol'
                }
            })
        elif not has_inquiry:
            concerns.append({
                'element': 'inquiry_support',
                'issue': 'Limited inquiry support - questions not explicitly encouraged',
                'severity': 'medium',
                'impact': 'Maya may have questions but no clear path to pursue them',
                'evidence': 'No explicit question generation or inquiry protocols in lesson',
                'recommendation': {
                    'change': 'Add "what questions do you have?" checkpoints throughout lesson',
                    'rationale': 'Acknowledging student questions validates curiosity',
                    'implementation': 'Build in 2-3 minute "parking lot" or question collection moments'
                }
            })
        else:
            strengths.append({
                'element': 'inquiry_support',
                'observation': 'Lesson explicitly encourages student-generated questions',
                'why_helpful': 'Maya can pursue authentic curiosity and self-directed inquiry'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_discussion_quality(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check for substantive peer-to-peer academic discourse opportunities."""
        strengths = []
        concerns = []

        discussion_indicators = ['discuss', 'debate', 'share ideas', 'partner talk',
                                 'group discussion', 'seminar', 'build on', 'respond to',
                                 'agree or disagree', 'perspective', 'argue', 'defend']
        shallow_collab = ['share answers', 'check with partner', 'compare answers', 'quiz each other']

        lesson_text = str(lesson).lower()

        has_discussion = any(ind in lesson_text for ind in discussion_indicators)
        is_shallow = any(ind in lesson_text for ind in shallow_collab)

        # Check activities for discussion components
        activities = lesson.get('activities', [])
        no_collab_count = 0

        for activity in activities:
            activity_text = str(activity).lower()
            has_collab = any(ind in activity_text for ind in discussion_indicators + shallow_collab)
            if not has_collab:
                no_collab_count += 1

        if no_collab_count == len(activities) and len(activities) > 0:
            concerns.append({
                'element': 'discussion_quality',
                'issue': 'No collaborative or discussion components - entirely individual work',
                'severity': 'high',
                'impact': 'Maya values peer interaction and loses opportunity to deepen understanding through discourse',
                'evidence': f'All {len(activities)} activities are individual work with no discussion',
                'recommendation': {
                    'change': 'Add substantive discussion component to at least one activity',
                    'rationale': 'Academic discourse deepens understanding and engages social learners',
                    'implementation': 'Include think-pair-share, Socratic seminar, or structured academic controversy'
                }
            })
        elif is_shallow and not has_discussion:
            concerns.append({
                'element': 'discussion_quality',
                'issue': 'Discussion present but shallow - sharing answers rather than building ideas',
                'severity': 'medium',
                'impact': 'Maya wants intellectual discourse, not just answer checking',
                'evidence': 'Collaboration limited to answer comparison rather than idea development',
                'recommendation': {
                    'change': 'Deepen discussion prompts to push thinking beyond answer sharing',
                    'rationale': 'Substantive discourse requires prompts that invite multiple perspectives',
                    'implementation': 'Use prompts like "What would you add to that idea?" or "What\'s another perspective?"'
                }
            })
        elif has_discussion:
            strengths.append({
                'element': 'discussion_quality',
                'observation': 'Lesson includes substantive discussion opportunities',
                'why_helpful': 'Maya can engage in meaningful academic discourse with peers'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_extension_availability(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check for meaningful extension paths for advanced or interested students."""
        strengths = []
        concerns = []

        extension_indicators = ['extension', 'challenge', 'if you finish', 'go further',
                                'advanced', 'bonus', 'deeper dive', 'optional', 'enrichment']

        lesson_text = str(lesson).lower()

        has_extensions = any(ind in lesson_text for ind in extension_indicators)

        # Check if all students do identical work
        activities = lesson.get('activities', [])
        differentiated = False

        for activity in activities:
            if 'differentiation' in str(activity).lower() or 'extension' in str(activity).lower():
                differentiated = True
                break

        if not has_extensions and not differentiated:
            concerns.append({
                'element': 'extension_availability',
                'issue': 'No extension or advanced paths - all students do identical work',
                'severity': 'high',
                'impact': 'Maya finishes quickly and has nothing meaningful to pursue',
                'evidence': 'No differentiation or extension options mentioned in any activity',
                'recommendation': {
                    'change': 'Add intellectually rich extension options for students who finish early or want more',
                    'rationale': 'Interested students need pathways to deeper or broader exploration',
                    'implementation': 'Include "take it further" options with genuinely advanced work, not just more of the same'
                }
            })
        elif has_extensions:
            # Check if extensions are meaningful or just "more work"
            more_of_same = ['more problems', 'additional practice', 'extra worksheet']
            is_busywork = any(ind in lesson_text for ind in more_of_same)

            if is_busywork:
                concerns.append({
                    'element': 'extension_availability',
                    'issue': 'Extensions feel like busywork - more of the same rather than deeper work',
                    'severity': 'low',
                    'impact': 'Maya sees through surface-level extensions; wants genuine intellectual challenge',
                    'evidence': 'Extensions are quantitative (more problems) rather than qualitative (deeper thinking)',
                    'recommendation': {
                        'change': 'Replace "more of same" extensions with genuinely advanced tasks',
                        'rationale': 'Quality extensions offer vertical growth, not horizontal repetition',
                        'implementation': 'Extensions should require new thinking, not just more time'
                    }
                })
            else:
                strengths.append({
                    'element': 'extension_availability',
                    'observation': 'Lesson includes meaningful extension opportunities',
                    'why_helpful': 'Maya has paths to pursue deeper learning when ready'
                })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_intellectual_rigor(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check for appropriate cognitive complexity and demand."""
        strengths = []
        concerns = []

        activities = lesson.get('activities', [])
        higher_order_levels = ['analysis', 'knowledge_utilization']

        higher_order_count = 0
        only_retrieval = True

        for activity in activities:
            marzano_level = activity.get('marzano_level', '').lower()
            if marzano_level in higher_order_levels:
                higher_order_count += 1
                only_retrieval = False
            elif marzano_level and marzano_level not in ['retrieval', 'comprehension']:
                only_retrieval = False

        if only_retrieval and len(activities) > 0:
            concerns.append({
                'element': 'intellectual_rigor',
                'issue': 'Only retrieval/comprehension tasks - insufficient intellectual rigor',
                'severity': 'high',
                'impact': 'Maya is intellectually capable of much more; lesson feels dumbed down',
                'evidence': f'All activities at basic cognitive levels: {[a.get("marzano_level", "unknown") for a in activities]}',
                'recommendation': {
                    'change': 'Add analysis, evaluation, or creation tasks requiring deeper thinking',
                    'rationale': 'Capable, interested students need cognitive challenge to stay engaged',
                    'implementation': 'Include tasks requiring comparison, synthesis, argument, or original thought'
                }
            })
        elif higher_order_count == 0 and len(activities) > 0:
            concerns.append({
                'element': 'intellectual_rigor',
                'issue': 'Lacking higher-order thinking activities',
                'severity': 'medium',
                'impact': 'Maya may find work routine; insufficient intellectual stimulation',
                'evidence': 'No analysis or knowledge utilization activities present',
                'recommendation': {
                    'change': 'Add at least one genuinely rigorous thinking task',
                    'rationale': 'Interested students want to think hard, not just complete tasks',
                    'implementation': 'Include open-ended analysis or evaluation activity'
                }
            })
        elif higher_order_count >= 2:
            strengths.append({
                'element': 'intellectual_rigor',
                'observation': f'{higher_order_count} activities require higher-order thinking',
                'why_helpful': 'Maya has opportunities for genuine intellectual engagement'
            })

        return {'strengths': strengths, 'concerns': concerns}

    # ============================================================================
    # MARCUS (high achieving) EVALUATION METHODS
    # ============================================================================

    def evaluate_challenge_level(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if tasks are appropriately challenging for gifted learners."""
        strengths = []
        concerns = []

        activities = lesson.get('activities', [])
        grade_level = lesson.get('grade_level', 10)

        # Check for advanced options
        advanced_indicators = ['advanced', 'challenge', 'gifted', 'extension',
                               'above grade level', 'accelerated', 'honors']

        lesson_text = str(lesson).lower()
        has_advanced = any(ind in lesson_text for ind in advanced_indicators)

        # Check Marzano levels for challenge
        all_basic = True
        for activity in activities:
            marzano_level = activity.get('marzano_level', '').lower()
            if marzano_level in ['analysis', 'knowledge_utilization']:
                all_basic = False
                break

        if all_basic and not has_advanced and len(activities) > 0:
            concerns.append({
                'element': 'challenge_level',
                'issue': 'All tasks at or below grade level with no advanced options',
                'severity': 'high',
                'impact': 'Marcus will master content in minutes and have nothing appropriate to do',
                'evidence': f'Grade {grade_level} lesson with no above-level paths or advanced tasks',
                'recommendation': {
                    'change': 'Add above-grade-level options or open-ended advanced challenges',
                    'rationale': 'Gifted students (3+ years ahead) need qualitatively different work',
                    'implementation': 'Include tasks requiring synthesis, creation, or application to complex scenarios'
                }
            })
        elif not has_advanced:
            concerns.append({
                'element': 'challenge_level',
                'issue': 'Challenge level may be insufficient for significantly advanced learners',
                'severity': 'medium',
                'impact': 'Marcus may find standard tasks too easy; potential for boredom',
                'evidence': 'No explicit advanced or accelerated options mentioned',
                'recommendation': {
                    'change': 'Add genuinely challenging options for highly capable students',
                    'rationale': 'Different work (not more work) keeps gifted students engaged',
                    'implementation': 'Create parallel advanced track or open-ended challenge problems'
                }
            })
        else:
            strengths.append({
                'element': 'challenge_level',
                'observation': 'Lesson includes advanced or challenging options',
                'why_helpful': 'Marcus has access to appropriately challenging work'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_pacing_flexibility(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if gifted students can move ahead or compact curriculum."""
        strengths = []
        concerns = []

        flexibility_indicators = ['self-paced', 'when ready', 'move ahead', 'compact',
                                  'pre-test', 'test out', 'accelerate', 'skip if mastered']
        lockstep_indicators = ['everyone', 'all together', 'wait', 'as a class',
                               'do not move on', 'together we will', 'whole class']

        lesson_text = str(lesson).lower()

        has_flexibility = any(ind in lesson_text for ind in flexibility_indicators)
        is_lockstep = any(ind in lesson_text for ind in lockstep_indicators)

        # Check activities for rigid timing
        activities = lesson.get('activities', [])
        rigid_count = 0

        for activity in activities:
            instr_text = ' '.join(activity.get('instructions', [])).lower()
            if any(ind in instr_text for ind in lockstep_indicators):
                rigid_count += 1

        if is_lockstep and not has_flexibility:
            concerns.append({
                'element': 'pacing_flexibility',
                'issue': 'Lock-step instruction - gifted students must move at whole-class pace',
                'severity': 'high',
                'impact': 'Marcus will wait through 80% of class; time wasted on already-mastered content',
                'evidence': f'Lesson emphasizes whole-class timing; {rigid_count} activities are lock-step',
                'recommendation': {
                    'change': 'Add pre-assessment and allow content compacting or acceleration',
                    'rationale': 'Gifted students shouldn\'t practice what they\'ve already mastered',
                    'implementation': 'Include pre-test option or "if you\'ve mastered X, proceed to Y" pathway'
                }
            })
        elif not has_flexibility:
            concerns.append({
                'element': 'pacing_flexibility',
                'issue': 'Limited pacing flexibility for students who master content quickly',
                'severity': 'medium',
                'impact': 'Marcus may finish early and wait; no option to move to advanced content',
                'evidence': 'No explicit curriculum compacting or acceleration options',
                'recommendation': {
                    'change': 'Build in flexible pacing for students who demonstrate early mastery',
                    'rationale': 'Respecting gifted students\' time shows they are valued',
                    'implementation': 'Create "early finisher" pathway to substantively different work'
                }
            })
        else:
            strengths.append({
                'element': 'pacing_flexibility',
                'observation': 'Lesson includes pacing flexibility for advanced learners',
                'why_helpful': 'Marcus can move through mastered content efficiently'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_abstract_complexity(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check for theoretical or abstract extensions beyond concrete examples."""
        strengths = []
        concerns = []

        abstract_indicators = ['theory', 'theoretical', 'abstract', 'principle',
                               'generalize', 'pattern', 'framework', 'model',
                               'hypothesis', 'implications', 'derive', 'prove']
        concrete_only = ['example', 'practice', 'apply to', 'worksheet', 'fill in']

        lesson_text = str(lesson).lower()

        has_abstract = any(ind in lesson_text for ind in abstract_indicators)
        is_only_concrete = sum(1 for ind in concrete_only if ind in lesson_text) >= 3

        if not has_abstract and is_only_concrete:
            concerns.append({
                'element': 'abstract_complexity',
                'issue': 'Lesson is exclusively concrete - no theoretical or abstract extension',
                'severity': 'high',
                'impact': 'Marcus excels at abstract reasoning; missing opportunity for appropriate challenge',
                'evidence': 'All activities focus on concrete examples and practice without abstraction',
                'recommendation': {
                    'change': 'Add theoretical framework or abstract generalization opportunity',
                    'rationale': 'Gifted students can and should engage with underlying principles',
                    'implementation': 'Include task requiring generalization, pattern identification, or theory building'
                }
            })
        elif not has_abstract:
            concerns.append({
                'element': 'abstract_complexity',
                'issue': 'Limited abstract or theoretical content for advanced reasoners',
                'severity': 'medium',
                'impact': 'Marcus\'s abstract reasoning abilities underutilized',
                'evidence': 'Lesson stays close to concrete examples without theoretical extension',
                'recommendation': {
                    'change': 'Add "big picture" or theoretical extension for interested students',
                    'rationale': 'Abstract thinkers benefit from seeing underlying patterns and principles',
                    'implementation': 'Include optional theoretical framework or "what\'s the general principle?" discussion'
                }
            })
        else:
            strengths.append({
                'element': 'abstract_complexity',
                'observation': 'Lesson includes abstract or theoretical components',
                'why_helpful': 'Marcus can engage at appropriate level of abstraction'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_ceiling_removal(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if tasks allow unlimited exploration vs. capped expectations."""
        strengths = []
        concerns = []

        open_ceiling = ['explore further', 'no limit', 'as far as', 'unlimited',
                        'pursue your own', 'independent research', 'go beyond', 'open-ended']
        capped = ['complete these', 'answer all', 'finish the', 'problems 1-',
                  'do not go beyond', 'stop when', 'just the required']

        lesson_text = str(lesson).lower()

        has_open_ceiling = any(ind in lesson_text for ind in open_ceiling)
        is_capped = any(ind in lesson_text for ind in capped)

        # Check activities for fixed vs. open tasks
        activities = lesson.get('activities', [])
        fixed_task_count = 0

        for activity in activities:
            output = activity.get('student_output', '').lower()
            if any(term in output for term in ['completed worksheet', 'filled', 'answers to', 'matching']):
                fixed_task_count += 1

        if fixed_task_count == len(activities) and len(activities) > 0:
            concerns.append({
                'element': 'ceiling_removal',
                'issue': 'All tasks have fixed endpoints - no option for deeper/broader exploration',
                'severity': 'high',
                'impact': 'Marcus hits ceiling quickly; prevented from pursuing genuine challenge',
                'evidence': f'All {len(activities)} tasks are bounded: {[a.get("student_output", "") for a in activities]}',
                'recommendation': {
                    'change': 'Add at least one open-ended task with no upper limit',
                    'rationale': 'Gifted students need permission to exceed expectations',
                    'implementation': 'Include research project, open investigation, or "how far can you take this?" challenge'
                }
            })
        elif is_capped and not has_open_ceiling:
            concerns.append({
                'element': 'ceiling_removal',
                'issue': 'Tasks have capped expectations without pathways to exceed',
                'severity': 'medium',
                'impact': 'Marcus completes required work but has nowhere meaningful to go next',
                'evidence': 'Fixed task requirements without explicit "go further" options',
                'recommendation': {
                    'change': 'Add explicit ceiling-removal opportunities',
                    'rationale': 'Gifted students should never be told "that\'s enough"',
                    'implementation': 'Include "for those who want more" paths with genuine intellectual depth'
                }
            })
        elif has_open_ceiling:
            strengths.append({
                'element': 'ceiling_removal',
                'observation': 'Lesson includes open-ended exploration opportunities',
                'why_helpful': 'Marcus can pursue learning without artificial limits'
            })

        return {'strengths': strengths, 'concerns': concerns}

    def evaluate_meaningful_work(self, lesson: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """Check if work is substantive vs. repetitive drill for mastery students."""
        strengths = []
        concerns = []

        repetitive_indicators = ['practice', 'drill', 'repeat', 'again', 'more problems',
                                 'additional practice', 'keep practicing', 'worksheet',
                                 'copy', 'memorize']
        meaningful_indicators = ['create', 'design', 'develop', 'investigate', 'analyze',
                                 'original', 'novel', 'synthesis', 'evaluate', 'argue']

        lesson_text = str(lesson).lower()

        has_meaningful = any(ind in lesson_text for ind in meaningful_indicators)
        is_repetitive = sum(1 for ind in repetitive_indicators if ind in lesson_text) >= 3

        # Check activities for repetitive vs. substantive work
        activities = lesson.get('activities', [])
        drill_activities = 0

        for activity in activities:
            desc = activity.get('description', '').lower()
            activity_type = activity.get('type', '').lower()

            if any(term in desc for term in ['copy', 'memorize', 'drill', 'practice']):
                drill_activities += 1
            elif activity_type == 'practice' and 'apply' not in desc:
                drill_activities += 1

        if drill_activities >= len(activities) / 2 and len(activities) > 0:
            concerns.append({
                'element': 'meaningful_work',
                'issue': 'Majority of work is repetitive practice - meaningless for students who\'ve mastered content',
                'severity': 'high',
                'impact': 'Marcus already understands this; repetition is punishment, not learning',
                'evidence': f'{drill_activities} of {len(activities)} activities are drill/practice: {[a.get("description", "")[:50] for a in activities]}',
                'recommendation': {
                    'change': 'Replace repetitive practice with substantive intellectual work for mastery students',
                    'rationale': 'Different work (not more work) - gifted students need challenge, not repetition',
                    'implementation': 'Offer application to complex scenario, creation task, or analysis instead of drill'
                }
            })
        elif is_repetitive and not has_meaningful:
            concerns.append({
                'element': 'meaningful_work',
                'issue': 'Work is primarily repetitive with limited substantive intellectual tasks',
                'severity': 'medium',
                'impact': 'Marcus may see work as busywork; effort investment decreases',
                'evidence': 'Activities emphasize practice and repetition over creation and analysis',
                'recommendation': {
                    'change': 'Add genuinely substantive work options for advanced students',
                    'rationale': 'Gifted students need intellectual substance, not quantity',
                    'implementation': 'Include fewer problems but with greater complexity and depth'
                }
            })
        elif has_meaningful:
            strengths.append({
                'element': 'meaningful_work',
                'observation': 'Lesson includes substantive intellectual work beyond drill',
                'why_helpful': 'Marcus has access to genuinely meaningful learning experiences'
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
