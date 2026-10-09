from typing import List, Dict


def calculate_skill_priority(
    required_skills: List[str],
    matched_skills: List[str],
    partial_skills: List[str],
    missing_skills: List[str],
) -> List[Dict]:
    """
    Assign learning priority to job-related skills.

    Priority is based on the user's current skill-gap status:
    - Missing  -> High
    - Partial  -> High
    - Matched  -> Low
    """

    matched_set = {skill.lower(): skill for skill in matched_skills}
    partial_set = {skill.lower(): skill for skill in partial_skills}
    missing_set = {skill.lower(): skill for skill in missing_skills}

    priorities = []

    for skill in required_skills:
        normalized = skill.lower()

        if normalized in missing_set:
            priority = "High"
            reason = "Skill is required by the job but missing from the resume."

        elif normalized in partial_set:
            priority = "High"
            reason = "Skill is present but needs stronger proficiency."

        elif normalized in matched_set:
            priority = "Low"
            reason = "Skill is already present in the resume."

        else:
            priority = "Medium"
            reason = "Skill requires further review."

        priorities.append(
            {
                "skill": skill,
                "priority": priority,
                "reason": reason,
            }
        )

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    priorities.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            item["skill"].lower(),
        )
    )

    return priorities