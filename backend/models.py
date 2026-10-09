from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)

    extracted_text = Column(Text, nullable=True)
    extracted_skills = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TargetJob(Base):
    __tablename__ = "target_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)

    job_title = Column(String(255), nullable=False)
    job_url = Column(String(1000), nullable=True)
    job_description = Column(Text, nullable=True)

    required_skills = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    target_job_id = Column(Integer, ForeignKey("target_jobs.id"), nullable=False)

    matched_skills = Column(JSON, nullable=True)
    missing_skills = Column(JSON, nullable=True)
    partial_skills = Column(JSON, nullable=True)

    match_score = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_job_id = Column(Integer, ForeignKey("target_jobs.id"), nullable=True)
    skill = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    difficulty = Column(String(50), nullable=False, default="medium")
    questions = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    weak_skills = Column(JSON, nullable=True)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())