from skills import extract_skills


def test_java_not_matched_inside_javascript():
    assert extract_skills("Built apps with JavaScript and React") == ["javascript", "react"]


def test_ml_not_matched_inside_html():
    assert extract_skills("Designed pages in HTML and CSS") == []
    assert extract_skills("ML engineer") == ["machine learning"]


def test_git_not_matched_inside_digital():
    assert extract_skills("Led digital transformation") == []
    assert extract_skills("Used Git and GitHub") == ["git", "github"]


def test_cpp_survives_punctuation():
    assert extract_skills("Proficient in C++, Python") == ["c++", "python"]


def test_case_insensitive_multiword():
    assert extract_skills("Natural Language Processing and Power BI") == ["nlp", "power bi"]


from skills import find_skill_evidence, evidence_level, is_listing_line


def test_listing_line_vs_real_usage():
    assert is_listing_line("Languages: Python, Java, SQL, JavaScript")
    assert not is_listing_line("Built an NLP pipeline in Python, scoring resumes against job descriptions")


def test_evidence_levels():
    text = "Languages: Python, Java, SQL\nBuilt a resume scorer in Python using cosine similarity"
    ev = find_skill_evidence(text, ["python", "sql"])
    assert evidence_level(ev["python"]) == "used in context"
    assert evidence_level(ev["sql"]) == "listed only"
