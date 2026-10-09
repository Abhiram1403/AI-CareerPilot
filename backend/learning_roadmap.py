from typing import List, Dict


def generate_learning_roadmap(
    skill_priorities: List[Dict],
) -> List[Dict]:
    """
    Convert skill priorities into a personalized learning roadmap.
    """

    roadmap = []

    for item in skill_priorities:
        skill = item["skill"]
        priority = item["priority"]

        if priority == "High":
            roadmap.append(
                {
                    "skill": skill,
                    "priority": "High",
                    "focus": f"Build strong practical skills in {skill}.",
                    "practice": f"Complete practical {skill} exercises related to the target job.",
                    "recommended_action": "Learn fundamentals → practice → complete a job-oriented task.",
                }
            )

        elif priority == "Medium":
            roadmap.append(
                {
                    "skill": skill,
                    "priority": "Medium",
                    "focus": f"Improve your practical ability in {skill}.",
                    "practice": f"Complete intermediate {skill} exercises.",
                    "recommended_action": "Review concepts → practice → build a small task.",
                }
            )

        else:
            roadmap.append(
                {
                    "skill": skill,
                    "priority": "Low",
                    "focus": f"Maintain and strengthen your existing {skill} knowledge.",
                    "practice": f"Practice advanced or job-oriented {skill} problems.",
                    "recommended_action": "Continue practicing through realistic job tasks.",
                }
            )

    return roadmap