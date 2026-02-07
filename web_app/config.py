"""
Lesson Designer v2 — Configuration
Personas, lesson type structures, system prompts, Discovery Principle, branding constants.
"""

# ─── Branding ───────────────────────────────────────────────────────────────────

DARK_GREEN = "#00582c"
LIGHT_GREEN = "#4DAE58"
WHITE = "#FFFFFF"
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# ─── Persona Definitions ────────────────────────────────────────────────────────

PERSONAS = {
    "alex": {
        "name": "Alex",
        "type": "Struggling Learner / ELL",
        "icon": "📚",
        "description": "8th-grade student reading 2–3 years below grade level with limited academic vocabulary.",
        "focus_areas": [
            "vocabulary accessibility",
            "instruction clarity",
            "scaffolding adequacy",
            "pacing appropriateness",
            "engagement accessibility",
        ],
        "profile": (
            "Alex reads at a 5th–6th grade level, struggles with academic (Tier 2) and domain-specific "
            "(Tier 3) vocabulary, has a sustained attention span of about 20 minutes, can handle at most "
            "3-step instructions without a checklist, and needs explicit definitions, visual supports, "
            "sentence frames, graphic organizers, and worked examples."
        ),
        "evaluation_lens": (
            "Look at this lesson through Alex's eyes. Flag:\n"
            "- Academic or domain terms used without explicit definitions or visual support\n"
            "- Activities longer than 20 min without clear break points\n"
            "- Writing/speaking tasks without models or sentence frames\n"
            "- Instructions with more than 3 steps and no visual checklist\n"
            "- Dense text or long sentences (averaging >20 words per sentence)"
        ),
    },
    "jordan": {
        "name": "Jordan",
        "type": "Unmotivated but Capable",
        "icon": "🎧",
        "description": "10th-grade student with above-grade-level ability but low engagement — needs to see why it matters.",
        "focus_areas": [
            "task relevance",
            "cognitive challenge",
            "student choice",
            "real-world connection",
            "autonomy opportunities",
        ],
        "profile": (
            "Jordan is a 10th grader performing at a 12th-grade cognitive level but exerts minimum effort "
            "when content feels irrelevant. Zero tolerance for busywork. Responds to real-world connections, "
            "student choice, and autonomy. Quality of work is high when interested, low when not."
        ),
        "evaluation_lens": (
            "Look at this lesson through Jordan's eyes. Flag:\n"
            "- Activities with no clear real-world connection or relevance to student life\n"
            "- Tasks below grade level or lacking intellectual depth\n"
            "- No opportunities for student choice in approach, method, or product format\n"
            "- Pure academic exercises with no authentic context\n"
            "- Rigid pacing where everyone does the exact same thing at the exact same time"
        ),
    },
    "maya": {
        "name": "Maya",
        "type": "Interested & Capable",
        "icon": "🔬",
        "description": "11th-grade student with strong skills and genuine curiosity — seeks depth, inquiry, and exploration.",
        "focus_areas": [
            "depth opportunities",
            "inquiry support",
            "discussion quality",
            "extension availability",
            "intellectual rigor",
        ],
        "profile": (
            "Maya is an 11th grader reading above grade level with high intrinsic motivation and curiosity. "
            "She participates actively, asks questions, goes beyond requirements, and gets frustrated by "
            "surface-level work. She thrives on inquiry, discussion, and research opportunities."
        ),
        "evaluation_lens": (
            "Look at this lesson through Maya's eyes. Flag:\n"
            "- Surface-level content with no opportunity for deeper exploration\n"
            "- Lessons that don't encourage student-generated questions or lines of inquiry\n"
            "- No collaborative or substantive peer-to-peer discussion components\n"
            "- No meaningful extension paths beyond the basics\n"
            "- Activities below students' intellectual capacity or lacking cognitive complexity"
        ),
    },
    "marcus": {
        "name": "Marcus",
        "type": "High Achieving / Gifted",
        "icon": "🚀",
        "description": "9th-grade gifted student who quickly masters grade-level content and needs advanced challenges.",
        "focus_areas": [
            "challenge level",
            "pacing flexibility",
            "abstract complexity",
            "ceiling removal",
            "meaningful work",
        ],
        "profile": (
            "Marcus is a 9th grader performing 3+ years above grade level with rapid mastery, advanced "
            "reasoning, and exceptional pattern recognition. He disengages when bored, is frustrated by "
            "repetition, and needs different (not just more) work. Prefers autonomy and abstract concepts."
        ),
        "evaluation_lens": (
            "Look at this lesson through Marcus's eyes. Flag:\n"
            "- Tasks that are too easy or lack cognitive demand for gifted learners\n"
            "- Rigid pacing that forces gifted students to wait or repeat mastered content\n"
            "- Lessons that are exclusively concrete with no abstract or theoretical extension\n"
            "- Fixed tasks with capped expectations that prevent unlimited exploration\n"
            "- Repetitive practice or busywork without substantive new intellectual work"
        ),
    },
}

# ─── Lesson Type Structures ─────────────────────────────────────────────────────

LESSON_TYPES = {
    "Introducing New Knowledge": {
        "key": "introducing",
        "description": "First exposure to new concepts, vocabulary, or content. More teacher support, scaffolded exploration.",
        "structure": [
            {"segment": "Do Now", "duration_pct": 0.10, "purpose": "Activate prior knowledge or surface misconceptions related to the new content."},
            {"segment": "Framing", "duration_pct": 0.06, "purpose": "Hook students with a compelling question, scenario, or connection. Frame the day's objective."},
            {"segment": "Core Content / Direct Instruction", "duration_pct": 0.30, "purpose": "Introduce new knowledge through teacher-led instruction with checks for understanding. Use visuals, models, and examples."},
            {"segment": "Guided Practice / Exploration", "duration_pct": 0.30, "purpose": "Students work with the new content in a scaffolded way — graphic organizers, partner work, structured exploration."},
            {"segment": "Discussion", "duration_pct": 0.10, "purpose": "Whole-class or small-group discussion connecting the new content to a bigger idea or question."},
            {"segment": "Exit Ticket", "duration_pct": 0.14, "purpose": "Brief individual assessment of the daily objective."},
        ],
        "prompt_guidance": (
            "This is an INTRODUCING lesson — students are encountering this content for the first time. "
            "Prioritize clarity, scaffolding, and building conceptual understanding. Use concrete examples "
            "before abstract principles. Include vocabulary support. The core activity should be scaffolded "
            "(graphic organizers, partner work, guided exploration) rather than fully independent."
        ),
    },
    "Deepening Through Application": {
        "key": "deepening",
        "description": "Building fluency through guided then independent practice. Applying concepts learned previously.",
        "structure": [
            {"segment": "Do Now", "duration_pct": 0.10, "purpose": "Retrieval practice on previously introduced knowledge/skills."},
            {"segment": "Framing", "duration_pct": 0.06, "purpose": "Connect today's deeper work to the foundational knowledge. Frame how today builds on prior learning."},
            {"segment": "Guided Practice", "duration_pct": 0.20, "purpose": "Teacher-guided application with modeling. Work through examples together."},
            {"segment": "Independent / Group Application", "duration_pct": 0.35, "purpose": "Students apply concepts with increasing independence. Error analysis, pattern recognition, case studies."},
            {"segment": "Share & Discuss", "duration_pct": 0.15, "purpose": "Students share findings, compare approaches, and discuss patterns or insights."},
            {"segment": "Exit Ticket", "duration_pct": 0.14, "purpose": "Assessment that requires application, not just recall."},
        ],
        "prompt_guidance": (
            "This is a DEEPENING lesson — students have been introduced to this content and are now building "
            "fluency. Emphasize application over explanation. Include error analysis or pattern recognition. "
            "Move from guided to independent practice. Discussion should push students to articulate their "
            "thinking and compare approaches."
        ),
    },
    "Synthesis & Application": {
        "key": "synthesis",
        "description": "Connecting ideas across concepts, analyzing patterns, higher-order thinking, authentic problem-solving.",
        "structure": [
            {"segment": "Do Now", "duration_pct": 0.10, "purpose": "Quick retrieval that activates multiple prior concepts needed for synthesis."},
            {"segment": "Framing", "duration_pct": 0.06, "purpose": "Pose the synthesis question or authentic problem. Frame how different pieces connect."},
            {"segment": "Synthesis Activity", "duration_pct": 0.45, "purpose": "Major group or individual task requiring students to connect multiple concepts, analyze complex scenarios, or solve authentic problems. This is the heart of the lesson."},
            {"segment": "Debrief & Discussion", "duration_pct": 0.25, "purpose": "Rich discussion connecting student work to bigger ideas. Gallery walk, presentations, or Socratic discussion."},
            {"segment": "Exit Ticket", "duration_pct": 0.14, "purpose": "Assessment requiring synthesis or transfer, not just recall."},
        ],
        "prompt_guidance": (
            "This is a SYNTHESIS lesson — students are connecting multiple ideas and applying them to complex "
            "or authentic problems. The core activity should be substantial and require higher-order thinking. "
            "Discussion should be rich and student-driven. Provide enough raw material (data, cases, sources) "
            "for students to work with, following the Discovery Principle."
        ),
    },
    "Review": {
        "key": "review",
        "description": "Consolidating learning through retrieval practice, self-assessment, and performance tasks.",
        "structure": [
            {"segment": "Do Now", "duration_pct": 0.10, "purpose": "Retrieval practice covering key concepts from the unit."},
            {"segment": "Framing", "duration_pct": 0.06, "purpose": "Frame the review purpose — what are we consolidating and why? Self-assessment opportunity."},
            {"segment": "Retrieval / Review Activities", "duration_pct": 0.35, "purpose": "Structured review activities: retrieval practice, sorting, matching, or low-stakes quizzing. Mix of individual and partner work."},
            {"segment": "Application / Performance Task", "duration_pct": 0.30, "purpose": "Apply consolidated knowledge to a performance task or authentic scenario."},
            {"segment": "Reflection & Exit", "duration_pct": 0.19, "purpose": "Student self-assessment: what do I know well vs. what do I need to review? Exit ticket on key concepts."},
        ],
        "prompt_guidance": (
            "This is a REVIEW lesson — students are consolidating and retrieving previously learned content. "
            "Use spaced retrieval practice, interleaving, and self-assessment. Avoid just 're-teaching' — "
            "make students actively reconstruct their knowledge. Include a performance task or authentic "
            "application to demonstrate mastery."
        ),
    },
}

# ─── Discovery Principle ────────────────────────────────────────────────────────

DISCOVERY_PRINCIPLE = """
**THE DISCOVERY PRINCIPLE — CRITICAL FOR ALL GROUP/STATION MATERIALS:**

- DO NOT give away answers. Cards, data sheets, and station materials should provide raw information,
  data, scenarios, or primary-source-style context that students must analyze to arrive at conclusions.
- Limit to 1–2 thought-provoking questions per card. Questions should require synthesis, not fact-finding.
- Provide enough information for students to figure it out through discussion — not so much that the
  answer is obvious, and not so little that they're guessing.
- Avoid leading language. Don't say "This shows X because…" — provide the data and let students
  draw conclusions.
- Think of each card as a mini case study or data set, not an answer key.

**Good card structure:**
1. Topic/region title
2. Context paragraph (scene-setting, not answer-giving)
3. 3–5 data points, statistics, or real-world examples
4. 1–2 discussion questions requiring analysis
5. Space for students to record key takeaway
"""

# ─── System Prompts ─────────────────────────────────────────────────────────────

KNOWLEDGE_SKILLS_SYSTEM_PROMPT = """You are an expert instructional designer specializing in Marzano's New Taxonomy. Your task is to decompose competency statements into the underlying knowledge and skills students need."""

LESSON_PLAN_SYSTEM_PROMPT = """You are an expert instructional designer creating detailed, classroom-ready lesson plans using Marzano's New Taxonomy.

Your lesson plans must:
- Follow the specific lesson type structure provided
- Include concrete, specific activities (not vague descriptions)
- Specify discussion prompts that provoke real thinking
- Include timing for each segment
- Reference specific materials that will be created (worksheets, station cards, data sheets, etc.)
- Include Do Now, Framing, Core Activity, Discussion, and Exit Ticket
- Ensure the Exit Ticket directly assesses the daily objective
- Maintain at least 40% higher-order thinking (analysis + application)

Format your response as a structured lesson plan with clear segments, timing, and specific content."""

PERSONA_FEEDBACK_SYSTEM_PROMPT = """You are simulating 4 diverse student personas evaluating a lesson plan. Each persona has specific needs and perspectives.

For EACH persona, provide:
1. A brief, authentic reaction (1 sentence in the student's voice)
2. 2-3 specific concerns with severity (high/medium/low), each referencing a specific part of the lesson
3. Focus on what would actually matter to this student — not generic feedback

Be specific and actionable. Reference actual lesson segments, activities, and timing."""

PROMPT_ADDITIONS_SYSTEM_PROMPT = """You are an instructional design assistant. Based on persona feedback about a lesson plan, generate concise, actionable additions that a teacher can add to their lesson prompt to address the feedback.

Format each addition as a single bullet point starting with an action verb, followed by a parenthetical noting which persona raised the concern. Example:
- Add a word bank for key vocabulary terms (Alex: vocabulary accessibility concern)
- Include a real-world connection hook in the framing (Jordan: relevance concern)

Only include additions that would meaningfully improve the lesson. Do not repeat concerns already addressed in the plan."""

CONTENT_GENERATION_SYSTEM_PROMPT = """You are an expert instructional designer creating complete, structured lesson content. Generate ALL content blocks for the lesson.

CONTENT QUALITY STANDARDS:
- Discussion prompts must be thought-provoking and open-ended, not yes/no questions
- Activities must have specific, step-by-step student instructions
- The Do Now must connect to the day's content (not generic "journal about your feelings")
- The Framing must hook student interest with a compelling question, scenario, or connection
- The Exit Ticket must directly assess the daily objective — not the competency broadly, the SPECIFIC daily objective
- All vocabulary should be defined in student-friendly language
- Group/station materials MUST follow the Discovery Principle (provide data, not conclusions)

{discovery_principle}

FORMATTING:
Return your response as clearly labeled sections using markdown headers (##). Include ALL of these sections:

## Lesson Plan
(Complete lesson plan with timing, teacher notes, and materials list)

## Do Now
(Full Do Now activity with instructions and expected student response)

## Framing
(The hook/framing text — what the teacher says/shows to set up the lesson)

## Core Content
(The main instructional content — key concepts, vocabulary, examples, explanations)

## Discussion Prompts
(Numbered discussion questions with follow-up probes and possible student responses)

## Activity Instructions
(Detailed student-facing instructions for the main activity)

## Group Materials
(Station cards, data sheets, case studies, etc. — if the activity requires them. Follow the Discovery Principle.)

## Worksheet Content
(Complete content for the student worksheet — sections, questions, graphic organizers, response spaces)

## Exit Ticket
(The exit ticket question(s) that assess the daily objective)
"""

DOCUMENT_CODE_SYSTEM_PROMPT = """You are a Python developer creating classroom materials using python-pptx and python-docx.

Write Python code that creates polished, classroom-ready documents from the provided lesson content.

SLIDE DECK REQUIREMENTS:
- Use Helvetica (or Calibri as fallback) font throughout
- Minimum 16pt font size for body text, larger for titles
- Slide 1 is HIDDEN and contains the complete lesson plan for teacher reference
- Slide 2 shows the objective in context
- Remaining slides support lesson execution (one per major segment)
- SPARSE content — talking points, not paragraphs (3-5 bullets max per slide)
- NO TEXT CUTOFF — all text must fit within slide boundaries
- Include presenter notes with SAY/ASK/WATCH FOR guidance
- Professional, clean visual design with consistent styling
- Use the school colors: dark green (#00582c) and light green (#4DAE58) for accents

WORKSHEET REQUIREMENTS:
- Helvetica (or Calibri) font throughout
- Header with lesson title, Name:____, Date:____, Period:____
- Clear sections matching the lesson activities
- Appropriate response formats (tables, graphic organizers, answer lines)
- Adequate writing space (more for complex thinking tasks)
- Exit Ticket section at the end
- Double-spaced answer lines where appropriate

SUPPLEMENTARY MATERIALS (if needed):
- Station cards, data sheets, etc. referenced in activities
- Each material is self-contained and student-facing
- Follow the Discovery Principle for group materials

MODIFIED WORKSHEET (if requested):
- Same objectives as main worksheet
- Add word banks, sentence starters, visual supports
- Simplify language where appropriate
- Chunk complex instructions into steps
- Should feel like helpful tools, not a "dumbed down" version

EXTENSION WORKSHEET (if requested):
- Same core objectives as main worksheet
- Add more complex analytical questions
- Include research/inquiry prompts
- Add open-ended challenges
- Different work, not just more work

CRITICAL CODE REQUIREMENTS:
- Write ONLY executable Python code — no markdown, no explanations
- Use the exact file path variables provided (slides_path, worksheet_path, etc.)
- All imports are pre-loaded (Presentation, Document, Inches, Pt, RGBColor, etc.)
- Ensure all text fits within boundaries — check content length and adjust font size if needed
- Handle special characters properly
- Create all files that have paths provided
"""

# ─── Material Generation Setup Code ─────────────────────────────────────────────

EXEC_SETUP_CODE = """
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

from docx import Document
from docx.shared import Pt as DocxPt, Inches as DocxInches, Twips, RGBColor as DocxRGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn as docx_qn
from docx.oxml import OxmlElement

def set_cell_shading(cell, color):
    shading = OxmlElement('w:shd')
    shading.set(docx_qn('w:fill'), color)
    cell._tc.get_or_add_tcPr().append(shading)
"""

# ─── Marzano Framework Summary (embedded for prompts) ───────────────────────────

MARZANO_SUMMARY = """
Marzano's New Taxonomy — Four Cognitive Levels:

1. RETRIEVAL — Recognizing, recalling, executing. (list, define, recall, identify)
   Use for: warm-ups, vocabulary, activating prior knowledge. 5-10 min activities.

2. COMPREHENSION — Integrating and representing. (summarize, explain, compare, classify)
   Use for: concept mapping, summarization, comparison. 10-15 min activities.

3. ANALYSIS — Reasoning with knowledge. (analyze, investigate, critique, error analysis)
   Use for: case studies, error analysis, pattern recognition. 15-25 min activities.

4. KNOWLEDGE UTILIZATION — Applying to real-world tasks. (design, create, investigate, solve)
   Use for: design challenges, investigations, authentic problems. 20-40 min activities.

COGNITIVE RIGOR REQUIREMENT: Minimum 40% of lesson time on higher-order thinking
(analysis + knowledge utilization combined). Maximum 30% on retrieval-only activities.
"""
