# 🧠 AI Resume Analyzer (NLP + Semantic Matching)

An AI-powered web application that analyzes how well a resume matches a job description.
It uses **Natural Language Processing (NLP)** and **semantic similarity models** to provide a **match score, skill extraction, missing skills, and intelligent feedback**.

This project simulates a real-world **ATS (Applicant Tracking System)** used in recruitment pipelines.

---

## 🚀 Latest Upgrades (v2)

- 🔄 Upgraded from TF-IDF → **Sentence Transformers (semantic embeddings)**
- 🧠 Added **context-aware resume-job matching**
- 📊 Introduced **skill gap analysis (present vs missing skills)**
- 💡 Added **AI-based improvement suggestions**
- 🖥️ Enhanced **Streamlit UI for better visualization**
- 📈 Added **explainable scoring system for skills**

---

## ✨ Features

- 📄 Resume vs Job Description similarity score
- 🧠 Semantic matching using NLP embeddings
- 🔍 Automatic skill extraction
- ❌ Detection of missing required skills
- 📊 ATS-style match score with progress bar
- 💡 AI-generated resume improvement suggestions
- 🖥️ Clean and interactive Streamlit UI

---

## ⚙️ Tech Stack

- **Python**
- **Streamlit** – Web interface
- **Sentence Transformers** – Semantic embeddings
- **Scikit-learn** – Cosine similarity (used in earlier version)
- **NLTK** – Text preprocessing
- **PyPDF2** – Resume PDF parsing

---

## 🧠 How It Works

1. User uploads **resume (PDF/text)**  
2. User pastes **job description**  
3. Text is cleaned using NLP preprocessing  
4. Skills are extracted using keyword + synonym mapping  
5. Sentence embeddings are generated using transformer model  
6. **Cosine similarity** calculates semantic match score  
7. System identifies missing skills  
8. Suggestions are generated for improvement  

---

## 📊 Output Includes

- 🧠 Resume–Job Match Score  
- 🔍 Skills Found in Resume  
- 📌 Required Skills from Job Description  
- ❌ Missing Skills  
- 💡 AI Improvement Suggestions  

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/vishusehgal79/AI-Resume-Analyzer.git
