import re
from typing import List, Dict


# ============================================================
# PROFICIENCY TERMS
# ============================================================

LOW_PROFICIENCY_TERMS = [
    "basic",
    "beginner",
    "beginners",
    "familiar",
    "familiarity",
    "exposure",
    "working knowledge",
    "limited experience",
    "introductory",
]

HIGH_PROFICIENCY_TERMS = [
    "advanced",
    "expert",
    "expertise",
    "proficient",
    "proficiency",
    "strong",
    "extensive experience",
    "deep knowledge",
]


# ============================================================
# GET THE CLAUSE CONTAINING A SPECIFIC SKILL
# ============================================================

def _get_skill_clause(
    text: str,
    skill: str,
) -> str:
    """
    Return the sentence/clause containing the specific skill.

    We split on common separators so that proficiency
    belonging to another skill is not incorrectly assigned.
    """

    if not text or not skill:
        return ""

    # Split into smaller clauses.
    clauses = re.split(
        r"[.;,:|\n]+|\s+\band\b\s+|\s+\bbut\b\s+|\s+\bwhile\b\s+",
        text,
        flags=re.IGNORECASE,
    )

    skill_lower = skill.lower()

    for clause in clauses:
        if skill_lower in clause.lower():
            return clause.lower().strip()

    return ""


# ============================================================
# DETECT PROFICIENCY
# ============================================================

def _get_proficiency_level(
    text: str,
    skill: str,
) -> str:
    """
    Detect proficiency wording associated with one skill.
    """

    clause = _get_skill_clause(
        text,
        skill,
    )

    if not clause:
        return "unspecified"

    # --------------------------------------------------------
    # HIGH proficiency
    # --------------------------------------------------------

    for term in HIGH_PROFICIENCY_TERMS:
        if re.search(
            rf"\b{re.escape(term)}\b",
            clause,
            re.IGNORECASE,
        ):
            return "high"

    # --------------------------------------------------------
    # LOW proficiency
    # --------------------------------------------------------

    for term in LOW_PROFICIENCY_TERMS:
        if re.search(
            rf"\b{re.escape(term)}\b",
            clause,
            re.IGNORECASE,
        ):
            return "low"

    return "unspecified"


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def analyze_skill_gap(
    resume_skills: List[str],
    required_skills: List[str],
    resume_text: str = "",
    job_description: str = "",
) -> Dict:
    """
    Compare resume skills with job-required skills.

    Categories:
    - matched
    - partial
    - missing

    This does not decide whether the user should apply.
    """

    resume_map = {
        skill.strip().lower(): skill
        for skill in resume_skills
        if skill and skill.strip()
    }

    required_map = {
        skill.strip().lower(): skill
        for skill in required_skills
        if skill and skill.strip()
    }

    matched_skills = []
    partial_skills = []
    missing_skills = []

    for normalized_skill, original_skill in required_map.items():

        # ----------------------------------------------------
        # Skill missing from resume
        # ----------------------------------------------------

        if normalized_skill not in resume_map:
            missing_skills.append(original_skill)
            continue

        # ----------------------------------------------------
        # Detect proficiency for this exact skill
        # ----------------------------------------------------

        resume_level = _get_proficiency_level(
            resume_text,
            original_skill,
        )

        job_level = _get_proficiency_level(
            job_description,
            original_skill,
        )

        # ----------------------------------------------------
        # LOW resume proficiency + HIGH job requirement
        # = PARTIAL
        # ----------------------------------------------------

        if (
            resume_level == "low"
            and job_level == "high"
        ):
            partial_skills.append(original_skill)

        else:
            matched_skills.append(original_skill)

    # --------------------------------------------------------
    # Match score
    # --------------------------------------------------------

    total_required = len(required_map)

    if total_required == 0:
        match_score = 0.0
    else:
        match_score = round(
            (
                len(matched_skills)
                / total_required
            ) * 100,
            2,
        )

    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "partial_skills": sorted(partial_skills),
        "match_score": match_score,
        "total_required_skills": total_required,
        "total_matched_skills": len(matched_skills),
        "total_missing_skills": len(missing_skills),
        "total_partial_skills": len(partial_skills),
    }