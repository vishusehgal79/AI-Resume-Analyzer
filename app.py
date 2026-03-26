import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import string

# Download stopwords safely
try:
    stop_words = set(stopwords.words('english'))
except:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

# Skills database
skills_list = [
    "python", "java", "c++", "sql", "react", "javascript",
    "machine learning", "data analysis", "deep learning",
    "nlp", "pandas", "numpy", "tensorflow", "pytorch",
    "power bi", "excel", "tableau", "git", "github"
]

# Text preprocessing
def preprocess(text):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# Skill extraction
def extract_skills(text):
    found_skills = []

    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)

    return found_skills


# --------------------------
# Streamlit UI
# --------------------------

st.title("AI Resume Analyzer")

resume = st.text_area("Paste Resume Text")
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze Resume"):

    if resume.strip() == "" or job_desc.strip() == "":
        st.warning("Please enter both Resume and Job Description.")

    else:
        # Clean text
        resume_clean = preprocess(resume)
        job_clean = preprocess(job_desc)

        # Extract skills
        resume_skills = extract_skills(resume_clean)
        job_skills = extract_skills(job_clean)

        # Find missing skills
        missing_skills = list(set(job_skills) - set(resume_skills))

        # TF-IDF similarity
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform([resume_clean, job_clean])

        similarity = cosine_similarity(vectors)[0][1]
        score = round(similarity * 100, 2)

        # Display score
        st.subheader(f"Match Score: {score}%")
        st.progress(int(score))

        # Resume skills
        st.subheader("Skills Found in Resume")
        if resume_skills:
            for skill in resume_skills:
                st.markdown(f"✅ {skill}")
        else:
            st.write("No skills detected.")

        # Job skills
        st.subheader("Skills Required by Job")
        if job_skills:
            for skill in job_skills:
                st.markdown(f"📌 {skill}")
        else:
            st.write("No job skills detected.")

        # Missing skills
        st.subheader("Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"❌ {skill}")
        else:
            st.success("No missing skills! Your resume contains all required skills.")

        # Score feedback
        if score > 70:
            st.success("Great match! Your resume fits the job well.")
        elif score > 40:
            st.warning("Moderate match. Consider improving your resume.")
        else:
            st.error("Low match. Add more relevant skills.")