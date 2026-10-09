def compare_skills(
    resume_skills: list[str],
    job_skills: list[str],
) -> dict:
    """
    Compare candidate skills against skills required by a job.
    """

    resume_set = {skill.lower(): skill for skill in resume_skills}
    job_set = {skill.lower(): skill for skill in job_skills}

    matched_skills = []
    missing_skills = []

    for normalized_skill, original_skill in job_set.items():
        if normalized_skill in resume_set:
            matched_skills.append(original_skill)
        else:
            missing_skills.append(original_skill)

    total_required = len(job_set)

    if total_required == 0:
        match_score = 0.0
    else:
        match_score = round(
            (len(matched_skills) / total_required) * 100,
            2,
        )

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_score": match_score,
    }