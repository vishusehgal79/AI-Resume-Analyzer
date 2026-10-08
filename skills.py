import re


# Canonical skill name -> variations that may appear in resumes/JDs.
#
# The canonical name is what the rest of the application uses.
skills_dict = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "sql": ["sql"],
    "react": ["react", "react.js", "reactjs"],
    "javascript": ["javascript"],
    "machine learning": ["machine learning", "machine-learning", "ml"],
    "data analysis": ["data analysis", "data analytics"],
    "deep learning": ["deep learning", "deep-learning", "dl"],
    "nlp": [
        "nlp",
        "natural language processing",
        "natural-language processing",
    ],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "power bi": ["power bi", "power-bi"],
    "excel": ["excel", "microsoft excel"],
    "tableau": ["tableau"],
    "git": ["git"],
    "github": ["github"],
}


# Compile patterns once when the module is imported.
#
# (?<!\w) and (?!\w) prevent matching a skill inside a larger word.
# For example:
#
#     git       -> match
#     digital   -> no match
#
# We don't use \b because skills such as C++ contain '+' characters.
_PATTERNS = {
    skill: [
        re.compile(
            rf"(?<!\w){re.escape(variation)}(?!\w)",
            re.IGNORECASE,
        )
        for variation in variations
    ]
    for skill, variations in skills_dict.items()
}


def extract_skills(text: str) -> list[str]:
    """Return canonical skills found in the supplied text."""

    if not text:
        return []

    found = set()

    for skill, patterns in _PATTERNS.items():
        if any(pattern.search(text) for pattern in patterns):
            found.add(skill)

    return sorted(found)


# ---------------------------------------------------------
# Skill evidence
# ---------------------------------------------------------


def is_listing_line(line: str) -> bool:
    """Heuristic for detecting skill-list lines rather than usage evidence."""
    text = line.strip().lower()

    # Common resume headings that usually introduce lists.
    listing_prefixes = (
        "skills:",
        "technical skills:",
        "technologies:",
        "tools:",
        "languages:",
        "frameworks:",
        "libraries:",
    )

    if text.startswith(listing_prefixes):
        return True

    # Comma-heavy short lines are also likely to be lists.
    commas = line.count(",")
    if commas >= 2 and len(line.split()) / commas < 3.5:
        return True

    return False


def find_skill_evidence(
    text: str,
    skills: list[str] | None = None,
) -> dict[str, list[str]]:
    """Return resume lines containing each requested skill."""

    if not text:
        return {}

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    evidence = {}

    for skill, patterns in _PATTERNS.items():

        if skills is not None and skill not in skills:
            continue

        hits = [
            line
            for line in lines
            if any(pattern.search(line) for pattern in patterns)
        ]

        if hits:
            evidence[skill] = hits

    return evidence


def evidence_level(lines: list[str]) -> str:
    """Classify skill evidence as listed-only or used in context."""

    if any(not is_listing_line(line) for line in lines):
        return "used in context"

    return "listed only"
