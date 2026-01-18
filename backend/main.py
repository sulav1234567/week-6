from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import quizzes
from .config import settings

# Create database tables in simple deployments. For production, use migrations (Alembic).
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Quiz Authoring Platform API",
    description="RESTful API for creating and managing quizzes",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware configuration using settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quizzes.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Quiz Authoring Platform API",
        "docs": "/api/docs",
        "version": "1.0.0",
        "env": settings.ENV,
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
