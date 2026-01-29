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
from generate_worksheet import generate_worksheet
from generate_slides import generate_slides

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


def design_lesson_with_claude(input_data: dict, marzano_framework: str, knowledge: list = None, skills: list = None) -> dict:
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

    if lesson_count == 1:
        # Single lesson design
        prompt = f"""You are an expert instructional designer using Marzano's New Taxonomy.

Design a complete lesson based on this input:
- Competency: {input_data['competency']}
- Grade Level: {input_data['grade_level']}
- Duration: {input_data['duration']} minutes
- Lesson Type: {input_data['lesson_type']}
- Constraints: {input_data.get('constraints', 'None')}{knowledge_text}{skills_text}

Requirements:
1. Include activities at multiple Marzano levels (retrieval, comprehension, analysis, knowledge_utilization)
2. At least 40% of time should be higher-order thinking (analysis + knowledge_utilization)
3. Include vocabulary terms with definitions (especially related to the confirmed knowledge above)
4. Include an exit ticket or embedded assessment
5. Activities should help students master the confirmed skills listed above
6. For activities that would benefit from visuals, include a "visual_description" field describing what image/diagram would help

Return a JSON object with this exact structure:
{{
    "is_sequence": false,
    "title": "Lesson title",
    "grade_level": "{input_data['grade_level']}",
    "duration": {input_data['duration']},
    "lesson_type": "{input_data['lesson_type']}",
    "objective": "Students will be able to...",
    "vocabulary": [
        {{"word": "term1", "definition": "definition1"}},
        {{"word": "term2", "definition": "definition2"}}
    ],
    "activities": [
        {{
            "name": "Activity Name",
            "duration": 10,
            "marzano_level": "retrieval|comprehension|analysis|knowledge_utilization",
            "instructions": ["Step 1", "Step 2"],
            "materials": ["Material 1"],
            "student_output": "What students produce",
            "assessment_method": "How to assess",
            "visual_description": "Description of helpful image/diagram (or null if not needed)"
        }}
    ],
    "hidden_slide_content": {{
        "objective": "Learning objective",
        "agenda": [{{"activity": "Name", "duration": 10}}],
        "misconceptions": ["Common misconception 1"],
        "delivery_tips": ["Tip 1"]
    }},
    "assessment": {{
        "type": "exit_ticket",
        "description": "Brief description",
        "questions": ["Question 1", "Question 2"]
    }}
}}

MARZANO FRAMEWORK REFERENCE:
{marzano_framework[:3000]}

Return ONLY the JSON object, no other text."""
    else:
        # Multi-lesson sequence design
        prompt = f"""You are an expert instructional designer using Marzano's New Taxonomy.

Design a {lesson_count}-LESSON SEQUENCE based on this input:
- Competency: {input_data['competency']}
- Grade Level: {input_data['grade_level']}
- Duration per lesson: {input_data['duration']} minutes
- Total lessons: {lesson_count}
- Constraints: {input_data.get('constraints', 'None')}{knowledge_text}{skills_text}

SEQUENCE DESIGN REQUIREMENTS:
1. Each lesson should have a DISTINCT objective that builds toward the overall competency
2. Lesson 1 should focus more on retrieval/comprehension (introducing concepts)
3. Middle lessons should build analysis skills
4. Final lesson should emphasize knowledge utilization and synthesis
5. Vocabulary should be distributed across lessons (introduce new terms progressively)
6. Each lesson should have at least 40% higher-order thinking time
7. The sequence should tell a coherent learning story
8. For activities that would benefit from visuals, include a "visual_description" field

Return a JSON object with this exact structure:
{{
    "is_sequence": true,
    "sequence_title": "Overall sequence title",
    "competency": "{input_data['competency']}",
    "grade_level": "{input_data['grade_level']}",
    "total_lessons": {lesson_count},
    "duration_per_lesson": {input_data['duration']},
    "sequence_overview": "Brief description of how the lessons build toward mastery",
    "lessons": [
        {{
            "lesson_number": 1,
            "title": "Lesson 1 title",
            "lesson_type": "introducing",
            "objective": "Lesson 1 specific objective",
            "vocabulary": [{{"word": "term1", "definition": "def1"}}],
            "activities": [
                {{
                    "name": "Activity Name",
                    "duration": 10,
                    "marzano_level": "retrieval|comprehension|analysis|knowledge_utilization",
                    "instructions": ["Step 1", "Step 2"],
                    "materials": ["Material 1"],
                    "student_output": "What students produce",
                    "assessment_method": "How to assess",
                    "visual_description": "Description of helpful image/diagram (or null if not needed)"
                }}
            ],
            "hidden_slide_content": {{
                "objective": "Learning objective",
                "agenda": [{{"activity": "Name", "duration": 10}}],
                "misconceptions": ["Common misconception 1"],
                "delivery_tips": ["Tip 1"]
            }},
            "assessment": {{
                "type": "exit_ticket",
                "description": "Brief description",
                "questions": ["Question 1"]
            }}
        }}
    ]
}}

Include {lesson_count} lesson objects in the "lessons" array.

MARZANO FRAMEWORK REFERENCE:
{marzano_framework[:2500]}

Return ONLY the JSON object, no other text."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
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

Evaluate this ENTIRE SEQUENCE from {persona['name']}'s perspective. Consider:
1. Does the sequence build appropriately across lessons?
2. Is vocabulary introduced at the right pace?
3. Does cognitive complexity increase appropriately?
4. Will this student stay engaged across all {len(lessons)} lessons?
5. Are there adequate scaffolds/challenges throughout?

Return a JSON object:
{{
    "persona_key": "{persona_key}",
    "persona_name": "{persona['name']}",
    "overall_rating": 1-5,
    "reaction": "A 2-3 sentence description of how {persona['name']} would likely respond to this sequence over {len(lessons)} days",
    "concerns": [
        {{
            "id": "unique_id",
            "lesson": "all|1|2|3|4",
            "element": "vocabulary|instructions|scaffolding|pacing|engagement|challenge|progression",
            "issue": "Specific issue description",
            "severity": "high|medium|low",
            "recommendation": "Specific suggested fix"
        }}
    ],
    "strengths": ["What works well for this student across the sequence"]
}}

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

Evaluate this lesson from {persona['name']}'s perspective. Consider:
1. Would this student understand the vocabulary?
2. Are the instructions clear enough?
3. Is there adequate scaffolding?
4. Is the pacing appropriate?
5. Would this student be engaged?

Return a JSON object:
{{
    "persona_key": "{persona_key}",
    "persona_name": "{persona['name']}",
    "overall_rating": 1-5,
    "reaction": "A 2-3 sentence description of how {persona['name']} would likely respond to this lesson",
    "concerns": [
        {{
            "id": "unique_id",
            "element": "vocabulary|instructions|scaffolding|pacing|engagement|challenge",
            "issue": "Specific issue description",
            "severity": "high|medium|low",
            "recommendation": "Specific suggested fix"
        }}
    ],
    "strengths": ["What works well for this student"]
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

    if lesson_num:
        parts.append(f'''<div class="lesson-section" style="border-left: 4px solid {DARK_GREEN}; background: #f8faf8;">
<h4 style="color: {DARK_GREEN}; font-size: 1.2rem;">📅 Lesson {lesson_num}: {title}</h4>''')
    else:
        parts.append(f'''<div class="lesson-section">
<h4>📎 Lesson Overview</h4>
<p><strong>Title:</strong> {title}</p>''')

    parts.append(f'''<p><strong>Objective:</strong> {objective}</p>
<p><strong>Type:</strong> {lesson_type}</p>
<p><strong>Duration:</strong> {duration} minutes</p>
</div>''')

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

            instructions = act.get('instructions', [])
            instruction_items = ''.join([f"<li>{escape_html(step)}</li>" for step in instructions])

            # Materials
            materials = act.get('materials', [])
            materials_html = ""
            if materials:
                materials_list = ''.join([f"<li>{escape_html(m)}</li>" for m in materials])
                materials_html = f"<p><strong>Materials:</strong></p><ul>{materials_list}</ul>"

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

            card = f'''<div class="activity-card">
<div class="activity-name">{i}. {name}</div>
<div class="activity-meta">
<span>⏱️ {duration_act} min</span>
<span class="marzano-tag">{level_display}</span>
</div>
<p><strong>Instructions:</strong></p>
<ol>{instruction_items}</ol>
{materials_html}
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

        parts.append(f'''<div class="lesson-section">
<h4>✅ Assessment</h4>
<p><strong>Type:</strong> {assess_type}</p>
<p><strong>Questions:</strong></p>
<ol>{question_items}</ol>
</div>''')

    # Hidden slide content (teacher tips)
    hidden = lesson.get('hidden_slide_content', {})
    if hidden:
        misconceptions = hidden.get('misconceptions', [])
        tips = hidden.get('delivery_tips', [])
        if misconceptions or tips:
            parts.append('<div class="lesson-section"><h4>💡 Teacher Notes</h4>')
            if misconceptions:
                misc_items = ''.join([f"<li>{escape_html(m)}</li>" for m in misconceptions])
                parts.append(f'<p><strong>Watch for these misconceptions:</strong></p><ul>{misc_items}</ul>')
            if tips:
                tip_items = ''.join([f"<li>{escape_html(t)}</li>" for t in tips])
                parts.append(f'<p><strong>Delivery tips:</strong></p><ul>{tip_items}</ul>')
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
        total_lessons = lesson_or_sequence.get('total_lessons', 0)
        duration = lesson_or_sequence.get('duration_per_lesson', 0)

        parts.append(f'''<div class="lesson-section" style="background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);">
<h4>📚 Sequence Overview</h4>
<p><strong>Title:</strong> {title}</p>
<p><strong>Competency:</strong> {competency}</p>
<p><strong>Duration:</strong> {total_lessons} lessons × {duration} minutes</p>
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


def generate_modified_worksheet(lesson: dict, concerns: list) -> bytes:
    """Generate a modified worksheet for struggling learners based on Alex's concerns."""
    client = get_claude_client()

    concerns_text = "\n".join([f"- {c.get('element', 'Issue')}: {c.get('issue', '')} (Recommendation: {c.get('recommendation', '')})" for c in concerns])

    prompt = f"""Create a MODIFIED version of this lesson's student worksheet designed for struggling learners and ELL students.

ORIGINAL LESSON:
Title: {lesson.get('title', 'Lesson')}
Objective: {lesson.get('objective', '')}
Grade Level: {lesson.get('grade_level', '')}

Activities:
{json.dumps(lesson.get('activities', []), indent=2)}

Vocabulary:
{json.dumps(lesson.get('vocabulary', []), indent=2)}

CONCERNS TO ADDRESS (from struggling learner persona):
{concerns_text}

Create a modified worksheet that:
1. KEEPS THE SAME LEARNING OBJECTIVES
2. Addresses each concern listed above
3. Includes these scaffolds as appropriate:
   - Simplified vocabulary with definitions provided inline
   - Sentence starters/frames for written responses
   - Word banks for key terms
   - Visual supports (describe where images/diagrams should go)
   - Chunked instructions (one step at a time)
   - Reduced text density (fewer questions per page, more white space)
   - Pre-taught vocabulary section at the top
   - Check-for-understanding boxes after each section

Format the worksheet as clean, printable content with clear sections.
Use simple formatting: headers with === underneath, bullet points with -, numbered lists.
Include [VISUAL: description] placeholders where images would help.

Start with a header:
MODIFIED WORKSHEET - Additional Support Version
{lesson.get('title', 'Lesson')}
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


def generate_extension_worksheet(lesson: dict, concerns: list) -> bytes:
    """Generate an extension worksheet for advanced learners based on Marcus's concerns."""
    client = get_claude_client()

    concerns_text = "\n".join([f"- {c.get('element', 'Issue')}: {c.get('issue', '')} (Recommendation: {c.get('recommendation', '')})" for c in concerns])

    prompt = f"""Create an EXTENSION version of this lesson's student worksheet designed for advanced/gifted learners.

ORIGINAL LESSON:
Title: {lesson.get('title', 'Lesson')}
Objective: {lesson.get('objective', '')}
Grade Level: {lesson.get('grade_level', '')}

Activities:
{json.dumps(lesson.get('activities', []), indent=2)}

Vocabulary:
{json.dumps(lesson.get('vocabulary', []), indent=2)}

CONCERNS TO ADDRESS (from high-achieving student persona):
{concerns_text}

Create an extension worksheet that:
1. KEEPS THE SAME CORE LEARNING OBJECTIVES but adds depth
2. Addresses each concern listed above (typically about ceiling/challenge)
3. Includes these extensions as appropriate:
   - Deeper, more complex questions that require synthesis
   - Open-ended investigation prompts
   - Connections to advanced concepts or cross-curricular links
   - Independent research opportunities
   - Creative application challenges
   - "What if?" scenarios that extend thinking
   - Opportunities to teach/explain to others
   - Self-directed learning paths

Format the worksheet as clean, printable content with clear sections.
Use simple formatting: headers with === underneath, bullet points with -, numbered lists.

Start with a header:
EXTENSION WORKSHEET - Advanced Challenge Version
{lesson.get('title', 'Lesson')}

Note: Students should complete the core worksheet first, then work on these extensions.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


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


# Stage 1: Input Requirements
if st.session_state.stage == 1:
    st.markdown('<div class="stage-header"><span class="stage-header-icon">📝</span> Define Your Lessons</div>', unsafe_allow_html=True)

    # Initialize temp competencies list in session state if not exists
    if "temp_competencies" not in st.session_state:
        st.session_state.temp_competencies = []

    # Shared settings
    st.markdown("### General Settings")
    col1, col2 = st.columns(2)
    with col1:
        grade_level = st.selectbox(
            "Grade Level",
            ["6th grade", "7th grade", "8th grade", "9th grade",
             "10th grade", "11th grade", "12th grade", "AP", "College"],
            key="grade_level_input"
        )
    with col2:
        duration = st.slider("Lesson Duration (minutes)", 30, 90, 50, 5, key="duration_input")

    constraints = st.text_area(
        "Any constraints? (optional)",
        placeholder="e.g., Limited technology, students already know X...",
        height=68,
        key="constraints_input"
    )

    st.divider()

    # Competency input section
    st.markdown("### Add Competencies")
    st.markdown('<p style="color: #666; font-size: 0.9rem;">Add one or more competencies. Each can span 1-4 lessons.</p>', unsafe_allow_html=True)

    with st.form("add_competency_form"):
        competency = st.text_area(
            "Competency",
            placeholder="e.g., Students will analyze primary sources to evaluate historical claims",
            help="State what students will DO, not just what they'll learn about",
            height=80
        )

        comp_col1, comp_col2 = st.columns(2)
        with comp_col1:
            lesson_count = st.selectbox(
                "Number of lessons for this competency",
                [1, 2, 3, 4],
                format_func=lambda x: f"{x} lesson{'s' if x > 1 else ''}"
            )
        with comp_col2:
            lesson_type = st.selectbox(
                "Primary lesson type",
                ["introducing", "practicing", "applying", "synthesizing", "novel_application"],
                format_func=lambda x: {
                    "introducing": "Introducing New Content",
                    "practicing": "Practicing Skills",
                    "applying": "Applying Knowledge",
                    "synthesizing": "Synthesizing Ideas",
                    "novel_application": "Novel Application"
                }.get(x, x)
            )

        add_competency = st.form_submit_button("➕ Add Competency", use_container_width=True)

        if add_competency and competency.strip():
            st.session_state.temp_competencies.append({
                "competency": competency.strip(),
                "lesson_count": lesson_count,
                "lesson_type": lesson_type,
                "grade_level": grade_level,
                "duration": duration,
                "constraints": constraints
            })
            st.rerun()

    # Display queued competencies
    if st.session_state.temp_competencies:
        st.divider()
        st.markdown("### Queued Competencies")

        total_lessons = sum(c["lesson_count"] for c in st.session_state.temp_competencies)
        st.markdown(f'<p style="color: {DARK_GREEN}; font-weight: 600;">Total: {len(st.session_state.temp_competencies)} competenc{"ies" if len(st.session_state.temp_competencies) > 1 else "y"} → {total_lessons} lesson{"s" if total_lessons > 1 else ""}</p>', unsafe_allow_html=True)

        for i, comp in enumerate(st.session_state.temp_competencies):
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                lesson_word = "lesson" if comp["lesson_count"] == 1 else "lessons"
                st.markdown(f"""
                <div style="background: #f8faf8; border-left: 3px solid {LIGHT_GREEN}; padding: 0.75rem 1rem; margin: 0.5rem 0; border-radius: 0 8px 8px 0;">
                    <strong style="color: {DARK_GREEN};">Competency {i+1}</strong> ({comp["lesson_count"]} {lesson_word})<br>
                    <span style="color: #555;">{comp["competency"][:100]}{"..." if len(comp["competency"]) > 100 else ""}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"remove_comp_{i}"):
                    st.session_state.temp_competencies.pop(i)
                    st.rerun()

        st.divider()

        # Start button
        if st.button("🚀 Start Designing Lessons", type="primary", use_container_width=True):
            if st.session_state.temp_competencies:
                # Transfer to competency queue
                st.session_state.competency_queue = st.session_state.temp_competencies.copy()
                st.session_state.current_competency_index = 0
                st.session_state.temp_competencies = []

                # Load first competency
                first_comp = st.session_state.competency_queue[0]
                st.session_state.lesson_data["input"] = first_comp
                st.session_state.session_id = str(uuid.uuid4())[:8]
                st.session_state.stage = 2
                st.rerun()
    else:
        st.info("👆 Add at least one competency to get started.")


# Stage 2: Review Knowledge & Skills
elif st.session_state.stage == 2:
    st.markdown('<div class="stage-header"><span class="stage-header-icon">🔍</span> Review Knowledge & Skills</div>', unsafe_allow_html=True)

    input_data = st.session_state.lesson_data["input"]

    st.markdown(f"""
    <div class="info-box">
        <strong>Competency:</strong> {input_data['competency']}<br>
        <strong>Grade:</strong> {input_data['grade_level']}
    </div>
    """, unsafe_allow_html=True)

    # Extract knowledge and skills if not already done
    if "knowledge_skills" not in st.session_state.lesson_data:
        with st.spinner("🔍 Analyzing competency to extract underlying knowledge and skills..."):
            try:
                ks_data = extract_knowledge_skills(input_data["competency"], input_data["grade_level"])
                st.session_state.lesson_data["knowledge_skills"] = ks_data
                # Initialize selections
                st.session_state.lesson_data["selected_knowledge"] = {
                    k["id"]: True for k in ks_data.get("knowledge", [])
                }
                st.session_state.lesson_data["selected_skills"] = {
                    s["id"]: True for s in ks_data.get("skills", [])
                }
                st.rerun()
            except Exception as e:
                st.error(f"Error extracting knowledge/skills: {str(e)}")
                if st.button("Try Again"):
                    st.rerun()
    else:
        ks_data = st.session_state.lesson_data["knowledge_skills"]

        st.markdown("""
        <p style="color: #666; margin-bottom: 1rem;">
        Review the knowledge and skills below. Uncheck any that aren't relevant,
        and add your own if something is missing.
        </p>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # Knowledge column
        with col1:
            st.markdown(f'<h4 style="color: {DARK_GREEN};">📚 Knowledge (What students must KNOW)</h4>', unsafe_allow_html=True)

            for item in ks_data.get("knowledge", []):
                item_id = item["id"]
                is_selected = st.checkbox(
                    item["item"],
                    value=st.session_state.lesson_data["selected_knowledge"].get(item_id, True),
                    key=f"know_{item_id}",
                    help=f"Category: {item.get('category', 'concept').title()}"
                )
                st.session_state.lesson_data["selected_knowledge"][item_id] = is_selected

            # Add custom knowledge
            st.markdown("---")
            new_knowledge = st.text_input(
                "Add custom knowledge item:",
                key="new_knowledge_input",
                placeholder="e.g., Understanding of binary numbers"
            )
            if st.button("➕ Add Knowledge", key="add_knowledge_btn"):
                if new_knowledge.strip():
                    new_id = f"k_custom_{len(ks_data['knowledge']) + 1}"
                    ks_data["knowledge"].append({
                        "id": new_id,
                        "item": new_knowledge.strip(),
                        "category": "custom"
                    })
                    st.session_state.lesson_data["selected_knowledge"][new_id] = True
                    st.rerun()

        # Skills column
        with col2:
            st.markdown(f'<h4 style="color: {DARK_GREEN};">🛠️ Skills (What students must DO)</h4>', unsafe_allow_html=True)

            for item in ks_data.get("skills", []):
                item_id = item["id"]
                is_selected = st.checkbox(
                    item["item"],
                    value=st.session_state.lesson_data["selected_skills"].get(item_id, True),
                    key=f"skill_{item_id}",
                    help=f"Category: {item.get('category', 'cognitive').title()}"
                )
                st.session_state.lesson_data["selected_skills"][item_id] = is_selected

            # Add custom skill
            st.markdown("---")
            new_skill = st.text_input(
                "Add custom skill:",
                key="new_skill_input",
                placeholder="e.g., Debug simple programs"
            )
            if st.button("➕ Add Skill", key="add_skill_btn"):
                if new_skill.strip():
                    new_id = f"s_custom_{len(ks_data['skills']) + 1}"
                    ks_data["skills"].append({
                        "id": new_id,
                        "item": new_skill.strip(),
                        "category": "custom"
                    })
                    st.session_state.lesson_data["selected_skills"][new_id] = True
                    st.rerun()

        st.divider()

        # Count selections
        selected_k = sum(1 for v in st.session_state.lesson_data["selected_knowledge"].values() if v)
        selected_s = sum(1 for v in st.session_state.lesson_data["selected_skills"].values() if v)

        st.markdown(f"**Selected:** {selected_k} knowledge items, {selected_s} skills")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("← Back", use_container_width=True):
                del st.session_state.lesson_data["knowledge_skills"]
                st.session_state.stage = 1
                st.rerun()
        with col2:
            if st.button("Continue to Lesson Design →", type="primary", use_container_width=True):
                # Store confirmed knowledge and skills
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
                st.session_state.stage = 3
                st.rerun()


# Stage 3: Design Lesson
elif st.session_state.stage == 3:
    lesson_count = st.session_state.lesson_data["input"].get("lesson_count", 1)
    header_text = "Designing Your Lesson Sequence" if lesson_count > 1 else "Designing Your Lesson"
    st.markdown(f'<div class="stage-header"><span class="stage-header-icon">🎨</span> {header_text}</div>', unsafe_allow_html=True)

    input_data = st.session_state.lesson_data["input"]

    lesson_info = f"{lesson_count} lessons × {input_data['duration']} min" if lesson_count > 1 else f"{input_data['duration']} min"

    st.markdown(f"""
    <div class="info-box">
        <strong>Designing for:</strong> {input_data['competency']}<br>
        <strong>Grade:</strong> {input_data['grade_level']} |
        <strong>Duration:</strong> {lesson_info} |
        <strong>Type:</strong> {input_data['lesson_type'].replace('_', ' ').title()}
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

    with st.spinner("🎨 Claude is designing your lesson using Marzano's taxonomy..."):
        try:
            marzano = load_marzano_framework()
            lesson = design_lesson_with_claude(input_data, marzano, confirmed_knowledge, confirmed_skills)

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
    st.markdown('<div class="stage-header"><span class="stage-header-icon">👥</span> Student Persona Review</div>', unsafe_allow_html=True)

    lesson_or_sequence = st.session_state.lesson_data["lesson"]
    is_sequence = lesson_or_sequence.get('is_sequence', False)

    # Show current competency info
    current_idx = st.session_state.current_competency_index
    total_competencies = len(st.session_state.competency_queue)
    if total_competencies > 1:
        st.markdown(f'<p style="color: {LIGHT_GREEN}; font-weight: 600;">Competency {current_idx + 1} of {total_competencies}</p>', unsafe_allow_html=True)

    # Show lesson/sequence in readable format
    expander_title = "📋 View Your Lesson Sequence" if is_sequence else "📋 View Your Lesson Design"
    with st.expander(expander_title, expanded=False):
        st.markdown(format_lesson_display(lesson_or_sequence), unsafe_allow_html=True)

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
        total_lessons = lesson_or_sequence.get("total_lessons", 1)
    else:
        all_activities = lesson_or_sequence.get("activities", [])
        total_time = sum(a["duration"] for a in all_activities)
        higher_order_time = sum(
            a["duration"] for a in all_activities
            if a.get("marzano_level") in ["analysis", "knowledge_utilization"]
        )
        total_lessons = 1

    cognitive_percent = (higher_order_time / total_time * 100) if total_time > 0 else 0

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

    st.divider()

    # Persona feedback
    if "persona_feedback" not in st.session_state.lesson_data:
        st.markdown("### 👥 Running lesson through student personas...")

        feedback_list = []
        progress = st.progress(0)

        for i, (persona_key, persona) in enumerate(PERSONAS.items()):
            with st.spinner(f"Getting feedback from {persona['name']} ({persona['type']})..."):
                try:
                    feedback = get_persona_feedback(lesson, persona_key, persona)
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

        st.markdown("### 👥 Persona Feedback")

        # Display each persona's feedback
        for feedback in feedback_list:
            persona_key = feedback.get("persona_key", "")
            persona = PERSONAS.get(persona_key, {})

            rating = feedback.get("overall_rating", 3)
            stars = "⭐" * rating + "☆" * (5 - rating)

            st.markdown(f"""
            <div class="persona-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span style="font-size: 1.5rem;">{persona.get('icon', '👤')}</span>
                        <span class="persona-name">{feedback.get('persona_name', 'Student')}</span>
                        <div class="persona-type">{persona.get('type', '')}</div>
                    </div>
                    <div class="rating">{stars}</div>
                </div>
                <div class="persona-traits">
                    <strong>Key traits:</strong> {', '.join(persona.get('traits', [])[:2])}
                </div>
                <p style="margin-top: 0.75rem; font-style: italic; color: #555;">
                    "{feedback.get('reaction', 'No reaction provided.')}"
                </p>
            </div>
            """, unsafe_allow_html=True)

            # Show concerns with checkboxes
            concerns = feedback.get("concerns", [])
            if concerns:
                st.markdown(f"**Concerns from {feedback.get('persona_name')}:**")
                for idx, concern in enumerate(concerns):
                    concern_id = concern.get("id", f"{persona_key}_{idx}")
                    # Create a unique key combining persona and index
                    unique_key = f"{persona_key}_{idx}_{concern_id}"
                    severity = concern.get("severity", "medium")

                    col1, col2 = st.columns([0.05, 0.95])
                    with col1:
                        # Checkbox for selecting this concern
                        is_selected = st.checkbox(
                            "",
                            value=st.session_state.selected_feedback.get(unique_key, True),
                            key=f"cb_{unique_key}",
                            label_visibility="collapsed"
                        )
                        st.session_state.selected_feedback[unique_key] = is_selected

                    with col2:
                        severity_class = f"concern-{severity}"
                        st.markdown(f"""
                        <div class="{severity_class}">
                            <strong>{concern.get('element', 'Issue').title()}</strong>
                            <span style="font-size: 0.75rem; color: #888;">({severity} priority)</span><br>
                            {concern.get('issue', '')}<br>
                            <em style="color: #666;">💡 {concern.get('recommendation', '')}</em>
                        </div>
                        """, unsafe_allow_html=True)

            # Add option to generate modified/extension materials for Alex and Marcus
            if persona_key == "alex" and concerns:
                st.markdown("")
                st.markdown(f'''
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border: 2px solid #1976d2; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                    <p style="color: #1565c0; font-weight: 600; margin: 0 0 0.5rem 0;">📝 Differentiated Materials Option</p>
                    <p style="color: #424242; font-size: 0.9rem; margin: 0;">Create an additional worksheet with scaffolds (word banks, sentence starters, visual supports) for struggling learners.</p>
                </div>
                ''', unsafe_allow_html=True)
                st.session_state.generate_modified_materials = st.checkbox(
                    "Generate modified materials for struggling learners",
                    value=st.session_state.generate_modified_materials,
                    key="generate_modified_checkbox"
                )
            elif persona_key == "marcus" and concerns:
                st.markdown("")
                st.markdown(f'''
                <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); border: 2px solid #1976d2; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;">
                    <p style="color: #1565c0; font-weight: 600; margin: 0 0 0.5rem 0;">🚀 Differentiated Materials Option</p>
                    <p style="color: #424242; font-size: 0.9rem; margin: 0;">Create an additional worksheet with challenges (deeper questions, research prompts, creative extensions) for advanced learners.</p>
                </div>
                ''', unsafe_allow_html=True)
                st.session_state.generate_extension_materials = st.checkbox(
                    "Generate extension materials for advanced learners",
                    value=st.session_state.generate_extension_materials,
                    key="generate_extension_checkbox"
                )

            st.markdown("")  # Spacing

        st.divider()

        # Count selected concerns
        selected_count = sum(1 for v in st.session_state.selected_feedback.values() if v)
        total_concerns = len(st.session_state.selected_feedback)

        st.markdown(f"**Selected {selected_count} of {total_concerns} concerns for redesign**")

        # Show what additional materials will be generated
        additional_materials = []
        if st.session_state.generate_modified_materials:
            additional_materials.append("modified worksheet (struggling learners)")
        if st.session_state.generate_extension_materials:
            additional_materials.append("extension worksheet (advanced learners)")

        if additional_materials:
            st.markdown(f"**Additional materials to generate:** {', '.join(additional_materials)}")

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
                    modified_content = generate_modified_worksheet(lesson_or_sequence, alex_concerns)
                    modified_path = temp_dir / "worksheet_modified.txt"
                    with open(modified_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                    st.session_state.lesson_data["modified_worksheet_path"] = str(modified_path)
                except Exception as e:
                    st.error(f"Error generating modified worksheet: {e}")

    # Generate extension worksheet for advanced learners if selected
    if st.session_state.lesson_data.get("generate_extension", False):
        marcus_concerns = st.session_state.lesson_data.get("marcus_concerns", [])
        if marcus_concerns:
            with st.spinner("🚀 Generating extension materials for advanced learners..."):
                try:
                    extension_content = generate_extension_worksheet(lesson_or_sequence, marcus_concerns)
                    extension_path = temp_dir / "worksheet_extension.txt"
                    with open(extension_path, 'w', encoding='utf-8') as f:
                        f.write(extension_content)
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
                with open(modified_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.download_button(
                    label="⬇️ Download Modified Worksheet",
                    data=content,
                    file_name=f"lesson_{st.session_state.session_id}_worksheet_modified.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.caption("Same objectives with added scaffolds: word banks, sentence starters, visual supports")

                with st.expander("Preview modified worksheet"):
                    st.text(content[:2000] + ("..." if len(content) > 2000 else ""))

        with diff_col2:
            if extension_path and Path(extension_path).exists():
                st.markdown(f"#### 🚀 Extension Version")
                st.markdown(f'<p style="color: #2196f3; font-size: 0.85rem;">For advanced / gifted learners</p>', unsafe_allow_html=True)
                with open(extension_path, "r", encoding="utf-8") as f:
                    content = f.read()
                st.download_button(
                    label="⬇️ Download Extension Worksheet",
                    data=content,
                    file_name=f"lesson_{st.session_state.session_id}_worksheet_extension.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                st.caption("Same objectives with added depth: complex questions, research prompts, creative challenges")

                with st.expander("Preview extension worksheet"):
                    st.text(content[:2000] + ("..." if len(content) > 2000 else ""))

    st.divider()

    # Show lesson details in readable format
    with st.expander("📋 View Full Lesson Plan"):
        st.markdown(format_lesson_display(lesson), unsafe_allow_html=True)

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
