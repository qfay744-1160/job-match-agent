from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from agents.cv_parser import parse_cv
from agents.cv_tailor import tailor_cv
from agents.interview_prep import prepare_interview
from agents.jd_analyzer import analyze_jd
from agents.matcher import match_profile_to_job
from agents.skill_gap import analyze_skill_gap
from agents.tracker import add_application, load_applications


st.set_page_config(
    page_title="JobMatch Agent",
    page_icon="JM",
    layout="wide",
)


SAMPLE_CV = """MSc Computer Science student with experience in Python, SQL, machine learning,
data analysis, Streamlit dashboards, and web development. Built a movie recommendation
project using pandas and scikit-learn, and a job scraping project using BeautifulSoup.
Interned as a data analyst, cleaned Excel datasets, created Power BI reports, and presented
insights to stakeholders. Familiar with Git, APIs, JavaScript, HTML, CSS, and teamwork."""


SAMPLE_JD = """Junior Data Analyst role in a fintech company. Responsibilities include cleaning
large datasets, writing SQL queries, building dashboards, communicating findings, and
supporting product teams. Required skills: Python, SQL, Excel, data visualization,
communication, Git. Preferred skills: Power BI, machine learning, API integration,
financial services knowledge. Suitable for graduates with internship or project experience."""


def render_metric_card(label: str, value: str, help_text: str | None = None) -> None:
    st.metric(label, value, help=help_text)


def main() -> None:
    st.title("JobMatch Agent")
    st.caption(
        "An intelligent job application assistant that parses a CV, analyzes a job description, "
        "decides fit, and produces practical next actions."
    )

    with st.sidebar:
        st.header("Demo Controls")
        use_sample = st.toggle("Use sample CV and JD", value=True)
        st.info("This prototype uses rule-based agent logic so it can run without an API key.")

    col_cv, col_jd = st.columns(2)

    with col_cv:
        st.subheader("1. CV Input")
        cv_text = st.text_area(
            "Paste CV text",
            value=SAMPLE_CV if use_sample else "",
            height=260,
            placeholder="Paste the candidate CV or resume text here...",
        )

    with col_jd:
        st.subheader("2. Job Description Input")
        jd_text = st.text_area(
            "Paste job description",
            value=SAMPLE_JD if use_sample else "",
            height=260,
            placeholder="Paste the job description here...",
        )

    analyze = st.button("Run JobMatch Agent", type="primary", use_container_width=True)

    if analyze:
        if not cv_text.strip() or not jd_text.strip():
            st.error("Please provide both CV text and job description text.")
            return

        cv_profile = parse_cv(cv_text)
        job_profile = analyze_jd(jd_text)
        match_result = match_profile_to_job(cv_profile, job_profile)
        gap_result = analyze_skill_gap(cv_profile, job_profile, match_result)
        tailored_cv = tailor_cv(cv_profile, job_profile, gap_result)
        interview_pack = prepare_interview(cv_profile, job_profile, match_result)

        st.session_state["latest_result"] = {
            "cv_profile": cv_profile,
            "job_profile": job_profile,
            "match_result": match_result,
            "gap_result": gap_result,
            "tailored_cv": tailored_cv,
            "interview_pack": interview_pack,
        }

    latest = st.session_state.get("latest_result")

    if latest:
        cv_profile = latest["cv_profile"]
        job_profile = latest["job_profile"]
        match_result = latest["match_result"]
        gap_result = latest["gap_result"]
        tailored_cv = latest["tailored_cv"]
        interview_pack = latest["interview_pack"]

        st.divider()
        st.subheader("3. Agent Decision")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_metric_card("Match Score", f"{match_result['score']}%")
        with m2:
            render_metric_card("Seniority", job_profile["seniority"].title())
        with m3:
            render_metric_card("Required Skills Found", str(len(match_result["matched_required"])))
        with m4:
            render_metric_card("Missing Keywords", str(len(match_result["missing_keywords"])))

        st.progress(match_result["score"] / 100)
        st.write(f"**Recommendation:** {match_result['recommendation']}")

        tabs = st.tabs(
            [
                "Parsed CV",
                "JD Analysis",
                "Match & Gap",
                "CV Tailoring",
                "Interview Prep",
                "Tracker",
            ]
        )

        with tabs[0]:
            st.write("The CV Parser perceives candidate evidence from resume text.")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("**Technical Skills**")
                st.write(", ".join(cv_profile["technical_skills"]) or "None detected")
            with c2:
                st.markdown("**Projects**")
                st.write("\n".join(f"- {item}" for item in cv_profile["projects"]) or "None detected")
            with c3:
                st.markdown("**Experience Signals**")
                st.write("\n".join(f"- {item}" for item in cv_profile["experience"]) or "None detected")
            st.markdown("**Extracted Keywords**")
            st.write(", ".join(cv_profile["keywords"]))

        with tabs[1]:
            st.write("The JD Analyzer extracts what the employer explicitly and implicitly expects.")
            j1, j2 = st.columns(2)
            with j1:
                st.markdown("**Required Skills**")
                st.write(", ".join(job_profile["required_skills"]) or "None detected")
                st.markdown("**Preferred Skills**")
                st.write(", ".join(job_profile["preferred_skills"]) or "None detected")
            with j2:
                st.markdown("**Responsibilities**")
                st.write("\n".join(f"- {item}" for item in job_profile["responsibilities"]) or "None detected")
                st.markdown("**Hidden Expectations**")
                st.write("\n".join(f"- {item}" for item in job_profile["hidden_expectations"]))

        with tabs[2]:
            left, right = st.columns(2)
            with left:
                st.markdown("**Strong Match Areas**")
                st.write("\n".join(f"- {item}" for item in match_result["strong_areas"]) or "No strong areas detected")
                st.markdown("**Weak Areas**")
                st.write("\n".join(f"- {item}" for item in match_result["weak_areas"]) or "No major weak areas detected")
            with right:
                st.markdown("**Missing Keywords**")
                st.write(", ".join(match_result["missing_keywords"]) or "None")
                st.markdown("**Risk Points**")
                st.write("\n".join(f"- {item}" for item in match_result["risk_points"]) or "No major risks")

            st.markdown("**Skill Gap Plan**")
            gap_df = pd.DataFrame(
                [
                    {"Category": "Must improve before applying", "Items": ", ".join(gap_result["must_improve"])},
                    {"Category": "Can mention as learning", "Items": ", ".join(gap_result["can_mention_learning"])},
                    {"Category": "Not necessary for this role", "Items": ", ".join(gap_result["not_necessary"])},
                    {"Category": "Project evidence needed", "Items": ", ".join(gap_result["project_evidence_needed"])},
                ]
            )
            st.dataframe(gap_df, use_container_width=True, hide_index=True)

        with tabs[3]:
            st.markdown("**Resume Summary**")
            st.write(tailored_cv["summary"])
            st.markdown("**Project Bullet Points**")
            st.write("\n".join(f"- {item}" for item in tailored_cv["project_bullets"]))
            st.markdown("**Experience Bullet Points**")
            st.write("\n".join(f"- {item}" for item in tailored_cv["experience_bullets"]))
            st.markdown("**Skills Section**")
            st.write(", ".join(tailored_cv["skills_section"]))
            st.markdown("**Cover Letter Paragraph**")
            st.write(tailored_cv["cover_letter"])

        with tabs[4]:
            st.markdown("**Likely Interview Questions**")
            st.write("\n".join(f"- {item}" for item in interview_pack["likely_questions"]))
            st.markdown("**STAR Answer Drafts**")
            for answer in interview_pack["star_answers"]:
                st.info(answer)
            st.markdown("**Technical Questions**")
            st.write("\n".join(f"- {item}" for item in interview_pack["technical_questions"]))
            st.markdown("**Why This Role?**")
            st.write(interview_pack["why_this_role"])

        with tabs[5]:
            st.write("The tracker stores the agent's action recommendation as application memory.")
            with st.form("tracker_form"):
                company = st.text_input("Company", value="Example Fintech")
                role = st.text_input("Role", value="Junior Data Analyst")
                status = st.selectbox("Status", ["Interested", "Applied", "Interview", "Offer", "Rejected"])
                deadline = st.date_input("Deadline", value=date.today())
                submitted = st.form_submit_button("Save Application")

            if submitted:
                add_application(
                    company=company,
                    role=role,
                    status=status,
                    deadline=str(deadline),
                    match_score=match_result["score"],
                    next_action=match_result["next_action"],
                )
                st.success("Application saved to tracker.")

            st.dataframe(load_applications(), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
