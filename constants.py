# Section Headers for Resume Parsing
SECTION_HEADERS = {
    "EXPERIENCE": ["experience", "work history", "employment", "professional background"],
    "SKILLS": ["skills", "technical skills", "technologies", "competencies"],
    "EDUCATION": ["education", "academic background", "certifications"]
}

# Hiring jargon to ignore during extraction (if using the hybrid engine)
JD_BLACKLIST = {
    "experience", "years", "bachelor", "degree", "equivalent", "practical",
    "minimum", "qualifications", "job", "products", "product", "year",
    "plus", "preferred", "required", "requirements", "teams", "team", 
    "excellent", "written", "verbal", "skills", "ability", "work"
}