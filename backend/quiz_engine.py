from typing import List, Dict

def generate_fallback_question(skill: str, level: int) -> Dict:
    level_questions = {
        1: {
            "question": f"Which option best demonstrates basic knowledge of {skill}?",
            "options": [
                f"Understanding the fundamental concepts of {skill}",
                f"Designing a complex system using {skill}",
                f"Optimizing a large production system using {skill}",
                f"Troubleshooting advanced problems in {skill}",
            ],
            "correct_answer": f"Understanding the fundamental concepts of {skill}",
        },
        2: {
            "question": f"Which option best demonstrates medium-level practical knowledge of {skill}?",
            "options": [
                f"Knowing the definition of {skill}",
                f"Applying {skill} to a practical task",
                f"Designing a highly complex architecture using {skill}",
                f"Optimizing enterprise-scale systems using {skill}",
            ],
            "correct_answer": f"Applying {skill} to a practical task",
        },
        3: {
            "question": f"Which option best demonstrates hard-level problem-solving ability in {skill}?",
            "options": [
                f"Memorizing basic concepts of {skill}",
                f"Following a simple tutorial for {skill}",
                f"Troubleshooting and solving realistic problems using {skill}",
                f"Reading the documentation for {skill}",
            ],
            "correct_answer": f"Troubleshooting and solving realistic problems using {skill}",
        },
        4: {
            "question": f"Which option best demonstrates advanced expertise in {skill}?",
            "options": [
                f"Understanding basic concepts of {skill}",
                f"Completing simple tasks using {skill}",
                f"Solving standard practical problems using {skill}",
                f"Designing, optimizing, and solving complex real-world problems using {skill}",
            ],
            "correct_answer": f"Designing, optimizing, and solving complex real-world problems using {skill}",
        },
    }

    return level_questions[level]
SKILL_QUESTION_TEMPLATES = {
    "default": {
        1: "Test the candidate's fundamental understanding of {skill}.",
        2: "Test the candidate's practical working knowledge of {skill}.",
        3: "Test the candidate's ability to solve realistic problems using {skill}.",
        4: "Test the candidate's advanced ability to apply {skill} in complex real-world situations.",
    }
}
SKILL_QUESTION_BANK = {
    "python": {
        1: [
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": ["def", "func", "function", "define"],
                "correct_answer": "def",
            }
        ],
        2: [
            {
                "question": "Which Python data structure stores key-value pairs?",
                "options": ["List", "Tuple", "Dictionary", "Set"],
                "correct_answer": "Dictionary",
            }
        ],
        3: [
            {
                "question": "Which Python feature allows a function to remember variables from its enclosing scope?",
                "options": ["Inheritance", "Closure", "Casting", "Iteration"],
                "correct_answer": "Closure",
            }
        ],
        4: [
            {
                "question": "Which approach is generally appropriate when processing a very large file that cannot fit comfortably into memory?",
                "options": [
                    "Load the entire file into a list",
                    "Process the file incrementally",
                    "Convert the entire file to a tuple first",
                    "Duplicate the file in memory"
                ],
                "correct_answer": "Process the file incrementally",
            }
        ],
    },

    "sql": {
        1: [
            {
                "question": "Which SQL clause is used to filter rows?",
                "options": ["WHERE", "ORDER BY", "GROUP BY", "JOIN"],
                "correct_answer": "WHERE",
            }
        ],
        2: [
            {
                "question": "Which SQL operation combines rows from two tables using a related column?",
                "options": ["JOIN", "SORT", "GROUP", "INDEX"],
                "correct_answer": "JOIN",
            }
        ],
        3: [
            {
                "question": "Which clause is used to filter groups after aggregation?",
                "options": ["WHERE", "HAVING", "ORDER BY", "FROM"],
                "correct_answer": "HAVING",
            }
        ],
        4: [
            {
                "question": "Which technique can improve the performance of frequently filtered database columns?",
                "options": [
                    "Adding appropriate indexes",
                    "Removing all constraints",
                    "Duplicating every row",
                    "Avoiding all query optimization"
                ],
                "correct_answer": "Adding appropriate indexes",
            }
        ],
    },

    "java": {
        1: [
            {
                "question": "Which keyword is used to create an object in Java?",
                "options": ["new", "class", "object", "create"],
                "correct_answer": "new",
            }
        ],
        2: [
            {
                "question": "Which concept allows a Java class to inherit properties and methods from another class?",
                "options": ["Inheritance", "Encapsulation", "Compilation", "Casting"],
                "correct_answer": "Inheritance",
            }
        ],
        3: [
            {
                "question": "Which Java mechanism allows multiple methods to have the same name with different parameter lists?",
                "options": ["Method overloading", "Method overriding", "Inheritance", "Abstraction"],
                "correct_answer": "Method overloading",
            }
        ],
        4: [
            {
                "question": "Which Java feature is commonly used to execute tasks asynchronously using a pool of worker threads?",
                "options": [
                    "ExecutorService",
                    "Scanner",
                    "StringBuilder",
                    "System.out"
                ],
                "correct_answer": "ExecutorService",
            }
        ],
    },
}
def get_question_template(skill: str, level: int) -> str:
    skill_key = skill.strip().lower()

    skill_templates = SKILL_QUESTION_TEMPLATES.get(
        skill_key,
        SKILL_QUESTION_TEMPLATES["default"],
    )

    return skill_templates[level]
SKILL_LEVELS = {
    1: {
        "name": "Basic",
        "difficulty": "basic",
        "pass_score": 80,
    },
    2: {
        "name": "Medium",
        "difficulty": "medium",
        "pass_score": 80,
    },
    3: {
        "name": "Hard",
        "difficulty": "hard",
        "pass_score": 80,
    },
    4: {
        "name": "Advanced",
        "difficulty": "advanced",
        "pass_score": 80,
    },
}
def get_skill_questions(skill: str, level: int) -> List[Dict]:
    skill_key = skill.strip().lower()

    return SKILL_QUESTION_BANK.get(
        skill_key,
        {}
    ).get(level, [])


def generate_ai_question(skill: str, level: int) -> Dict:
    """
    Placeholder interface for AI-generated skill questions.

    Later this function will call an AI model and generate
    skill-specific questions based on the requested level.
    """
    level_name = SKILL_LEVELS[level]["name"]

    return {
        "question": (
            f"AI-generated {level_name.lower()}-level question "
            f"for {skill} will be added here."
        ),
        "options": [
            f"Option related to {skill}",
            f"Another option related to {skill}",
            f"Alternative {skill} concept",
            f"Different {skill} approach",
        ],
        "correct_answer": f"Option related to {skill}",
    }


def generate_quiz(
    skills: List[str],
    difficulty: str = "medium",
    number_of_questions: int = 5,
    level: int = 2,
) -> List[Dict]:
    """
    Generate a basic skill-focused quiz.

    This is the initial quiz engine.
    AI-generated questions will be added later.
    """

    if level not in SKILL_LEVELS:
        raise ValueError("Skill level must be between 1 and 4")

    difficulty = SKILL_LEVELS[level]["difficulty"]

    questions = []

    question_number = 1

    for skill in skills:
        skill_questions = get_skill_questions(skill, level)

        if not skill_questions:
         skill_questions = [
        generate_ai_question(skill, level)
    ]

        for question_data in skill_questions:
            if question_number > number_of_questions:
                break

            questions.append(
                {
                    "question_number": question_number,
                    "skill": skill,
                    "level": level,
                    "level_name": SKILL_LEVELS[level]["name"],
                    "difficulty": difficulty,
                    "question": question_data["question"],
                    "options": question_data["options"],
                    "correct_answer": question_data["correct_answer"],
                }
            )

            question_number += 1

        if question_number > number_of_questions:
            break

    return questions
    questions = []

    question_number = 1

    for skill in skills:
        skill_questions = get_skill_questions(skill, level)

        if not skill_questions:
            skill_questions = [
                generate_fallback_question(skill, level)
            ]

        for question_data in skill_questions:
            if question_number > number_of_questions:
                break

            questions.append(
                {
                    "question_number": question_number,
                    "skill": skill,
                    "level": level,
                    "level_name": SKILL_LEVELS[level]["name"],
                    "difficulty": difficulty,
                    "question": question_data["question"],
                    "options": question_data["options"],
                    "correct_answer": question_data["correct_answer"],
                }
            )

            question_number += 1

        if question_number > number_of_questions:
            break

    return questions
def get_next_skill_level(current_level: int, score: float) -> int:
    """
    Decide whether the user can progress to the next skill level.

    A score of 80% or higher unlocks the next level.
    """
    if current_level >= 4:
      return 4

    if score >= SKILL_LEVELS[current_level]["pass_score"]:
        return current_level + 1

    return current_level