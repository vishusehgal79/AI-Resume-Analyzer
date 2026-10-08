import re

ACTION_VERBS = {
    "achieved", "analyzed", "analysed", "applied", "automated", "built",
    "cleaned", "collaborated", "compared", "conducted", "contributed",
    "created", "delivered", "deployed", "designed", "developed", "documented",
    "engineered", "evaluated", "extracted", "generated", "implemented",
    "improved", "increased", "integrated", "launched", "led", "maintained",
    "managed", "migrated", "optimized", "optimised", "performed", "processed",
    "reduced", "reproduced", "researched", "streamlined", "tested", "trained",
    "visualized", "visualised", "wrote",
}

_BULLET_PREFIX = re.compile(r"^\s*[•●▪◦\-\*–]\s*")
ACHIEVEMENT_SECTIONS = {
    "experience",
    "work experience",
    "professional experience",
    "projects",
    "personal projects",
    "academic projects",
}

NON_ACHIEVEMENT_SECTIONS = {
    "education",
    "certifications",
    "certificates",
    "skills",
    "technical skills",
    "summary",
    "profile",
}


def _normalize_section_heading(line: str) -> str:
    """Normalize a possible resume section heading."""
    return re.sub(r"[^a-z ]", "", line.lower()).strip()


def extract_bullets(text: str) -> list[str]:
    bullets = []
    for line in text.splitlines():
        if _BULLET_PREFIX.match(line):
            bullets.append(_BULLET_PREFIX.sub("", line).strip())
    return [b for b in bullets if b]


def has_measurable_result(text: str) -> bool:
    """Detect numbers or common outcome-oriented phrases in a bullet."""

    if re.search(r"\d", text):
        return True

    outcome_patterns = (
        r"\b(increased|improved|reduced|saved|boosted|grew|accelerated)\b.*\b(by|to)\b",
        r"\b(reduced|saved|cut)\b.*\b(time|cost|effort)\b",
        r"\b(handled|processed|analyzed|analysed)\b.*\b(records|rows|users|requests|transactions|datasets)\b",
    )

    return any(re.search(pattern, text.lower()) for pattern in outcome_patterns)


def analyze_bullets(text: str) -> dict:
    """Rule-based bullet quality analysis with basic section awareness."""

    bullets = []
    current_section = None

    for line in text.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        normalized = _normalize_section_heading(stripped)

        if normalized in ACHIEVEMENT_SECTIONS:
            current_section = normalized
            continue

        if normalized in NON_ACHIEVEMENT_SECTIONS:
            current_section = normalized
            continue

        if _BULLET_PREFIX.match(line):
            bullet = _BULLET_PREFIX.sub("", line).strip()

            if not bullet:
                continue

            bullets.append((bullet, current_section))

    weak = []
    with_verb = 0
    with_metric = 0
    analyzed_bullets = 0

    for b, section in bullets:

        # Don't apply achievement-bullet rules to
        # certifications, education, skills, etc.
        if section in NON_ACHIEVEMENT_SECTIONS:
            continue

        analyzed_bullets += 1

        words = b.split()
        first = re.sub(r"[^a-z]", "", words[0].lower()) if words else ""

        has_verb = first in ACTION_VERBS
        has_metric = has_measurable_result(b)

        with_verb += has_verb
        with_metric += has_metric

        issues = []

        if not has_verb:
            issues.append("doesn't start with an action verb")

        if not has_metric:
            issues.append("no number/result")

        if issues:
            weak.append((b, issues))

    return {
        "total": analyzed_bullets,
        "with_action_verb": with_verb,
        "with_metric": with_metric,
        "weak": weak,
    }


def generate_feedback(matched, missing, levels, bullet_stats):
    """Every line below is derived from the actual resume/JD analysis."""
    strengths, weaknesses, suggestions = [], [], []

    in_context = sorted(s for s in matched if levels.get(s) == "used in context")
    listed_only = sorted(s for s in matched if levels.get(s) == "listed only")

    if in_context:
        strengths.append(f"Skills backed by project/experience text: {', '.join(in_context)}")
    if not matched:
        weaknesses.append("None of the skills this job asks for were found in your resume")

    if missing:
        weaknesses.append(f"Required skills not found: {', '.join(sorted(missing))}")
        for skill in sorted(missing)[:3]:
            suggestions.append(f"If you have used {skill}, add it with a concrete project bullet; if not, build a small project with it")
    if listed_only:
        weaknesses.append(f"Only listed, never shown in use: {', '.join(listed_only)}")
        suggestions.append(f"Add a bullet showing how you used {listed_only[0]}")

    total = bullet_stats["total"]
    if total:
        no_metric = total - bullet_stats["with_metric"]
        no_verb = total - bullet_stats["with_action_verb"]
        if bullet_stats["with_metric"] / total >= 0.5:
            strengths.append(f"{bullet_stats['with_metric']} of {total} bullets include a number/result")
        if no_metric:
            weaknesses.append(f"{no_metric} of {total} bullets have no number or measurable result")
            suggestions.append("Add a metric to weak bullets (accuracy, rows analyzed, time saved, users)")
        if no_verb:
            suggestions.append("Start each bullet with an action verb (Built, Deployed, Evaluated...)")
    else:
        weaknesses.append("No bullet points detected, so bullet quality could not be checked")

    return strengths, weaknesses, suggestions
