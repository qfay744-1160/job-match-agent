from __future__ import annotations

from pathlib import Path

import pandas as pd


TRACKER_PATH = Path("data/applications.csv")
TRACKER_COLUMNS = ["company", "role", "status", "deadline", "match_score", "next_action"]


def load_applications() -> pd.DataFrame:
    if not TRACKER_PATH.exists():
        return pd.DataFrame(columns=TRACKER_COLUMNS)
    return pd.read_csv(TRACKER_PATH)


def add_application(
    company: str,
    role: str,
    status: str,
    deadline: str,
    match_score: int,
    next_action: str,
) -> None:
    TRACKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = load_applications()
    new_row = pd.DataFrame(
        [
            {
                "company": company,
                "role": role,
                "status": status,
                "deadline": deadline,
                "match_score": match_score,
                "next_action": next_action,
            }
        ]
    )
    pd.concat([existing, new_row], ignore_index=True).to_csv(TRACKER_PATH, index=False)
