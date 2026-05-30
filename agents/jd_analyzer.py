from __future__ import annotations

from agents.constants import RESPONSIBILITY_VERBS, SENIORITY_KEYWORDS, SKILL_KEYWORDS
from agents.text_utils import find_keywords, normalize_text, split_sentences


def _extract_seniority(text: str) -> str:
    normalized = normalize_text(text)
    for keyword, level in SENIORITY_KEYWORDS.items():
        if keyword in normalized:
            return level
    return "unspecified"


def _split_required_preferred(text: str, skills: list[str]) -> tuple[list[str], list[str]]:
    normalized = normalize_text(text)
    sections = [section.strip() for section in normalized.split(".") if section.strip()]
    required = set()
    preferred = set()

    for section in sections:
        section_skills = [skill for skill in skills if skill in section]
        if not section_skills:
            continue
        if any(marker in section for marker in ["preferred", "nice to have", "plus", "bonus"]):
            preferred.update(section_skills)
        elif any(marker in section for marker in ["required", "must have", "responsibilities include", "responsibilities"]):
            required.update(section_skills)

    unclassified = set(skills) - required - preferred
    required.update(unclassified)
    preferred -= required

    return sorted(required), sorted(preferred)


def analyze_jd(jd_text: str) -> dict:
    """Extract explicit and implicit job expectations from a job description."""
    sentences = split_sentences(jd_text)
    skills = find_keywords(jd_text, SKILL_KEYWORDS)
    required, preferred = _split_required_preferred(jd_text, skills)

    responsibilities = [
        sentence
        for sentence in sentences
        if any(sentence.lower().startswith(verb) or f" {verb}" in sentence.lower() for verb in RESPONSIBILITY_VERBS)
    ]

    hidden_expectations = []
    normalized = normalize_text(jd_text)
    if "stakeholder" in normalized or "communicat" in normalized:
        hidden_expectations.append("Translate technical analysis into clear business communication.")
    if "dashboard" in normalized or "visualization" in normalized:
        hidden_expectations.append("Show evidence of presenting insights through dashboards or reports.")
    if "graduate" in normalized or "junior" in normalized:
        hidden_expectations.append("Demonstrate learning ability and project evidence, not only professional experience.")
    if "fintech" in normalized or "financial" in normalized:
        hidden_expectations.append("Connect data skills to financial or product decision-making.")

    industry = "technology"
    if "fintech" in normalized or "financial" in normalized:
        industry = "fintech / financial services"
    elif "health" in normalized:
        industry = "healthcare"
    elif "education" in normalized:
        industry = "education"

    return {
        "required_skills": required,
        "preferred_skills": preferred,
        "responsibilities": responsibilities[:6],
        "seniority": _extract_seniority(jd_text),
        "industry": industry,
        "hidden_expectations": hidden_expectations or ["Provide concrete evidence for the most important required skills."],
        "keywords": skills,
        "raw_text": jd_text,
    }
