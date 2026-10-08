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


def test_common_skill_headings_are_listings():
    assert is_listing_line("Skills: Python, SQL, React")
    assert is_listing_line("Technical Skills: Python, SQL")
    assert is_listing_line("Technologies: React, Node.js, Python")
    assert is_listing_line("Tools: Git, Docker, AWS")
    assert is_listing_line("Frameworks: React, Django, Flask")


def test_usage_sentence_is_not_listing():
    assert not is_listing_line(
        "Built a resume analyzer using Python, NLP, and sentence transformers"
    )


def test_evidence_levels():
    text = "Languages: Python, Java, SQL\nBuilt a resume scorer in Python using cosine similarity"
    ev = find_skill_evidence(text, ["python", "sql"])
    assert evidence_level(ev["python"]) == "used in context"
    assert evidence_level(ev["sql"]) == "listed only"


def test_mixed_skill_evidence():
    text = (
        "Skills: Python, SQL, React\n" "Built a resume analyzer using Python and React"
    )

    ev = find_skill_evidence(text, ["python", "sql", "react"])

    assert evidence_level(ev["python"]) == "used in context"
    assert evidence_level(ev["react"]) == "used in context"
    assert evidence_level(ev["sql"]) == "listed only"


def test_machine_learning_variants():
    assert extract_skills("Built a machine-learning model") == ["machine learning"]

    assert extract_skills("Worked as an ML engineer") == ["machine learning"]


def test_nlp_variants():
    assert extract_skills("Built a natural-language processing pipeline") == ["nlp"]

    assert extract_skills("Worked on NLP classification") == ["nlp"]


def test_react_variants():
    assert extract_skills("Built a ReactJS dashboard") == ["react"]

    assert extract_skills("Built a React.js dashboard") == ["react"]


def test_empty_text():
    assert extract_skills("") == []


def test_none_like_empty_input():
    assert extract_skills(None) == []
