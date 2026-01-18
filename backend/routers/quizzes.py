from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from database import get_db
from models import Quiz
from schemas import QuizCreate, QuizResponse

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])

@router.get("", response_model=List[QuizResponse])
def get_all_quizzes(db: Session = Depends(get_db)):
    """Retrieve a list of all quizzes"""
    quizzes = db.query(Quiz).order_by(Quiz.created_at.desc()).all()
    
    # Convert questions JSON string to dict for each quiz
    result = []
    for quiz in quizzes:
        quiz_dict = {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "questions": quiz.get_questions(),
            "created_at": quiz.created_at
        }
        result.append(quiz_dict)
    
    return result

@router.post("", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(quiz_data: QuizCreate, db: Session = Depends(get_db)):
    """Create a new quiz"""
    # Convert questions to JSON string
    questions_json = json.dumps([q.model_dump() for q in quiz_data.questions])
    
    # Create new quiz
    new_quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        questions=questions_json
    )
    
    db.add(new_quiz)
    db.commit()
    db.refresh(new_quiz)
    
    return {
        "id": new_quiz.id,
        "title": new_quiz.title,
        "description": new_quiz.description,
        "questions": new_quiz.get_questions(),
        "created_at": new_quiz.created_at
    }

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    """Retrieve specific quiz details"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id {quiz_id} not found"
        )
    
    return {
        "id": quiz.id,
        "title": quiz.title,
        "description": quiz.description,
        "questions": quiz.get_questions(),
        "created_at": quiz.created_at
    }

@router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Delete a quiz"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Quiz with id {quiz_id} not found"
        )
    
    db.delete(quiz)
    db.commit()
    
    return {"message": "Quiz deleted successfully", "id": quiz_id}
