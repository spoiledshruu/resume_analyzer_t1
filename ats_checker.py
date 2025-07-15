def check_ats_score(text):
    """
    Simple heuristic ATS score based on resume length and presence of sections.
    """
    feedback = []
    score = 100

    length = len(text.split())
    if length < 300:
        score -= 20
        feedback.append("Resume is too short for ATS (should be 300+ words)")

    required_sections = ['education', 'experience', 'skills', 'certifications']
    text_lower = text.lower()
    for section in required_sections:
        if section not in text_lower:
            score -= 10
            feedback.append(f"Missing section: {section.capitalize()}")

    score = max(0, min(100, score))
    return score, feedback
