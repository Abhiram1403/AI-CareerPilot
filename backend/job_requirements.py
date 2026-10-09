import re


def _clean(value: str) -> str:
    """Clean extracted text."""
    value = re.sub(r"\s+", " ", value)
    value = value.strip(" .,:;|-")
    return value


def _add_unique(requirements: dict, category: str, value: str):
    """Add a cleaned value without duplicates."""
    value = _clean(value)

    if value and value not in requirements[category]:
        requirements[category].append(value)


def extract_job_requirements(job_description: str) -> dict:
    """
    Extract common job requirements from a job description.

    This is an informational analyzer.
    It does not decide whether a user should apply.
    """

    text = job_description.strip()

    requirements = {
        "experience": [],
        "education": [],
        "certifications": [],
        "availability": [],
        "seniority": [],
        "responsibilities": [],
    }

    if not text:
        return requirements

    lowered_text = text.lower()

    # ========================================================
    # EXPERIENCE
    # ========================================================

    experience_ranges = re.findall(
        r"\b\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?\s*(?:\+|plus)?\s*(?:years?|yrs?)\b",
        text,
        re.IGNORECASE,
    )

    for match in experience_ranges:
        _add_unique(
            requirements,
            "experience",
            match,
        )

    text_without_ranges = re.sub(
        r"\b\d+(?:\.\d+)?\s*[-–]\s*\d+(?:\.\d+)?\s*(?:\+|plus)?\s*(?:years?|yrs?)\b",
        "",
        text,
        flags=re.IGNORECASE,
    )

    experience_patterns = [
        r"\bat\s+least\s+\d+(?:\.\d+)?\s*(?:\+|plus)?\s*(?:years?|yrs?)",
        r"\bminimum\s+(?:of\s+)?\d+(?:\.\d+)?\s*(?:\+|plus)?\s*(?:years?|yrs?)",
        r"\b\d+(?:\.\d+)?\s*(?:\+|plus)\s*(?:years?|yrs?)",
        r"\b\d+(?:\.\d+)?\s*(?:years?|yrs?)\s+(?:of\s+)?experience\b",
    ]

    for pattern in experience_patterns:
        matches = re.findall(
            pattern,
            text_without_ranges,
            re.IGNORECASE,
        )

        for match in matches:
            _add_unique(
                requirements,
                "experience",
                match,
            )

    # ========================================================
    # SENIORITY
    # ========================================================

    seniority_patterns = [
        r"\bfreshers?\b",
        r"\brecent\s+graduates?\b",
        r"\bnew\s+graduates?\b",
        r"\bentry[\s-]?level\b",
        r"\bjunior\b",
        r"\bassociate\b",
        r"\bmid[\s-]?level\b",
        r"\bsenior\b",
        r"\blead\b",
        r"\bprincipal\b",
        r"\bmanager\b",
        r"\bintern(?:ship)?\b",
    ]

    seniority_normalization = {
        "fresher": "Fresher",
        "freshers": "Fresher",
        "recent graduate": "Recent Graduate",
        "recent graduates": "Recent Graduate",
        "new graduate": "New Graduate",
        "new graduates": "New Graduate",
        "entry level": "Entry Level",
        "entry-level": "Entry Level",
        "junior": "Junior",
        "associate": "Associate",
        "mid-level": "Mid-Level",
        "mid level": "Mid-Level",
        "senior": "Senior",
        "lead": "Lead",
        "principal": "Principal",
        "manager": "Manager",
        "intern": "Intern",
        "internship": "Internship",
    }

    for pattern in seniority_patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:
            normalized = seniority_normalization.get(
                match.lower(),
                match.title(),
            )

            _add_unique(
                requirements,
                "seniority",
                normalized,
            )

    # ========================================================
    # EDUCATION
    # ========================================================

    education_patterns = [
        r"\bB\s*\.?\s*Tech\b",
        r"\bB\s*\.?\s*E\s*\.?\b",
        r"\bM\s*\.?\s*Tech\b",
        r"\bM\s*\.?\s*E\s*\.?\b",
        r"\bBCA\b",
        r"\bMCA\b",
        r"\bBBA\b",
        r"\bMBA\b",
        r"\bBSc\b",
        r"\bB\s*\.?\s*Sc\b",
        r"\bMSc\b",
        r"\bM\s*\.?\s*Sc\b",
        r"\bbachelor'?s?\s+degree\b",
        r"\bmaster'?s?\s+degree\b",
        r"\bbachelor'?s?\s+in\s+[A-Za-z][A-Za-z &/-]{1,80}",
        r"\bmaster'?s?\s+in\s+[A-Za-z][A-Za-z &/-]{1,80}",
        r"\bdegree\s+in\s+[A-Za-z][A-Za-z &/-]{1,80}",
    ]

    for pattern in education_patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:
            cleaned = _clean(match)

            cleaned = re.sub(
                r"\s+(required|preferred|mandatory|desired)$",
                "",
                cleaned,
                flags=re.IGNORECASE,
            )

            if len(cleaned) >= 3:
                _add_unique(
                    requirements,
                    "education",
                    cleaned,
                )

    # ========================================================
    # CERTIFICATIONS
    # ========================================================

    certification_patterns = [
        r"\bAWS\s+Certified\b",
        r"\bAWS\s+Certification\b",
        r"\bMicrosoft\s+Certified\b",
        r"\bMicrosoft\s+Certification\b",
        r"\bAzure\s+Certification\b",
        r"\bGoogle\s+Cloud\s+Certification\b",
        r"\bGoogle\s+Certified\b",
        r"\bCompTIA(?:\s+[A-Za-z0-9+.-]+)?\b",
        r"\bPMP\b",
        r"\bCISSP\b",
        r"\bScrum\s+Master\s+Certification\b",
        r"\bcertification\s+required\b",
        r"\bcertification\s+preferred\b",
        r"\bcertifications\s+required\b",
        r"\bcertifications\s+preferred\b",
    ]

    for pattern in certification_patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:
            _add_unique(
                requirements,
                "certifications",
                match,
            )

    # ========================================================
    # AVAILABILITY
    # ========================================================

    availability_patterns = [
        r"\bimmediate\s+join(?:er|ing)?\b",
        r"\bjoin\s+immediately\b",
        r"\bavailable\s+immediately\b",
        r"\bimmediate\s+availability\b",
        r"\bnotice\s+period\b",
        r"\bjoin\s+within\s+\d+\s+(?:days?|weeks?)\b",
        r"\bavailable\s+within\s+\d+\s+(?:days?|weeks?)\b",
        r"\bjoin(?:ing)?\s+date\b",
    ]

    for pattern in availability_patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:
            _add_unique(
                requirements,
                "availability",
                match,
            )

    # ========================================================
    # RESPONSIBILITIES
    # ========================================================

    responsibility_markers = [
        "responsibilities",
        "what you'll do",
        "what you will do",
        "key responsibilities",
        "job responsibilities",
        "roles and responsibilities",
        "your responsibilities",
        "duties",
        "job duties",
    ]

    for marker in responsibility_markers:
        if marker in lowered_text:
            _add_unique(
                requirements,
                "responsibilities",
                f"Job description contains a '{marker}' section",
            )

    # ========================================================
    # FINAL CLEANUP
    # ========================================================

    for category in requirements:
        requirements[category] = sorted(
            set(requirements[category]),
            key=str.lower,
        )

    return requirements