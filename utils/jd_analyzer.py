import re
from utils.skill_extractor import extract_skills


def classify_skills(jd_text):
    jd_text_lower = jd_text.lower()

    all_skills = extract_skills(jd_text)

    must_have = set()
    good_to_have = set()

    for skill in all_skills:
        pattern = r"(must|required|mandatory).*" + re.escape(skill)
        if re.search(pattern, jd_text_lower):
            must_have.add(skill)
        else:
            good_to_have.add(skill)

    return {
        "all_skills": sorted(all_skills),
        "must_have": sorted(must_have),
        "good_to_have": sorted(good_to_have)
    }
