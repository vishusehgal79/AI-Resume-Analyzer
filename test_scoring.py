import numpy as np
from scoring import chunk_text, semantic_score, resume_quality_score, calculate_overall_score


def fake_encode(texts):
    # 3-dim "embedding": counts of three keywords
    return np.array([[t.count("python"), t.count("sql"), t.count("tableau")] for t in texts], dtype=float) + 1e-6


def test_chunking_covers_whole_text():
    text = " ".join(f"w{i}" for i in range(400))
    chunks = chunk_text(text, max_words=150, overlap=30)
    assert chunks[0].startswith("w0 ")
    assert chunks[-1].endswith("w399")
    assert all(len(c.split()) <= 150 for c in chunks)


def test_chunk_empty():
    assert chunk_text("   ") == []


def test_identical_text_scores_100():
    assert semantic_score("python python sql", "python python sql", fake_encode) == 100.0


def test_unrelated_text_scores_low_and_is_clamped():
    s = semantic_score("python python", "tableau tableau", fake_encode)
    assert 0.0 <= s < 5.0


def test_empty_input_is_zero():
    assert semantic_score("", "python", fake_encode) == 0.0


def test_resume_quality_score():
    stats = {
        "total": 10,
        "with_action_verb": 8,
        "with_metric": 6,
    }

    assert resume_quality_score(stats) == 70.0


def test_resume_quality_score_with_no_bullets():
    stats = {
        "total": 0,
        "with_action_verb": 0,
        "with_metric": 0,
    }

    assert resume_quality_score(stats) == 0.0


def test_calculate_overall_score():
    assert (
        calculate_overall_score(
            semantic=80,
            skill_coverage=70,
            resume_quality=60,
        )
        == 73.0
    )


def test_overall_score_is_clamped():
    assert calculate_overall_score(120, 110, 105) == 100.0
    assert calculate_overall_score(-10, -20, -30) == 0.0
