import pandas as pd
import re


def load_skills(skill_file="data/skills.csv"):
    df = pd.read_csv(skill_file)
    skill_map = {}

    for _, row in df.iterrows():
        aliases = row["aliases"].split("|")
        for alias in aliases:
            skill_map[alias.lower()] = row["skill"].lower()

    return skill_map


def extract_skills(resume_text):
    resume_text = resume_text.lower()
    resume_text = re.sub(r"[^a-z0-9+ ]", " ", resume_text)

    skill_map = load_skills()
    extracted_skills = set()

    for alias, skill in skill_map.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, resume_text):
            extracted_skills.add(skill)

    return sorted(extracted_skills)
