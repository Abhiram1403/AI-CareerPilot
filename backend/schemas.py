from typing import Optional, List, Dict

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class TargetJobCreate(BaseModel):
    job_title: str
    job_url: Optional[str] = None
    job_description: Optional[str] = None


class JobAnalysisRequest(BaseModel):
    resume_id: int
    target_job_id: int


class QuizGenerateRequest(BaseModel):
    target_job_id: Optional[int] = None
    skills: List[str]
    difficulty: str = "medium"
    number_of_questions: int = 5
    level: int = 1


class QuizSubmitRequest(BaseModel):
    quiz_id: int
    answers: Dict[int, str]