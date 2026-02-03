from utils.skill_extractor import extract_skills
from utils.jd_analyzer import classify_skills
from utils.matching_engine import match_resume_to_job
from utils.gemini_suggestions import generate_ai_suggestions
import time


import streamlit as st
from utils.resume_parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

def render_skill_chips(skills, chip_class):
    if not skills:
        st.write("None")
        return

    chips_html = ""
    for skill in skills:
        chips_html += f"<span class='skill-chip {chip_class}'>{skill}</span>"

    st.markdown(chips_html, unsafe_allow_html=True)


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)
st.markdown("""
<style>
div.block-container {
    max-width: none !important;
}
.skill-chip {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px 6px 4px 0;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    color: white;
}
.matched { background-color: #16a34a; }      /* green */
.missing-must { background-color: #dc2626; } /* red */
.missing-good { background-color: #f59e0b; } /* amber */
.jd-skill { background-color: #2563eb; } /* blue */

</style>
""", unsafe_allow_html=True)


st.title("📄 AI Resume Analyzer & Job Matcher")
st.caption("ATS-style resume evaluation with skill gap analysis")
st.divider()

with st.container():
    st.subheader("📤 Upload Resume")
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF or DOCX)",
        type=["pdf", "docx"]
    )

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.success("Resume uploaded and parsed successfully!")



    skills = extract_skills(resume_text)

    if skills:
        with st.container():
            st.subheader("🧠 Extracted Resume Skills")
            render_skill_chips(skills, "matched")

    else:
        st.warning("No recognizable skills found.")

with st.container():
    st.subheader("📌 Paste Job Description")
    job_description = st.text_area("Job Description", height=200)

if job_description:
    jd_skills = classify_skills(job_description)

    st.subheader("🧾 Job Skills Extracted")
    # render_skill_chips(jd_skills["all_skills"], "jd-skill")


    with st.expander("📄 Job Skills Overview"):
        render_skill_chips(jd_skills["all_skills"], "jd-skill")

if uploaded_file and job_description:
    match_result = match_resume_to_job(skills, jd_skills)

    with st.container():
      st.subheader("📊 Match Results")

    final_score = int(match_result["match_score"])

    score_placeholder = st.empty()
    progress_placeholder = st.empty()

    # Animate score & progress bar
    for i in range(0, final_score + 1):
        score_placeholder.markdown(f"### {i}% Match Score")
        progress_placeholder.progress(i / 100)
        time.sleep(0.02)

    score_placeholder.markdown(f"### {final_score}% Match Score")
    progress_placeholder.progress(final_score / 100)



    st.write("### ✅ Matched Skills")
    render_skill_chips(match_result["matched_skills"], "matched")


    st.write("### ❌ Missing Must-Have Skills")
    render_skill_chips(match_result["missing_must"], "missing-must")

    st.write("### ⚠️ Missing Good-to-Have Skills")
    render_skill_chips(match_result["missing_good"], "missing-good")


    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Chances of Selection")
        if final_score >= 80:
            st.success("High Chances of Selection 🟢")
        elif final_score >= 60:
            st.warning("Medium Chances of Selection 🟡")
        else:
            st.error("Low Chances of Selection 🔴")

    with col2:
        st.subheader("🧠 Final Verdict")
        if final_score >= 80:
            st.success("Strong match. You are ready to apply.")
        elif final_score >= 60:
            st.warning("Moderate match. Improve key skills before applying.")
        else:
            st.error("Low match. Skill development recommended.")

    st.divider()
    st.subheader(" Resume Improvement Suggestions")

    if st.button("Generate AI Suggestions"):
        with st.spinner("Generating insights..."):
            try:
                ai_output = generate_ai_suggestions(match_result, jd_skills)

                why_text = ""
                improve_text = ""
                skills_text = ""

                # Parse the output based on headers
                parts = ai_output.split("### ")
                for part in parts:
                    if "Why this score?" in part:
                        why_text = part.replace("📌 Why this score?", "").strip()
                    elif "What to improve?" in part:
                        improve_text = part.replace("🛠️ What to improve?", "").strip()
                    elif "Skills to focus on" in part:
                        skills_text = part.replace("📚 Skills to focus on", "").strip()

                with st.expander("📌 Why this score?", expanded=True):
                    st.markdown(why_text)

                with st.expander("🛠️ What to improve?", expanded=True):
                    st.markdown(improve_text)

                with st.expander("📚 Skills to focus on", expanded=True):
                    st.markdown(skills_text)

            except Exception as e:
                st.error(f"Error generating suggestions: {e}")

