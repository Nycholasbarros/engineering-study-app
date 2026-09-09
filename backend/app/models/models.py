"""Database models for engineering subjects, formulas, and exercises"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum


class DifficultyLevel(str, enum.Enum):
    """Exercise difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Subject(Base):
    """Engineering subject/discipline"""
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    code = Column(String(50), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    topics = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    formulas = relationship("Formula", back_populates="subject", cascade="all, delete-orphan")
    exercises = relationship("Exercise", back_populates="subject", cascade="all, delete-orphan")


class Topic(Base):
    """Topics within a subject"""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subject = relationship("Subject", back_populates="topics")
    formulas = relationship("Formula", back_populates="topic", cascade="all, delete-orphan")


class Formula(Base):
    """Mathematical formulas with explanations"""
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    formula = Column(Text, nullable=False)  # LaTeX or text representation
    description = Column(Text, nullable=False)
    components = Column(Text, nullable=False)  # JSON with formula components explanation
    usage_example = Column(Text, nullable=False)
    unit = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subject = relationship("Subject", back_populates="formulas")
    topic = relationship("Topic", back_populates="formulas")


class Exercise(Base):
    """Practice exercises"""
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    difficulty = Column(SQLEnum(DifficultyLevel), default=DifficultyLevel.MEDIUM, nullable=False)
    statement = Column(Text, nullable=False)  # Exercise statement/problem
    expected_answer_type = Column(String(100), nullable=False)  # numeric, text, multiple_choice, etc
    tags = Column(Text, nullable=False)  # Comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subject = relationship("Subject", back_populates="exercises")
    solution = relationship("Solution", back_populates="exercise", uselist=False, cascade="all, delete-orphan")


class Solution(Base):
    """Step-by-step solutions for exercises"""
    __tablename__ = "solutions"

    id = Column(Integer, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True, unique=True)
    step_by_step = Column(Text, nullable=False)  # JSON array with solution steps
    final_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    alternative_methods = Column(Text, nullable=True)  # JSON with alternative solutions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    exercise = relationship("Exercise", back_populates="solution")
