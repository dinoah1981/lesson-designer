"""
Lesson Designer v2 — Claude API Functions
All Claude API interactions: knowledge/skills extraction, lesson planning,
persona feedback, prompt additions, content generation.
"""

import json
from typing import Dict, List, Any, Optional
import anthropic
import streamlit as st

from config import (
    CLAUDE_MODEL,
    CLAUDE_MODEL_LIGHT,
    PERSONAS,
    LESSON_TYPES,
    DISCOVERY_PRINCIPLE,
    MARZANO_SUMMARY,
    MISSION_CONTEXT,
    KNOWLEDGE_SKILLS_SYSTEM_PROMPT,
    LESSON_PLAN_SYSTEM_PROMPT,
    PERSONA_FEEDBACK_SYSTEM_PROMPT,
    PROMPT_ADDITIONS_SYSTEM_PROMPT,
    CONTENT_GENERATION_SYSTEM_PROMPT,
    CONTENT_OUTPUT_FORMAT,
)


def get_client() -> anthropic.Anthropic:
    """Get the Anthropic client using Streamlit secrets."""
    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


def _parse_json(text: str) -> dict:
    """Extract and parse JSON from a Claude response that may contain markdown fences."""
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return json.loads(text.strip())


# ─── 1. Knowledge & Skills Extraction ───────────────────────────────────────────

def extract_knowledge_skills(competency: str, grade_level: str) -> dict:
    """
    Analyze a competency statement and extract underlying knowledge items and skills.
    Returns {"knowledge": [...], "skills": [...]}.
    """
    client = get_client()

    prompt = f"""Analyze this competency statement and extract the underlying knowledge and skills students need.

COMPETENCY: {competency}
GRADE LEVEL: {grade_level}

Extract:
1. **Knowledge items** — Facts, concepts, vocabulary, and information students must KNOW
2. **Skills** — Procedures, processes, and abilities students must be able to DO

Return a JSON object:
{{
    "knowledge": [
        {{
            "id": "k1",
            "item": "The specific knowledge item",
            "category": "vocabulary|concept|fact|principle|text_exposure"
        }}
    ],
    "skills": [
        {{
            "id": "s1",
            "item": "The specific skill",
            "category": "cognitive|procedural|metacognitive"
        }}
    ]
}}

Guidelines:
- Be specific and granular — break down into teachable components
- Typically 4-8 knowledge items and 3-6 skills
- Knowledge = what students need to understand/remember
- Skills = what students need to be able to do/perform

IMPORTANT — English/Language Arts Distinction:
For ELA lessons, distinguish carefully between knowledge (content exposure) and skills:

KNOWLEDGE (category: text_exposure):
- Reading/experiencing a text, poem, novel, article = KNOWLEDGE (exposure to new content)
- Understanding plot, characters, setting = KNOWLEDGE (content comprehension)
- Learning literary terms (metaphor, irony, theme) = KNOWLEDGE (vocabulary/concepts)
- Historical/cultural context of a work = KNOWLEDGE (background information)

SKILLS (what students DO with the knowledge):
- Comparing two texts or characters = SKILL (analysis action)
- Interpreting themes or author's purpose = SKILL (interpretation action)
- Analyzing literary devices and their effects = SKILL (analysis action)
- Constructing arguments with textual evidence = SKILL (synthesis action)
- Writing in response to reading = SKILL (production action)

Simply READING or EXPERIENCING a text is acquiring new KNOWLEDGE. COMPARING, INTERPRETING, ANALYZING, or EVALUATING that text requires SKILLS.

Return ONLY the JSON object."""

    response = client.messages.create(
        model=CLAUDE_MODEL_LIGHT,
        max_tokens=2000,
        system=KNOWLEDGE_SKILLS_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_json(response.content[0].text)


# ─── 2. Lesson Plan Generation ──────────────────────────────────────────────────

def generate_lesson_plan(
    competency: str,
    daily_objectives: List[str],
    lesson_type: str,
    grade_level: str,
    duration: int,
    num_lessons: int,
    knowledge: List[dict],
    skills: List[dict],
    additional_guidance: str = "",
    doc_text: str = "",
) -> str:
    """
    Generate a structured lesson plan based on all Phase 1 inputs.
    Returns the lesson plan as formatted text (not JSON).
    """
    client = get_client()

    lt = LESSON_TYPES[lesson_type]

    # Build the structure description from the lesson type
    structure_lines = []
    for seg in lt["structure"]:
        mins = round(seg["duration_pct"] * duration)
        structure_lines.append(f"- **{seg['segment']}** (~{mins} min): {seg['purpose']}")
    structure_text = "\n".join(structure_lines)

    knowledge_text = "\n".join(f"- {k['item']} ({k['category']})" for k in knowledge)
    skills_text = "\n".join(f"- {s['item']} ({s['category']})" for s in skills)

    doc_section = ""
    if doc_text:
        doc_section = f"\n\nUPLOADED DOCUMENT CONTEXT:\n{doc_text[:8000]}\n"

    guidance_section = ""
    if additional_guidance:
        guidance_section = f"\n\nADDITIONAL TEACHER GUIDANCE:\n{additional_guidance}\n"

    # Format objectives — single or multi-lesson
    if num_lessons == 1:
        objectives_text = f"DAILY OBJECTIVE: {daily_objectives[0]}"
        exit_ticket_line = f'5. Exit ticket that directly assesses the DAILY OBJECTIVE: "{daily_objectives[0]}"'
    else:
        obj_lines = "\n".join(f"  Lesson {i+1}: {obj}" for i, obj in enumerate(daily_objectives[:num_lessons]))
        objectives_text = f"LESSON OBJECTIVES:\n{obj_lines}"
        exit_ticket_line = "5. Each lesson's exit ticket directly assesses THAT LESSON'S specific daily objective"

    prompt = f"""Design a detailed lesson plan for the following:

COMPETENCY: {competency}
{objectives_text}
LESSON TYPE: {lesson_type} — {lt['description']}
GRADE LEVEL: {grade_level}
DURATION: {duration} minutes per lesson
NUMBER OF LESSONS IN SEQUENCE: {num_lessons}

CONFIRMED KNOWLEDGE TO BUILD:
{knowledge_text}

CONFIRMED SKILLS TO DEVELOP:
{skills_text}
{doc_section}{guidance_section}

LESSON TYPE STRUCTURE — Follow this structure for each {lesson_type} lesson:
{structure_text}

{lt['prompt_guidance']}

{MARZANO_SUMMARY}

{"Create a complete, detailed lesson plan" if num_lessons == 1 else f"Create {num_lessons} complete, detailed lesson plans (one per lesson in the sequence). Each lesson should have its own objective and build on the previous lesson."} with:
1. Each segment named, timed, and described with SPECIFIC content (not vague descriptions)
2. Concrete discussion prompts (the actual questions to ask, not "ask questions about X")
3. Specific activity instructions (what students do step by step)
4. Materials referenced by name (worksheet, station cards, data sheet, etc.)
{exit_ticket_line}
6. Vocabulary with student-friendly definitions
7. Teacher notes for each segment (what to watch for, common misconceptions, how to scaffold)

{"Format the plan as a readable document with clear headers and sections." if num_lessons == 1 else "Format EACH lesson plan under its own top-level header: '# Lesson 1', '# Lesson 2', etc. Use ## subheaders within each lesson for segments."} Be specific and detailed — this plan will be used to generate all lesson materials."""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4000 * num_lessons,
        system=LESSON_PLAN_SYSTEM_PROMPT.format(mission_context=MISSION_CONTEXT),
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


# ─── 3. Persona Feedback ────────────────────────────────────────────────────────

def get_persona_feedback(lesson_plan: str, competency: str, daily_objectives: List[str], grade_level: str) -> dict:
    """
    Send the lesson plan to be evaluated by all 4 personas in a single call.
    Returns structured feedback: {"alex": {...}, "jordan": {...}, "maya": {...}, "marcus": {...}}.
    """
    client = get_client()

    # Build persona descriptions for the system prompt
    persona_block = ""
    for key, p in PERSONAS.items():
        persona_block += f"""
### {p['name']} ({p['type']})
{p['profile']}

EVALUATION LENS:
{p['evaluation_lens']}
---
"""

    # Format objectives
    if len(daily_objectives) == 1:
        obj_text = f"DAILY OBJECTIVE: {daily_objectives[0]}"
    else:
        obj_lines = "\n".join(f"  Lesson {i+1}: {obj}" for i, obj in enumerate(daily_objectives))
        obj_text = f"LESSON OBJECTIVES:\n{obj_lines}"

    prompt = f"""Evaluate this lesson plan from the perspective of 4 different student personas.

COMPETENCY: {competency}
{obj_text}
GRADE LEVEL: {grade_level}

LESSON PLAN:
{lesson_plan}

---

For EACH persona below, provide feedback in this exact JSON format:

{{
    "alex": {{
        "reaction": "One sentence authentic reaction in Alex's voice",
        "concerns": [
            {{
                "element": "Which part of the lesson this concern is about",
                "issue": "What the specific concern is",
                "severity": "high|medium|low"
            }}
        ]
    }},
    "jordan": {{
        "reaction": "...",
        "concerns": [...]
    }},
    "maya": {{
        "reaction": "...",
        "concerns": [...]
    }},
    "marcus": {{
        "reaction": "...",
        "concerns": [...]
    }}
}}

PERSONA PROFILES:
{persona_block}

Give 2-3 concerns per persona. Be specific — reference actual lesson segments, activities, or timing. Concerns should be things that would genuinely matter to this student, not generic feedback.

Return ONLY the JSON object."""

    response = client.messages.create(
        model=CLAUDE_MODEL_LIGHT,
        max_tokens=3000,
        system=PERSONA_FEEDBACK_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return _parse_json(response.content[0].text)


# ─── 4. Prompt Additions ────────────────────────────────────────────────────────

def generate_prompt_additions(persona_feedback: dict, lesson_plan: str) -> str:
    """
    Generate editable prompt additions based on persona feedback.
    Returns a bulleted text string the teacher can edit.
    """
    client = get_client()

    # Format the feedback for the prompt
    feedback_text = ""
    for key, fb in persona_feedback.items():
        name = PERSONAS[key]["name"]
        feedback_text += f"\n**{name}** ({PERSONAS[key]['type']}):\n"
        feedback_text += f"Reaction: {fb['reaction']}\n"
        for c in fb.get("concerns", []):
            feedback_text += f"- [{c['severity'].upper()}] {c['element']}: {c['issue']}\n"

    prompt = f"""Based on this persona feedback about a lesson plan, generate concise, actionable additions the teacher should incorporate into the final lesson prompt.

LESSON PLAN:
{lesson_plan}

PERSONA FEEDBACK:
{feedback_text}

Generate 4-8 bullet points. Each should:
- Start with an action verb (Add, Include, Provide, Create, Build, Modify)
- Be specific enough to act on
- Note which persona raised the concern in parentheses
- Only include additions that would meaningfully improve the lesson
- Do NOT repeat things already in the lesson plan

Example format:
- Add a word bank for key vocabulary terms on the worksheet (Alex: vocabulary accessibility)
- Include a real-world connection to current events in the framing (Jordan: relevance)
- Provide an extension question for students who finish early (Marcus: ceiling)

Return ONLY the bullet points, no other text."""

    response = client.messages.create(
        model=CLAUDE_MODEL_LIGHT,
        max_tokens=1000,
        system=PROMPT_ADDITIONS_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text.strip()


# ─── 5. Content Generation ──────────────────────────────────────────────────────

def generate_lesson_content(
    competency: str,
    daily_objectives: List[str],
    lesson_type: str,
    grade_level: str,
    duration: int,
    knowledge: List[dict],
    skills: List[dict],
    lesson_plan: str,
    prompt_additions: str,
    additional_guidance: str = "",
    doc_text: str = "",
    differentiate_struggling: bool = False,
    differentiate_advanced: bool = False,
) -> str:
    """
    The 'big prompt' — generate all structured content blocks for the lesson.
    Returns formatted text with ## headers for each section.
    """
    client = get_client()

    lt = LESSON_TYPES[lesson_type]
    knowledge_text = "\n".join(f"- {k['item']}" for k in knowledge)
    skills_text = "\n".join(f"- {s['item']}" for s in skills)

    doc_section = ""
    if doc_text:
        doc_section = f"\nUPLOADED DOCUMENT CONTEXT (use this content in the lesson):\n{doc_text[:6000]}\n"

    guidance_section = ""
    if additional_guidance:
        guidance_section = f"\nADDITIONAL TEACHER GUIDANCE:\n{additional_guidance}\n"

    diff_section = ""
    if differentiate_struggling:
        diff_section += "\nDIFFERENTIATION — STRUGGLING LEARNERS: Also generate modified content for struggling learners. Include word banks, sentence starters, simplified language, and chunked instructions. Mark this content clearly under a ## Modified Content (Struggling Learners) header.\n"
    if differentiate_advanced:
        diff_section += "\nDIFFERENTIATION — ADVANCED LEARNERS: Also generate extension content for advanced learners. Include deeper analytical questions, research prompts, and open-ended challenges. Mark this content clearly under a ## Extension Content (Advanced Learners) header.\n"

    system = CONTENT_GENERATION_SYSTEM_PROMPT.format(mission_context=MISSION_CONTEXT)
    output_format = CONTENT_OUTPUT_FORMAT.format(discovery_principle=DISCOVERY_PRINCIPLE)

    # Format objectives
    if len(daily_objectives) == 1:
        obj_text = f"DAILY OBJECTIVE: {daily_objectives[0]}"
    else:
        obj_lines = "\n".join(f"  Lesson {i+1}: {obj}" for i, obj in enumerate(daily_objectives))
        obj_text = f"LESSON OBJECTIVES:\n{obj_lines}"

    prompt = f"""Generate complete, structured lesson content for the following lesson.

COMPETENCY: {competency}
{obj_text}
LESSON TYPE: {lesson_type}
GRADE LEVEL: {grade_level}
DURATION: {duration} minutes

KNOWLEDGE TO BUILD:
{knowledge_text}

SKILLS TO DEVELOP:
{skills_text}
{doc_section}{guidance_section}

APPROVED LESSON PLAN:
{lesson_plan}

TEACHER-APPROVED PROMPT ADDITIONS (incorporate all of these):
{prompt_additions}

{lt['prompt_guidance']}

{MARZANO_SUMMARY}
{diff_section}
{output_format}

Generate ALL content blocks now. Remember: you are building the actual physical materials for tomorrow's class. Every slide will be projected to students. Every worksheet will be printed for students to write on. Every station card will be cut out and placed on a table. The ## Lesson Plan is the only section the teacher sees privately — answer keys, timing, and facilitation notes go there and nowhere else.

The ## Worksheet Content section must have ### sub-sections covering every activity where students produce written work. This is the student's primary document for the entire lesson.
{"" if len(daily_objectives) == 1 else f"IMPORTANT: Generate content for ALL {len(daily_objectives)} lessons. Structure your output with a top-level '# Lesson 1', '# Lesson 2', etc. header for each lesson, with the ## content block headers nested within each lesson."}"""

    num = len(daily_objectives)
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8000 * num,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text

