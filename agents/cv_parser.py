from __future__ import annotations

from agents.constants import SKILL_KEYWORDS
from agents.text_utils import find_keywords, split_sentences


def parse_cv(cv_text: str) -> dict:
    """Extract candidate evidence from CV text."""
    sentences = split_sentences(cv_text)
    skills = find_keywords(cv_text, SKILL_KEYWORDS)

    education = [
        sentence
        for sentence in sentences
        if any(token in sentence.lower() for token in ["university", "bachelor", "master", "msc", "degree"])
    ]
    experience = [
        sentence
        for sentence in sentences
        if any(token in sentence.lower() for token in ["intern", "worked", "experience", "stakeholder", "presented"])
    ]
    projects = [
        sentence
        for sentence in sentences
        if any(token in sentence.lower() for token in ["project", "built", "created", "developed"])
    ]
    achievements = [
        sentence
        for sentence in sentences
        if any(token in sentence.lower() for token in ["improved", "reduced", "increased", "award", "achieved"])
    ]

    return {
        "education": education[:4],
        "experience": experience[:5],
        "technical_skills": skills,
        "projects": projects[:5],
        "achievements": achievements[:4],
        "keywords": skills,
        "raw_text": cv_text,
    }
