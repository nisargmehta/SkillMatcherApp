import streamlit as st
from engine import extract_text_from_pdf, extract_sections
from analyzer import get_gemini_analysis

st.set_page_config(page_title="Pro ATS Matcher", layout="wide")
st.title("🎯 Smart ATS Skill Matcher")

col1, col2 = st.columns(2)
with col1:
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
with col2:
    jd_text = st.text_area("Paste Job Description:", height=250)

if st.button("Run Analysis", type="primary"):
    if resume_file and jd_text:
        with st.spinner("Processing..."):
            # 1. Extract and Sectionalize
            raw_text = extract_text_from_pdf(resume_file)
            sections = extract_sections(raw_text)
            
            # 2. Analyze
            result = get_gemini_analysis(sections, jd_text)
            
            if "error" in result:
                st.error(result["error"])
            else:
                # 3. Display Results
                score = sum(2 if "Experience" in i['status'] else 1 if "Skills" in i['status'] else 0 for i in result['analysis'])
                total = len(result['analysis']) * 2
                final_pct = int((score / total) * 100)
                
                st.header(f"Match Score: {final_pct}%")
                st.progress(final_pct / 100)
                
                c1, c2 = st.columns(2)
                with c1:
                    st.success("**Strengths**")
                    for i in result['analysis']:
                        if "Matched" in i['status']: st.write(f"✅ {i['skill']}")
                with c2:
                    st.error("**Missing**")
                    for i in result['analysis']:
                        if i['status'] == "Missing": st.write(f"❌ {i['skill']}: {i['why']}")
    else:
        st.warning("Please upload a resume and paste a JD.")
