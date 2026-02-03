def match_resume_to_job(resume_skills, jd_skills):
    resume_set = set(resume_skills)

    must_have = set(jd_skills["must_have"])
    good_to_have = set(jd_skills["good_to_have"])

    matched_must = resume_set & must_have
    matched_good = resume_set & good_to_have

    missing_must = must_have - resume_set
    missing_good = good_to_have - resume_set

    # Avoid division by zero
    must_score = (len(matched_must) / len(must_have)) if must_have else 1
    good_score = (len(matched_good) / len(good_to_have)) if good_to_have else 1

    # Weighted score
    final_score = round((0.7 * must_score + 0.3 * good_score) * 100, 2)

    return {
        "match_score": final_score,
        "matched_skills": sorted(matched_must | matched_good),
        "missing_must": sorted(missing_must),
        "missing_good": sorted(missing_good)
    }
