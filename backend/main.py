from fastapi import FastAPI

app = FastAPI(
    title="AI-CareerPilot API",
    description="AI-powered personalized career guidance and job matching platform.",
    version="0.1.0",
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