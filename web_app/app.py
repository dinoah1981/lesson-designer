"""
Lesson Designer Web App - CompSci High Edition
A Streamlit interface for the Marzano-based lesson planning tool.
"""

import streamlit as st
import anthropic
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import tempfile
import uuid

# Add scripts directory to path
SCRIPTS_DIR = Path(__file__).parent.parent / ".claude" / "skills" / "lesson-designer" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# Import lesson designer scripts
from parse_competency import generate_session_id, get_sessions_dir
from validate_marzano import validate_lesson
from generate_worksheet import generate_worksheet, generate_worksheet_from_lesson
from generate_slides import generate_slides

# Import docx for text-to-word conversion
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Page config
st.set_page_config(
    page_title="Lesson Designer | CompSci High",
    page_icon="<>",
    layout="wide"
)

# CompSci High Brand Colors
DARK_GREEN = "#00582c"
LIGHT_GREEN = "#4DAE58"
WHITE = "#FFFFFF"

# Custom CSS with CompSci High branding - Enhanced UI
st.markdown(f"""
<style>
    /* Import a clean sans-serif font similar to Post Grotesk */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {{
        font-family: 'Inter', sans-serif;
    }}

    /* Main header styling */
    .main-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {DARK_GREEN};
        margin-bottom: 0;
    }}

    .brand-highlight {{
        color: {LIGHT_GREEN};
    }}

    .sub-header {{
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 1rem;
    }}

    /* ===== PROGRESS STEPPER (Horizontal) ===== */
    .progress-stepper {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin: 1.5rem 0 2rem 0;
        padding: 1.5rem 1rem;
        background: linear-gradient(180deg, #f8faf8 0%, #ffffff 100%);
        border-radius: 16px;
        border: 1px solid #e8f0e8;
        box-shadow: 0 2px 8px rgba(0,88,44,0.06);
    }}

    .step {{
        display: flex;
        flex-direction: column;
        align-items: center;
        flex: 1;
        position: relative;
        z-index: 1;
    }}

    .step:not(:last-child)::after {{
        content: '';
        position: absolute;
        top: 18px;
        left: calc(50% + 20px);
        width: calc(100% - 40px);
        height: 3px;
        background: #e0e0e0;
        z-index: 0;
    }}

    .step.completed:not(:last-child)::after {{
        background: {LIGHT_GREEN};
    }}

    .step-circle {{
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        position: relative;
        z-index: 2;
    }}

    .step.pending .step-circle {{
        background: #f0f0f0;
        color: #999;
        border: 2px solid #e0e0e0;
    }}

    .step.current .step-circle {{
        background: {DARK_GREEN};
        color: white;
        border: 3px solid {LIGHT_GREEN};
        box-shadow: 0 0 0 4px rgba(77,174,88,0.2);
        animation: pulse 2s infinite;
    }}

    .step.completed .step-circle {{
        background: {LIGHT_GREEN};
        color: white;
        border: 2px solid {LIGHT_GREEN};
    }}

    @keyframes pulse {{
        0%, 100% {{ box-shadow: 0 0 0 4px rgba(77,174,88,0.2); }}
        50% {{ box-shadow: 0 0 0 8px rgba(77,174,88,0.1); }}
    }}

    .step-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-align: center;
        max-width: 80px;
        line-height: 1.2;
    }}

    .step.pending .step-label {{ color: #999; }}
    .step.current .step-label {{ color: {DARK_GREEN}; }}
    .step.completed .step-label {{ color: {LIGHT_GREEN}; }}

    /* ===== STAGE CARDS ===== */
    .stage-card {{
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,88,44,0.08);
        border: 1px solid #e8f0e8;
    }}

    .stage-header {{
        background: linear-gradient(135deg, {DARK_GREEN} 0%, {LIGHT_GREEN} 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        margin: 0 0 1.5rem 0;
        font-weight: 700;
        font-size: 1.3rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: 0 4px 12px rgba(0,88,44,0.2);
    }}

    .stage-header-icon {{
        font-size: 1.5rem;
    }}

    /* ===== SUCCESS BOX ===== */
    .success-box {{
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border-left: 5px solid {LIGHT_GREEN};
        padding: 1.75rem;
        border-radius: 0 16px 16px 0;
        margin: 1.5rem 0;
        box-shadow: 0 2px 12px rgba(77,174,88,0.1);
    }}

    /* ===== INFO BOX ===== */
    .info-box {{
        background: linear-gradient(135deg, #f0f7f0 0%, #f8faf8 100%);
        border: 1px solid {LIGHT_GREEN};
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }}

    /* ===== PERSONA CARDS ===== */
    .persona-card {{
        background: white;
        border: 2px solid #e8e8e8;
        border-radius: 16px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}

    .persona-card:hover {{
        border-color: {LIGHT_GREEN};
        box-shadow: 0 4px 16px rgba(77,174,88,0.15);
        transform: translateY(-2px);
    }}

    .persona-name {{
        font-weight: 700;
        font-size: 1.15rem;
        color: {DARK_GREEN};
        margin-bottom: 0.25rem;
    }}

    .persona-type {{
        font-size: 0.85rem;
        color: {LIGHT_GREEN};
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}

    .persona-traits {{
        font-size: 0.85rem;
        color: #666;
    }}

    /* Rating stars */
    .rating {{
        font-size: 1.2rem;
        margin: 0.5rem 0;
    }}

    /* ===== LESSON SECTION ===== */
    .lesson-section {{
        background: #fafafa;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid {LIGHT_GREEN};
    }}

    .lesson-section h4 {{
        color: {DARK_GREEN};
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
    }}

    /* ===== ACTIVITY CARD ===== */
    .activity-card {{
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        transition: all 0.2s ease;
    }}

    .activity-card:hover {{
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}

    .activity-name {{
        font-weight: 600;
        color: {DARK_GREEN};
        font-size: 1.05rem;
    }}

    .activity-meta {{
        display: flex;
        gap: 1rem;
        margin: 0.5rem 0;
        font-size: 0.85rem;
        color: #666;
    }}

    .marzano-tag {{
        background: linear-gradient(135deg, {LIGHT_GREEN} 0%, {DARK_GREEN} 100%);
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }}

    /* ===== SIDEBAR STYLING ===== */
    .sidebar-section {{
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
    }}

    .sidebar-title {{
        color: {DARK_GREEN};
        font-weight: 700;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }}

    /* Progress indicator (sidebar) */
    .progress-step {{
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        font-size: 0.9rem;
    }}

    .step-complete {{
        color: {LIGHT_GREEN};
    }}

    .step-current {{
        color: {DARK_GREEN};
        font-weight: 700;
    }}

    .step-pending {{
        color: #aaa;
    }}

    /* ===== CONCERN CARDS ===== */
    .concern-high {{
        background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
        border-left: 4px solid #e53935;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 0 12px 12px 0;
    }}

    .concern-medium {{
        background: linear-gradient(135deg, #fffbf0 0%, #fff8e1 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 0 12px 12px 0;
    }}

    .concern-low {{
        background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
        border-left: 4px solid #9e9e9e;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        border-radius: 0 12px 12px 0;
    }}

    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* ===== BUTTON STYLING ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {DARK_GREEN} 0%, {LIGHT_GREEN} 100%);
        color: white;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,88,44,0.2);
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, {LIGHT_GREEN} 0%, {DARK_GREEN} 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,88,44,0.3);
    }}

    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* ===== DOWNLOAD BUTTONS ===== */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        border: none;
        box-shadow: 0 2px 8px rgba(33,150,243,0.3);
    }}

    .stDownloadButton > button:hover {{
        background: linear-gradient(135deg, #1976d2 0%, #2196f3 100%);
    }}

    /* ===== FORM STYLING ===== */
    .stTextArea textarea, .stTextInput input, .stSelectbox {{
        border-radius: 10px !important;
    }}

    /* ===== METRIC STYLING ===== */
    [data-testid="stMetricValue"] {{
        font-size: 1.75rem !important;
        font-weight: 700 !important;
        color: {DARK_GREEN} !important;
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.9rem !important;
    }}

    /* ===== EXPANDER STYLING ===== */
    .streamlit-expanderHeader {{
        font-weight: 600;
        color: {DARK_GREEN};
    }}

    /* ===== DIVIDER ===== */
    hr {{
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #e8f0e8;
    }}
</style>
""", unsafe_allow_html=True)

# Persona definitions with detailed characteristics
PERSONAS = {
    "alex": {
        "name": "Alex",
        "type": "Struggling Learner / ELL",
        "icon": "📚",
        "color": "#e53935",
        "traits": [
            "Reads 2-3 years below grade level",
            "Needs vocabulary pre-teaching",
            "Benefits from visual supports",
            "Requires extended processing time"
        ],
        "focus": "Can this student ACCESS the content?",
        "description": "Alex represents students who face barriers to accessing grade-level content due to reading difficulties or language learning challenges."
    },
    "jordan": {
        "name": "Jordan",
        "type": "Unmotivated but Capable",
        "icon": "😐",
        "color": "#ff9800",
        "traits": [
            "High ability, low engagement",
            "Asks 'Why does this matter?'",
            "Needs real-world relevance",
            "Values autonomy and choice"
        ],
        "focus": "Will this student CARE about the content?",
        "description": "Jordan represents capable students who disengage when they don't see the relevance or purpose of what they're learning."
    },
    "maya": {
        "name": "Maya",
        "type": "Interested & Capable",
        "icon": "🌟",
        "color": "#4caf50",
        "traits": [
            "Intrinsically motivated",
            "Asks deep questions",
            "Seeks connections across topics",
            "Wants intellectual challenge"
        ],
        "focus": "Will this student be ENGAGED and challenged?",
        "description": "Maya represents students who are ready and eager to learn but need opportunities for depth and inquiry to stay engaged."
    },
    "marcus": {
        "name": "Marcus",
        "type": "High Achieving / Gifted",
        "icon": "🚀",
        "color": "#2196f3",
        "traits": [
            "3+ years above grade level",
            "Rapid mastery of new content",
            "Needs ceiling removal",
            "Benefits from different work, not more work"
        ],
        "focus": "Does this lesson have enough CEILING?",
        "description": "Marcus represents gifted learners who need acceleration and complexity, not just additional practice problems."
    }
}

# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "lesson_data" not in st.session_state:
    st.session_state.lesson_data = {}
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "selected_feedback" not in st.session_state:
    st.session_state.selected_feedback = {}
if "generate_modified_materials" not in st.session_state:
    st.session_state.generate_modified_materials = False
if "generate_extension_materials" not in st.session_state:
    st.session_state.generate_extension_materials = False
# Multi-competency queue
if "competency_queue" not in st.session_state:
    st.session_state.competency_queue = []  # List of {competency, lesson_count, ...}
if "current_competency_index" not in st.session_state:
    st.session_state.current_competency_index = 0
if "completed_competencies" not in st.session_state:
    st.session_state.completed_competencies = []  # Stores completed lesson sequences


def get_claude_client():
    """Get Anthropic client with API key from secrets or environment."""
    api_key = st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("Please set your ANTHROPIC_API_KEY in Streamlit secrets or environment variables.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


def search_image_for_activity(description: str, context: str = "") -> dict:
    """Search for a relevant image based on activity description.

    Returns dict with 'description' and optionally 'url'.
    Uses Unsplash Source API for free, high-quality images.
    """
    import urllib.parse
    import requests

    if not description:
        return {}

    # Create search query from description
    # Extract key terms for better search results
    search_terms = description.lower()
    # Remove common words that don't help image search
    for word in ['a', 'an', 'the', 'showing', 'depicting', 'of', 'with', 'for', 'that', 'which', 'image', 'visual', 'picture', 'diagram']:
        search_terms = search_terms.replace(f' {word} ', ' ')

    # Add context if provided (e.g., subject area)
    if context:
        search_terms = f"{context} {search_terms}"

    # Clean up and limit to key words
    search_terms = ' '.join(search_terms.split()[:6])  # Limit to 6 words

    try:
        # Use Unsplash Source API (free, no auth required)
        # This returns a redirect to an actual image
        encoded_query = urllib.parse.quote(search_terms)

        # Try to get image from Unsplash
        unsplash_url = f"https://source.unsplash.com/800x600/?{encoded_query}"

        # Verify the URL works by checking headers (don't download full image)
        response = requests.head(unsplash_url, allow_redirects=True, timeout=5)

        if response.status_code == 200:
            # Return the final URL after redirects
            return {
                "description": description,
                "url": response.url,
                "search_terms": search_terms
            }
    except Exception:
        pass  # Fall back to description only

    # If search fails, return just the description
    return {
        "description": description,
        "url": None,
        "search_terms": search_terms
    }


def process_lesson_images(lesson: dict, subject_context: str = "") -> dict:
    """Process visual_description fields and search for images."""
    enhanced = lesson.copy()

    activities = enhanced.get('activities', [])
    for activity in activities:
        visual_desc = activity.get('visual_description')

        # Skip if no visual description or if it's null/None
        if not visual_desc or visual_desc == 'null' or visual_desc.lower() == 'none':
            continue

        # Search for an appropriate image
        image_result = search_image_for_activity(visual_desc, subject_context)
        if image_result:
            activity['recommended_image'] = image_result

    enhanced['activities'] = activities
    return enhanced


def load_marzano_framework():
    """Load the Marzano framework reference."""
    marzano_path = Path(__file__).parent.parent / ".claude" / "skills" / "lesson-designer" / "MARZANO.md"
    if marzano_path.exists():
        return marzano_path.read_text(encoding="utf-8")
    return ""


def design_lesson_with_claude(input_data: dict, marzano_framework: str, knowledge: list = None, skills: list = None, redesign_concerns: list = None, user_feedback: str = None, approved_flow: dict = None) -> dict:
    """Use Claude to design a lesson or lesson sequence based on input."""
    client = get_claude_client()

    lesson_count = input_data.get('lesson_count', 1)

    # Format knowledge and skills if provided
    knowledge_text = ""
    if knowledge:
        knowledge_items = [k["item"] for k in knowledge]
        knowledge_text = f"\n\nCONFIRMED KNOWLEDGE (students must understand these):\n" + "\n".join(f"- {k}" for k in knowledge_items)

    skills_text = ""
    if skills:
        skills_items = [s["item"] for s in skills]
        skills_text = f"\n\nCONFIRMED SKILLS (students must be able to do these):\n" + "\n".join(f"- {s}" for s in skills_items)

    # Format approved lesson flow if provided
    flow_text = ""
    if approved_flow and approved_flow.get("lessons"):
        flow_text = "\n\nAPPROVED LESSON FLOW (follow this structure):\n"
        flow_text += f"Sequence: {approved_flow.get('sequence_title', 'Lesson Sequence')}\n"
        for lesson in approved_flow.get("lessons", []):
            flow_text += f"\n- Lesson {lesson.get('lesson_number', '?')}: {lesson.get('title', 'Untitled')}\n"
            flow_text += f"  Type: {lesson.get('lesson_type', 'introducing')}\n"
            flow_text += f"  Objective: {lesson.get('objective', 'TBD')}\n"
            flow_text += f"  Focus: {lesson.get('focus', '')}\n"

    # Format redesign concerns and user feedback if this is a redesign
    redesign_text = ""
    if redesign_concerns or user_feedback:
        redesign_text = "\n\n🔄 REDESIGN REQUEST - Address the following:\n"
        if redesign_concerns:
            redesign_text += "\nPERSONA FEEDBACK TO ADDRESS:\n"
            for concern in redesign_concerns:
                persona = concern.get('from_persona', 'Student')
                element = concern.get('element', 'General')
                issue = concern.get('issue', '')
                recommendation = concern.get('recommendation', '')
                redesign_text += f"- [{persona}] {element}: {issue}"
                if recommendation:
                    redesign_text += f" → Recommendation: {recommendation}"
                redesign_text += "\n"
        if user_feedback:
            redesign_text += f"\nADDITIONAL USER GUIDANCE:\n{user_feedback}\n"
        redesign_text += "\nIMPORTANT: Create an IMPROVED lesson that specifically addresses ALL the concerns and feedback above while maintaining pedagogical quality."

    # Subject-specific pedagogical guidance based on research
    subject_pedagogy = """
SUBJECT-SPECIFIC PEDAGOGY (Apply based on detected subject area):

First, identify the PRIMARY SUBJECT AREA from the competency:
- MATHEMATICS: equations, algebra, geometry, calculus, statistics, proofs, functions
- SCIENCE: biology, chemistry, physics, earth science, experiments, phenomena, hypotheses
- ELA: reading, writing, literature, essays, analysis of texts, grammar, rhetoric
- HISTORY/SOCIAL STUDIES: historical events, primary sources, civilizations, government, economics
- COMPUTER SCIENCE: programming, coding, algorithms, data structures, debugging, computational thinking

Then apply the appropriate instructional sequence:

FOR MATHEMATICS:
- Instructional Model: Launch-Explore-Summarize (NOT I Do, We Do, You Do by default)
- Launch (5-10 min): Present a rich problem or question that creates need-to-know
- Explore (20-30 min): Students work on problem with productive struggle (15-30 min optimal)
- Summarize (10-15 min): Class discussion to formalize understanding; teacher facilitates connections
- EXCEPTION: Use direct instruction ONLY for conventions (notation, terminology) not for discoverable concepts
- Key principle: Conceptual understanding must PRECEDE procedural fluency
- Include: Multiple representations (concrete, visual, symbolic)

FOR SCIENCE:
- Instructional Model: 5E (Engage-Explore-Explain-Elaborate-Evaluate)
- Engage (5 min): Anchoring phenomenon that creates wonder/questions
- Explore (15-20 min): Hands-on investigation BEFORE formal explanation
- Explain (10-15 min): Formalize concepts AFTER students have explored
- Elaborate (10-15 min): Apply understanding to new situations
- Evaluate (5-10 min): Formative assessment
- Key principle: Students explore phenomena BEFORE teacher explains concepts
- Include: Claim-Evidence-Reasoning (CER) for argumentation

FOR ELA (Reading/Writing):
- Instructional Model: Workshop (Mini-lesson → Work Time → Share)
- Mini-lesson (10-15 min MAX): Focused instruction on ONE skill/strategy
- Work Time (30-45 min): Students read/write independently with teacher conferring
- Share (5-10 min): Students share work, reflect on learning
- Key principle: 25% teacher instruction, 75% student practice
- Include: Student choice in texts or response formats when possible
- AVOID: Five-paragraph essay templates (use authentic purposes instead)

FOR HISTORY/SOCIAL STUDIES:
- Instructional Model: Inquiry Arc (Question → Investigate → Synthesize → Argue)
- Compelling Question (5 min): Open-ended question that drives investigation
- Background Context (5-10 min): Just-in-time background, NOT comprehensive lecture
- Document Analysis (20-25 min): Students analyze 2-4 primary sources (more for advanced)
- Synthesis/Argumentation (10-15 min): Students construct evidence-based arguments
- Key principle: Students investigate sources BEFORE being told "the answer"
- Include: Sourcing, contextualization, corroboration skills
- Balance: 20-30% direct instruction, 50-60% inquiry, 20-30% synthesis

FOR COMPUTER SCIENCE:
- Instructional Model: PRIMM (Predict-Run-Investigate-Modify-Make)
- Predict (5 min): Students predict what code will do BEFORE running it
- Run (2 min): Execute code, compare prediction to actual output
- Investigate (10 min): Trace through code, answer comprehension questions
- Modify (15 min): Make targeted changes to existing code (scaffolded)
- Make (15 min): Create new code applying the concept
- Key principle: Code READING must precede code WRITING
- Include: Parsons problems (reordering code), debugging activities
- For syntax: Direct instruction is appropriate
- For problem-solving: Guided exploration is more effective

IMPORTANT: Use the "instructional_phase" field with SUBJECT-APPROPRIATE phases:
- For Math: "launch", "explore", "summarize"
- For Science: "engage", "explore", "explain", "elaborate", "evaluate"
- For ELA: "mini_lesson", "work_time", "conferring", "share"
- For History: "question", "background", "investigate", "synthesize"
- For CS: "predict", "run", "investigate", "modify", "make"
"""

    if lesson_count == 1:
        # Single lesson design
        # Determine lesson type from approved flow or default
        lesson_type_str = "introducing"
        if approved_flow and approved_flow.get("lessons"):
            lesson_type_str = approved_flow["lessons"][0].get("lesson_type", "introducing")

        prompt = f"""You are an expert instructional designer using Marzano's New Taxonomy and SUBJECT-SPECIFIC pedagogical approaches.

Design a complete lesson based on this input:
- Competency: {input_data['competency']}
- Grade Level: {input_data['grade_level']}
- Duration: {input_data['duration']} minutes
- Lesson Type: {lesson_type_str}
- Constraints: {input_data.get('constraints', 'None')}{knowledge_text}{skills_text}{flow_text}{redesign_text}

{subject_pedagogy}

INSTRUCTIONAL DESIGN REQUIREMENTS:
1. FIRST: Identify the subject area from the competency (Math, Science, ELA, History, CS)
2. THEN: Apply the subject-appropriate instructional sequence from the pedagogy guide above
3. Include activities at multiple Marzano levels (retrieval, comprehension, analysis, knowledge_utilization)
4. At least 40% of time should be higher-order thinking (analysis + knowledge_utilization)
5. Include vocabulary terms with definitions
6. Include an exit ticket or embedded assessment
7. For activities that would benefit from visuals, include a "visual_description" field

CRITICAL: Do NOT default to "I Do, We Do, You Do" for all subjects.
- For Math/Science/History: Students should EXPLORE or INVESTIGATE before teacher explains
- For ELA: Mini-lesson should be SHORT (10-15 min max), then extended student work time
- For CS: Students PREDICT and READ code before writing code

TASK VARIETY REQUIREMENTS:
- Use different task_types: worked_example, guided_practice, collaborative, individual, productive_struggle, retrieval_practice, discussion_protocol, creation, inquiry, investigation
- Vary grouping structures: whole_class, pairs, small_groups, individual
- Include at least one collaborative learning structure
- Include differentiation support for each activity

ENGAGEMENT DESIGN (based on Self-Determination Theory):
- Include choice elements where students have autonomy
- Make relevance to students' lives explicit
- Scaffold challenge appropriately (productive struggle, not frustration)

🔴 CRITICAL - COMPLETENESS REQUIREMENT:
Design a creative, engaging lesson - but whatever you design, make it COMPLETE and TEACHER-READY:

- If you include vocabulary, provide FULL DEFINITIONS (not "definition here")
- If you include a reading or text, WRITE THE ACTUAL TEXT
- If you include data or comparisons, FILL IN THE ACTUAL DATA
- If you include questions, make them CONTENT-SPECIFIC (not generic "what patterns do you notice?")
- If you include an assessment, provide REAL QUESTIONS with answer keys
- If you include a worked example, show the COMPLETE SOLUTION

The test: Could a substitute teacher pick this up and run the lesson without needing to create any content themselves?

BE CREATIVE with lesson structure - not every lesson needs the same format. Consider: Socratic seminars, simulations, debates, project-based learning, gallery walks, jigsaw activities, case studies, labs, stations, games, creative projects, etc.

Return a JSON object with this exact structure:
{{
    "is_sequence": false,
    "subject_area": "math|science|ela|history|cs|other",
    "instructional_model": "The subject-specific model used (e.g., 'Launch-Explore-Summarize', '5E', 'Workshop', 'Inquiry Arc', 'PRIMM')",
    "title": "Lesson title",
    "grade_level": "{input_data['grade_level']}",
    "duration": {input_data['duration']},
    "lesson_type": "{lesson_type_str}",
    "objective": "Students will be able to...",
    "essential_question": "Overarching inquiry question that drives the lesson",
    "vocabulary": [
        {{"word": "term1", "definition": "COMPLETE definition with explanation"}},
        {{"word": "term2", "definition": "COMPLETE definition with explanation"}}
    ],
    "activities": [
        {{
            "name": "Activity Name",
            "task_type": "worked_example|guided_practice|collaborative|individual|productive_struggle|retrieval_practice|discussion_protocol|creation|inquiry|investigation",
            "duration": 10,
            "marzano_level": "retrieval|comprehension|analysis|knowledge_utilization",
            "grouping": "whole_class|pairs|small_groups|individual",
            "instructional_phase": "Use subject-appropriate phase (e.g., 'launch', 'explore', 'explain', 'mini_lesson', 'investigate', 'predict')",
            "instructions": ["Step 1", "Step 2"],
            "teacher_moves": ["What teacher does during this activity"],
            "student_directions": "Clear directions students see on slides/worksheets (e.g., 'Read the passage below and answer questions 1-3')",
            "student_questions": ["Question 1 for students to answer", "Question 2 for students to answer"],
            "materials": ["Material 1"],
            "material_format": "worksheet|graphic_organizer|discussion_protocol|choice_board|lab_sheet|digital_interactive|manipulative|primary_source|code_template|none",
            "student_output": "What students produce",
            "assessment_method": "How to assess",
            "differentiation": {{
                "support": "Scaffold for struggling learners",
                "extension": "Challenge for advanced learners"
            }},
            "engagement_hook": {{
                "relevance": "Why this matters to students",
                "choice_element": "Where students have autonomy (or null)"
            }},
            "visual_description": "Description of helpful image/diagram (or null if not needed)"
        }}
    ],
    "slide_content": {{
        "opening_hook": "Engaging question, scenario, or visual to start the lesson",
        "essential_question_display": "How the essential question should appear on slides",
        "agenda": [{{"activity": "Name", "duration": 10}}],
        "discussion_prompts": [
            {{
                "after_activity": "Activity Name",
                "prompt": "Turn-and-talk or discussion question",
                "expected_responses": ["What students might say"]
            }}
        ],
        "worked_examples": [
            {{
                "concept": "What this demonstrates",
                "example": "Step-by-step walkthrough",
                "common_errors": ["Error to address and correct"]
            }}
        ],
        "check_for_understanding": [
            {{
                "timing": "After which activity",
                "question": "Quick check question",
                "success_looks_like": "What correct understanding looks like"
            }}
        ],
        "key_visuals": ["Description of diagram, chart, or image needed for slides"],
        "misconceptions": ["Common misconception 1"],
        "delivery_tips": ["Tip 1"],
        "transitions": ["Transition statement between major activities"],
        "scaffolding_notes": {{
            "struggling_learners": "Support strategies during instruction",
            "accelerated_learners": "Extension opportunities during instruction"
        }},
        "closure_synthesis": "How to tie everything together at the end"
    }},
    "assessment": {{
        "type": "exit_ticket|performance_task|discussion|portfolio|peer_review|self_assessment|project|presentation|other",
        "description": "What students do for assessment",
        "questions": ["Actual question 1 with content-specific details", "Actual question 2"],
        "answer_key": "Correct answers or rubric criteria",
        "success_criteria": "What mastery looks like"
    }}
}}

MARZANO FRAMEWORK REFERENCE:
{marzano_framework[:3000]}

Return ONLY the JSON object, no other text."""
    else:
        # Multi-lesson sequence design
        prompt = f"""You are an expert instructional designer using Marzano's New Taxonomy and SUBJECT-SPECIFIC pedagogical approaches.

Design a {lesson_count}-LESSON SEQUENCE based on this input:
- Competency: {input_data['competency']}
- Grade Level: {input_data['grade_level']}
- Duration per lesson: {input_data['duration']} minutes
- Total lessons: {lesson_count}
- Constraints: {input_data.get('constraints', 'None')}{knowledge_text}{skills_text}{flow_text}{redesign_text}

{subject_pedagogy}

SEQUENCE DESIGN REQUIREMENTS:
1. FIRST: Identify the subject area from the competency (Math, Science, ELA, History, CS)
2. THEN: Apply the subject-appropriate instructional sequence WITHIN each lesson
3. Each lesson should have a DISTINCT objective that builds toward the overall competency
4. Vocabulary should be distributed across lessons (introduce new terms progressively)
5. Each lesson should have at least 40% higher-order thinking time
6. The sequence should tell a coherent learning story
7. Include spaced retrieval practice - each lesson should briefly review key concepts from previous lessons

CRITICAL: Do NOT default to "I Do, We Do, You Do" for all subjects.
- For Math: Use Launch-Explore-Summarize; students explore problems before teacher formalizes
- For Science: Use 5E model; students explore phenomena BEFORE teacher explains
- For ELA: Use Workshop model; short mini-lesson then extended student work time
- For History: Use Inquiry Arc; students investigate sources before being told conclusions
- For CS: Use PRIMM; students predict/read code before writing code

TASK VARIETY REQUIREMENTS (use diverse task types across the sequence):
- Use different task_types: worked_example, guided_practice, collaborative, individual, productive_struggle, retrieval_practice, discussion_protocol, creation, inquiry, investigation
- Vary grouping structures: whole_class, pairs, small_groups, individual
- Include at least one collaborative learning structure per lesson
- Include differentiation support for each activity
- Vary material formats: worksheet, graphic_organizer, discussion_protocol, choice_board, lab_sheet, digital_interactive, primary_source, code_template

ENGAGEMENT DESIGN (based on Self-Determination Theory):
- Include choice elements where students have autonomy
- Make relevance to students' lives explicit
- Scaffold challenge appropriately (productive struggle, not frustration)

🔴 CRITICAL - COMPLETENESS REQUIREMENT:
Design creative, engaging lessons - but whatever you design, make it COMPLETE and TEACHER-READY:

- If you include vocabulary, provide FULL DEFINITIONS (not placeholders)
- If you include readings/texts, WRITE THE ACTUAL TEXT
- If you include data or comparisons, FILL IN THE ACTUAL DATA
- If you include questions, make them CONTENT-SPECIFIC
- If you include assessments, provide REAL QUESTIONS with answer keys
- If you include worked examples, show COMPLETE SOLUTIONS

BE CREATIVE - vary lesson structures across the sequence. Consider: Socratic seminars, simulations, debates, project-based learning, gallery walks, jigsaw activities, case studies, labs, stations, games, creative projects, etc.

Return a JSON object with this exact structure:
{{
    "is_sequence": true,
    "subject_area": "math|science|ela|history|cs|other",
    "instructional_model": "The subject-specific model used consistently across lessons",
    "sequence_title": "Overall sequence title",
    "competency": "{input_data['competency']}",
    "grade_level": "{input_data['grade_level']}",
    "total_lessons": {lesson_count},
    "duration_per_lesson": {input_data['duration']},
    "sequence_overview": "Brief description of how the lessons build toward mastery",
    "essential_question": "Overarching inquiry question that drives the entire sequence",
    "lessons": [
        {{
            "lesson_number": 1,
            "title": "Lesson 1 title",
            "lesson_type": "introducing",
            "objective": "Lesson 1 specific objective",
            "connection_to_previous": "How this connects to prior learning (null for lesson 1)",
            "vocabulary": [{{"word": "term1", "definition": "COMPLETE definition"}}],
            "activities": [
                {{
                    "name": "Activity Name",
                    "task_type": "worked_example|guided_practice|collaborative|individual|productive_struggle|retrieval_practice|discussion_protocol|creation|inquiry|investigation",
                    "duration": 10,
                    "marzano_level": "retrieval|comprehension|analysis|knowledge_utilization",
                    "grouping": "whole_class|pairs|small_groups|individual",
                    "instructional_phase": "Use subject-appropriate phase (e.g., 'launch', 'explore', 'explain', 'mini_lesson', 'investigate', 'predict')",
                    "instructions": ["Step 1", "Step 2"],
                    "teacher_moves": ["What teacher does during this activity"],
                    "student_directions": "Clear directions students see on slides/worksheets",
                    "student_questions": ["Question 1 for students", "Question 2 for students"],
                    "materials": ["Material 1"],
                    "material_format": "worksheet|graphic_organizer|discussion_protocol|choice_board|lab_sheet|digital_interactive|manipulative|primary_source|code_template|none",
                    "student_output": "What students produce",
                    "assessment_method": "How to assess",
                    "differentiation": {{
                        "support": "Scaffold for struggling learners",
                        "extension": "Challenge for advanced learners"
                    }},
                    "engagement_hook": {{
                        "relevance": "Why this matters to students",
                        "choice_element": "Where students have autonomy (or null)"
                    }},
                    "visual_description": "Description of helpful image/diagram (or null if not needed)"
                }}
            ],
            "slide_content": {{
                "opening_hook": "Engaging question, scenario, or visual to start",
                "retrieval_from_previous": "Quick review question from previous lesson (null for lesson 1)",
                "agenda": [{{"activity": "Name", "duration": 10}}],
                "discussion_prompts": [
                    {{
                        "after_activity": "Activity Name",
                        "prompt": "Turn-and-talk or discussion question",
                        "expected_responses": ["What students might say"]
                    }}
                ],
                "worked_examples": [
                    {{
                        "concept": "What this demonstrates",
                        "example": "Step-by-step walkthrough",
                        "common_errors": ["Error to address and correct"]
                    }}
                ],
                "check_for_understanding": [
                    {{
                        "timing": "After which activity",
                        "question": "Quick check question",
                        "success_looks_like": "What correct understanding looks like"
                    }}
                ],
                "key_visuals": ["Description of diagram, chart, or image needed"],
                "misconceptions": ["Common misconception to address"],
                "delivery_tips": ["Instructional tip"],
                "transitions": ["Transition statement between activities"],
                "scaffolding_notes": {{
                    "struggling_learners": "Support strategies",
                    "accelerated_learners": "Extension opportunities"
                }},
                "closure_synthesis": "How to tie this lesson together"
            }},
            "assessment": {{
                "type": "exit_ticket",
                "description": "Brief description",
                "questions": ["Question 1"],
                "success_criteria": "What mastery looks like"
            }}
        }}
    ]
}}

Include {lesson_count} lesson objects in the "lessons" array. Ensure VARIETY in task_types and material_formats across lessons.

MARZANO FRAMEWORK REFERENCE:
{marzano_framework[:2500]}

Return ONLY the JSON object, no other text."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=12000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.content[0].text
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())


def extract_knowledge_skills(competency: str, grade_level: str) -> dict:
    """Extract underlying knowledge and skills from a competency statement."""
    client = get_claude_client()

    prompt = f"""Analyze this competency statement and extract the underlying knowledge and skills students need.

COMPETENCY: {competency}
GRADE LEVEL: {grade_level}

Extract:
1. **Knowledge items** - Facts, concepts, vocabulary, and information students must KNOW
2. **Skills** - Procedures, processes, and abilities students must be able to DO

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
- Be specific and granular - break down into teachable components
- Typically 4-8 knowledge items and 3-6 skills
- Knowledge = what students need to understand/remember
- Skills = what students need to be able to do/perform

IMPORTANT - English/Language Arts Distinction:
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
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.content[0].text
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())


def propose_lesson_flow(competency: str, lesson_count: int, grade_level: str, lesson_objectives: list = None, knowledge: list = None, skills: list = None) -> dict:
    """Propose a lesson flow with types for each lesson in the sequence."""
    client = get_claude_client()

    # Format user-provided objectives if any
    objectives_text = ""
    if lesson_objectives and any(lesson_objectives):
        objectives_text = "\n\nUSER-SPECIFIED OBJECTIVES (incorporate these):\n"
        for i, obj in enumerate(lesson_objectives):
            if obj:
                objectives_text += f"- Lesson {i+1}: {obj}\n"

    # Format extracted knowledge/skills
    ks_text = ""
    if knowledge:
        ks_text += "\n\nKNOWLEDGE TO BUILD:\n" + "\n".join(f"- {k['item']}" for k in knowledge)
    if skills:
        ks_text += "\n\nSKILLS TO DEVELOP:\n" + "\n".join(f"- {s['item']}" for s in skills)

    prompt = f"""Design a {lesson_count}-lesson sequence to teach this competency:

COMPETENCY: {competency}
GRADE LEVEL: {grade_level}
NUMBER OF LESSONS: {lesson_count}{objectives_text}{ks_text}

Design an effective learning progression. Consider:
- Lesson types should build logically (typically: Introducing → Deepening → Synthesis)
- Each lesson needs a distinct, achievable objective
- Knowledge/vocabulary should be introduced before skills that use them
- Later lessons should build on and reference earlier ones

LESSON TYPES (choose appropriately for each):
- **Introducing**: First exposure to new concepts/vocabulary - more teacher support, scaffolded exploration
- **Deepening**: Building fluency through guided then independent practice - applying concepts
- **Synthesis**: Connecting ideas, analyzing patterns, higher-order thinking
- **Review**: Consolidating and assessing - retrieval practice, performance tasks

Return a JSON object:
{{
    "sequence_title": "Brief, engaging title for the lesson sequence",
    "sequence_rationale": "1-2 sentences explaining the learning progression",
    "lessons": [
        {{
            "lesson_number": 1,
            "lesson_type": "introducing|deepening|synthesis|review",
            "title": "Lesson title",
            "objective": "Students will be able to...",
            "focus": "Brief description of what this lesson covers",
            "builds_on": null,
            "prepares_for": "What this lesson sets up for the next one"
        }}
    ]
}}

Return ONLY the JSON object."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.content[0].text
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())


def get_persona_feedback(lesson_or_sequence: dict, persona_key: str, persona: dict) -> dict:
    """Get feedback from a student persona on a lesson or lesson sequence."""
    client = get_claude_client()

    is_sequence = lesson_or_sequence.get('is_sequence', False)

    if is_sequence:
        # Format sequence for evaluation
        lessons = lesson_or_sequence.get('lessons', [])
        lessons_text = ""
        for i, lesson in enumerate(lessons, 1):
            lessons_text += f"""
LESSON {i}: {lesson.get('title', 'Untitled')}
Objective: {lesson.get('objective', 'Not specified')}
Vocabulary: {', '.join([v.get('word', '') for v in lesson.get('vocabulary', [])])}
Activities: {', '.join([a.get('name', '') + ' (' + a.get('marzano_level', '') + ')' for a in lesson.get('activities', [])])}
"""

        prompt = f"""You are evaluating a {len(lessons)}-LESSON SEQUENCE from the perspective of this student:

STUDENT PERSONA: {persona['name']} ({persona['type']})
Key Traits:
{chr(10).join('- ' + t for t in persona['traits'])}

Focus Question: {persona['focus']}

SEQUENCE TO EVALUATE:
Title: {lesson_or_sequence.get('sequence_title', 'Untitled Sequence')}
Competency: {lesson_or_sequence.get('competency', 'Not specified')}
Overview: {lesson_or_sequence.get('sequence_overview', 'Not specified')}
Total Duration: {len(lessons)} lessons x {lesson_or_sequence.get('duration_per_lesson', 50)} minutes
{lessons_text}

Evaluate this ENTIRE SEQUENCE from {persona['name']}'s perspective.

IMPORTANT: Be CONCISE. Only flag issues that would significantly impact this student's learning.

Return a JSON object:
{{
    "persona_key": "{persona_key}",
    "persona_name": "{persona['name']}",
    "overall_rating": 1-5,
    "reaction": "One sentence: how {persona['name']} would feel about this sequence",
    "concerns": [
        {{
            "id": "unique_id",
            "lesson": "all|1|2|3|4",
            "element": "scaffolding|pacing|engagement|challenge|progression",
            "issue": "Concise issue (max 15 words)",
            "severity": "high|medium",
            "recommendation": "Quick fix suggestion (max 15 words)"
        }}
    ],
    "strengths": ["One key strength for this student"]
}}

LIMIT: Maximum 2-3 concerns total. Only include HIGH or MEDIUM severity issues.

Return ONLY the JSON object."""
    else:
        # Single lesson evaluation
        prompt = f"""You are evaluating a lesson from the perspective of this student:

STUDENT PERSONA: {persona['name']} ({persona['type']})
Key Traits:
{chr(10).join('- ' + t for t in persona['traits'])}

Focus Question: {persona['focus']}

LESSON TO EVALUATE:
Title: {lesson_or_sequence.get('title', 'Untitled')}
Objective: {lesson_or_sequence.get('objective', 'Not specified')}
Duration: {lesson_or_sequence.get('duration', 0)} minutes

Activities:
{json.dumps(lesson_or_sequence.get('activities', []), indent=2)}

Vocabulary:
{json.dumps(lesson_or_sequence.get('vocabulary', []), indent=2)}

Evaluate this lesson from {persona['name']}'s perspective.

IMPORTANT: Be CONCISE. Only flag issues that would significantly impact this student's learning.

Return a JSON object:
{{
    "persona_key": "{persona_key}",
    "persona_name": "{persona['name']}",
    "overall_rating": 1-5,
    "reaction": "One sentence: how {persona['name']} would feel about this lesson",
    "concerns": [
        {{
            "id": "unique_id",
            "element": "scaffolding|pacing|engagement|challenge",
            "issue": "Concise issue (max 15 words)",
            "severity": "high|medium",
            "recommendation": "Quick fix suggestion (max 15 words)"
        }}
    ],
    "strengths": ["One key strength for this student"]
}}

LIMIT: Maximum 2-3 concerns total. Only include HIGH or MEDIUM severity issues.

Return ONLY the JSON object."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response.content[0].text
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    result = json.loads(response_text.strip())

    # Add unique IDs to concerns if missing
    for i, concern in enumerate(result.get("concerns", [])):
        if "id" not in concern:
            concern["id"] = f"{persona_key}_{i}"

    return result


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    if not isinstance(text, str):
        text = str(text)
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def format_single_lesson_html(lesson: dict, lesson_num: int = None) -> str:
    """Format a single lesson as detailed HTML."""
    parts = []

    # Lesson header
    title = escape_html(lesson.get('title', 'Untitled'))
    objective = escape_html(lesson.get('objective', 'Not specified'))
    lesson_type = escape_html(lesson.get('lesson_type', 'Not specified').replace('_', ' ').title())
    duration = lesson.get('duration', lesson.get('duration_per_lesson', 0))
    essential_question = lesson.get('essential_question', '')
    subject_area = lesson.get('subject_area', '')
    instructional_model = lesson.get('instructional_model', '')

    if lesson_num:
        parts.append(f'''<div class="lesson-section" style="border-left: 4px solid {DARK_GREEN}; background: #f8faf8;">
<h4 style="color: {DARK_GREEN}; font-size: 1.2rem;">📅 Lesson {lesson_num}: {title}</h4>''')
    else:
        parts.append(f'''<div class="lesson-section">
<h4>📎 Lesson Overview</h4>
<p><strong>Title:</strong> {title}</p>''')

    parts.append(f'''<p><strong>Objective:</strong> {objective}</p>
<p><strong>Type:</strong> {lesson_type}</p>
<p><strong>Duration:</strong> {duration} minutes</p>''')

    # Show subject-specific instructional model if present
    if subject_area or instructional_model:
        model_info = []
        if subject_area:
            subject_labels = {'math': 'Mathematics', 'science': 'Science', 'ela': 'English Language Arts', 'history': 'History/Social Studies', 'cs': 'Computer Science', 'other': 'General'}
            model_info.append(f"<strong>Subject:</strong> {subject_labels.get(subject_area, subject_area.title())}")
        if instructional_model:
            model_info.append(f"<strong>Instructional Model:</strong> {escape_html(instructional_model)}")
        parts.append(f'<p>{" | ".join(model_info)}</p>')

    if essential_question:
        parts.append(f'<p><strong>Essential Question:</strong> <em>{escape_html(essential_question)}</em></p>')

    # Connection to previous lesson (for sequences)
    connection = lesson.get('connection_to_previous')
    if connection:
        parts.append(f'<p><strong>Connection to Previous:</strong> {escape_html(connection)}</p>')

    parts.append('</div>')

    # Vocabulary section
    vocab = lesson.get('vocabulary', [])
    if vocab:
        vocab_items = ''.join([f"<li><strong>{escape_html(v.get('word', ''))}:</strong> {escape_html(v.get('definition', ''))}</li>" for v in vocab])
        parts.append(f'<div class="lesson-section"><h4>📖 Key Vocabulary</h4><ul>{vocab_items}</ul></div>')

    # Activities section with full detail
    activities = lesson.get('activities', [])
    if activities:
        activity_cards = []
        for i, act in enumerate(activities, 1):
            level = act.get('marzano_level', 'unknown')
            level_display = escape_html(level.replace('_', ' ').title())
            name = escape_html(act.get('name', 'Activity'))
            duration_act = act.get('duration', 0)
            student_output = escape_html(act.get('student_output', 'Not specified'))

            # New task variety fields
            task_type = act.get('task_type', '')
            task_type_display = escape_html(task_type.replace('_', ' ').title()) if task_type else ''
            grouping = act.get('grouping', '')
            grouping_display = escape_html(grouping.replace('_', ' ').title()) if grouping else ''
            # Instructional phase (subject-specific) - fallback to gradual_release_phase for backward compatibility
            instructional_phase = act.get('instructional_phase', act.get('gradual_release_phase', ''))
            # Map common phase names to display labels
            phase_labels = {
                # Math: Launch-Explore-Summarize
                'launch': 'Launch', 'explore': 'Explore', 'summarize': 'Summarize',
                # Science: 5E
                'engage': 'Engage', 'explain': 'Explain', 'elaborate': 'Elaborate', 'evaluate': 'Evaluate',
                # ELA: Workshop
                'mini_lesson': 'Mini-Lesson', 'work_time': 'Work Time', 'conferring': 'Conferring', 'share': 'Share',
                # History: Inquiry Arc
                'question': 'Question', 'background': 'Background', 'investigate': 'Investigate', 'synthesize': 'Synthesize',
                # CS: PRIMM
                'predict': 'Predict', 'run': 'Run', 'modify': 'Modify', 'make': 'Make',
                # Legacy GRR (still supported)
                'i_do': 'I Do', 'we_do': 'We Do', 'you_do_together': 'You Do Together', 'you_do_alone': 'You Do Alone'
            }
            phase_display = phase_labels.get(instructional_phase, instructional_phase.replace('_', ' ').title()) if instructional_phase else ''
            material_format = act.get('material_format', '')
            material_format_display = escape_html(material_format.replace('_', ' ').title()) if material_format else ''

            instructions = act.get('instructions', [])
            instruction_items = ''.join([f"<li>{escape_html(step)}</li>" for step in instructions])

            # Teacher moves
            teacher_moves = act.get('teacher_moves', [])
            teacher_moves_html = ""
            if teacher_moves:
                moves_list = ''.join([f"<li>{escape_html(m)}</li>" for m in teacher_moves])
                teacher_moves_html = f"<p><strong>Teacher Moves:</strong></p><ul>{moves_list}</ul>"

            # Materials
            materials = act.get('materials', [])
            materials_html = ""
            if materials:
                materials_list = ''.join([f"<li>{escape_html(m)}</li>" for m in materials])
                format_note = f" <em>({material_format_display})</em>" if material_format_display and material_format != 'none' else ""
                materials_html = f"<p><strong>Materials{format_note}:</strong></p><ul>{materials_list}</ul>"

            # Differentiation
            diff = act.get('differentiation', {})
            diff_html = ""
            if diff:
                support = diff.get('support', '')
                extension = diff.get('extension', '')
                if support or extension:
                    diff_html = '<p><strong>Differentiation:</strong></p><ul>'
                    if support:
                        diff_html += f'<li><em>Support:</em> {escape_html(support)}</li>'
                    if extension:
                        diff_html += f'<li><em>Extension:</em> {escape_html(extension)}</li>'
                    diff_html += '</ul>'

            # Engagement hooks
            engagement = act.get('engagement_hook', {})
            engagement_html = ""
            if engagement:
                relevance = engagement.get('relevance', '')
                choice = engagement.get('choice_element', '')
                if relevance or (choice and choice != 'null'):
                    engagement_html = '<p><strong>Engagement Design:</strong></p><ul>'
                    if relevance:
                        engagement_html += f'<li><em>Relevance:</em> {escape_html(relevance)}</li>'
                    if choice and choice != 'null':
                        engagement_html += f'<li><em>Student Choice:</em> {escape_html(choice)}</li>'
                    engagement_html += '</ul>'

            # Image recommendation if available
            image_html = ""
            image_rec = act.get('recommended_image', {})
            if image_rec:
                desc = escape_html(image_rec.get('description', ''))
                url = image_rec.get('url', '')
                if url:
                    image_html = f'<p><strong>🖼️ Suggested Visual:</strong> {desc}<br><a href="{url}" target="_blank" style="color: #1976d2;">View/Download Image →</a></p>'
                elif desc:
                    image_html = f'<p><strong>🖼️ Suggested Visual:</strong> {desc}</p>'

            # Build activity metadata tags
            meta_tags = [f'<span>⏱️ {duration_act} min</span>', f'<span class="marzano-tag">{level_display}</span>']
            if task_type_display:
                meta_tags.append(f'<span style="background: #e3f2fd; color: #1565c0; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">{task_type_display}</span>')
            if grouping_display:
                meta_tags.append(f'<span style="background: #fff3e0; color: #e65100; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">👥 {grouping_display}</span>')
            if phase_display:
                meta_tags.append(f'<span style="background: #f3e5f5; color: #7b1fa2; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">{phase_display}</span>')

            card = f'''<div class="activity-card">
<div class="activity-name">{i}. {name}</div>
<div class="activity-meta" style="flex-wrap: wrap; gap: 6px;">
{' '.join(meta_tags)}
</div>
<p><strong>Instructions:</strong></p>
<ol>{instruction_items}</ol>
{teacher_moves_html}
{materials_html}
{diff_html}
{engagement_html}
<p><strong>Student Output:</strong> {student_output}</p>
{image_html}
</div>'''
            activity_cards.append(card)

        parts.append(f'<div class="lesson-section"><h4>📋 Activities</h4>{"".join(activity_cards)}</div>')

    # Assessment section
    assessment = lesson.get('assessment', {})
    if assessment:
        assess_type = escape_html(assessment.get('type', 'exit_ticket').replace('_', ' ').title())
        questions = assessment.get('questions', [])
        question_items = ''.join([f"<li>{escape_html(q)}</li>" for q in questions])
        success_criteria = assessment.get('success_criteria', '')

        parts.append(f'''<div class="lesson-section">
<h4>✅ Assessment</h4>
<p><strong>Type:</strong> {assess_type}</p>
<p><strong>Questions:</strong></p>
<ol>{question_items}</ol>''')
        if success_criteria:
            parts.append(f'<p><strong>Success Criteria:</strong> {escape_html(success_criteria)}</p>')
        parts.append('</div>')

    # Enhanced slide content (new schema) or hidden_slide_content (legacy)
    slide_content = lesson.get('slide_content', lesson.get('hidden_slide_content', {}))
    if slide_content:
        parts.append('<div class="lesson-section" style="background: #fffde7; border-left: 4px solid #fbc02d;"><h4>🎯 Slide Content & Teacher Notes</h4>')

        # Opening hook
        opening_hook = slide_content.get('opening_hook', '')
        if opening_hook:
            parts.append(f'<p><strong>Opening Hook:</strong> {escape_html(opening_hook)}</p>')

        # Retrieval from previous (for sequences)
        retrieval = slide_content.get('retrieval_from_previous', '')
        if retrieval and retrieval != 'null':
            parts.append(f'<p><strong>Review from Previous:</strong> {escape_html(retrieval)}</p>')

        # Discussion prompts
        discussion_prompts = slide_content.get('discussion_prompts', [])
        if discussion_prompts:
            parts.append('<p><strong>Discussion Prompts:</strong></p><ul>')
            for dp in discussion_prompts:
                prompt_text = escape_html(dp.get('prompt', ''))
                after = escape_html(dp.get('after_activity', ''))
                expected = dp.get('expected_responses', [])
                expected_text = ', '.join([escape_html(e) for e in expected[:2]]) if expected else ''
                parts.append(f'<li><em>After {after}:</em> "{prompt_text}"')
                if expected_text:
                    parts.append(f' <small>(expect: {expected_text})</small>')
                parts.append('</li>')
            parts.append('</ul>')

        # Worked examples
        worked_examples = slide_content.get('worked_examples', [])
        if worked_examples:
            parts.append('<p><strong>Worked Examples for Slides:</strong></p>')
            for we in worked_examples:
                concept = escape_html(we.get('concept', ''))
                example = escape_html(we.get('example', ''))
                errors = we.get('common_errors', [])
                parts.append(f'<div style="background: #fff; padding: 10px; margin: 5px 0; border-radius: 4px;">')
                parts.append(f'<p><em>{concept}</em></p>')
                parts.append(f'<p>{example}</p>')
                if errors:
                    error_text = ', '.join([escape_html(e) for e in errors])
                    parts.append(f'<p><small>⚠️ Watch for: {error_text}</small></p>')
                parts.append('</div>')

        # Check for understanding
        cfu = slide_content.get('check_for_understanding', [])
        if cfu:
            parts.append('<p><strong>Check for Understanding:</strong></p><ul>')
            for check in cfu:
                timing = escape_html(check.get('timing', ''))
                question = escape_html(check.get('question', ''))
                success = escape_html(check.get('success_looks_like', ''))
                parts.append(f'<li><em>{timing}:</em> {question}')
                if success:
                    parts.append(f' <small>(success: {success})</small>')
                parts.append('</li>')
            parts.append('</ul>')

        # Key visuals needed
        key_visuals = slide_content.get('key_visuals', [])
        if key_visuals:
            visuals_list = ''.join([f"<li>{escape_html(v)}</li>" for v in key_visuals])
            parts.append(f'<p><strong>Key Visuals Needed:</strong></p><ul>{visuals_list}</ul>')

        # Misconceptions
        misconceptions = slide_content.get('misconceptions', [])
        if misconceptions:
            misc_items = ''.join([f"<li>{escape_html(m)}</li>" for m in misconceptions])
            parts.append(f'<p><strong>Watch for Misconceptions:</strong></p><ul>{misc_items}</ul>')

        # Delivery tips
        tips = slide_content.get('delivery_tips', [])
        if tips:
            tip_items = ''.join([f"<li>{escape_html(t)}</li>" for t in tips])
            parts.append(f'<p><strong>Delivery Tips:</strong></p><ul>{tip_items}</ul>')

        # Transitions
        transitions = slide_content.get('transitions', [])
        if transitions:
            trans_items = ''.join([f"<li>{escape_html(t)}</li>" for t in transitions])
            parts.append(f'<p><strong>Transition Statements:</strong></p><ul>{trans_items}</ul>')

        # Scaffolding notes
        scaffolding = slide_content.get('scaffolding_notes', {})
        if scaffolding:
            struggling = scaffolding.get('struggling_learners', '')
            accelerated = scaffolding.get('accelerated_learners', '')
            if struggling or accelerated:
                parts.append('<p><strong>Scaffolding During Instruction:</strong></p><ul>')
                if struggling:
                    parts.append(f'<li><em>For struggling learners:</em> {escape_html(struggling)}</li>')
                if accelerated:
                    parts.append(f'<li><em>For accelerated learners:</em> {escape_html(accelerated)}</li>')
                parts.append('</ul>')

        # Closure synthesis
        closure = slide_content.get('closure_synthesis', '')
        if closure:
            parts.append(f'<p><strong>Closure/Synthesis:</strong> {escape_html(closure)}</p>')

        parts.append('</div>')

    return ''.join(parts)


def format_lesson_display(lesson_or_sequence: dict) -> str:
    """Format lesson or sequence as readable HTML for teachers."""
    parts = []

    is_sequence = lesson_or_sequence.get('is_sequence', False)

    if is_sequence:
        # Sequence overview
        title = escape_html(lesson_or_sequence.get('sequence_title', 'Untitled Sequence'))
        competency = escape_html(lesson_or_sequence.get('competency', 'Not specified'))
        overview = escape_html(lesson_or_sequence.get('sequence_overview', ''))
        essential_question = lesson_or_sequence.get('essential_question', '')
        total_lessons = lesson_or_sequence.get('total_lessons', 0)
        duration = lesson_or_sequence.get('duration_per_lesson', 0)
        subject_area = lesson_or_sequence.get('subject_area', '')
        instructional_model = lesson_or_sequence.get('instructional_model', '')

        parts.append(f'''<div class="lesson-section" style="background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);">
<h4>📚 Sequence Overview</h4>
<p><strong>Title:</strong> {title}</p>
<p><strong>Competency:</strong> {competency}</p>
<p><strong>Duration:</strong> {total_lessons} lessons × {duration} minutes</p>''')

        # Show subject-specific instructional model for sequence
        if subject_area or instructional_model:
            subject_labels = {'math': 'Mathematics', 'science': 'Science', 'ela': 'English Language Arts', 'history': 'History/Social Studies', 'cs': 'Computer Science', 'other': 'General'}
            model_parts = []
            if subject_area:
                model_parts.append(f"<strong>Subject:</strong> {subject_labels.get(subject_area, subject_area.title())}")
            if instructional_model:
                model_parts.append(f"<strong>Instructional Model:</strong> {escape_html(instructional_model)}")
            parts.append(f'<p>{" | ".join(model_parts)}</p>')

        if essential_question:
            parts.append(f'<p><strong>Essential Question:</strong> <em>{escape_html(essential_question)}</em></p>')
        parts.append(f'''
<p><strong>Overview:</strong> {overview}</p>
</div>''')

        # Each lesson in sequence - FULL DETAIL
        for lesson in lesson_or_sequence.get('lessons', []):
            lesson_num = lesson.get('lesson_number', 0)
            parts.append(f'<div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 2px dashed #e0e0e0;">')
            parts.append(format_single_lesson_html(lesson, lesson_num))
            parts.append('</div>')

    else:
        # Single lesson - use the same detailed format
        parts.append(format_single_lesson_html(lesson_or_sequence))

    return ''.join(parts)


def format_compact_agenda(lesson: dict, lesson_num: int = None) -> str:
    """Format a compact agenda view for a single lesson (collapsed view)."""
    parts = []

    title = escape_html(lesson.get('title', 'Untitled'))
    objective = escape_html(lesson.get('objective', 'Not specified'))
    lesson_type = escape_html(lesson.get('lesson_type', '').replace('_', ' ').title())
    duration = lesson.get('duration', lesson.get('duration_per_lesson', 50))

    # Header with lesson number and title
    header = f"Lesson {lesson_num}: {title}" if lesson_num else title

    parts.append(f'''<div style="background: #f8faf8; border-left: 4px solid {LIGHT_GREEN}; padding: 0.75rem 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0;">
<div style="display: flex; justify-content: space-between; align-items: center;">
<strong style="color: {DARK_GREEN};">{escape_html(header)}</strong>
<span style="color: #888; font-size: 0.85rem;">{lesson_type} • {duration} min</span>
</div>
<p style="color: #555; font-size: 0.9rem; margin: 0.5rem 0 0.75rem 0;">{objective}</p>
<div style="font-size: 0.85rem;">''')

    # Compact activity list with timing
    activities = lesson.get('activities', [])
    for i, act in enumerate(activities, 1):
        name = escape_html(act.get('name', 'Activity'))
        dur = act.get('duration', 0)
        parts.append(f'<span style="color: #666;">{i}. {name} ({dur}m)</span>')
        if i < len(activities):
            parts.append(' → ')

    parts.append('</div></div>')

    return ''.join(parts)


def format_sequence_overview_compact(lesson_or_sequence: dict) -> str:
    """Format a compact sequence overview showing all lessons."""
    parts = []

    title = escape_html(lesson_or_sequence.get('sequence_title', 'Lesson Sequence'))
    total_lessons = lesson_or_sequence.get('total_lessons', len(lesson_or_sequence.get('lessons', [])))
    duration = lesson_or_sequence.get('duration_per_lesson', 50)

    parts.append(f'''<div style="background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%); padding: 1rem; border-radius: 12px; margin-bottom: 1rem;">
<h4 style="color: {DARK_GREEN}; margin: 0 0 0.5rem 0;">📚 {title}</h4>
<p style="color: #555; margin: 0; font-size: 0.9rem;">{total_lessons} lessons × {duration} minutes</p>
</div>''')

    return ''.join(parts)


def reset_session():
    """Reset the session state."""
    st.session_state.stage = 1
    st.session_state.lesson_data = {}
    st.session_state.session_id = None
    st.session_state.selected_feedback = {}
    st.session_state.generate_modified_materials = False
    st.session_state.generate_extension_materials = False
    st.session_state.competency_queue = []
    st.session_state.current_competency_index = 0
    st.session_state.completed_competencies = []


def start_next_competency():
    """Move to the next competency in the queue."""
    st.session_state.current_competency_index += 1
    st.session_state.stage = 2  # Go to knowledge/skills review for next competency
    st.session_state.lesson_data = {}
    st.session_state.selected_feedback = {}
    st.session_state.generate_modified_materials = False
    st.session_state.generate_extension_materials = False
    # Load the next competency's input data
    if st.session_state.current_competency_index < len(st.session_state.competency_queue):
        next_comp = st.session_state.competency_queue[st.session_state.current_competency_index]
        st.session_state.lesson_data["input"] = next_comp


def render_progress_stepper(current_stage: int):
    """Render a horizontal progress stepper using Streamlit columns."""
    stages = [
        ("1", "Define", "📝"),
        ("2", "Review", "🔍"),
        ("3", "Design", "🎨"),
        ("4", "Evaluate", "👥"),
        ("5", "Generate", "⚙️"),
        ("6", "Download", "📥"),
    ]

    cols = st.columns(6)
    for i, (num, label, icon) in enumerate(stages):
        stage_num = int(num)
        with cols[i]:
            if stage_num < current_stage:
                # Completed
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: {LIGHT_GREEN}; color: white; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">✓</div>
                    <div style="font-size: 0.8rem; color: {LIGHT_GREEN}; font-weight: 600;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
            elif stage_num == current_stage:
                # Current
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: {DARK_GREEN}; color: white; display: inline-flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem; box-shadow: 0 0 0 4px rgba(77,174,88,0.3);">{num}</div>
                    <div style="font-size: 0.8rem; color: {DARK_GREEN}; font-weight: 700;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Pending
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: #f0f0f0; color: #999; display: inline-flex; align-items: center; justify-content: center; font-weight: 600; font-size: 1rem; margin-bottom: 0.5rem; border: 2px solid #e0e0e0;">{num}</div>
                    <div style="font-size: 0.8rem; color: #999;">{label}</div>
                </div>
                """, unsafe_allow_html=True)


def _store_persona_concerns_for_materials(feedback_list: list):
    """Store selected concerns from Alex and Marcus for material generation."""
    alex_concerns = []
    marcus_concerns = []

    for fb in feedback_list:
        persona_key = fb.get("persona_key", "unknown")
        for idx, concern in enumerate(fb.get("concerns", [])):
            concern_id = concern.get("id", f"{persona_key}_{idx}")
            unique_key = f"{persona_key}_{idx}_{concern_id}"
            if st.session_state.selected_feedback.get(unique_key, False):
                if persona_key == "alex":
                    alex_concerns.append(concern)
                elif persona_key == "marcus":
                    marcus_concerns.append(concern)

    st.session_state.lesson_data["alex_concerns"] = alex_concerns
    st.session_state.lesson_data["marcus_concerns"] = marcus_concerns


def generate_modified_worksheet(lesson: dict, concerns: list) -> dict:
    """Generate a modified worksheet for struggling learners based on Alex's concerns.

    Returns a lesson-like dict that can be passed to generate_worksheet_from_lesson.
    """
    client = get_claude_client()

    concerns_text = "\n".join([f"- {c.get('element', 'Issue')}: {c.get('issue', '')} (Recommendation: {c.get('recommendation', '')})" for c in concerns])

    prompt = f"""Create a MODIFIED version of this lesson designed for struggling learners and ELL students.

ORIGINAL LESSON:
Title: {lesson.get('title', 'Lesson')}
Objective: {lesson.get('objective', '')}
Grade Level: {lesson.get('grade_level', '')}

Activities:
{json.dumps(lesson.get('activities', []), indent=2)}

Vocabulary:
{json.dumps(lesson.get('vocabulary', []), indent=2)}

Assessment:
{json.dumps(lesson.get('assessment', {}), indent=2)}

CONCERNS TO ADDRESS (from struggling learner persona):
{concerns_text}

Create a modified lesson structure that:
1. KEEPS THE SAME LEARNING OBJECTIVES
2. Addresses each concern listed above
3. Includes scaffolds: simplified vocabulary, sentence starters, word banks, chunked instructions, visual cues

Return ONLY valid JSON in this exact format:
{{
    "title": "Modified: [original title]",
    "grade_level": "{lesson.get('grade_level', '')}",
    "objective": "[same objective, possibly simplified wording]",
    "activities": [
        {{
            "name": "[activity name - e.g., 'Vocabulary Preview' or 'Guided Practice']",
            "marzano_level": "retrieval|comprehension|analysis|knowledge_utilization",
            "instructions": ["Step 1...", "Step 2..."],
            "student_output": "[what students will produce]",
            "discussion_questions": ["Question with sentence starter: I think ___ because ___"]
        }}
    ],
    "vocabulary": [
        {{"word": "term", "definition": "simple definition with example"}}
    ],
    "assessment": {{
        "questions": ["Exit ticket question 1 (with scaffold if needed)", "Exit ticket question 2"]
    }}
}}

Include 2-4 activities with scaffolded instructions. Simplify vocabulary definitions. Add sentence starters to discussion questions."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON from response
    response_text = response.content[0].text
    # Extract JSON if wrapped in markdown code blocks
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())


def generate_extension_worksheet(lesson: dict, concerns: list) -> dict:
    """Generate an extension worksheet for advanced learners based on Marcus's concerns.

    Returns a lesson-like dict that can be passed to generate_worksheet_from_lesson.
    """
    client = get_claude_client()

    concerns_text = "\n".join([f"- {c.get('element', 'Issue')}: {c.get('issue', '')} (Recommendation: {c.get('recommendation', '')})" for c in concerns])

    prompt = f"""Create an EXTENSION version of this lesson designed for advanced/gifted learners.

ORIGINAL LESSON:
Title: {lesson.get('title', 'Lesson')}
Objective: {lesson.get('objective', '')}
Grade Level: {lesson.get('grade_level', '')}

Activities:
{json.dumps(lesson.get('activities', []), indent=2)}

Vocabulary:
{json.dumps(lesson.get('vocabulary', []), indent=2)}

Assessment:
{json.dumps(lesson.get('assessment', {}), indent=2)}

CONCERNS TO ADDRESS (from high-achieving student persona):
{concerns_text}

Create an extension lesson structure that:
1. KEEPS THE SAME CORE LEARNING OBJECTIVES but adds depth
2. Addresses each concern listed above (typically about ceiling/challenge)
3. Includes: deeper analysis questions, research prompts, creative challenges, cross-curricular connections

Return ONLY valid JSON in this exact format:
{{
    "title": "Extension: [original title]",
    "grade_level": "{lesson.get('grade_level', '')}",
    "objective": "[enhanced objective with deeper mastery expectations]",
    "activities": [
        {{
            "name": "[activity name - e.g., 'Deep Dive Analysis' or 'Independent Investigation']",
            "marzano_level": "analysis|knowledge_utilization",
            "instructions": ["Challenge step 1...", "Challenge step 2..."],
            "student_output": "[what students will produce - more complex output]",
            "discussion_questions": ["Higher-order thinking question requiring synthesis"]
        }}
    ],
    "vocabulary": [
        {{"word": "advanced term", "definition": "definition with nuance and connections"}}
    ],
    "assessment": {{
        "questions": ["Complex exit ticket question 1", "Open-ended reflection question"]
    }}
}}

Include 2-4 challenging activities at analysis or knowledge_utilization level. Add advanced vocabulary. Questions should require synthesis and evaluation."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON from response
    response_text = response.content[0].text
    # Extract JSON if wrapped in markdown code blocks
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())


def text_to_word_document(text: str, output_path: str, title: str = "Worksheet") -> None:
    """Convert plain text worksheet content to a formatted Word document."""
    doc = Document()

    # Set narrow margins
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    lines = text.split('\n')

    for line in lines:
        line = line.rstrip()

        # Skip empty lines but add paragraph for spacing
        if not line:
            doc.add_paragraph()
            continue

        # Detect headers (lines with === underneath or ALL CAPS headers)
        if line.startswith('===') or line.startswith('---'):
            continue  # Skip separator lines

        # Check if this is a main header (ALL CAPS or starts with specific patterns)
        is_main_header = (line.isupper() and len(line) > 5) or line.startswith('MODIFIED WORKSHEET') or line.startswith('EXTENSION WORKSHEET')
        is_section_header = line.endswith(':') and len(line) < 50 and not line.startswith('-')

        p = doc.add_paragraph()
        run = p.add_run(line)

        if is_main_header:
            run.bold = True
            run.font.size = Pt(14)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif is_section_header:
            run.bold = True
            run.font.size = Pt(11)
        elif line.startswith('- ') or line.startswith('• '):
            run.font.size = Pt(10)
            p.paragraph_format.left_indent = Inches(0.25)
        elif line[0:3].replace('.', '').replace(')', '').isdigit():
            # Numbered items
            run.font.size = Pt(10)
        else:
            run.font.size = Pt(10)

    doc.save(output_path)


# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    # Logo/Brand - using actual logo image
    logo_path = Path(__file__).parent / "assets" / "logo.jpg"
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <span style="font-size: 2rem; font-weight: 800; color: {DARK_GREEN};">COMP SCI</span><br>
            <span style="font-size: 2rem; font-weight: 800; color: {LIGHT_GREEN};">HIGH</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<p style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 0.5rem;">Lesson Designer</p>', unsafe_allow_html=True)

    st.divider()

    # Process explanation
    st.markdown(f'<div class="sidebar-title">📍 How It Works</div>', unsafe_allow_html=True)

    stages = [
        ("1", "Define Requirements", "Tell us what you want to teach"),
        ("2", "Review Knowledge & Skills", "Confirm underlying concepts"),
        ("3", "AI Designs Lesson", "Claude creates a Marzano-aligned lesson"),
        ("4", "Persona Review", "4 student perspectives evaluate accessibility"),
        ("5", "Generate Files", "Create .pptx slides and .docx worksheets"),
        ("6", "Download", "Get your classroom-ready materials"),
    ]

    for num, title, desc in stages:
        stage_num = int(num)
        if stage_num < st.session_state.stage:
            status = "✅"
            style = "step-complete"
        elif stage_num == st.session_state.stage:
            status = "▶️"
            style = "step-current"
        else:
            status = "○"
            style = "step-pending"

        st.markdown(f"""
        <div class="progress-step {style}">
            <span style="margin-right: 0.5rem;">{status}</span>
            <div>
                <strong>{title}</strong><br>
                <span style="font-size: 0.75rem; color: #888;">{desc}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Persona explanation
    st.markdown(f'<div class="sidebar-title">👥 About Student Personas</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size: 0.85rem; color: #666;">
    Your lesson is reviewed by 4 simulated students, each representing different learner needs:
    </p>
    """, unsafe_allow_html=True)

    for key, p in PERSONAS.items():
        st.markdown(f"""
        <div style="margin: 0.5rem 0; padding: 0.5rem; background: #f8f9fa; border-radius: 6px;">
            <span style="font-size: 1.2rem;">{p['icon']}</span>
            <strong style="color: {DARK_GREEN};">{p['name']}</strong>
            <span style="font-size: 0.75rem; color: {p['color']};">({p['type']})</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if st.button("🔄 Start Over", use_container_width=True):
        reset_session()
        st.rerun()


# ============================================
# MAIN CONTENT
# ============================================

# Header
st.markdown(f"""
<p class="main-header">Lesson <span class="brand-highlight">Designer</span></p>
""", unsafe_allow_html=True)
st.markdown('<p class="sub-header">Marzano-aligned lesson planning for every learner</p>', unsafe_allow_html=True)

# Horizontal Progress Stepper
render_progress_stepper(st.session_state.stage)


# Stage 1: Input Requirements - Simplified
if st.session_state.stage == 1:
    st.markdown('<div class="stage-header"><span class="stage-header-icon">📝</span> Define Your Lesson</div>', unsafe_allow_html=True)

    # Initialize session state for lesson objectives
    if "lesson_objectives" not in st.session_state:
        st.session_state.lesson_objectives = {}

    # Main competency input
    st.markdown("### What do you want students to learn?")

    competency = st.text_area(
        "Competency",
        placeholder="e.g., Students will analyze primary sources to evaluate historical claims about the causes of World War I",
        help="State what students will be able to DO by the end of the lesson(s)",
        height=100,
        key="competency_input"
    )

    # Settings row
    col1, col2, col3 = st.columns(3)
    with col1:
        lesson_count = st.selectbox(
            "Number of Lessons",
            [1, 2, 3, 4, 5],
            format_func=lambda x: f"{x} lesson{'s' if x > 1 else ''}",
            key="lesson_count_input",
            help="How many class periods to spend on this competency"
        )
    with col2:
        grade_level = st.selectbox(
            "Grade Level",
            ["6th grade", "7th grade", "8th grade", "9th grade",
             "10th grade", "11th grade", "12th grade", "AP", "College"],
            key="grade_level_input"
        )
    with col3:
        duration = st.slider("Minutes per Lesson", 30, 90, 50, 5, key="duration_input")

    # Optional: Specific objectives per lesson
    if lesson_count > 1:
        st.divider()
        with st.expander("📋 Add specific objectives for each lesson (optional)", expanded=False):
            st.markdown(f'<p style="color: #666; font-size: 0.9rem;">Leave blank to let Claude design the lesson flow automatically. Or specify what you want each lesson to focus on.</p>', unsafe_allow_html=True)

            for i in range(lesson_count):
                obj_key = f"lesson_obj_{i}"
                # Initialize if not exists
                if obj_key not in st.session_state.lesson_objectives:
                    st.session_state.lesson_objectives[obj_key] = ""

                st.session_state.lesson_objectives[obj_key] = st.text_input(
                    f"Lesson {i+1} objective",
                    value=st.session_state.lesson_objectives.get(obj_key, ""),
                    placeholder=f"e.g., {'Introduce key vocabulary and concepts' if i == 0 else 'Apply concepts to new scenarios' if i == lesson_count-1 else 'Practice with guided examples'}",
                    key=f"obj_input_{i}"
                )

    # Constraints
    constraints = st.text_area(
        "Any constraints or context? (optional)",
        placeholder="e.g., Limited technology, students already covered X, want to include Y activity...",
        height=68,
        key="constraints_input"
    )

    st.divider()

    # Start button
    if st.button("🚀 Continue", type="primary", use_container_width=True, disabled=not competency.strip()):
        if competency.strip():
            # Gather lesson objectives
            lesson_objectives = []
            for i in range(lesson_count):
                obj = st.session_state.lesson_objectives.get(f"lesson_obj_{i}", "").strip()
                lesson_objectives.append(obj if obj else None)

            # Build input data
            input_data = {
                "competency": competency.strip(),
                "lesson_count": lesson_count,
                "grade_level": grade_level,
                "duration": duration,
                "constraints": constraints,
                "lesson_objectives": lesson_objectives  # User-specified objectives per lesson (may be None)
            }

            # Store input data
            st.session_state.lesson_data["input"] = input_data

            # Initialize competency queue (for compatibility with download stage)
            st.session_state.competency_queue = [input_data]
            st.session_state.current_competency_index = 0

            st.session_state.session_id = str(uuid.uuid4())[:8]
            st.session_state.stage = 2
            st.rerun()

    if not competency.strip():
        st.info("👆 Enter a competency to get started.")


# Stage 2: Review Lesson Plan
elif st.session_state.stage == 2:
    st.markdown('<div class="stage-header"><span class="stage-header-icon">🔍</span> Review Lesson Plan</div>', unsafe_allow_html=True)

    input_data = st.session_state.lesson_data["input"]
    lesson_count = input_data.get("lesson_count", 1)

    st.markdown(f"""
    <div class="info-box">
        <strong>Competency:</strong> {input_data['competency']}<br>
        <strong>Grade:</strong> {input_data['grade_level']} |
        <strong>Lessons:</strong> {lesson_count} × {input_data['duration']} minutes
    </div>
    """, unsafe_allow_html=True)

    # Phase 1: Extract knowledge and skills
    if "knowledge_skills" not in st.session_state.lesson_data:
        with st.spinner("🔍 Analyzing competency..."):
            try:
                ks_data = extract_knowledge_skills(input_data["competency"], input_data["grade_level"])
                st.session_state.lesson_data["knowledge_skills"] = ks_data
                st.session_state.lesson_data["selected_knowledge"] = {
                    k["id"]: True for k in ks_data.get("knowledge", [])
                }
                st.session_state.lesson_data["selected_skills"] = {
                    s["id"]: True for s in ks_data.get("skills", [])
                }
                st.rerun()
            except Exception as e:
                st.error(f"Error analyzing competency: {str(e)}")
                if st.button("Try Again"):
                    st.rerun()

    # Phase 2: Propose lesson flow (after knowledge/skills extracted)
    elif "lesson_flow" not in st.session_state.lesson_data:
        ks_data = st.session_state.lesson_data["knowledge_skills"]

        # Get confirmed knowledge/skills for the flow proposal
        confirmed_knowledge = [
            item for item in ks_data["knowledge"]
            if st.session_state.lesson_data["selected_knowledge"].get(item["id"], True)
        ]
        confirmed_skills = [
            item for item in ks_data["skills"]
            if st.session_state.lesson_data["selected_skills"].get(item["id"], True)
        ]

        with st.spinner("📋 Designing lesson flow..."):
            try:
                flow = propose_lesson_flow(
                    input_data["competency"],
                    lesson_count,
                    input_data["grade_level"],
                    input_data.get("lesson_objectives", []),
                    confirmed_knowledge,
                    confirmed_skills
                )
                st.session_state.lesson_data["lesson_flow"] = flow
                # Initialize editable lesson types
                st.session_state.lesson_data["lesson_types"] = {
                    i: lesson["lesson_type"] for i, lesson in enumerate(flow.get("lessons", []))
                }
                st.rerun()
            except Exception as e:
                st.error(f"Error proposing lesson flow: {str(e)}")
                if st.button("Try Again"):
                    st.rerun()

    else:
        # Display everything for review
        ks_data = st.session_state.lesson_data["knowledge_skills"]
        flow_data = st.session_state.lesson_data["lesson_flow"]

        # LESSON FLOW SECTION (Primary focus)
        st.markdown(f"### 📋 Proposed Lesson Flow")
        st.markdown(f'<p style="color: #666; font-size: 0.95rem;">{flow_data.get("sequence_rationale", "")}</p>', unsafe_allow_html=True)

        lesson_type_options = ["introducing", "deepening", "synthesis", "review"]
        lesson_type_labels = {
            "introducing": "🆕 Introducing",
            "deepening": "📈 Deepening",
            "synthesis": "🔗 Synthesis",
            "review": "📝 Review"
        }

        for i, lesson in enumerate(flow_data.get("lessons", [])):
            current_type = st.session_state.lesson_data["lesson_types"].get(i, lesson.get("lesson_type", "introducing"))

            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div style="background: #f8faf8; border-left: 4px solid {LIGHT_GREEN}; padding: 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0;">
                        <strong style="color: {DARK_GREEN}; font-size: 1.1rem;">Lesson {lesson.get('lesson_number', i+1)}: {lesson.get('title', 'Untitled')}</strong><br>
                        <span style="color: #555; font-size: 0.9rem;">{lesson.get('objective', '')}</span><br>
                        <span style="color: #888; font-size: 0.85rem; font-style: italic;">{lesson.get('focus', '')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    new_type = st.selectbox(
                        "Type",
                        lesson_type_options,
                        index=lesson_type_options.index(current_type) if current_type in lesson_type_options else 0,
                        format_func=lambda x: lesson_type_labels.get(x, x.title()),
                        key=f"lesson_type_{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.lesson_data["lesson_types"][i] = new_type

        # KNOWLEDGE & SKILLS (Collapsible)
        st.divider()
        with st.expander("📚 Review Knowledge & Skills (optional)", expanded=False):
            st.markdown('<p style="color: #666; font-size: 0.9rem;">Uncheck items that aren\'t relevant or add custom items.</p>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<h5 style="color: {DARK_GREEN};">Knowledge</h5>', unsafe_allow_html=True)
                for item in ks_data.get("knowledge", []):
                    item_id = item["id"]
                    is_selected = st.checkbox(
                        item["item"],
                        value=st.session_state.lesson_data["selected_knowledge"].get(item_id, True),
                        key=f"know_{item_id}"
                    )
                    st.session_state.lesson_data["selected_knowledge"][item_id] = is_selected

            with col2:
                st.markdown(f'<h5 style="color: {DARK_GREEN};">Skills</h5>', unsafe_allow_html=True)
                for item in ks_data.get("skills", []):
                    item_id = item["id"]
                    is_selected = st.checkbox(
                        item["item"],
                        value=st.session_state.lesson_data["selected_skills"].get(item_id, True),
                        key=f"skill_{item_id}"
                    )
                    st.session_state.lesson_data["selected_skills"][item_id] = is_selected

        st.divider()

        # Navigation
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("← Back", use_container_width=True):
                # Clear flow data to allow re-generation
                if "lesson_flow" in st.session_state.lesson_data:
                    del st.session_state.lesson_data["lesson_flow"]
                if "knowledge_skills" in st.session_state.lesson_data:
                    del st.session_state.lesson_data["knowledge_skills"]
                st.session_state.stage = 1
                st.rerun()
        with col2:
            if st.button("✅ Approve & Design Lessons", type="primary", use_container_width=True):
                # Store confirmed data
                confirmed_knowledge = [
                    item for item in ks_data["knowledge"]
                    if st.session_state.lesson_data["selected_knowledge"].get(item["id"], False)
                ]
                confirmed_skills = [
                    item for item in ks_data["skills"]
                    if st.session_state.lesson_data["selected_skills"].get(item["id"], False)
                ]
                st.session_state.lesson_data["confirmed_knowledge"] = confirmed_knowledge
                st.session_state.lesson_data["confirmed_skills"] = confirmed_skills

                # Store approved lesson flow with any user modifications
                approved_flow = flow_data.copy()
                for i, lesson in enumerate(approved_flow.get("lessons", [])):
                    lesson["lesson_type"] = st.session_state.lesson_data["lesson_types"].get(i, lesson.get("lesson_type"))
                st.session_state.lesson_data["approved_flow"] = approved_flow

                st.session_state.stage = 3
                st.rerun()


# Stage 3: Design Lesson
elif st.session_state.stage == 3:
    lesson_count = st.session_state.lesson_data["input"].get("lesson_count", 1)
    header_text = "Designing Your Lesson Sequence" if lesson_count > 1 else "Designing Your Lesson"
    st.markdown(f'<div class="stage-header"><span class="stage-header-icon">🎨</span> {header_text}</div>', unsafe_allow_html=True)

    input_data = st.session_state.lesson_data["input"]
    approved_flow = st.session_state.lesson_data.get("approved_flow", {})

    lesson_info = f"{lesson_count} lessons × {input_data['duration']} min" if lesson_count > 1 else f"{input_data['duration']} min"

    # Get flow title or fallback
    flow_title = approved_flow.get('sequence_title', 'Lesson')

    st.markdown(f"""
    <div class="info-box">
        <strong>Designing:</strong> {flow_title}<br>
        <strong>Competency:</strong> {input_data['competency'][:100]}{'...' if len(input_data['competency']) > 100 else ''}<br>
        <strong>Grade:</strong> {input_data['grade_level']} |
        <strong>Duration:</strong> {lesson_info}
    </div>
    """, unsafe_allow_html=True)

    # Get confirmed knowledge and skills from stage 2
    confirmed_knowledge = st.session_state.lesson_data.get("confirmed_knowledge", [])
    confirmed_skills = st.session_state.lesson_data.get("confirmed_skills", [])

    if confirmed_knowledge or confirmed_skills:
        st.markdown(f"""
        <div style="background: #f0f7f0; padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem;">
            <strong>Using:</strong> {len(confirmed_knowledge)} knowledge items, {len(confirmed_skills)} skills
        </div>
        """, unsafe_allow_html=True)

    # Check if this is a redesign (has selected concerns or user feedback)
    redesign_concerns = st.session_state.lesson_data.get("selected_concerns", [])
    user_feedback = st.session_state.lesson_data.get("user_redesign_feedback", "")

    spinner_text = "🔄 Claude is redesigning your lesson based on feedback..." if (redesign_concerns or user_feedback) else "🎨 Claude is designing your lesson using Marzano's taxonomy..."

    with st.spinner(spinner_text):
        try:
            marzano = load_marzano_framework()
            lesson = design_lesson_with_claude(input_data, marzano, confirmed_knowledge, confirmed_skills, redesign_concerns, user_feedback, approved_flow)

            # Clear redesign data after use
            if "selected_concerns" in st.session_state.lesson_data:
                del st.session_state.lesson_data["selected_concerns"]
            if "user_redesign_feedback" in st.session_state.lesson_data:
                del st.session_state.lesson_data["user_redesign_feedback"]

            # Extract subject context from competency for better image search
            subject_context = input_data.get('competency', '')[:50]

            # Enhance lesson(s) with image recommendations
            with st.spinner("🖼️ Finding recommended images for activities..."):
                if lesson.get('is_sequence', False):
                    # Process each lesson in sequence
                    for i, single_lesson in enumerate(lesson.get('lessons', [])):
                        lesson['lessons'][i] = process_lesson_images(single_lesson, subject_context)
                else:
                    lesson = process_lesson_images(lesson, subject_context)

            st.session_state.lesson_data["lesson"] = lesson
            st.session_state.stage = 4
            st.rerun()
        except Exception as e:
            st.error(f"Error designing lesson: {str(e)}")
            if st.button("Try Again"):
                st.rerun()


# Stage 4: Persona Feedback
elif st.session_state.stage == 4:
    st.markdown('<div class="stage-header"><span class="stage-header-icon">👥</span> Review Your Lessons</div>', unsafe_allow_html=True)

    lesson_or_sequence = st.session_state.lesson_data["lesson"]
    is_sequence = lesson_or_sequence.get('is_sequence', False)

    # Calculate cognitive distribution
    if is_sequence:
        all_activities = []
        for lesson in lesson_or_sequence.get("lessons", []):
            all_activities.extend(lesson.get("activities", []))
        total_time = sum(a["duration"] for a in all_activities)
        higher_order_time = sum(
            a["duration"] for a in all_activities
            if a.get("marzano_level") in ["analysis", "knowledge_utilization"]
        )
        total_lessons = lesson_or_sequence.get("total_lessons", len(lesson_or_sequence.get("lessons", [])))
    else:
        all_activities = lesson_or_sequence.get("activities", [])
        total_time = sum(a["duration"] for a in all_activities)
        higher_order_time = sum(
            a["duration"] for a in all_activities
            if a.get("marzano_level") in ["analysis", "knowledge_utilization"]
        )
        total_lessons = 1

    cognitive_percent = (higher_order_time / total_time * 100) if total_time > 0 else 0

    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Lessons", total_lessons)
    with col2:
        st.metric("Activities", len(all_activities))
    with col3:
        st.metric("Higher-Order", f"{cognitive_percent:.0f}%")
    with col4:
        status = "✅ Pass" if cognitive_percent >= 40 else "⚠️ Low"
        st.metric("Rigor", status)

    # COLLAPSIBLE AGENDA VIEW
    st.markdown("### 📋 Lesson Agenda")
    st.markdown('<p style="color: #666; font-size: 0.9rem;">Click any lesson to see full details.</p>', unsafe_allow_html=True)

    if is_sequence:
        # Show sequence overview
        st.markdown(format_sequence_overview_compact(lesson_or_sequence), unsafe_allow_html=True)

        # Show each lesson as collapsible
        for lesson in lesson_or_sequence.get("lessons", []):
            lesson_num = lesson.get('lesson_number', 1)
            lesson_title = lesson.get('title', f'Lesson {lesson_num}')
            lesson_type = lesson.get('lesson_type', 'introducing').replace('_', ' ').title()

            # Compact agenda as expander header content
            with st.expander(f"**Lesson {lesson_num}:** {lesson_title} ({lesson_type})", expanded=False):
                st.markdown(format_single_lesson_html(lesson, lesson_num), unsafe_allow_html=True)
    else:
        # Single lesson - show compact agenda then expandable detail
        st.markdown(format_compact_agenda(lesson_or_sequence), unsafe_allow_html=True)

        with st.expander("📖 View Full Lesson Details", expanded=False):
            st.markdown(format_single_lesson_html(lesson_or_sequence), unsafe_allow_html=True)

    st.divider()

    # Persona feedback
    if "persona_feedback" not in st.session_state.lesson_data:
        st.markdown("### 👥 Running lesson through student personas...")

        feedback_list = []
        progress = st.progress(0)

        for i, (persona_key, persona) in enumerate(PERSONAS.items()):
            with st.spinner(f"Getting feedback from {persona['name']} ({persona['type']})..."):
                try:
                    feedback = get_persona_feedback(lesson_or_sequence, persona_key, persona)
                    feedback_list.append(feedback)
                except Exception as e:
                    st.warning(f"Could not get feedback from {persona['name']}: {e}")
            progress.progress((i + 1) / len(PERSONAS))

        st.session_state.lesson_data["persona_feedback"] = feedback_list
        # Initialize all feedback as selected with unique keys
        for fb in feedback_list:
            persona_key = fb.get("persona_key", "unknown")
            for idx, concern in enumerate(fb.get("concerns", [])):
                concern_id = concern.get("id", f"{persona_key}_{idx}")
                unique_key = f"{persona_key}_{idx}_{concern_id}"
                st.session_state.selected_feedback[unique_key] = True
        st.rerun()

    else:
        feedback_list = st.session_state.lesson_data["persona_feedback"]

        st.divider()
        st.markdown("### 👥 Student Persona Feedback")
        st.markdown('<p style="color: #666; font-size: 0.9rem;">Quick feedback from different student perspectives. Check concerns to address in redesign.</p>', unsafe_allow_html=True)

        # Display personas in a compact 2-column grid
        cols = st.columns(2)
        col_idx = 0

        for feedback in feedback_list:
            persona_key = feedback.get("persona_key", "")
            persona = PERSONAS.get(persona_key, {})
            rating = feedback.get("overall_rating", 3)
            concerns = feedback.get("concerns", [])

            with cols[col_idx % 2]:
                # Compact persona card
                rating_color = "#4CAF50" if rating >= 4 else "#FFC107" if rating >= 3 else "#f44336"
                st.markdown(f"""
                <div style="background: #fafafa; border-radius: 8px; padding: 0.75rem; margin-bottom: 0.75rem; border-left: 3px solid {rating_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 600;">{persona.get('icon', '👤')} {feedback.get('persona_name', 'Student')}</span>
                        <span style="color: {rating_color}; font-weight: bold;">{rating}/5</span>
                    </div>
                    <p style="font-size: 0.85rem; color: #555; margin: 0.5rem 0; font-style: italic;">"{feedback.get('reaction', '')}"</p>
                </div>
                """, unsafe_allow_html=True)

                # Compact concerns as bullets with checkboxes
                if concerns:
                    for idx, concern in enumerate(concerns[:3]):  # Max 3 concerns
                        concern_id = concern.get("id", f"{persona_key}_{idx}")
                        unique_key = f"{persona_key}_{idx}_{concern_id}"
                        severity = concern.get("severity", "medium")
                        severity_icon = "🔴" if severity == "high" else "🟡"

                        is_selected = st.checkbox(
                            f"{severity_icon} {concern.get('issue', 'Issue')}",
                            value=st.session_state.selected_feedback.get(unique_key, True),
                            key=f"cb_{unique_key}",
                            help=f"💡 {concern.get('recommendation', '')}"
                        )
                        st.session_state.selected_feedback[unique_key] = is_selected

                # Differentiated materials options - compact
                if persona_key == "alex" and concerns:
                    st.session_state.generate_modified_materials = st.checkbox(
                        "📝 Generate scaffolded materials",
                        value=st.session_state.generate_modified_materials,
                        key="generate_modified_checkbox",
                        help="Word banks, sentence starters for struggling learners"
                    )
                elif persona_key == "marcus" and concerns:
                    st.session_state.generate_extension_materials = st.checkbox(
                        "🚀 Generate extension materials",
                        value=st.session_state.generate_extension_materials,
                        key="generate_extension_checkbox",
                        help="Deeper questions, challenges for advanced learners"
                    )

            col_idx += 1

        st.divider()

        # Count selected concerns
        selected_count = sum(1 for v in st.session_state.selected_feedback.values() if v)
        total_concerns = len(st.session_state.selected_feedback)

        if total_concerns > 0:
            st.markdown(f"**{selected_count} of {total_concerns} concerns selected for redesign**")

        # User feedback text area for additional redesign guidance
        st.markdown("### ✏️ Additional Feedback (Optional)")
        user_redesign_feedback = st.text_area(
            "Add your own feedback or guidance for the redesign:",
            placeholder="E.g., 'Make the activities more hands-on', 'Add more scaffolding for ELL students', 'Include a real-world example about climate change'...",
            height=100,
            key="user_redesign_feedback"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Proceed Without Changes", use_container_width=True):
                # Store material generation preferences
                st.session_state.lesson_data["generate_modified"] = st.session_state.generate_modified_materials
                st.session_state.lesson_data["generate_extension"] = st.session_state.generate_extension_materials
                # Store Alex's and Marcus's selected concerns for material generation
                _store_persona_concerns_for_materials(feedback_list)
                st.session_state.stage = 5
                st.rerun()
        with col2:
            if st.button(f"🔄 Redesign with {selected_count} Selected Concerns", type="primary", use_container_width=True):
                # Store selected concerns for redesign
                selected_concerns = []
                for fb in feedback_list:
                    persona_key = fb.get("persona_key", "unknown")
                    for idx, concern in enumerate(fb.get("concerns", [])):
                        concern_id = concern.get("id", f"{persona_key}_{idx}")
                        unique_key = f"{persona_key}_{idx}_{concern_id}"
                        if st.session_state.selected_feedback.get(unique_key, False):
                            concern["from_persona"] = fb.get("persona_name", "Unknown")
                            selected_concerns.append(concern)
                st.session_state.lesson_data["selected_concerns"] = selected_concerns
                # Store user's additional feedback
                st.session_state.lesson_data["user_redesign_feedback"] = user_redesign_feedback
                # Clear feedback to trigger redesign
                del st.session_state.lesson_data["persona_feedback"]
                st.session_state.stage = 3
                st.rerun()


# Stage 5: Generate Materials
elif st.session_state.stage == 5:
    st.markdown('<div class="stage-header"><span class="stage-header-icon">⚙️</span> Generating Materials</div>', unsafe_allow_html=True)

    lesson_or_sequence = st.session_state.lesson_data["lesson"]
    is_sequence = lesson_or_sequence.get('is_sequence', False)
    temp_dir = Path(tempfile.mkdtemp())

    if is_sequence:
        # Generate materials for each lesson in the sequence
        lessons = lesson_or_sequence.get('lessons', [])
        st.session_state.lesson_data["sequence_materials"] = []

        progress = st.progress(0)
        for i, lesson in enumerate(lessons):
            lesson_num = lesson.get('lesson_number', i + 1)

            with st.spinner(f"📊 Generating materials for Lesson {lesson_num} of {len(lessons)}..."):
                try:
                    # Save individual lesson JSON
                    lesson_path = temp_dir / f"lesson_{lesson_num}.json"
                    # Add required fields from sequence
                    lesson_with_meta = lesson.copy()
                    lesson_with_meta['grade_level'] = lesson_or_sequence.get('grade_level')
                    lesson_with_meta['duration'] = lesson_or_sequence.get('duration_per_lesson')

                    with open(lesson_path, 'w', encoding='utf-8') as f:
                        json.dump(lesson_with_meta, f, indent=2)

                    # Generate slides
                    slides_path = temp_dir / f"lesson_{lesson_num}_slides.pptx"
                    generate_slides(str(lesson_path), str(slides_path))

                    # Generate worksheet
                    worksheet_path = temp_dir / f"lesson_{lesson_num}_worksheet.docx"
                    template_path = Path(__file__).parent.parent / ".claude" / "skills" / "lesson-designer" / "templates" / "student_worksheet.docx"
                    if template_path.exists():
                        generate_worksheet(str(lesson_path), str(template_path), str(worksheet_path))
                    else:
                        generate_worksheet(str(lesson_path), None, str(worksheet_path))

                    st.session_state.lesson_data["sequence_materials"].append({
                        "lesson_number": lesson_num,
                        "title": lesson.get('title', f'Lesson {lesson_num}'),
                        "slides_path": str(slides_path),
                        "worksheet_path": str(worksheet_path)
                    })

                except Exception as e:
                    st.error(f"Error generating materials for Lesson {lesson_num}: {e}")

            progress.progress((i + 1) / len(lessons))

    else:
        # Single lesson generation
        with st.spinner("📊 Generating PowerPoint slides..."):
            try:
                lesson_path = temp_dir / "lesson.json"

                with open(lesson_path, 'w', encoding='utf-8') as f:
                    json.dump(lesson_or_sequence, f, indent=2)

                slides_path = temp_dir / "slides.pptx"
                generate_slides(str(lesson_path), str(slides_path))
                st.session_state.lesson_data["slides_path"] = str(slides_path)

            except Exception as e:
                st.error(f"Error generating slides: {e}")

        with st.spinner("📝 Generating student worksheet..."):
            try:
                worksheet_path = temp_dir / "worksheet.docx"
                template_path = Path(__file__).parent.parent / ".claude" / "skills" / "lesson-designer" / "templates" / "student_worksheet.docx"

                if template_path.exists():
                    generate_worksheet(str(lesson_path), str(template_path), str(worksheet_path))
                else:
                    generate_worksheet(str(lesson_path), None, str(worksheet_path))

                st.session_state.lesson_data["worksheet_path"] = str(worksheet_path)

            except Exception as e:
                st.error(f"Error generating worksheet: {e}")

    # Generate modified worksheet for struggling learners if selected (for single lessons or entire sequence)
    if st.session_state.lesson_data.get("generate_modified", False):
        alex_concerns = st.session_state.lesson_data.get("alex_concerns", [])
        if alex_concerns:
            with st.spinner("📝 Generating modified materials for struggling learners..."):
                try:
                    modified_lesson = generate_modified_worksheet(lesson_or_sequence, alex_concerns)
                    modified_path = temp_dir / "worksheet_modified.docx"
                    generate_worksheet_from_lesson(modified_lesson, str(modified_path))
                    st.session_state.lesson_data["modified_worksheet_path"] = str(modified_path)
                except Exception as e:
                    st.error(f"Error generating modified worksheet: {e}")

    # Generate extension worksheet for advanced learners if selected
    if st.session_state.lesson_data.get("generate_extension", False):
        marcus_concerns = st.session_state.lesson_data.get("marcus_concerns", [])
        if marcus_concerns:
            with st.spinner("🚀 Generating extension materials for advanced learners..."):
                try:
                    extension_lesson = generate_extension_worksheet(lesson_or_sequence, marcus_concerns)
                    extension_path = temp_dir / "worksheet_extension.docx"
                    generate_worksheet_from_lesson(extension_lesson, str(extension_path))
                    st.session_state.lesson_data["extension_worksheet_path"] = str(extension_path)
                except Exception as e:
                    st.error(f"Error generating extension worksheet: {e}")

    st.session_state.stage = 6
    st.rerun()


# Stage 6: Download
elif st.session_state.stage == 6:
    st.markdown('<div class="stage-header"><span class="stage-header-icon">🎉</span> Your Materials Are Ready!</div>', unsafe_allow_html=True)

    lesson_or_sequence = st.session_state.lesson_data["lesson"]
    is_sequence = lesson_or_sequence.get('is_sequence', False)

    if is_sequence:
        # Sequence complete message
        st.markdown(f"""
        <div class="success-box">
            <h3 style="color: {DARK_GREEN}; margin-top: 0;">✅ Lesson Sequence Complete!</h3>
            <p><strong>{lesson_or_sequence.get('sequence_title', 'Your Sequence')}</strong></p>
            <p>Grade: {lesson_or_sequence.get('grade_level')} | {lesson_or_sequence.get('total_lessons')} lessons × {lesson_or_sequence.get('duration_per_lesson')} minutes</p>
            <p><strong>Competency:</strong> {lesson_or_sequence.get('competency', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Download buttons for each lesson
        st.markdown("### 📚 Download Materials by Lesson")

        sequence_materials = st.session_state.lesson_data.get("sequence_materials", [])
        for mat in sequence_materials:
            lesson_num = mat.get("lesson_number", 0)
            lesson_title = mat.get("title", f"Lesson {lesson_num}")

            st.markdown(f"#### Lesson {lesson_num}: {lesson_title}")
            col1, col2 = st.columns(2)

            with col1:
                slides_path = mat.get("slides_path")
                if slides_path and Path(slides_path).exists():
                    with open(slides_path, "rb") as f:
                        st.download_button(
                            label=f"📊 Slides - Lesson {lesson_num}",
                            data=f.read(),
                            file_name=f"lesson_{st.session_state.session_id}_L{lesson_num}_slides.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True,
                            key=f"download_slides_{lesson_num}"
                        )

            with col2:
                worksheet_path = mat.get("worksheet_path")
                if worksheet_path and Path(worksheet_path).exists():
                    with open(worksheet_path, "rb") as f:
                        st.download_button(
                            label=f"📝 Worksheet - Lesson {lesson_num}",
                            data=f.read(),
                            file_name=f"lesson_{st.session_state.session_id}_L{lesson_num}_worksheet.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                            key=f"download_worksheet_{lesson_num}"
                        )

    else:
        # Single lesson complete message
        st.markdown(f"""
        <div class="success-box">
            <h3 style="color: {DARK_GREEN}; margin-top: 0;">✅ Lesson Complete!</h3>
            <p><strong>{lesson_or_sequence.get('title', 'Your Lesson')}</strong></p>
            <p>Grade: {lesson_or_sequence.get('grade_level')} | Duration: {lesson_or_sequence.get('duration')} minutes</p>
            <p><strong>Objective:</strong> {lesson_or_sequence.get('objective', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### 📊 Slide Deck")
            slides_path = st.session_state.lesson_data.get("slides_path")
            if slides_path and Path(slides_path).exists():
                with open(slides_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PowerPoint",
                        data=f.read(),
                        file_name=f"lesson_{st.session_state.session_id}_slides.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )
                st.caption("Includes hidden first slide with lesson plan for teachers")
            else:
                st.warning("Slides not available")

        with col2:
            st.markdown(f"### 📝 Student Worksheet")
            worksheet_path = st.session_state.lesson_data.get("worksheet_path")
            if worksheet_path and Path(worksheet_path).exists():
                with open(worksheet_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download Worksheet",
                        data=f.read(),
                        file_name=f"lesson_{st.session_state.session_id}_worksheet.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                st.caption("Formatted with answer space for students")
            else:
                st.warning("Worksheet not available")

    # Additional differentiated materials section
    modified_path = st.session_state.lesson_data.get("modified_worksheet_path")
    extension_path = st.session_state.lesson_data.get("extension_worksheet_path")

    if modified_path or extension_path:
        st.divider()
        st.markdown("### 🎯 Differentiated Materials")

        diff_col1, diff_col2 = st.columns(2)

        with diff_col1:
            if modified_path and Path(modified_path).exists():
                st.markdown(f"#### 📚 Modified Version")
                st.markdown(f'<p style="color: #e53935; font-size: 0.85rem;">For struggling learners / ELL students</p>', unsafe_allow_html=True)
                with open(modified_path, "rb") as f:
                    content = f.read()
                st.download_button(
                    label="⬇️ Download Modified Worksheet",
                    data=content,
                    file_name=f"lesson_{st.session_state.session_id}_worksheet_modified.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                st.caption("Same objectives with added scaffolds: word banks, sentence starters, visual supports")

        with diff_col2:
            if extension_path and Path(extension_path).exists():
                st.markdown(f"#### 🚀 Extension Version")
                st.markdown(f'<p style="color: #2196f3; font-size: 0.85rem;">For advanced / gifted learners</p>', unsafe_allow_html=True)
                with open(extension_path, "rb") as f:
                    content = f.read()
                st.download_button(
                    label="⬇️ Download Extension Worksheet",
                    data=content,
                    file_name=f"lesson_{st.session_state.session_id}_worksheet_extension.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
                st.caption("Same objectives with added depth: complex questions, research prompts, creative challenges")

    st.divider()

    # Show lesson details in readable format
    with st.expander("📋 View Full Lesson Plan"):
        st.markdown(format_lesson_display(lesson_or_sequence), unsafe_allow_html=True)

    # Persona feedback summary
    if "persona_feedback" in st.session_state.lesson_data:
        with st.expander("👥 View Persona Feedback Summary"):
            for fb in st.session_state.lesson_data["persona_feedback"]:
                persona = PERSONAS.get(fb.get("persona_key", ""), {})
                rating = fb.get("overall_rating", 3)
                stars = "⭐" * rating
                st.markdown(f"""
                **{persona.get('icon', '')} {fb.get('persona_name')}** ({persona.get('type', '')}) — {stars}

                _{fb.get('reaction', '')}_
                """)
                st.divider()

    st.markdown("---")

    # Check if there are more competencies in the queue
    current_idx = st.session_state.current_competency_index
    total_competencies = len(st.session_state.competency_queue)

    if current_idx < total_competencies - 1:
        # More competencies to process
        next_comp = st.session_state.competency_queue[current_idx + 1]
        remaining = total_competencies - current_idx - 1

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border: 2px solid #1976d2; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
            <p style="color: #1565c0; font-weight: 700; font-size: 1.1rem; margin: 0 0 0.5rem 0;">📋 {remaining} More Competenc{"ies" if remaining > 1 else "y"} Remaining</p>
            <p style="color: #424242; margin: 0 0 0.5rem 0;"><strong>Next up:</strong> {next_comp['competency'][:80]}{"..." if len(next_comp['competency']) > 80 else ""}</p>
            <p style="color: #666; font-size: 0.85rem; margin: 0;">{next_comp['lesson_count']} lesson{"s" if next_comp['lesson_count'] > 1 else ""}</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("➡️ Continue to Next Competency", type="primary", use_container_width=True):
                # Store completed competency
                st.session_state.completed_competencies.append({
                    "input": st.session_state.lesson_data.get("input"),
                    "lesson": st.session_state.lesson_data.get("lesson"),
                    "slides_path": st.session_state.lesson_data.get("slides_path"),
                    "worksheet_path": st.session_state.lesson_data.get("worksheet_path")
                })
                start_next_competency()
                st.rerun()
        with col2:
            if st.button("🏁 Finish & Start Over", use_container_width=True):
                reset_session()
                st.rerun()
    else:
        # All competencies complete
        if total_competencies > 1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); border: 2px solid {LIGHT_GREEN}; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;">
                <p style="color: {DARK_GREEN}; font-weight: 700; font-size: 1.1rem; margin: 0;">🎉 All {total_competencies} Competencies Complete!</p>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🎉 Design More Lessons", type="primary", use_container_width=True):
            reset_session()
            st.rerun()
