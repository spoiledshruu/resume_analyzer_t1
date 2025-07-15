import streamlit as st
import tempfile
import torch

from modules.analyze_resume import extract_text_from_file, extract_skills, extract_required_skills
from modules.extra_features import extract_experience_periods
from modules.salary_estimator import estimate_salary
from modules.interview_questions import generate_interview_questions
from modules.ats_checker import check_ats_score
from modules.role_classifier import classify_job_role
from modules.visualization import plot_keyword_density, plot_skill_match_radar
from modules.ml_visualization import plot_role_prediction_confidence

st.set_page_config(page_title="📄 Resume Analyzer", layout="wide")
st.title("💼 AI-Powered Resume Analyzer")

# Sidebar
with st.sidebar:
    st.header("🔎 Upload Files")
    resume_file = st.file_uploader("📄 Upload Resume (.pdf or .docx)", type=['pdf', 'docx'])
    jd_file = st.file_uploader("📋 Upload Job Description (.txt)", type=['txt'])
    st.markdown("---")
    st.info("Upload your resume and job description to get started!")

if resume_file and jd_file:
    try:
        # Save resume temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix="." + resume_file.name.split('.')[-1]) as temp_resume:
            temp_resume.write(resume_file.read())
            resume_path = temp_resume.name

        resume_text = extract_text_from_file(resume_path)
        jd_text = jd_file.read().decode('utf-8')

        # Extract data
        years, months = extract_experience_periods(resume_text)
        total_exp_years = round(years + months / 12, 1)

        resume_skills = extract_skills(resume_text)
        required_skills = extract_required_skills(jd_text)

        matched_skills = list(set(resume_skills) & set(required_skills))
        skill_match_percentage = (len(matched_skills) / len(required_skills) * 100) if required_skills else 0

        # AI Analysis
        questions = generate_interview_questions(resume_skills, required_skills)
        level, salary = estimate_salary(total_exp_years, resume_skills)
        ats_score, ats_feedback = check_ats_score(resume_text)
        predicted_role, matched_count, role_confidences = classify_job_role(resume_skills, return_confidences=True)

        # Layout
        st.subheader("📊 Career Insights")
        col1, col2, col3 = st.columns(3)
        col1.metric("Experience", f"{total_exp_years} yrs")
        col2.metric("Estimated Level", level)
        col3.metric("Estimated Salary", f"${salary:,.0f}")

        st.markdown("---")
        col4, col5 = st.columns([1, 2])
        with col4:
            st.metric("ATS Score", f"{ats_score}/100")
        with col5:
            for fb in ats_feedback:
                st.warning(f"⚠️ {fb}")

        st.markdown("---")

        # Role
        st.subheader("💼 Predicted Role")
        st.success(f"{predicted_role} (matched {matched_count} key skills)")

        st.markdown("---")

        # Skill Match Summary
        st.subheader("🎯 Skill Match")
        st.write(f"Matched {len(matched_skills)} out of {len(required_skills)} required skills.")
        st.write(f"Skill Match Percentage: {skill_match_percentage:.1f}%")

        # Graphs
        tab1, tab2, tab3 = st.tabs(["📌 Keyword Match", "📉 Role Confidence", "🎯 Skill Match Radar"])

        with tab1:
            st.markdown("Required skills presence in resume:")
            fig_keyword = plot_keyword_density(resume_text, required_skills)
            st.pyplot(fig_keyword)

        with tab2:
            roles = list(role_confidences.keys())
            probs = torch.tensor(list(role_confidences.values()))
            fig_role = plot_role_prediction_confidence(roles, probs)
            st.pyplot(fig_role)

        with tab3:
            fig_radar = plot_skill_match_radar(required_skills, resume_skills)
            st.pyplot(fig_radar)

        # Questions
        st.markdown("---")
        with st.expander("🧠 Suggested Interview Questions"):
            for i, q in enumerate(questions, 1):
                st.markdown(f"{i}. {q}")

        # Optional: Resume text preview
        with st.expander("📄 Preview Extracted Resume Text"):
            st.text(resume_text[:2000])  # limit preview

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")
else:
    st.info("Awaiting file uploads to begin analysis.")
