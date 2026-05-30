from __future__ import annotations


def match_profile_to_job(cv_profile: dict, job_profile: dict) -> dict:
    """Compare candidate evidence with job expectations and produce a decision."""
    cv_skills = set(cv_profile["technical_skills"])
    required = set(job_profile["required_skills"])
    preferred = set(job_profile["preferred_skills"])
    all_job_keywords = required | preferred

    matched_required = sorted(required & cv_skills)
    matched_preferred = sorted(preferred & cv_skills)
    missing_required = sorted(required - cv_skills)
    missing_preferred = sorted(preferred - cv_skills)
    missing_keywords = sorted(all_job_keywords - cv_skills)

    required_score = len(matched_required) / max(len(required), 1)
    preferred_score = len(matched_preferred) / max(len(preferred), 1)
    evidence_bonus = 0.1 if cv_profile["projects"] else 0
    experience_bonus = 0.1 if cv_profile["experience"] else 0
    score = round(min(1.0, required_score * 0.65 + preferred_score * 0.15 + evidence_bonus + experience_bonus) * 100)

    strong_areas = matched_required + matched_preferred
    weak_areas = missing_required[:5]

    risk_points = []
    if missing_required:
        risk_points.append("Some required skills are missing or not visible in the CV.")
    if job_profile["seniority"] in {"mid-level", "senior"}:
        risk_points.append("The role may expect more professional experience than a graduate candidate has.")
    if not cv_profile["projects"]:
        risk_points.append("The CV needs stronger project evidence for this role.")

    if score >= 75:
        recommendation = "Strong fit. Apply after tailoring the CV with job-specific keywords."
        next_action = "Tailor CV and submit application."
    elif score >= 55:
        recommendation = "Moderate fit. Apply if the candidate can add evidence for missing skills."
        next_action = "Add project evidence and revise key bullets before applying."
    else:
        recommendation = "Weak fit. Build missing skills or choose a more suitable junior role first."
        next_action = "Close skill gaps before applying."

    realistic_for_junior = score >= 55 and job_profile["seniority"] in {"intern", "graduate", "junior", "unspecified"}

    return {
        "score": score,
        "matched_required": matched_required,
        "matched_preferred": matched_preferred,
        "missing_required": missing_required,
        "missing_preferred": missing_preferred,
        "missing_keywords": missing_keywords,
        "strong_areas": strong_areas,
        "weak_areas": weak_areas,
        "risk_points": risk_points,
        "recommendation": recommendation,
        "next_action": next_action,
        "realistic_for_junior": realistic_for_junior,
    }
