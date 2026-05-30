from __future__ import annotations

import re


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def split_sentences(text: str) -> list[str]:
    candidates = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [item.strip(" -•\t") for item in candidates if item.strip(" -•\t")]


def find_keywords(text: str, keyword_bank: set[str]) -> list[str]:
    normalized = normalize_text(text)
    found = []
    for keyword in sorted(keyword_bank):
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, normalized):
            found.append(keyword)
    return found
