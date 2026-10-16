# 🤖 AI Resume Analyzer

**An NLP-powered resume analysis tool that evaluates how well a resume aligns with a target job description.**

AI Resume Analyzer combines **transformer-based semantic similarity, technical skill analysis, and rule-based resume quality checks** to produce an explainable resume-to-job match score and actionable feedback.

## ✨ Features

- **Semantic Matching** — compares resume and job description using transformer-based sentence embeddings.
- **Skill Analysis** — identifies matched, missing, and contextually supported technical skills.
- **Resume Quality Analysis** — evaluates resume bullet points for action verbs and measurable results.
- **Explainable Scoring** — combines semantic similarity, skill coverage, and resume quality into a transparent overall score.
- **Actionable Feedback** — generates strengths, weaknesses, and practical improvement suggestions.
- **Interactive Dashboard** — provides an easy-to-use Streamlit interface for resume analysis.

## 🧠 How It Works

The analyzer processes a resume and target job description through several stages:

### 1. Resume Parsing

Extracts text from the uploaded PDF resume.

### 2. Semantic Matching

Uses the `all-MiniLM-L6-v2` Sentence Transformer model to generate embeddings and measure semantic similarity between the resume and job description.

### 3. Skill Analysis

Extracts relevant technical skills and categorizes them based on their presence and evidence in the resume:

- Matched
- Missing
- Used in context
- Listed only

### 4. Resume Quality Analysis

Analyzes resume bullet points for:

- Action verbs
- Measurable results
- Potentially weak bullet points

### 5. Explainable Feedback

Combines the analysis into an overall score and generates:

- Strengths
- Weaknesses
- Improvement suggestions

## 📊 Scoring Model

The overall resume-to-job alignment score combines three signals:

| Component | Weight |
|---|---:|
| Semantic Match | 50% |
| Skill Coverage | 30% |
| Resume Quality | 20% |

```text
Overall Score =
    0.50 × Semantic Match
  + 0.30 × Skill Coverage
  + 0.20 × Resume Quality
```

The weights are heuristic choices rather than parameters learned from a labeled hiring dataset.

**Important:** The score represents resume-to-job alignment. It is not a prediction of interview selection or hiring probability.

## 💡 Engineering Highlights

- Transformer-based semantic matching using Sentence Transformers
- Explainable multi-signal scoring instead of a black-box prediction
- Technical skill extraction and contextual skill evidence analysis
- Rule-based resume bullet quality analysis
- Modular scoring and feedback components
- Streamlit-based interactive application
- Automated testing with Pytest

## 🛠️ Tech Stack

- **Python**
- **Streamlit** — interactive web application
- **Sentence Transformers** — semantic embeddings
- **PyPDF2** — PDF text extraction
- **NumPy** — numerical calculations
- **Pytest** — automated testing

### NLP Model

Semantic matching uses:

`sentence-transformers/all-MiniLM-L6-v2`

## 📁 Project Structure

```text
AI-Resume-Analyzer/
├── app.py
├── skills.py
├── scoring.py
├── feedback.py
├── requirements.txt
├── test_skills.py
├── test_scoring.py
├── test_feedback.py
└── README.md
```

| File | Purpose |
|---|---|
| `app.py` | Streamlit application and user interface |
| `skills.py` | Skill extraction and evidence analysis |
| `scoring.py` | Resume-to-job scoring logic |
| `feedback.py` | Resume quality analysis and feedback generation |
| `test_skills.py` | Skill analysis tests |
| `test_scoring.py` | Scoring tests |
| `test_feedback.py` | Feedback tests |

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vishusehgal79/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open locally in your browser.

## 🧪 Testing

The project includes automated tests covering:

- Skill extraction
- Skill matching and evidence
- Scoring logic
- Resume bullet analysis
- Feedback generation

Run the test suite:

```bash
pytest
```

Current test suite:

**29 tests passing**

## 🔮 Future Improvements

- Learn scoring weights from a labeled resume/job-description dataset
- Expand the technical skill taxonomy
- Add seniority and experience-level matching
- Add model evaluation using benchmark datasets
- Support additional resume formats
- Add more advanced resume section analysis
- Introduce CI-based automated testing

## 👩‍💻 Author

**Vishu Sehgal**


