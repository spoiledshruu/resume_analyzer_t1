import re

def extract_experience_periods(text):
    """
    Extract years and months of experience from text.
    """
    text = text.lower()
    patterns = [
        r'(\d+)\s+years?\s*(\d+)?\s*months?',
        r'(\d+)\s+yrs?\s*(\d+)?\s*mos?',
        r'(\d+)\s+years?',
        r'(\d+)\s+yrs?'
    ]

    total_years = 0
    total_months = 0

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                years = int(match[0]) if match[0].isdigit() else 0
                months = int(match[1]) if len(match) > 1 and match[1].isdigit() else 0
            else:
                years = int(match) if match.isdigit() else 0
                months = 0
            total_years += years
            total_months += months

    total_years += total_months // 12
    total_months = total_months % 12

    return total_years, total_months
