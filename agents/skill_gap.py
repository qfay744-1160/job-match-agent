from __future__ import annotations


def analyze_skill_gap(cv_profile: dict, job_profile: dict, match_result: dict) -> dict:
    missing_required = match_result["missing_required"]
    missing_preferred = match_result["missing_preferred"]

    project_evidence_needed = []
    for skill in missing_required[:4]:
        project_evidence_needed.append(f"Create or describe a project that demonstrates {skill}.")

    not_necessary = [
        skill
        for skill in job_profile["preferred_skills"]
        if skill not in cv_profile["technical_skills"] and skill not in missing_required
    ]

    return {
        "must_improve": missing_required[:5],
        "can_mention_learning": missing_preferred[:5],
        "not_necessary": not_necessary[:5],
        "project_evidence_needed": project_evidence_needed,
    }
