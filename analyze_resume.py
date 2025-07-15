import docx2txt
import PyPDF2
import re

def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
        return text
    elif file_path.lower().endswith('.docx'):
        text = docx2txt.process(file_path)
        return text
    else:
        raise ValueError("Unsupported file type. Please upload a .pdf or .docx file")

def extract_skills(text):
    # Example: a simple keyword list for demo purposes
    skill_keywords = ['python', 'java', 'c++', 'sql', 'javascript', 'react', 'node.js', 'docker', 'kubernetes', 'aws']
    text = text.lower()
    found_skills = set()
    for skill in skill_keywords:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill)
    return list(found_skills)

def extract_required_skills(jd_text):
    """
    Extract required skills from job description text.
    Looks for a 'Skills required:' section or bullet points under it.
    """
    pattern = r"Skills required:\s*(.*?)(?:\n\n|$)"  # non-greedy until double newline or end of text
    match = re.search(pattern, jd_text, re.DOTALL | re.IGNORECASE)
    if match:
        skills_text = match.group(1).strip()
        # Split by newlines, commas, or dashes
        skills = re.split(r'[\n,-]+', skills_text)
        # Clean and lowercase
        skills = [skill.strip().lower() for skill in skills if skill.strip()]
        # Remove duplicates
        return list(set(skills))
    else:
        # fallback: return all words split by whitespace, lowercase
        return jd_text.lower().split()
