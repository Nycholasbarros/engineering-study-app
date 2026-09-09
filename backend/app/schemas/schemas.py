"""Pydantic schemas for API requests and responses"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    """Exercise difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# Subject Schemas
class SubjectBase(BaseModel):
    """Base subject schema"""
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1, max_length=50)


class SubjectCreate(SubjectBase):
    """Schema for creating a subject"""
    pass


class SubjectUpdate(BaseModel):
    """Schema for updating a subject"""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    code: Optional[str] = Field(None, max_length=50)


class SubjectResponse(SubjectBase):
    """Schema for subject response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Topic Schemas
class TopicBase(BaseModel):
    """Base topic schema"""
    subject_id: int
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    order: int


class TopicCreate(TopicBase):
    """Schema for creating a topic"""
    pass


class TopicUpdate(BaseModel):
    """Schema for updating a topic"""
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    order: Optional[int] = None


class TopicResponse(TopicBase):
    """Schema for topic response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Formula Schemas
class FormulaBase(BaseModel):
    """Base formula schema"""
    subject_id: int
    topic_id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=255)
    formula: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    components: str = Field(..., min_length=1)  # JSON string
    usage_example: str = Field(..., min_length=1)
    unit: Optional[str] = Field(None, max_length=100)


class FormulaCreate(FormulaBase):
    """Schema for creating a formula"""
    pass


class FormulaUpdate(BaseModel):
    """Schema for updating a formula"""
    name: Optional[str] = Field(None, max_length=255)
    formula: Optional[str] = None
    description: Optional[str] = None
    components: Optional[str] = None
    usage_example: Optional[str] = None
    unit: Optional[str] = Field(None, max_length=100)


class FormulaResponse(FormulaBase):
    """Schema for formula response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Exercise Schemas
class ExerciseBase(BaseModel):
    """Base exercise schema"""
    subject_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    statement: str = Field(..., min_length=1)
    expected_answer_type: str = Field(..., max_length=100)
    tags: str = Field(..., min_length=1)  # Comma-separated


class ExerciseCreate(ExerciseBase):
    """Schema for creating an exercise"""
    pass


class ExerciseUpdate(BaseModel):
    """Schema for updating an exercise"""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    statement: Optional[str] = None
    expected_answer_type: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = None


class ExerciseResponse(ExerciseBase):
    """Schema for exercise response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Solution Schemas
class SolutionBase(BaseModel):
    """Base solution schema"""
    exercise_id: int
    step_by_step: str = Field(..., min_length=1)  # JSON string with steps
    final_answer: str = Field(..., min_length=1)
    explanation: str = Field(..., min_length=1)
    alternative_methods: Optional[str] = None  # JSON string


class SolutionCreate(SolutionBase):
    """Schema for creating a solution"""
    pass


class SolutionUpdate(BaseModel):
    """Schema for updating a solution"""
    step_by_step: Optional[str] = None
    final_answer: Optional[str] = None
    explanation: Optional[str] = None
    alternative_methods: Optional[str] = None


class SolutionResponse(SolutionBase):
    """Schema for solution response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Combined Schemas
class ExerciseWithSolutionResponse(ExerciseResponse):
    """Exercise with its solution"""
    solution: Optional[SolutionResponse] = None


class SubjectDetailedResponse(SubjectResponse):
    """Subject with related topics and formulas"""
    topics: List[TopicResponse] = []
    formulas: List[FormulaResponse] = []
