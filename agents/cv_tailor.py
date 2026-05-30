from __future__ import annotations


def tailor_cv(cv_profile: dict, job_profile: dict, gap_result: dict) -> dict:
    matched_skills = [skill for skill in job_profile["keywords"] if skill in cv_profile["technical_skills"]]
    top_skills = matched_skills[:6] or cv_profile["technical_skills"][:6]
    industry = job_profile["industry"]

    summary = (
        f"Graduate candidate with hands-on experience in {', '.join(top_skills[:4])}. "
        f"Interested in applying analytical and technical skills to {industry} problems, "
        "with project evidence in data-driven problem solving and clear communication."
    )

    project_bullets = []
    for skill in top_skills[:4]:
        project_bullets.append(
            f"Applied {skill} in a practical project to analyze requirements, build outputs, and communicate results."
        )
    if not project_bullets:
        project_bullets.append("Built a practical project that demonstrates problem solving, technical learning, and communication.")

    experience_bullets = [
        "Translated messy information into structured outputs that supported decision-making.",
        "Collaborated with stakeholders to understand requirements and present findings clearly.",
    ]
    if job_profile["responsibilities"]:
        experience_bullets.insert(0, f"Prepared to contribute to responsibilities such as: {job_profile['responsibilities'][0]}")

    cover_letter = (
        f"I am interested in this role because it combines {', '.join(top_skills[:3])} with practical "
        f"{industry} impact. My CV shows relevant project and learning evidence, and I am currently improving "
        f"{', '.join(gap_result['must_improve'][:2]) if gap_result['must_improve'] else 'role-specific skills'} "
        "to contribute effectively as a junior candidate."
    )

    return {
        "summary": summary,
        "project_bullets": project_bullets,
        "experience_bullets": experience_bullets,
        "skills_section": sorted(set(top_skills + job_profile["required_skills"][:4])),
        "cover_letter": cover_letter,
    }
