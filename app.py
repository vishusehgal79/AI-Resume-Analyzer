import PyPDF2
import streamlit as st

from skills import (
    extract_skills,
    find_skill_evidence,
    evidence_level,
    is_listing_line,
)
from feedback import analyze_bullets, generate_feedback
from scoring import semantic_score, resume_quality_score, calculate_overall_score


# --------------------------
# PDF extraction (pages joined with newlines so bullets stay on their own lines)
# --------------------------
def extract_text_from_pdf(uploaded_file) -> str:
    reader = PyPDF2.PdfReader(uploaded_file)
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


# --------------------------
# Load model once
# --------------------------
@st.cache_resource
def load_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------
# UI
# --------------------------
st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
resume = extract_text_from_pdf(uploaded_file) if uploaded_file else ""
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if not resume.strip() or not job_desc.strip():
        st.warning("Enter both fields")
        st.stop()

    # ---- Skills + evidence (all derived from the text) ----
    job_skills = extract_skills(job_desc)
    resume_skills = extract_skills(resume)
    matched = sorted(set(job_skills) & set(resume_skills))
    missing = sorted(set(job_skills) - set(resume_skills))

    evidence = find_skill_evidence(resume, matched)
    levels = {skill: evidence_level(lines) for skill, lines in evidence.items()}

    # ---- Bullet quality ----
    bullet_stats = analyze_bullets(resume)

    # ---- Semantic similarity (chunked, no stopword stripping) ----
    model = load_model()
    score = semantic_score(resume, job_desc, lambda texts: model.encode(texts))

    skill_coverage = round(100 * len(matched) / len(job_skills)) if job_skills else 0.0

    quality_score = resume_quality_score(bullet_stats)

    overall_score = calculate_overall_score(
        semantic=score,
        skill_coverage=skill_coverage,
        resume_quality=quality_score,
    )

    strengths, weaknesses, suggestions = generate_feedback(
        matched, missing, levels, bullet_stats
    )

    # ================= UI =================
    st.subheader(f"Overall Resume Match: {overall_score}/100")
    st.progress(int(overall_score))

    c1, c2, c3 = st.columns(3)
    c1.metric("Semantic Match", f"{score}%")
    c2.metric("Skill Coverage", f"{skill_coverage}%")
    c3.metric("Resume Quality", f"{quality_score}%")

    st.subheader(f"Semantic similarity: {score}%")
    st.progress(int(score))

    st.subheader("Skill coverage")
    if job_skills:
        coverage = skill_coverage
        st.write(
            f"{len(matched)} of {len(job_skills)} skills required by the job "
            f"were found ({coverage}%)"
        )
        st.progress(coverage)

        rows = []
        for skill in job_skills:
            if skill in evidence:
                evidence_lines = evidence[skill]

                if levels[skill] == "used in context":
                    displayed_evidence = next(
                        (line for line in evidence_lines if not is_listing_line(line)),
                        evidence_lines[0],
                    )
                else:
                    displayed_evidence = evidence_lines[0]

                rows.append(
                    {
                        "Skill": skill,
                        "Status": levels[skill],
                        "Evidence from resume": displayed_evidence[:110],
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

        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info(
            "No known skills detected in the job description. "
            "The skill list covers a limited set of technologies."
        )

    st.subheader("Resume bullet check")
    if bullet_stats["total"]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Bullets found", bullet_stats["total"])
        c2.metric("Start with action verb", bullet_stats["with_action_verb"])
        c3.metric("Contain a number", bullet_stats["with_metric"])

        if bullet_stats["weak"]:
            with st.expander(
        f"{len(bullet_stats['weak'])} bullets to improve"
    ):
                for i, (bullet, issues) in enumerate(
            bullet_stats["weak"], start=1
        ):
                    st.markdown(f"**{i}.** {bullet}")
                    st.caption(f"Issues: {'; '.join(issues)}")
    else:
        st.info("No bullet points detected in the PDF text.")

    st.subheader("Feedback")
    for title, items in (
        ("Strengths", strengths),
        ("Weaknesses", weaknesses),
        ("Suggestions", suggestions),
    ):
        st.markdown(f"**{title}**")
        for item in items or ["-"]:
            st.write(f"- {item}")
