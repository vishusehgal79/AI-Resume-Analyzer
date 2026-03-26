# AI Resume Analyzer

An AI-powered web application that analyzes how well a resume matches a job description.
The app compares the resume and job description using **Natural Language Processing (NLP)** and provides a **match score, detected skills, and missing skills** to help improve the resume.

---

## Features

* Resume vs Job Description similarity score
* Automatic **skill extraction**
* Detects **missing skills** from the job description
* Provides **ATS-style feedback**
* Clean and simple **Streamlit UI**

---

## Tech Stack

* **Python**
* **Streamlit** – for the web interface
* **Scikit-learn** – TF-IDF and cosine similarity
* **NLTK** – text preprocessing and stopword removal
* **Natural Language Processing (NLP)**

---

## How It Works

1. The user pastes their **resume text**.
2. The user pastes a **job description**.
3. The app cleans the text using NLP techniques.
4. Skills are extracted from both texts.
5. **TF-IDF vectorization** converts text to numerical vectors.
6. **Cosine similarity** calculates the match score between the resume and job description.
7. The app shows:

   * Match score
   * Skills found in the resume
   * Skills required by the job
   * Missing skills

---

## Installation

Clone the repository:

git clone https://github.com/vishusehgal79/AI-Resume-Analyzer.git

Go into the project folder:

cd AI-Resume-Analyzer

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

---

## Example Output

The app displays:

* **Match Score**
* **Skills Found in Resume**
* **Skills Required by Job**
* **Missing Skills**
* Resume improvement feedback

---

## Future Improvements

* Upload **PDF resumes**
* Better **skill extraction using NLP models**
* **Skill gap visualization charts**
* AI-based **resume improvement suggestions**

---


