import streamlit as st
import google.generativeai as genai
import json

def get_gemini_analysis(resume_sections, jd_text):
    """Uses Gemini to find semantic matches and missing gaps."""
    
    if "GEMINI_API_KEY" not in st.secrets:
        return {"error": "API Key missing in Streamlit Secrets."}

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')

    prompt = f"""
    You are an expert ATS analyzer.
    JOB DESCRIPTION:
    {jd_text}

    RESUME SECTIONS:
    Experience: {resume_sections['EXPERIENCE']}
    Skills: {resume_sections['SKILLS']}

    TASK:
    1. Identify the top 8 essential hard skills/requirements from the JD.
    2. Categorize as: 'Matched in Experience', 'Matched in Skills Only', or 'Missing'.
    3. Provide a brief 'Why' for missing skills.

    Return JSON format:
    {{
        "analysis": [
            {{"skill": "Skill Name", "status": "Matched in Experience/Matched in Skills Only/Missing", "why": "reason"}}
        ]
    }}
    """
    try:
        response = model.generate_content(prompt)
        json_str = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(json_str)
    except Exception as e:
        if "429" in str(e):
            return {"error": "Rate limit reached. Please wait 60 seconds."}
        return {"error": f"AI Analysis failed: {str(e)}"}
