import PyPDF2
import streamlit as st

from skills import extract_skills, find_skill_evidence, evidence_level
from feedback import analyze_bullets, generate_feedback
from scoring import semantic_score


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

    strengths, weaknesses, suggestions = generate_feedback(
        matched, missing, levels, bullet_stats
    )

    # ================= UI =================
    st.subheader(f"Semantic similarity: {score}%")
    st.progress(int(score))
    st.caption(
        "How close the resume text is to the job description in meaning. "
        "This is not yet calibrated against labelled data, so treat it as a relative signal."
    )

    st.subheader("Skill coverage")
    if job_skills:
        coverage = round(100 * len(matched) / len(job_skills))
        st.write(f"{len(matched)} of {len(job_skills)} skills required by the job were found ({coverage}%)")
        st.progress(coverage)

        rows = []
        for skill in job_skills:
            if skill in evidence:
                rows.append({
                    "Skill": skill,
                    "Status": levels[skill],
                    "Evidence from resume": evidence[skill][0][:110],
                })
            else:
                rows.append({"Skill": skill, "Status": "missing", "Evidence from resume": "-"})
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("No known skills detected in the job description. The skill list covers a limited set of technologies.")

    st.subheader("Resume bullet check")
    if bullet_stats["total"]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Bullets found", bullet_stats["total"])
        c2.metric("Start with action verb", bullet_stats["with_action_verb"])
        c3.metric("Contain a number", bullet_stats["with_metric"])
        if bullet_stats["weak"]:
            with st.expander(f"{len(bullet_stats['weak'])} bullets to improve"):
                for bullet, issues in bullet_stats["weak"]:
                    st.write(f"- {bullet}  \n  _{'; '.join(issues)}_")
    else:
        st.info("No bullet points detected in the PDF text.")

    st.subheader("Feedback")
    for title, items in (("Strengths", strengths), ("Weaknesses", weaknesses), ("Suggestions", suggestions)):
        st.markdown(f"**{title}**")
        for item in items or ["-"]:
            st.write(f"- {item}")
