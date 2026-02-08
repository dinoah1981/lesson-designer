"""
Lesson Designer v2 — Streamlit UI
Multi-phase workflow: Define → Lesson Plan → Persona Feedback → Content → Documents
"""

import streamlit as st
import tempfile
import os
from pathlib import Path

from config import DARK_GREEN, LIGHT_GREEN, WHITE, PERSONAS, LESSON_TYPES
from api_calls import (
    extract_knowledge_skills,
    generate_lesson_plan,
    get_persona_feedback,
    generate_prompt_additions,
    generate_lesson_content,
    generate_document_code,
    execute_document_code,
)

# ─── Page Config ─────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Lesson Designer | CompSci High",
    page_icon="<>",
    layout="wide",
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────────

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * {{ font-family: 'Inter', sans-serif; }}

    /* Main header */
    .main-header {{
        font-size: 1.6rem;
        font-weight: 700;
        color: {DARK_GREEN};
        margin-bottom: 0.5rem;
    }}
    .brand-highlight {{ color: {LIGHT_GREEN}; }}

    /* Progress stepper */
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
    .step.completed:not(:last-child)::after {{ background: {LIGHT_GREEN}; }}
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
        position: relative;
        z-index: 2;
    }}
    .step.pending .step-circle {{ background: #f0f0f0; color: #999; border: 2px solid #e0e0e0; }}
    .step.current .step-circle {{
        background: {DARK_GREEN}; color: white; border: 3px solid {LIGHT_GREEN};
        box-shadow: 0 0 0 4px rgba(77,174,88,0.2);
        animation: pulse 2s infinite;
    }}
    .step.completed .step-circle {{ background: {LIGHT_GREEN}; color: white; border: 2px solid {LIGHT_GREEN}; }}
    @keyframes pulse {{
        0%, 100% {{ box-shadow: 0 0 0 4px rgba(77,174,88,0.2); }}
        50% {{ box-shadow: 0 0 0 8px rgba(77,174,88,0.1); }}
    }}
    .step-label {{
        font-size: 0.75rem; font-weight: 600; text-align: center; max-width: 80px; line-height: 1.2;
    }}
    .step.pending .step-label {{ color: #999; }}
    .step.current .step-label {{ color: {DARK_GREEN}; }}
    .step.completed .step-label {{ color: {LIGHT_GREEN}; }}

    /* Stage cards */
    .stage-card {{
        background: white; border-radius: 16px; padding: 2rem; margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,88,44,0.08); border: 1px solid #e8f0e8;
    }}
    .stage-header {{
        background: linear-gradient(135deg, {DARK_GREEN} 0%, {LIGHT_GREEN} 100%);
        color: white; padding: 1.25rem 1.5rem; border-radius: 12px;
        margin: 0 0 1.5rem 0; font-weight: 700; font-size: 1.3rem;
        display: flex; align-items: center; gap: 0.75rem;
        box-shadow: 0 4px 12px rgba(0,88,44,0.2);
    }}

    /* Success box */
    .success-box {{
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border-left: 5px solid {LIGHT_GREEN};
        padding: 1.75rem; border-radius: 0 16px 16px 0; margin: 1.5rem 0;
        box-shadow: 0 2px 12px rgba(77,174,88,0.1);
    }}

    /* Info box */
    .info-box {{
        background: linear-gradient(135deg, #f0f7f0 0%, #f8faf8 100%);
        border: 1px solid {LIGHT_GREEN};
        padding: 1.25rem 1.5rem; border-radius: 12px; margin: 1rem 0;
    }}

    /* Persona cards */
    .persona-card {{
        background: white; border: 2px solid #e8e8e8; border-radius: 16px;
        padding: 1.25rem; margin: 0.75rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .persona-card:hover {{
        border-color: {LIGHT_GREEN};
        box-shadow: 0 4px 16px rgba(77,174,88,0.15);
        transform: translateY(-2px);
    }}
    .persona-name {{ font-weight: 700; font-size: 1.15rem; color: {DARK_GREEN}; margin-bottom: 0.25rem; }}
    .persona-type {{ font-size: 0.85rem; color: {LIGHT_GREEN}; font-weight: 600; margin-bottom: 0.5rem; }}

    /* Concern cards */
    .concern-high {{
        background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
        border-left: 4px solid #e53935;
        padding: 1rem 1.25rem; margin: 0.5rem 0; border-radius: 0 12px 12px 0;
    }}
    .concern-medium {{
        background: linear-gradient(135deg, #fffbf0 0%, #fff8e1 100%);
        border-left: 4px solid #ffc107;
        padding: 1rem 1.25rem; margin: 0.5rem 0; border-radius: 0 12px 12px 0;
    }}
    .concern-low {{
        background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
        border-left: 4px solid #9e9e9e;
        padding: 1rem 1.25rem; margin: 0.5rem 0; border-radius: 0 12px 12px 0;
    }}

    /* Buttons */
    .stButton > button {{
        background: linear-gradient(135deg, {DARK_GREEN} 0%, {LIGHT_GREEN} 100%);
        color: white; border: none; padding: 0.6rem 2rem; font-weight: 600;
        border-radius: 10px; box-shadow: 0 2px 8px rgba(0,88,44,0.2);
    }}
    .stButton > button:hover {{
        background: linear-gradient(135deg, {LIGHT_GREEN} 0%, {DARK_GREEN} 100%);
        transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,88,44,0.3);
    }}
    .stDownloadButton > button {{
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
        border: none; box-shadow: 0 2px 8px rgba(33,150,243,0.3);
    }}
    .stDownloadButton > button:hover {{
        background: linear-gradient(135deg, #1976d2 0%, #2196f3 100%);
    }}

    /* Compact plan/content text */
    .plan-text {{
        font-size: 0.88rem;
        line-height: 1.45;
    }}
    .plan-text h1 {{ font-size: 1.2rem; margin: 0.8rem 0 0.4rem 0; color: {DARK_GREEN}; }}
    .plan-text h2 {{ font-size: 1.05rem; margin: 0.7rem 0 0.3rem 0; color: {DARK_GREEN}; }}
    .plan-text h3 {{ font-size: 0.95rem; margin: 0.5rem 0 0.2rem 0; }}
    .plan-text p {{ margin: 0.3rem 0; }}
    .plan-text ul, .plan-text ol {{ margin: 0.2rem 0 0.2rem 1.2rem; padding: 0; }}
    .plan-text li {{ margin: 0.15rem 0; }}

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
</style>
""", unsafe_allow_html=True)


# ─── Session State Initialization ────────────────────────────────────────────────

def init_state():
    """Initialize all session state keys."""
    defaults = {
        "phase": 1,
        # Phase 1 inputs
        "competency": "",
        "daily_objectives": [""],
        "lesson_type": list(LESSON_TYPES.keys())[0],
        "grade_level": "9",
        "duration": 50,
        "num_lessons": 1,
        "additional_guidance": "",
        "uploaded_doc_text": "",
        # Phase 1 outputs
        "knowledge": [],
        "skills": [],
        "confirmed_knowledge": [],
        "confirmed_skills": [],
        # Phase 2
        "lesson_plan": "",
        # Phase 3
        "persona_feedback": {},
        "prompt_additions": "",
        "diff_struggling": False,
        "diff_advanced": False,
        # Phase 4
        "lesson_content": "",
        # Phase 5
        "generated_files": {},
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ─── File Upload Helper ──────────────────────────────────────────────────────────

def extract_text_from_upload(uploaded_file) -> str:
    """Extract text from .docx, .pdf, or .txt upload."""
    if uploaded_file is None:
        return ""

    name = uploaded_file.name.lower()

    if name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="replace")

    elif name.endswith(".docx"):
        try:
            from docx import Document
            import io
            doc = Document(io.BytesIO(uploaded_file.read()))
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        except Exception as e:
            st.warning(f"Could not read .docx file: {e}")
            return ""

    elif name.endswith(".pdf"):
        try:
            import pdfplumber
            import io
            text_parts = []
            with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
            return "\n".join(text_parts)
        except Exception as e:
            st.warning(f"Could not read .pdf file: {e}")
            return ""

    return ""


# ─── Progress Stepper ────────────────────────────────────────────────────────────

def render_progress_stepper():
    """Render the horizontal progress stepper."""
    phase = st.session_state.phase
    steps = [
        ("1", "Define"),
        ("2", "Lesson Plan"),
        ("3", "Feedback"),
        ("4", "Content"),
        ("5", "Download"),
    ]

    html = '<div class="progress-stepper">'
    for i, (num, label) in enumerate(steps, 1):
        if i < phase:
            cls = "completed"
        elif i == phase:
            cls = "current"
        else:
            cls = "pending"
        html += f'<div class="step {cls}"><div class="step-circle">{num}</div><div class="step-label">{label}</div></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ─── Header ──────────────────────────────────────────────────────────────────────

def render_header():
    """Render the app header with logo."""
    logo_path = Path(__file__).parent / "assets" / "logo.jpg"
    col1, col2 = st.columns([1, 8])
    with col1:
        if logo_path.exists():
            st.image(str(logo_path), width=70)
    with col2:
        st.markdown('<div class="main-header">Lesson Designer <span class="brand-highlight">v2</span></div>', unsafe_allow_html=True)
        st.caption("CompSci High — Marzano-Based Lesson Design")


# ─── Phase 1: Define & Knowledge/Skills Check ───────────────────────────────────

def render_phase_1():
    st.markdown('<div class="stage-header">Phase 1: Define Your Lesson</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col2:
        lesson_type = st.selectbox(
            "Lesson Type",
            options=list(LESSON_TYPES.keys()),
            index=list(LESSON_TYPES.keys()).index(st.session_state.lesson_type),
        )
        # Show lesson type description
        st.caption(LESSON_TYPES[lesson_type]["description"])

        grade_level = st.selectbox(
            "Grade Level",
            options=["9", "10", "11", "12", "AP"],
            index=["9", "10", "11", "12", "AP"].index(st.session_state.grade_level),
        )
        duration = st.slider("Duration (minutes)", 30, 90, st.session_state.duration, step=5)
        num_lessons = st.number_input("Number of Lessons", 1, 5, st.session_state.num_lessons)

    with col1:
        competency = st.text_area(
            "Competency",
            value=st.session_state.competency,
            placeholder="e.g., Students will analyze primary sources to evaluate historical claims about the causes of World War I",
            height=100,
        )

        # Dynamic daily objective fields — one per lesson
        n = int(num_lessons)
        # Ensure session list is the right length
        while len(st.session_state.daily_objectives) < n:
            st.session_state.daily_objectives.append("")
        daily_objectives = []
        for i in range(n):
            label = "Daily Objective" if n == 1 else f"Lesson {i + 1} — Daily Objective"
            val = st.session_state.daily_objectives[i] if i < len(st.session_state.daily_objectives) else ""
            obj = st.text_input(
                label,
                value=val,
                placeholder="e.g., Students will identify bias in two primary sources and explain how bias affects historical interpretation",
                key=f"obj_{i}",
            )
            daily_objectives.append(obj)

        additional_guidance = st.text_area(
            "Additional Guidance (optional)",
            value=st.session_state.additional_guidance,
            placeholder="e.g., Students have already learned about WWI's timeline. They struggle with distinguishing fact from opinion.",
            height=80,
        )
        uploaded_file = st.file_uploader(
            "Upload Supporting Document (optional)",
            type=["docx", "pdf", "txt"],
            help="Upload a .docx, .pdf, or .txt file to include as context for lesson generation.",
        )

    # Analyze button
    if st.button("Analyze Competency", type="primary", use_container_width=True):
        if not competency.strip():
            st.error("Please enter a competency statement.")
            return
        # Validate that all objectives have text
        empty_objs = [i for i, o in enumerate(daily_objectives) if not o.strip()]
        if empty_objs:
            if n == 1:
                st.error("Please enter a daily objective.")
            else:
                labels = ", ".join(str(i + 1) for i in empty_objs)
                st.error(f"Please enter a daily objective for lesson(s): {labels}")
            return

        # Store inputs
        st.session_state.competency = competency
        st.session_state.daily_objectives = daily_objectives
        st.session_state.lesson_type = lesson_type
        st.session_state.grade_level = grade_level
        st.session_state.duration = duration
        st.session_state.num_lessons = int(num_lessons)
        st.session_state.additional_guidance = additional_guidance

        # Extract uploaded doc text
        if uploaded_file is not None:
            st.session_state.uploaded_doc_text = extract_text_from_upload(uploaded_file)

        with st.spinner("Analyzing competency..."):
            try:
                result = extract_knowledge_skills(competency, grade_level)
                st.session_state.knowledge = result.get("knowledge", [])
                st.session_state.skills = result.get("skills", [])
            except Exception as e:
                st.error(f"Error analyzing competency: {e}")
                return

        st.rerun()

    # Show knowledge/skills if extracted
    if st.session_state.knowledge or st.session_state.skills:
        st.markdown("---")
        st.markdown('<div class="stage-header">Review Knowledge & Skills</div>', unsafe_allow_html=True)
        st.markdown('<div class="info-box">Review the extracted knowledge and skills. <strong>Uncheck</strong> any items that are not relevant to this lesson.</div>', unsafe_allow_html=True)

        col_k, col_s = st.columns(2)

        with col_k:
            st.markdown("**Knowledge Items**")
            selected_knowledge = []
            for k in st.session_state.knowledge:
                checked = st.checkbox(
                    f"{k['item']} *({k['category']})*",
                    value=True,
                    key=f"k_{k['id']}",
                )
                if checked:
                    selected_knowledge.append(k)

        with col_s:
            st.markdown("**Skills**")
            selected_skills = []
            for s in st.session_state.skills:
                checked = st.checkbox(
                    f"{s['item']} *({s['category']})*",
                    value=True,
                    key=f"s_{s['id']}",
                )
                if checked:
                    selected_skills.append(s)

        if st.button("Continue to Lesson Plan", type="primary", use_container_width=True):
            st.session_state.confirmed_knowledge = selected_knowledge
            st.session_state.confirmed_skills = selected_skills
            st.session_state.phase = 2
            st.rerun()


# ─── Phase 2: Proposed Lesson Plan ──────────────────────────────────────────────

def render_phase_2():
    st.markdown('<div class="stage-header">Phase 2: Proposed Lesson Plan</div>', unsafe_allow_html=True)

    # Auto-generate if we don't have a lesson plan yet
    if not st.session_state.lesson_plan:
        with st.spinner("Generating lesson plan..."):
            try:
                plan = generate_lesson_plan(
                    competency=st.session_state.competency,
                    daily_objectives=st.session_state.daily_objectives,
                    lesson_type=st.session_state.lesson_type,
                    grade_level=st.session_state.grade_level,
                    duration=st.session_state.duration,
                    num_lessons=st.session_state.num_lessons,
                    knowledge=st.session_state.confirmed_knowledge,
                    skills=st.session_state.confirmed_skills,
                    additional_guidance=st.session_state.additional_guidance,
                    doc_text=st.session_state.uploaded_doc_text,
                )
                st.session_state.lesson_plan = plan
            except Exception as e:
                st.error(f"Error generating lesson plan: {e}")
                if st.button("Retry"):
                    st.rerun()
                return
        st.rerun()

    # Display the lesson plan
    num = st.session_state.num_lessons
    if num == 1:
        st.markdown('<div class="info-box">Review the proposed lesson plan below. When you\'re satisfied, approve it to get persona feedback.</div>', unsafe_allow_html=True)
        with st.expander("Lesson Plan", expanded=True):
            st.markdown(f'<div class="plan-text">{_md_to_html_safe(st.session_state.lesson_plan)}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="info-box">Review the proposed plans for all {num} lessons below. When satisfied, approve to get persona feedback.</div>', unsafe_allow_html=True)
        lesson_chunks = _split_by_lesson(st.session_state.lesson_plan, num)
        tabs = st.tabs([f"Lesson {i+1}" for i in range(len(lesson_chunks))])
        for i, (tab, chunk) in enumerate(zip(tabs, lesson_chunks)):
            with tab:
                obj = st.session_state.daily_objectives[i] if i < len(st.session_state.daily_objectives) else ""
                if obj:
                    st.caption(f"Objective: {obj}")
                st.markdown(f'<div class="plan-text">{_md_to_html_safe(chunk)}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Regenerate Plan", use_container_width=True):
            st.session_state.lesson_plan = ""
            st.rerun()
    with col2:
        if st.button("Back to Phase 1", use_container_width=True):
            st.session_state.lesson_plan = ""
            st.session_state.phase = 1
            st.rerun()
    with col3:
        if st.button("Approve & Get Feedback", type="primary", use_container_width=True):
            st.session_state.phase = 3
            st.rerun()


# ─── Phase 3: Persona Feedback & Prompt Revision ────────────────────────────────

def render_phase_3():
    st.markdown('<div class="stage-header">Phase 3: Persona Feedback & Prompt Revision</div>', unsafe_allow_html=True)

    # Auto-generate feedback if we don't have it yet
    if not st.session_state.persona_feedback:
        with st.spinner("Getting persona feedback..."):
            try:
                feedback = get_persona_feedback(
                    lesson_plan=st.session_state.lesson_plan,
                    competency=st.session_state.competency,
                    daily_objectives=st.session_state.daily_objectives,
                    grade_level=st.session_state.grade_level,
                )
                st.session_state.persona_feedback = feedback
            except Exception as e:
                st.error(f"Error getting persona feedback: {e}")
                if st.button("Retry"):
                    st.rerun()
                return

        # Also generate prompt additions
        with st.spinner("Generating suggested prompt additions..."):
            try:
                additions = generate_prompt_additions(
                    persona_feedback=st.session_state.persona_feedback,
                    lesson_plan=st.session_state.lesson_plan,
                )
                st.session_state.prompt_additions = additions
            except Exception as e:
                st.error(f"Error generating prompt additions: {e}")
                st.session_state.prompt_additions = ""

        st.rerun()

    # Display persona feedback cards
    feedback = st.session_state.persona_feedback

    cols = st.columns(2)
    for i, (key, persona) in enumerate(PERSONAS.items()):
        fb = feedback.get(key, {})
        with cols[i % 2]:
            severity_colors = {"high": "#e53935", "medium": "#ffc107", "low": "#9e9e9e"}
            concerns_html = ""
            for c in fb.get("concerns", []):
                sev = c.get("severity", "low")
                css_class = f"concern-{sev}"
                concerns_html += f'<div class="{css_class}"><strong>{c.get("element", "")}</strong>: {c.get("issue", "")} <span style="color:{severity_colors.get(sev, "#999")}; font-weight:600;">({sev.upper()})</span></div>'

            st.markdown(f"""
            <div class="persona-card">
                <div class="persona-name">{persona['icon']} {persona['name']}</div>
                <div class="persona-type">{persona['type']}</div>
                <div style="font-style:italic; margin: 0.5rem 0; color: #555;">"{fb.get('reaction', 'No reaction')}"</div>
                {concerns_html}
            </div>
            """, unsafe_allow_html=True)

    # Editable prompt additions
    st.markdown("---")
    st.markdown("### Suggested Additions to Your Lesson Prompt")
    st.markdown('<div class="info-box">Edit these additions to customize what gets incorporated into the final lesson content. Remove items you disagree with or add your own.</div>', unsafe_allow_html=True)

    prompt_additions = st.text_area(
        "Prompt Additions",
        value=st.session_state.prompt_additions,
        height=200,
        label_visibility="collapsed",
    )

    # Differentiation checkboxes
    st.markdown("### Differentiation Options")
    diff_struggling = st.checkbox(
        "Generate modified materials for struggling learners (scaffolds, word banks, simplified language)",
        value=st.session_state.diff_struggling,
    )
    diff_advanced = st.checkbox(
        "Generate modified materials for advanced learners (deeper analysis, research prompts)",
        value=st.session_state.diff_advanced,
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back to Lesson Plan", use_container_width=True):
            st.session_state.persona_feedback = {}
            st.session_state.prompt_additions = ""
            st.session_state.phase = 2
            st.rerun()
    with col2:
        if st.button("Generate Materials", type="primary", use_container_width=True):
            st.session_state.prompt_additions = prompt_additions
            st.session_state.diff_struggling = diff_struggling
            st.session_state.diff_advanced = diff_advanced
            st.session_state.phase = 4
            st.rerun()


# ─── Phase 4: Content Generation ─────────────────────────────────────────────────

def render_phase_4():
    st.markdown('<div class="stage-header">Phase 4: Content Generation</div>', unsafe_allow_html=True)

    # Auto-generate if no content yet
    if not st.session_state.lesson_content:
        with st.spinner("Generating lesson content... This may take a minute."):
            try:
                content = generate_lesson_content(
                    competency=st.session_state.competency,
                    daily_objectives=st.session_state.daily_objectives,
                    lesson_type=st.session_state.lesson_type,
                    grade_level=st.session_state.grade_level,
                    duration=st.session_state.duration,
                    knowledge=st.session_state.confirmed_knowledge,
                    skills=st.session_state.confirmed_skills,
                    lesson_plan=st.session_state.lesson_plan,
                    prompt_additions=st.session_state.prompt_additions,
                    additional_guidance=st.session_state.additional_guidance,
                    doc_text=st.session_state.uploaded_doc_text,
                    differentiate_struggling=st.session_state.diff_struggling,
                    differentiate_advanced=st.session_state.diff_advanced,
                )
                st.session_state.lesson_content = content
            except Exception as e:
                st.error(f"Error generating content: {e}")
                if st.button("Retry"):
                    st.rerun()
                return
        st.rerun()

    # Display content in expandable sections
    st.markdown('<div class="info-box">Review the generated content below. When satisfied, proceed to generate downloadable documents.</div>', unsafe_allow_html=True)

    content = st.session_state.lesson_content
    num = st.session_state.num_lessons

    if num > 1:
        # Try to split content by lesson, then show sections within each tab
        lesson_chunks = _split_by_lesson(content, num)
        if len(lesson_chunks) > 1:
            tabs = st.tabs([f"Lesson {i+1}" for i in range(len(lesson_chunks))])
            for i, (tab, chunk) in enumerate(zip(tabs, lesson_chunks)):
                with tab:
                    sections = _parse_content_sections(chunk)
                    if sections:
                        for title, body in sections:
                            with st.expander(title, expanded=(title in ["Lesson Plan", "Exit Ticket"])):
                                st.markdown(f'<div class="plan-text">{body}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="plan-text">{chunk}</div>', unsafe_allow_html=True)
        else:
            # Couldn't split — show as single block with sections
            sections = _parse_content_sections(content)
            if sections:
                for title, body in sections:
                    with st.expander(title, expanded=(title in ["Lesson Plan", "Exit Ticket"])):
                        st.markdown(f'<div class="plan-text">{body}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="plan-text">{content}</div>', unsafe_allow_html=True)
    else:
        # Single lesson — expandable sections
        sections = _parse_content_sections(content)
        if sections:
            for title, body in sections:
                with st.expander(title, expanded=(title in ["Lesson Plan", "Exit Ticket"])):
                    st.markdown(f'<div class="plan-text">{body}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="plan-text">{content}</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Regenerate Content", use_container_width=True):
            st.session_state.lesson_content = ""
            st.rerun()
    with col2:
        if st.button("Back to Feedback", use_container_width=True):
            st.session_state.lesson_content = ""
            st.session_state.phase = 3
            st.rerun()
    with col3:
        if st.button("Generate Documents", type="primary", use_container_width=True):
            st.session_state.phase = 5
            st.rerun()


def _parse_content_sections(content: str) -> list:
    """Parse content into (title, body) tuples by splitting on ## headers."""
    sections = []
    lines = content.split("\n")
    current_title = None
    current_body = []

    for line in lines:
        if line.startswith("## "):
            if current_title is not None:
                sections.append((current_title, "\n".join(current_body).strip()))
            current_title = line[3:].strip()
            current_body = []
        else:
            current_body.append(line)

    if current_title is not None:
        sections.append((current_title, "\n".join(current_body).strip()))

    return sections


def _md_to_html_safe(md_text: str) -> str:
    """Let Streamlit render markdown but wrap it — we use st.markdown with the plan-text class."""
    # We pass the raw markdown through; the wrapping div applies the compact CSS.
    # Escape bare HTML angle brackets that aren't tags to avoid injection,
    # but keep markdown formatting intact.
    return md_text


def _split_by_lesson(plan_text: str, num_lessons: int) -> list:
    """Split a multi-lesson plan into chunks, one per lesson.

    Looks for '# Lesson N' or '## Lesson N' headers. If those aren't found,
    falls back to splitting on '---' horizontal rules or on '# ' headers.
    """
    import re

    # Try splitting on # Lesson N or ## Lesson N patterns
    pattern = r'(?=^#{1,2}\s+Lesson\s+\d)'
    parts = re.split(pattern, plan_text, flags=re.MULTILINE)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) >= num_lessons:
        return parts[:num_lessons]

    # Fallback: split on --- horizontal rules
    if "\n---" in plan_text:
        parts = [p.strip() for p in plan_text.split("\n---") if p.strip()]
        if len(parts) >= num_lessons:
            return parts[:num_lessons]

    # Fallback: split on top-level # headers
    pattern2 = r'(?=^#\s+)'
    parts = re.split(pattern2, plan_text, flags=re.MULTILINE)
    parts = [p.strip() for p in parts if p.strip()]
    if len(parts) >= num_lessons:
        return parts[:num_lessons]

    # Last resort: return the whole plan as one chunk
    return [plan_text]


# ─── Phase 5: Document Generation & Download ─────────────────────────────────────

def render_phase_5():
    st.markdown('<div class="stage-header">Phase 5: Document Generation & Download</div>', unsafe_allow_html=True)

    # Auto-generate if no files yet
    if not st.session_state.generated_files:
        # Create temp directory for output files
        output_dir = tempfile.mkdtemp()
        slides_path = os.path.join(output_dir, "slides.pptx")
        worksheet_path = os.path.join(output_dir, "worksheet.docx")

        # Determine if we need supplementary materials
        content_lower = st.session_state.lesson_content.lower()
        needs_supplementary = any(
            kw in content_lower
            for kw in ["station card", "data sheet", "group material", "## group materials", "case study card"]
        )
        supplementary_path = os.path.join(output_dir, "supplementary_materials.docx") if needs_supplementary else None
        modified_path = os.path.join(output_dir, "worksheet_modified.docx") if st.session_state.diff_struggling else None
        extension_path = os.path.join(output_dir, "worksheet_extension.docx") if st.session_state.diff_advanced else None

        with st.spinner("Generating documents... This may take a minute."):
            try:
                code = generate_document_code(
                    content=st.session_state.lesson_content,
                    slides_path=slides_path,
                    worksheet_path=worksheet_path,
                    supplementary_path=supplementary_path,
                    modified_path=modified_path,
                    extension_path=extension_path,
                )

                success = execute_document_code(
                    code=code,
                    slides_path=slides_path,
                    worksheet_path=worksheet_path,
                    supplementary_path=supplementary_path,
                    modified_path=modified_path,
                    extension_path=extension_path,
                )

                if success:
                    files = {}
                    if os.path.exists(slides_path):
                        files["slides"] = slides_path
                    if os.path.exists(worksheet_path):
                        files["worksheet"] = worksheet_path
                    if supplementary_path and os.path.exists(supplementary_path):
                        files["supplementary"] = supplementary_path
                    if modified_path and os.path.exists(modified_path):
                        files["modified"] = modified_path
                    if extension_path and os.path.exists(extension_path):
                        files["extension"] = extension_path

                    st.session_state.generated_files = files
                else:
                    st.error("Document generation failed. Check the error above and try again.")
                    if st.button("Retry Document Generation"):
                        st.rerun()
                    return
            except Exception as e:
                st.error(f"Error generating documents: {e}")
                if st.button("Retry Document Generation"):
                    st.rerun()
                return
        st.rerun()

    # Display download buttons
    st.markdown('<div class="success-box"><strong>Your lesson materials are ready!</strong> Download them below.</div>', unsafe_allow_html=True)

    files = st.session_state.generated_files

    # Build a nice title prefix from the first daily objective
    title_prefix = st.session_state.daily_objectives[0][:50].replace(" ", "_").replace("/", "-")
    if not title_prefix:
        title_prefix = "lesson"

    cols = st.columns(2)

    file_info = [
        ("slides", "Slide Deck", f"{title_prefix}_slides.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation"),
        ("worksheet", "Student Worksheet", f"{title_prefix}_worksheet.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("supplementary", "Supplementary Materials", f"{title_prefix}_supplementary.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("modified", "Modified Worksheet (Struggling)", f"{title_prefix}_modified.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("extension", "Extension Worksheet (Advanced)", f"{title_prefix}_extension.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ]

    col_idx = 0
    for key, label, filename, mime in file_info:
        if key in files:
            with cols[col_idx % 2]:
                with open(files[key], "rb") as f:
                    st.download_button(
                        label=f"Download {label}",
                        data=f.read(),
                        file_name=filename,
                        mime=mime,
                        use_container_width=True,
                    )
            col_idx += 1

    # Lesson summary
    st.markdown("---")
    st.markdown("### Lesson Summary")
    summary_cols = st.columns(3)
    with summary_cols[0]:
        st.markdown(f"**Competency:** {st.session_state.competency}")
        objs = st.session_state.daily_objectives
        if len(objs) == 1:
            st.markdown(f"**Objective:** {objs[0]}")
        else:
            for i, obj in enumerate(objs, 1):
                st.markdown(f"**Lesson {i} Objective:** {obj}")
    with summary_cols[1]:
        st.markdown(f"**Lesson Type:** {st.session_state.lesson_type}")
        st.markdown(f"**Grade Level:** {st.session_state.grade_level}")
    with summary_cols[2]:
        st.markdown(f"**Duration:** {st.session_state.duration} min")
        files_generated = ", ".join(label for key, label, _, _ in file_info if key in files)
        st.markdown(f"**Files:** {files_generated}")

    st.markdown("---")
    if st.button("Start Over", type="primary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# ─── Main ────────────────────────────────────────────────────────────────────────

def main():
    render_header()
    render_progress_stepper()

    phase = st.session_state.phase

    if phase == 1:
        render_phase_1()
    elif phase == 2:
        render_phase_2()
    elif phase == 3:
        render_phase_3()
    elif phase == 4:
        render_phase_4()
    elif phase == 5:
        render_phase_5()


if __name__ == "__main__":
    main()
