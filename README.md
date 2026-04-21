# 🧠 AI Resume Analyzer (NLP + Semantic Matching)

An AI-powered web application that evaluates how well a resume matches a job description using Natural Language Processing (NLP) and semantic similarity.

The system analyzes resumes by extracting skills, computing contextual similarity, identifying missing skills, and generating structured feedback (strengths, weaknesses, and actionable suggestions).

This project simulates a real-world ATS (Applicant Tracking System) used in modern recruitment pipelines.

---

## 🚀 Latest Upgrades (v3)

🔄 Upgraded to semantic similarity using Sentence Transformers  
🧠 Improved contextual resume-job matching  
📊 Added detailed skill match analysis with scoring  
💡 Introduced structured feedback (Strengths, Weaknesses, Suggestions)  
🧱 Improved system reliability using rule-based feedback (no API dependency)  
🖥️ Enhanced UI for clearer insights and better usability  

---

## ✨ Features

- 📄 Resume vs Job Description semantic similarity score  
- 🧠 Context-aware matching using NLP embeddings  
- 🔍 Automatic skill extraction  
- ❌ Detection of missing required skills  
- 📊 Skill-wise match analysis with scoring  
- 💡 Structured feedback:
  - Strengths  
  - Weaknesses  
  - Suggestions  
- 🖥️ Clean and interactive Streamlit UI  

---

## ⚙️ Tech Stack

- Python  
- Streamlit (Frontend UI)  
- Sentence Transformers (Semantic Similarity)  
- NLTK (Text Preprocessing)  
- PyPDF2 (PDF Parsing)  

---

## 🧠 How It Works

1. User uploads resume (PDF)  
2. User enters job description  
3. Text is preprocessed using NLP techniques  
4. Skills are extracted using keyword mapping  
5. Sentence embeddings are generated  
6. Cosine similarity calculates match score  
7. Missing skills are identified  
8. Structured feedback is generated  

---

## 📊 Output Includes

- 🧠 Resume–Job Match Score  
- 🔍 Skills Found in Resume  
- 📌 Required Skills from Job Description  
- ❌ Missing Skills  
- 💡 Structured Feedback (Strengths, Weaknesses, Suggestions)  

---

## 🚀 Future Improvements

- Integration with LLMs for advanced feedback generation  
- Backend migration using FastAPI  
- API-based resume analysis system  
- Deployment on cloud platforms  

---

## 🚀 Installation

```bash
git clone https://github.com/vishusehgal79/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
pip install -r requirements.txt
streamlit run app.py
