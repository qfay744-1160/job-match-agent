from __future__ import annotations


def prepare_interview(cv_profile: dict, job_profile: dict, match_result: dict) -> dict:
    top_skills = match_result["strong_areas"][:4] or cv_profile["technical_skills"][:4]
    missing = match_result["missing_keywords"][:3]

    likely_questions = [
        "Tell me about yourself and why you are interested in this role.",
        "Which project best demonstrates your fit for this job?",
        "How do you handle a skill requirement that you have not fully mastered yet?",
    ]
    likely_questions.extend([f"Can you explain your experience with {skill}?" for skill in top_skills[:3]])

    star_answers = [
        "Situation: I worked on a project with unclear data requirements. Task: I needed to create a useful output. Action: I cleaned the data, selected relevant features, and built a simple analysis or dashboard. Result: The final output made the findings easier to understand and explain.",
        "Situation: I noticed a gap between my current skills and a target role. Task: I needed to improve quickly. Action: I built a focused project and documented the learning process. Result: I gained evidence that could be shown in my CV and interview.",
    ]

    technical_questions = [f"How would you use {skill} in this role?" for skill in top_skills[:4]]
    technical_questions.extend([f"What is your plan to improve {skill}?" for skill in missing])

    why_this_role = (
        f"This role fits my goal because it uses {', '.join(top_skills[:3]) or 'my technical foundation'} "
        f"in a {job_profile['industry']} context. I am especially interested in the responsibilities around "
        f"{job_profile['responsibilities'][0] if job_profile['responsibilities'] else 'solving practical business problems'}."
    )

    return {
        "likely_questions": likely_questions,
        "star_answers": star_answers,
        "technical_questions": technical_questions,
        "project_explanation": "Explain the project goal, the tools used, the decision process, and the measurable outcome.",
        "why_this_role": why_this_role,
    }
