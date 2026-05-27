## Summary
A simplified ATS Skill checker. It combines document processing, web scraping, and NLP (Natural Language Processing).

### Details
Given a resume (pdf) and a job description we want to find out the critical gaps.
- Sectional Awareness: We will use Regex to split your resume into blocks (e.g., EXPERIENCE, SKILLS, EDUCATION).
- Semantic Matching: We will send these sections to Gemini to verify if the candidate actually did the tasks described in the JD.
- Weighted Scoring: Experience matches will now carry 2x weight, while Skills/Summary matches carry 1x.
