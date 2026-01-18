from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QuestionSchema(BaseModel):
    question: str = Field(..., min_length=1, description="The question text")
    options: List[str] = Field(..., min_items=2, max_items=6, description="Answer options")
    correct_answer: int = Field(..., ge=0, description="Index of the correct answer")

    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the capital of France?",
                "options": ["London", "Paris", "Berlin", "Madrid"],
                "correct_answer": 1
            }
        }

class QuizCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Quiz title")
    description: Optional[str] = Field(None, max_length=1000, description="Quiz description")
    questions: List[QuestionSchema] = Field(..., min_items=1, description="List of questions")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "General Knowledge Quiz",
                "description": "Test your general knowledge",
                "questions": [
                    {
                        "question": "What is the capital of France?",
                        "options": ["London", "Paris", "Berlin", "Madrid"],
                        "correct_answer": 1
                    }
                ]
            }
        }

class QuizResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    questions: List[dict]
    created_at: datetime

    class Config:
        from_attributes = True
