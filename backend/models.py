from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base
import json

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    questions = Column(Text, nullable=False)  # JSON stored as text
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def get_questions(self):
        """Parse questions from JSON string"""
        return json.loads(self.questions) if self.questions else []

    def set_questions(self, questions_list):
        """Store questions as JSON string"""
        self.questions = json.dumps(questions_list)
