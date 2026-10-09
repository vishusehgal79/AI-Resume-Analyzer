import PyPDF2
import streamlit as st

from skills import (
    extract_skills,
    find_skill_evidence,
    evidence_level,
    is_listing_line,
)
from feedback import analyze_bullets, generate_feedback
from scoring import (
    semantic_score,
    resume_quality_score,
    calculate_overall_score,
)

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🧠",
    layout="wide",
)


# --------------------------------------------------
# Minimal styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    :root {
        --accent: #818cf8;
        --accent-soft: rgba(129, 140, 248, 0.10);
        --teal: #5eead4;
        --amber: #fbbf24;
        --rose: #fda4af;
        --border: rgba(148, 163, 184, 0.22);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.8rem;
        padding-bottom: 3rem;
    }

    h1 {
        letter-spacing: -0.8px;
        font-weight: 700;
    }

    h2, h3 {
        letter-spacing: -0.3px;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            var(--accent-soft),
            rgba(128, 128, 128, 0.025) 72%
        );
        border: 1px solid var(--border);
        border-top: 2px solid rgba(129, 140, 248, 0.7);
        border-radius: 12px;
        padding: 16px;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        border-color: rgba(129, 140, 248, 0.55);
        transform: translateY(-1px);
    }

    [data-testid="stMetricLabel"] {
        color: #a5b4fc;
    }

    [data-testid="stProgressBar"] {
        margin-top: 6px;
        margin-bottom: 6px;
    }

    [data-testid="stProgressBar"] > div > div {
        background-color: var(--accent);
        border-radius: 99px;
    }

    div.stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"] {
        border: 1px solid rgba(129, 140, 248, 0.65);
        background: #6366f1;
        color: #ffffff;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #4f46e5;
        border-color: #a5b4fc;
    }

    [data-testid="stFileUploader"] section {
        border: 1px dashed rgba(129, 140, 248, 0.42);
        border-radius: 10px;
        background: rgba(129, 140, 248, 0.035);
    }

    [data-testid="stTextArea"] textarea {
        border-radius: 10px;
        line-height: 1.5;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: var(--accent);
        box-shadow: 0 0 0 1px var(--accent);
    }

    [data-testid="stTabs"] button {
        font-weight: 600;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #a5b4fc;
    }

    [data-testid="stTabs"] button[aria-selected="true"] p {
        color: #a5b4fc;
    }

    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: var(--accent);
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        margin-top: 1.4rem;
        margin-bottom: 1.4rem;
        opacity: 0.35;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------


def extract_text_from_pdf(uploaded_file) -> str:
    reader = PyPDF2.PdfReader(uploaded_file)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


@st.cache_resource
def load_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🧠 AI Resume Analyzer")
st.caption(
    "Compare your resume with a job description and get "
    "clear, actionable improvement insights."
)

st.divider()


# --------------------------------------------------
# Input section
# --------------------------------------------------

resume_col, job_col = st.columns(2, gap="large")

with resume_col:
    st.subheader("📄 Upload Resume")
    st.caption("Upload your resume as a PDF file.")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type="pdf",
        label_visibility="collapsed",
    )

with job_col:
    st.subheader("💼 Job Description")
    st.caption("Paste the requirements for the role.")

    job_desc = st.text_area(
        "Job description",
        height=160,
        placeholder=(
            "Paste the job description here, including "
            "required skills, responsibilities, and qualifications..."
        ),
        label_visibility="collapsed",
    )


# Centered, compact Analyze button
left_space, button_col, right_space = st.columns([2, 1, 2])

with button_col:
    analyze_clicked = st.button(
        "Analyze Resume",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# Run analysis
# --------------------------------------------------

if analyze_clicked:
    if uploaded_file is None or not job_desc.strip():
        st.warning("Please upload a PDF resume and enter a job description.")
        st.stop()

    try:
        resume = extract_text_from_pdf(uploaded_file)
    except Exception as error:
        st.error(f"Could not read the uploaded PDF: {error}")
        st.stop()

    if not resume.strip():
        st.error(
            "No readable text was found in this PDF. "
            "If it is a scanned document, OCR may be required."
        )
        st.stop()

    with st.spinner("Analyzing your resume..."):
        job_skills = extract_skills(job_desc)
        resume_skills = extract_skills(resume)

        matched = sorted(set(job_skills) & set(resume_skills))
        missing = sorted(set(job_skills) - set(resume_skills))

        evidence = find_skill_evidence(resume, matched)
        levels = {skill: evidence_level(lines) for skill, lines in evidence.items()}

        bullet_stats = analyze_bullets(resume)

        model = load_model()
        score = semantic_score(
            resume,
            job_desc,
            lambda texts: model.encode(texts),
        )

        skill_coverage = (
            round(100 * len(matched) / len(job_skills)) if job_skills else 0.0
        )

        quality_score = resume_quality_score(bullet_stats)

        overall_score = calculate_overall_score(
            semantic=score,
            skill_coverage=skill_coverage,
            resume_quality=quality_score,
        )

        strengths, weaknesses, suggestions = generate_feedback(
            matched,
            missing,
            levels,
            bullet_stats,
        )

    st.divider()
    st.header("📊 Resume Analysis")
    st.caption("Explore your score, skill matches, and improvement areas.")

    # --------------------------------------------------
    # Navigation
    # --------------------------------------------------

    overview_tab, skills_tab, bullets_tab, feedback_tab = st.tabs(
        [
            "Overview",
            "Skill Analysis",
            "Bullet Check",
            "Feedback",
        ]
    )

    # --------------------------------------------------
    # Overview tab
    # --------------------------------------------------

    with overview_tab:
        st.subheader("Overall Resume Match")

        score_col, progress_col = st.columns([1, 2], gap="large")

        with score_col:
            st.metric(
                "Overall Score",
                f"{overall_score:.2f}/100",
            )

        with progress_col:
            st.write("Match score")
            st.progress(max(0, min(100, int(overall_score))))
            st.caption(
                "A weighted combination of semantic match, "
                "skill coverage, and resume quality."
            )

        st.markdown("#### Score Breakdown")

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric("🧠 Semantic Match", f"{score:.2f}%")
            st.progress(max(0, min(100, int(score))))

        with metric_col2:
            st.metric("🔎 Skill Coverage", f"{skill_coverage}%")
            st.progress(max(0, min(100, int(skill_coverage))))

        with metric_col3:
            st.metric("📝 Resume Quality", f"{quality_score:.1f}%")
            st.progress(max(0, min(100, int(quality_score))))

        with st.expander("How is the overall score calculated?"):
            semantic_contribution = score * 0.50
            skill_contribution = skill_coverage * 0.30
            quality_contribution = quality_score * 0.20

            st.write("The overall score combines three signals using " "fixed weights:")

            st.write(
                f"**Semantic Match:** {score:.2f}% × 50% = "
                f"**{semantic_contribution:.2f}**"
            )

            st.write(
                f"**Skill Coverage:** {skill_coverage}% × 30% = "
                f"**{skill_contribution:.2f}**"
            )

            st.write(
                f"**Resume Quality:** {quality_score:.1f}% × 20% = "
                f"**{quality_contribution:.2f}**"
            )

            st.divider()

            st.write(
                f"**Overall Score:** {semantic_contribution:.2f} + "
                f"{skill_contribution:.2f} + "
                f"{quality_contribution:.2f} = "
                f"**{overall_score:.2f}**"
            )

            st.caption(
                "These are initial heuristic weights, not weights "
                "learned from a labeled hiring dataset."
            )

        st.info(
            "This score is a resume-matching estimate, not a hiring "
            "decision or a probability of getting hired."
        )

    # --------------------------------------------------
    # Skill analysis tab
    # --------------------------------------------------

    with skills_tab:
        st.subheader("Skill Coverage")

        if job_skills:
            st.write(
                f"**{len(matched)} of {len(job_skills)}** detected "
                f"job skills were found in your resume."
            )

            st.progress(max(0, min(100, int(skill_coverage))))

            st.caption(f"{skill_coverage}% skill coverage")

            rows = []

            for skill in job_skills:
                if skill in evidence:
                    evidence_lines = evidence[skill]

                    if levels[skill] == "used in context":
                        displayed_evidence = next(
                            (
                                line
                                for line in evidence_lines
                                if not is_listing_line(line)
                            ),
                            evidence_lines[0],
                        )
                    else:
                        displayed_evidence = evidence_lines[0]

                    rows.append(
                        {
                            "Skill": skill,
                            "Status": levels[skill],
                            "Evidence from resume": (displayed_evidence[:110]),
                        }
                    )
                else:
                    rows.append(
                        {
                            "Skill": skill,
                            "Status": "missing",
                            "Evidence from resume": "-",
                        }
                    )

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.info(
                "No known skills were detected in the job description. "
                "The current skill dictionary covers a limited set "
                "of technologies."
            )

    # --------------------------------------------------
    # Resume bullet check tab
    # --------------------------------------------------

    with bullets_tab:
        st.subheader("Resume Bullet Check")
        st.caption(
            "Review how clearly your project and experience bullets "
            "communicate actions and measurable impact."
        )

        if bullet_stats["total"]:
            bullet_col1, bullet_col2, bullet_col3 = st.columns(3)

            bullet_col1.metric(
                "Bullets Analyzed",
                bullet_stats["total"],
            )

            bullet_col2.metric(
                "Start with Action Verbs",
                bullet_stats["with_action_verb"],
            )

            bullet_col3.metric(
                "Contain a Number",
                bullet_stats["with_metric"],
            )

            weak_bullets = bullet_stats["weak"]

            if weak_bullets:
                with st.expander(f"Review {len(weak_bullets)} bullets for improvement"):
                    for index, (bullet, issues) in enumerate(
                        weak_bullets,
                        start=1,
                    ):
                        st.markdown(f"**{index}.** {bullet}")
                        st.caption(f"Issues: {'; '.join(issues)}")

                        if index < len(weak_bullets):
                            st.divider()
            else:
                st.success("No bullet issues were detected by the current checks.")

        else:
            st.info("No bullet points were detected in the extracted PDF text.")

    # --------------------------------------------------
    # Feedback tab
    # --------------------------------------------------

    with feedback_tab:
        st.subheader("Resume Improvement Insights")
        st.caption("Use these findings to decide what to keep and what to improve.")

        feedback_col1, feedback_col2, feedback_col3 = st.columns(
            3,
            gap="medium",
        )

        with feedback_col1:
            with st.container(border=True):
                st.markdown(
                    '<h4 style="color:#5eead4; margin-bottom:0.8rem;">'
                    "✓ Strengths</h4>",
                    unsafe_allow_html=True,
                )

                for item in strengths or ["No strengths identified yet."]:
                    st.markdown(f"- {item}")

        with feedback_col2:
            with st.container(border=True):
                st.markdown(
                    '<h4 style="color:#fda4af; margin-bottom:0.8rem;">'
                    "⚠ Weaknesses</h4>",
                    unsafe_allow_html=True,
                )

                for item in weaknesses or ["No weaknesses identified."]:
                    st.markdown(f"- {item}")

        with feedback_col3:
            with st.container(border=True):
                st.markdown(
                    '<h4 style="color:#fbbf24; margin-bottom:0.8rem;">'
                    "✦ Suggestions</h4>",
                    unsafe_allow_html=True,
                )

                for item in suggestions or ["No suggestions available."]:
                    st.markdown(f"- {item}")

        st.divider()

        st.caption(
            "This tool provides heuristic resume feedback. "
            "It does not make hiring decisions."
        )
