from feedback import analyze_bullets, generate_feedback

RESUME = """Projects
• Built an NLP pipeline with 92% accuracy on 50 samples
• Worked on a payroll app
- Deployed a dashboard used by 10 interns
"""


def test_bullet_counts():
    s = analyze_bullets(RESUME)
    assert s["total"] == 3
    assert s["with_action_verb"] == 2      # "Worked" is not in the verb list
    assert s["with_metric"] == 2


def test_weak_bullet_has_issues():
    weak = dict(analyze_bullets(RESUME)["weak"])
    assert "Worked on a payroll app" in weak
    assert len(weak["Worked on a payroll app"]) == 2


def test_no_bullets_is_reported_not_faked():
    s = analyze_bullets("just a paragraph with no bullets")
    assert s["total"] == 0
    _, weak, _ = generate_feedback([], [], {}, s)
    assert any("No bullet points" in w for w in weak)


def test_feedback_uses_real_skills():
    s = analyze_bullets(RESUME)
    strengths, weaknesses, suggestions = generate_feedback(
        ["python"], ["sql"], {"python": "used in context"}, s
    )
    assert any("python" in x for x in strengths)
    assert any("sql" in x for x in weaknesses)
