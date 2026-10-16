# 🧠 AI Resume Analyzer

**An NLP-powered tool for resume-to-job matching, skill analysis, and explainable feedback.**

Analyze how well a resume aligns with a job description using semantic similarity, technical skill detection, and rule-based resume quality checks.

## ✨ Features

* **Semantic Matching** — compares resume and job description using sentence embeddings.
* **Skill Analysis** — identifies matched, missing, and contextually supported skills.
* **Resume Quality** — evaluates action verbs and measurable results in bullet points.
* **Explainable Scoring** — combines three signals into an overall match score.
* **Actionable Feedback** — highlights strengths, weaknesses, and improvement suggestions.
* **Interactive Dashboard** — presents results through a Streamlit interface.

## 📊 Scoring Model

| Component      | Weight |
| -------------- | -----: |
| Semantic Match |    50% |
| Skill Coverage |    30% |
| Resume Quality |    20% |

```text
Overall Score =
    0.50 × Semantic Match
  + 0.30 × Skill Coverage
  + 0.20 × Resume Quality
```

*The weights are heuristic choices, not learned from a labeled hiring dataset. The score indicates resume-to-job alignment, not the probability of getting hired.*

## ⚙️ Tech Stack

`Python` · `Streamlit` · `Sentence Transformers` · `PyPDF2` · `NumPy` · `Pytest`

Semantic matching uses the **`all-MiniLM-L6-v2`** model.

## 🚀 Getting Started

```bash
git clone https://github.com/vishusehgal79/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

## 🧪 Tests

Run the automated test suite:

```bash
pytest
```

Tests cover skill extraction, scoring, skill evidence, and resume feedback.

## 👩‍💻 Author

**Vishu Sehgal**


