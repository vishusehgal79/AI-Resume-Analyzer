from sentence_transformers import SentenceTransformer, util
import PyPDF2
import streamlit as st
import nltk
import string
from typing import List

# --------------------------
# Download stopwords properly
# --------------------------
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))

# --------------------------
# Skills dictionary
# --------------------------
skills_dict = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++"],
    "sql": ["sql"],
    "react": ["react"],
    "javascript": ["javascript", "js"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "power bi": ["power bi"],
    "excel": ["excel"],
    "tableau": ["tableau"],
    "git": ["git"],
    "github": ["github"]
}

# --------------------------
# Preprocess text
# --------------------------
def preprocess(text: str) -> str:
    text = text.lower()
    text = "".join(c for c in text if c not in string.punctuation)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

# --------------------------
# Extract skills
# --------------------------
def extract_skills(text: str) -> List[str]:
    found = set()
    for skill, variations in skills_dict.items():
        for v in variations:
            if v in text:
                found.add(skill)
                break
    return list(found)

# --------------------------
# Suggestions
# --------------------------
def generate_suggestions(missing: List[str]) -> List[str]:
    return [f"Add projects related to {s}" for s in missing]

# --------------------------
# NEW: Skill Match Score
# --------------------------
def skill_match_score(resume_skills, job_skills):
    scores = {}
    for skill in job_skills:
        if skill in resume_skills:
            scores[skill] = 80
        else:
            scores[skill] = 20
    return scores

# --------------------------
# PDF extraction
# --------------------------
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# --------------------------
# Load model
# --------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

# --------------------------
# UI
# --------------------------
st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

resume = ""
if uploaded_file:
    resume = extract_text_from_pdf(uploaded_file)

job_desc = st.text_area("Paste Job Description")

if st.button("Analyze"):

    if not resume.strip() or not job_desc.strip():
        st.warning("Enter both fields")
        st.stop()

    resume_clean = preprocess(resume)
    job_clean = preprocess(job_desc)

    if not resume_clean or not job_clean:
        st.error("Text too short after preprocessing")
        st.stop()

    resume_skills = extract_skills(resume_clean)
    job_skills = extract_skills(job_clean)

    missing_skills = list(set(job_skills) - set(resume_skills))

    # --------------------------
    # Semantic similarity
    # --------------------------
    model = load_model()

    emb1 = model.encode(resume_clean, convert_to_tensor=True)
    emb2 = model.encode(job_clean, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2).item() * 100
    score = round(score, 2)

    # --------------------------
    # Skill score calculation
    # --------------------------
    skill_scores = skill_match_score(resume_skills, job_skills)

    # --------------------------
    # UI Output
    # --------------------------
    st.subheader(f"Match Score: {score}%")
    st.progress(int(score))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Skills Found in Resume")
        if resume_skills:
            for skill in sorted(resume_skills):
                st.markdown(f"✅ {skill}")
        else:
            st.write("No skills detected.")

    with col2:
        st.subheader("Skills Required by Job")
        if job_skills:
            for skill in sorted(job_skills):
                st.markdown(f"📌 {skill}")
        else:
            st.write("No job skills detected.")

    # --------------------------
    # NEW: Skill Match Analysis
    # --------------------------
    st.subheader("Skill Match Analysis")

    for skill, val in skill_scores.items():
        st.write(f"{skill}: {val}%")
        st.progress(val)

    # Suggestions
    st.subheader("Suggestions")
    suggestions = generate_suggestions(missing_skills)
    st.write(suggestions or "No suggestions")

    # Feedback
    if score > 70:
        st.success("Good match")
    elif score > 40:
        st.warning("Moderate match")
    else:
        st.error("Low match")