def estimate_salary(total_exp_years, skills):
    """
    Estimate level and salary based on experience and skills.
    """
    if total_exp_years < 2:
        level = 'Junior'
        base_salary = 45000
    elif total_exp_years < 5:
        level = 'Mid'
        base_salary = 70000
    else:
        level = 'Senior'
        base_salary = 100000

    # Add bonus for certain skills
    bonus_skills = ['aws', 'docker', 'kubernetes', 'machine learning', 'data science']
    bonus = 0
    for skill in skills:
        if skill in bonus_skills:
            bonus += 5000

    estimated_salary = base_salary + bonus
    return level, estimated_salary
