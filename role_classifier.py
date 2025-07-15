def classify_job_role(skills, return_confidences=False):
    """
    Classify job role based on core skill sets.
    """
    roles = {
        "Software Developer": {'python', 'java', 'c++', 'react', 'node.js'},
        "Data Scientist": {'python', 'machine learning', 'data science', 'tensorflow', 'pandas'},
        "DevOps Engineer": {'docker', 'kubernetes', 'aws', 'terraform'}
    }

    confidences = {}
    for role, core_skills in roles.items():
        matched = len(set(skills) & core_skills)
        confidences[role] = matched / len(core_skills) if core_skills else 0

    best_role = max(confidences, key=confidences.get)
    confidence_score = confidences[best_role]

    if return_confidences:
        return best_role, confidence_score, confidences
    else:
        return best_role, confidence_score
