# 🧠 AI Resume Analyzer

### NLP-powered resume-to-job matching with semantic similarity and explainable feedback.

An AI-powered Streamlit application that analyzes how well a resume matches a job description using **Sentence Transformers, skill extraction, evidence analysis, and rule-based resume quality checks**.

The system provides an explainable score along with missing skills, resume strengths, weaknesses, and actionable suggestions.

---

## ✨ Features

- 🧠 **Semantic Matching** — compares resume and job description using embeddings
- 🔍 **Skill Extraction** — detects and normalizes technical skills
- 📌 **Skill Evidence** — identifies whether skills are actually used or only listed
- ❌ **Missing Skills** — highlights skills required by the job but absent from the resume
- 📝 **Resume Quality Analysis** — checks action verbs and measurable results
- 📊 **Explainable Overall Score** — combines multiple resume signals
- 💡 **Structured Feedback** — Strengths, Weaknesses, and Suggestions
- 🖥️ **Interactive UI** — built with Streamlit

---

## 📊 Scoring

The overall score combines three signals:

| Signal | Weight |
|---|---:|
| 🧠 Semantic Match | 50% |
| 🔍 Skill Coverage | 30% |
| 📝 Resume Quality | 20% |

```text
Overall Score =
0.50 × Semantic Match
+ 0.30 × Skill Coverage
+ 0.20 × Resume Quality
````

The application also shows the individual contributions so the score is transparent and explainable.

> These weights are initial heuristic weights and are not learned from a labeled dataset.

---

## 🧠 How It Works

```text
Resume PDF ──┐
             ├──> Text Extraction
Job Description ─┘
                    │
                    ├── Skill Analysis
                    ├── Semantic Matching
                    └── Resume Quality Analysis
                              │
                              ▼
                    Explainable Overall Score
                              │
                              ▼
                    Strengths / Weaknesses /
                         Suggestions
```

Semantic matching uses the **`all-MiniLM-L6-v2`** Sentence Transformer model.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Sentence Transformers**
* **PyPDF2**
* **NumPy**
* **Pytest**

---

## 📁 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── skills.py
├── scoring.py
├── feedback.py
├── test_skills.py
├── test_scoring.py
├── test_feedback.py
├── requirements.txt
└── README.md
```

---

## 🧪 Testing

The project includes automated tests for skill extraction, scoring, evidence detection, and resume feedback.

Run:

```bash
pytest
```

Current test suite:

```text
29 passed
```

---

## 🚀 Installation

```bash
git clone https://github.com/vishusehgal79/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

---

## ⚠️ Limitations

* Skill extraction currently uses a predefined skill dictionary.
* Resume quality scoring is heuristic-based.
* Score weights are manually selected and not trained on hiring data.
* PDF text extraction depends on the document structure.
* Semantic similarity is a matching signal, not a hiring probability.

---

## 🔮 Future Improvements

* LLM-powered personalized feedback
* Larger skill taxonomy
* Learned/calibrated scoring weights
* FastAPI backend
* Cloud deployment
* More extensive evaluation datasets

---

## 👩‍💻 Author

**Vishu Sehgal**


