import streamlit as st
import pdfplumber
import re
import json
import google.generativeai as genai

# --- SECURE CONFIGURATION ---
# Check if key exists in secrets before proceeding
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-3.5-flash')

# Common Resume Section Headers
SECTION_HEADERS = {
    "EXPERIENCE": ["experience", "work history", "employment", "professional background"],
    "SKILLS": ["skills", "technical skills", "technologies", "competencies"],
    "EDUCATION": ["education", "academic background", "certifications"]
}

# --- LOGIC FUNCTIONS ---

def extract_sections(text):
    """Splits resume text into logic blocks based on common headers."""
    sections = {"SUMMARY": "", "EXPERIENCE": "", "SKILLS": "", "EDUCATION": ""}
    current_section = "SUMMARY"
    
    lines = text.split('\n')
    for line in lines:
        clean_line = line.strip().lower()
        found_header = False
        
        for section, keywords in SECTION_HEADERS.items():
            if any(clean_line == k or clean_line.startswith(k + ":") for k in keywords):
                current_section = section
                found_header = True
                break
        
        if not found_header:
            sections[current_section] += line + "\n"
            
    return sections

def get_gemini_analysis(resume_sections, jd_text):
    """Uses Gemini to find semantic matches and missing gaps."""
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) analyzer.
    JOB DESCRIPTION:
    {jd_text}

    RESUME SECTIONS:
    Experience: {resume_sections['EXPERIENCE']}
    Skills: {resume_sections['SKILLS']}

    TASK:
    1. Identify the top 8 essential hard skills/requirements from the JD.
    2. For each skill, check the Resume Sections. 
    3. Categorize as: 'Matched in Experience' (Strongest), 'Matched in Skills Only' (Medium), or 'Missing' (Gap).
    4. Provide a brief 'Why' for missing skills.

    Return the result in JSON format only:
    {{
        "analysis": [
            {{"skill": "Skill Name", "status": "Matched in Experience/Matched in Skills Only/Missing", "why": "reason"}}
        ]
    }}
    """
    try:
        response = model.generate_content(prompt)
        return json.loads(response.text.strip())
    except Exception as e:
        if "429" in str(e):
            return {"error": "Free tier limit reached. Please wait a minute and try again!"}
        return {"error": f"AI Analysis failed: {str(e)}"}

# --- UI SETUP ---
st.set_page_config(page_title="AI Pro ATS", layout="wide")
st.title("🧠 ATS Skill Matcher")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
with col2:
    jd_text = st.text_area("Paste Job Description:", height=250)

if st.button("Run Analysis", type="primary"):
    if resume_file and jd_text:
        with st.spinner("Analyzing sectional relevance and semantic matches..."):
            # 1. Extract Text
            with pdfplumber.open(resume_file) as pdf:
                full_text = "".join([p.extract_text() for p in pdf.pages])
            
            # 2. Sectional Awareness
            sections = extract_sections(full_text)
            
            # 3. AI Analysis
            result = get_gemini_analysis(sections, jd_text)
            
            if "error" in result:
                st.error(result["error"])
            else:
                # 4. Weighted Scoring Logic
                score = 0
                total_possible = len(result['analysis']) * 2
                
                for item in result['analysis']:
                    if item['status'] == "Matched in Experience":
                        score += 2
                    elif item['status'] == "Matched in Skills Only":
                        score += 1
                
                final_percentage = int((score / total_possible) * 100)
                
                # --- RESULTS UI ---
                st.divider()
                st.header(f"Match Rating: {final_percentage}%")
                st.progress(final_percentage / 100)
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.subheader("✅ Strengths")
                    for item in result['analysis']:
                        if "Matched" in item['status']:
                            st.write(f"**{item['skill']}** ({item['status']})")
                
                with res_col2:
                    st.subheader("❌ Critical Gaps")
                    for item in result['analysis']:
                        if item['status'] == "Missing":
                            st.write(f"**{item['skill']}**: {item['why']}")
                            
    else:
        st.warning("Please provide both a resume and a job description.")
