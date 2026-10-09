from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, Resume, TargetJob, JobAnalysis, Quiz, QuizAttempt
from backend.schemas import (
    UserCreate,
    TargetJobCreate,
    JobAnalysisRequest,
    QuizGenerateRequest,
    QuizSubmitRequest,
)
from backend.security import hash_password, verify_password
from backend.auth import create_access_token
from backend.dependencies import get_current_user
from backend.resume_service import save_resume, extract_resume_text
from backend.skill_extractor import extract_skills
from backend.job_matcher import compare_skills
from backend.job_requirements import extract_job_requirements
from backend.skill_gap_engine import analyze_skill_gap
from backend.skill_priority import calculate_skill_priority
from backend.learning_roadmap import generate_learning_roadmap
from backend.quiz_engine import generate_quiz, get_next_skill_level

app = FastAPI(
    title="AI-CareerPilot API",
    description="AI-powered personalized career guidance and job matching platform.",
    version="0.4.0",
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI-CareerPilot API is running!",
        "status": "success",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-CareerPilot API",
    }


# ============================================================
# USERS
# ============================================================

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "created_at": user.created_at,
        }
        for user in users
    ]


@app.post("/users")
def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "full_name": new_user.full_name,
        "email": new_user.email,
        "created_at": new_user.created_at,
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ============================================================
# CURRENT USER PROFILE
# ============================================================

@app.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
    }


# ============================================================
# TARGET JOB
# ============================================================

@app.post("/jobs")
def create_target_job(
    job: TargetJobCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # A job must have either a URL or a job description.
    if not job.job_url and not job.job_description:
        raise HTTPException(
            status_code=400,
            detail="Provide either a job URL or a job description",
        )

    target_job = TargetJob(
        user_id=current_user.id,
        job_title=job.job_title,
        job_url=job.job_url,
        job_description=job.job_description,
    )

    db.add(target_job)
    db.commit()
    db.refresh(target_job)

    return {
        "message": "Target job created successfully",
        "job_id": target_job.id,
        "job_title": target_job.job_title,
        "job_url": target_job.job_url,
    }


# ============================================================
# RESUME UPLOAD
# ============================================================

@app.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    try:
        file_path = await save_resume(file)
        resume_text = extract_resume_text(file_path)

        return {
            "message": "Resume uploaded successfully",
            "filename": file.filename,
            "text_length": len(resume_text),
            "text_preview": resume_text[:500],
            "user_id": current_user.id,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


# ============================================================
# RESUME ANALYSIS
# ============================================================

@app.post("/resume/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        file_path = await save_resume(file)
        resume_text = extract_resume_text(file_path)
        skills = extract_skills(resume_text)

        resume = Resume(
            user_id=current_user.id,
            original_filename=file.filename,
            stored_filename=file_path.name,
            file_path=str(file_path),
            extracted_text=resume_text,
            extracted_skills=skills,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return {
            "message": "Resume analyzed successfully",
            "resume_id": resume.id,
            "filename": file.filename,
            "user_id": current_user.id,
            "skills": skills,
            "skill_count": len(skills),
            "text_length": len(resume_text),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

# ============================================================
# JOB ANALYSIS
# ============================================================

@app.post("/jobs/analyze")
def analyze_job(
    request: JobAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # --------------------------------------------------------
    # Find the selected resume
    # --------------------------------------------------------

    resume = (
        db.query(Resume)
        .filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id,
        )
        .first()
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    # --------------------------------------------------------
    # Find the selected target job
    # --------------------------------------------------------

    target_job = (
        db.query(TargetJob)
        .filter(
            TargetJob.id == request.target_job_id,
            TargetJob.user_id == current_user.id,
        )
        .first()
    )

    if not target_job:
        raise HTTPException(
            status_code=404,
            detail="Target job not found",
        )

    # --------------------------------------------------------
    # Get resume skills
    # --------------------------------------------------------

    resume_skills = resume.extracted_skills or []

    # --------------------------------------------------------
    # Job description is currently required
    # --------------------------------------------------------

    if not target_job.job_description:
        raise HTTPException(
            status_code=400,
            detail=(
                "Job description is required for analysis. "
                "A URL alone cannot be analyzed yet."
            ),
        )

    # --------------------------------------------------------
    # Extract required skills
    # --------------------------------------------------------

    job_skills = extract_skills(
        target_job.job_description
    )

    # --------------------------------------------------------
    # Extract job requirements
    # --------------------------------------------------------

    job_requirements = extract_job_requirements(
    target_job.job_description
)
    # --------------------------------------------------------
    # Analyze skill gap
    # --------------------------------------------------------

    comparison = analyze_skill_gap(
        resume_skills=resume_skills,
        required_skills=job_skills,
        resume_text=resume.extracted_text or "",
        job_description=target_job.job_description,
    )

    skill_priorities = calculate_skill_priority(
    required_skills=job_skills,
    matched_skills=comparison["matched_skills"],
    partial_skills=comparison["partial_skills"],
    missing_skills=comparison["missing_skills"],
)
    learning_roadmap = generate_learning_roadmap(
    skill_priorities=skill_priorities,
)

    # --------------------------------------------------------
    # Save analysis
    # --------------------------------------------------------

    analysis = JobAnalysis(
        user_id=current_user.id,
        resume_id=resume.id,
        target_job_id=target_job.id,
        matched_skills=comparison["matched_skills"],
        missing_skills=comparison["missing_skills"],
        partial_skills=comparison["partial_skills"],
        match_score=comparison["match_score"],
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    # --------------------------------------------------------
    # Return analysis
    # --------------------------------------------------------

    return {
    "message": "Job analysis completed successfully",
    "analysis_id": analysis.id,
    "job_title": target_job.job_title,
    "required_skills": job_skills,
    "matched_skills": comparison["matched_skills"],
    "missing_skills": comparison["missing_skills"],
    "partial_skills": comparison["partial_skills"],
    "match_score": comparison["match_score"],
    "total_required_skills": comparison[
        "total_required_skills"
    ],
    "total_matched_skills": comparison[
        "total_matched_skills"
    ],
    "total_missing_skills": comparison[
        "total_missing_skills"
    ],
    "total_partial_skills": comparison[
        "total_partial_skills"
    ],
   "skill_priorities": skill_priorities,
"learning_roadmap": learning_roadmap,
"job_requirements": job_requirements,
}

# ============================================================
# QUIZ GENERATION
# ============================================================

@app.post("/quizzes/generate")
def create_quiz(
    request: QuizGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    questions = generate_quiz(
    skills=request.skills,
    difficulty=request.difficulty,
    number_of_questions=request.number_of_questions,
    level=request.level,
)

    quiz = Quiz(
    user_id=current_user.id,
    target_job_id=request.target_job_id,
    skill=", ".join(request.skills),
    title="Career Skill Assessment",
    difficulty=questions[0]["difficulty"] if questions else request.difficulty,
    questions=questions,
)

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return {
        "quiz_id": quiz.id,
        "title": quiz.title,
        "difficulty": quiz.difficulty,
        "skills": request.skills,
        "questions": questions,
    }

# ============================================================
# QUIZ SUBMISSION
# ============================================================

@app.post("/quizzes/submit")
def submit_quiz(
    request: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.id == request.quiz_id,
            Quiz.user_id == current_user.id,
        )
        .first()
    )

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found",
        )

    questions = quiz.questions or []

    correct_answers = 0
    weak_skills = []

    for question in questions:
        question_number = question["question_number"]
        correct_answer = question["correct_answer"]
        user_answer = request.answers.get(question_number)

        if user_answer == correct_answer:
            correct_answers += 1
        else:
            skill = question["skill"]
            if skill not in weak_skills:
                weak_skills.append(skill)

    total_questions = len(questions)

    score = (
        round((correct_answers / total_questions) * 100, 2)
        if total_questions > 0
        else 0
    )

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
        weak_skills=weak_skills,
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "quiz_id": quiz.id,
        "score": score,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "weak_skills": weak_skills,
    }