import os
from dotenv import load_dotenv
import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai
load_dotenv()
# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- GEMINI API ----------------

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- BEAUTIFUL UI ----------------

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f8fafc);
}

/* Title */
.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: 800;
    color: #2563eb;
    margin-bottom: 0px;
}

/* Subtitle */
.sub-title {
    text-align: center;
    color: #64748b;
    font-size: 18px;
    margin-bottom: 25px;
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: white;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
}

/* Metrics */
[data-testid="metric-container"] {
    background: white;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Result Card */
.result-box {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-top: 15px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
    """
    <div class='main-title'>
    📄 AI Resume Analyzer
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
    Smart Resume Analysis using Gemini AI
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "🚀 Upload your resume and get ATS Score, Skill Analysis, Career Suggestions and Interview Questions."
)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("⚙ Settings")

    target_role = st.selectbox(
        "🎯 Target Role",
        [
            "Software Engineer",
            "Data Analyst",
            "Web Developer",
            "AIML Engineer"
        ]
    )

    st.markdown("---")

    st.success("AI Powered Resume Screening")

# ---------------- UPLOAD SECTION ----------------

left, right = st.columns([2, 1])

with left:

    uploaded_file = st.file_uploader(
        "📂 Upload Resume PDF",
        type=["pdf"]
    )

with right:

    st.markdown("""
    ### ✨ Features

    ✅ Resume Score

    ✅ ATS Score

    ✅ Skills Analysis

    ✅ Missing Skills

    ✅ Strengths & Weaknesses

    ✅ Career Roadmap
    """)           
# ---------------- PROCESS PDF ----------------

if uploaded_file is not None:

    st.success("✅ Resume uploaded successfully!")

    try:

        pdf = PdfReader(uploaded_file)

        resume_text = ""

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                resume_text += page_text

        # ---------------- RESUME STATS ----------------

        st.subheader("📊 Resume Statistics")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("📄 Pages", len(pdf.pages))

        with c2:
            st.metric("📝 Words", len(resume_text.split()))

        with c3:
            st.metric("🔤 Characters", len(resume_text))

        # ---------------- PREVIEW ----------------

        with st.expander("📑 View Resume Content"):
            st.write(resume_text[:3000] + "...")

        # ---------------- ANALYZE BUTTON ----------------

        if st.button("🚀 Analyze Resume"):

            with st.spinner("🤖 AI is analyzing your resume..."):

                prompt = f"""
You are an expert ATS and HR recruiter.

Analyze this resume for the target role.

Target Role:
{target_role}

Provide:

1. Resume Score (/100)
2. ATS Score (/100)
3. Predicted Job Role
4. Skills Identified
5. Missing Skills
6. Strengths
7. Weaknesses
8. Improvement Suggestions
9. Learning Roadmap
10. Final Verdict

Resume:
{resume_text}
"""

                response = model.generate_content(prompt)

            st.subheader("📊 AI Analysis Result")

            st.markdown(
                f"""
                <div class="result-box">
                {response.text}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.download_button(
                "📥 Download Analysis Report",
                response.text,
                file_name="resume_analysis.txt",
                mime="text/plain"
            )

        # ---------------- INTERVIEW QUESTIONS ----------------

        if st.button("🎤 Generate Interview Questions"):

            with st.spinner("Generating Questions..."):

                prompt = f"""
Generate 10 interview questions for:

{target_role}

Based on this resume:

{resume_text}

Divide into:
1. Beginner
2. Intermediate
3. Advanced
"""

                response = model.generate_content(prompt)

            st.subheader("🎯 Interview Questions")

            st.markdown(
                f"""
                <div class="result-box">
                {response.text}
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:

        if "429" in str(e):
            st.warning(
                "⚠️ Gemini API limit reached. Please wait a minute and try again."
            )
        else:
            st.error(f"Error: {e}")