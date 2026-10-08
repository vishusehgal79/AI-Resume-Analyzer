import re

skills_dict = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++"],
    "sql": ["sql"],
    "react": ["react"],
    "javascript": ["javascript", "js"],
    "machine learning": ["machine learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "power bi": ["power bi"],
    "excel": ["excel"],
    "tableau": ["tableau"],
    "git": ["git"],
    "github": ["github"],
}

# Compile once. (?<!\w) / (?!\w) mean "not inside a longer word".
# We use these instead of \b because \b fails next to "+" in "c++".
_PATTERNS = {
    skill: [
        re.compile(rf"(?<!\w){re.escape(v)}(?!\w)", re.IGNORECASE)
        for v in variations
    ]
    for skill, variations in skills_dict.items()
}


def extract_skills(text: str) -> list[str]:
    found = set()
    for skill, patterns in _PATTERNS.items():
        if any(p.search(text) for p in patterns):
            found.add(skill)
    return sorted(found)


# --------------------------
# Evidence: WHERE was each skill found?
# --------------------------
def is_listing_line(line: str) -> bool:
    """Heuristic: 'Languages: Python, Java, SQL' is a skills list, not real usage.

    A line is a listing if it has 2+ commas and very few words between commas.
    """
    commas = line.count(",")
    if commas < 2:
        return False
    return len(line.split()) / commas < 3.5


def find_skill_evidence(text: str, skills: list[str] | None = None) -> dict[str, list[str]]:
    """Map each skill to the resume lines that mention it.

    Pass `skills` to only look up specific skills (e.g. the ones a job needs).
    """
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    evidence = {}
    for skill, patterns in _PATTERNS.items():
        if skills is not None and skill not in skills:
            continue
        hits = [ln for ln in lines if any(p.search(ln) for p in patterns)]
        if hits:
            evidence[skill] = hits
    return evidence


def evidence_level(lines: list[str]) -> str:
    """'used in context' if any mention is outside a plain skills list."""
    if any(not is_listing_line(ln) for ln in lines):
        return "used in context"
    return "listed only"
