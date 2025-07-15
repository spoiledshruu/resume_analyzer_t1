import matplotlib.pyplot as plt
import numpy as np

def plot_keyword_density(resume_text, required_skills):
    """
    Creates a bar chart figure showing which required skills are present in the resume text.
    Green bars indicate skill found, red bars indicate missing skill.
    Returns the matplotlib figure object.
    """
    resume_text = resume_text.lower()

    presence = []
    for skill in required_skills:
        presence.append(1 if skill.lower() in resume_text else 0)

    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(required_skills, presence, color=['green' if p else 'red' for p in presence])
    ax.set_ylim(0, 1.2)
    ax.set_ylabel('Presence')
    ax.set_title('Required Skills Match in Resume')
    plt.xticks(rotation=45, ha='right')

    # Add labels on top of bars
    for bar, p in zip(bars, presence):
        label = 'Found' if p == 1 else 'Missing'
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, label, ha='center')

    plt.tight_layout()
    return fig


def plot_skill_match_radar(skills_resume, skills_job):
    """
    Creates a radar chart figure comparing skill matches between resume and job description.
    Returns the matplotlib figure object.
    """
    # Union of all skills
    all_skills = list(set(skills_resume) | set(skills_job))
    resume_presence = [1 if skill in skills_resume else 0 for skill in all_skills]
    job_presence = [1 if skill in skills_job else 0 for skill in all_skills]

    angles = np.linspace(0, 2 * np.pi, len(all_skills), endpoint=False).tolist()
    resume_presence += resume_presence[:1]
    job_presence += job_presence[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, resume_presence, color='blue', alpha=0.25, label='Resume Skills')
    ax.fill(angles, job_presence, color='red', alpha=0.25, label='Job Skills')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(all_skills, fontsize=9)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(['0', '0.5', '1'])
    ax.set_ylim(0, 1)
    ax.set_title('Skill Match Radar')
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    plt.tight_layout()
    return fig
