import numpy as np


def chunk_text(text: str, max_words: int = 150, overlap: int = 30) -> list[str]:
    """Split text into overlapping word windows so no part of a long resume
    is silently cut off by the model's token limit."""
    words = text.split()
    if not words:
        return []
    step = max_words - overlap
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + max_words]))
        if start + max_words >= len(words):
            break
    return chunks


def _normalize(m: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    return m / np.clip(norms, 1e-12, None)


def semantic_score(resume: str, job: str, encode) -> float:
    """For each job-description chunk, find its best-matching resume chunk,
    then average. Result is cosine similarity scaled to 0-100.

    `encode` takes a list of strings and returns a 2D array of embeddings
    (e.g. lambda texts: model.encode(texts)).
    """
    r_chunks, j_chunks = chunk_text(resume), chunk_text(job)
    if not r_chunks or not j_chunks:
        return 0.0
    r = _normalize(np.asarray(encode(r_chunks), dtype=float))
    j = _normalize(np.asarray(encode(j_chunks), dtype=float))
    sims = j @ r.T                      # (job chunks x resume chunks)
    score = float(sims.max(axis=1).mean()) * 100
    return round(min(100.0, max(0.0, score)), 2)


def resume_quality_score(bullet_stats: dict) -> float:
    """Estimate resume quality from bullet structure."""
    total = bullet_stats.get("total", 0)

    if total == 0:
        return 0.0

    action_rate = bullet_stats.get("with_action_verb", 0) / total
    metric_rate = bullet_stats.get("with_metric", 0) / total

    score = ((action_rate + metric_rate) / 2) * 100

    return round(score, 2)


def calculate_overall_score(
    semantic: float,
    skill_coverage: float,
    resume_quality: float,
) -> float:
    """Combine the three resume-analysis signals into an explainable score."""
    score = 0.50 * semantic + 0.30 * skill_coverage + 0.20 * resume_quality

    return round(min(100.0, max(0.0, score)), 2)
