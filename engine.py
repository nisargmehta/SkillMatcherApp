import pdfplumber
from constants import SECTION_HEADERS

def extract_text_from_pdf(file):
    """Extracts raw text from a PDF file object."""
    with pdfplumber.open(file) as pdf:
        return "".join([page.extract_text() for page in pdf.pages])

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