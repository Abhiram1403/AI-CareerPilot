from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User

app = FastAPI(
    title="AI-CareerPilot API",
    description="AI-powered personalized career guidance and job matching platform.",
    version="0.2.0",
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