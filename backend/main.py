from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User
from backend.schemas import UserCreate
from backend.security import hash_password

app = FastAPI(
    title="AI-CareerPilot API",
    description="AI-powered personalized career guidance and job matching platform.",
    version="0.3.0",
)


@app.get("/")
def root():
    return {
        "message": "AI-CareerPilot API is running!",
        "status": "success",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-CareerPilot API",
    }


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
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()

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
from fastapi.security import OAuth2PasswordRequestForm
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
from backend.auth import create_access_token
from backend.security import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth import create_access_token
from backend.security import hash_password, verify_password
from backend.dependencies import get_current_user
@app.get("/me")
def get_my_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "full_name": current_user.full_name,
        "email": current_user.email,
    }
from fastapi import File, UploadFile

from backend.resume_service import save_resume, extract_resume_text
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
    