import numpy as np
from scoring import chunk_text, semantic_score


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
