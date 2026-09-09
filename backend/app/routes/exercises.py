"""Routes for exercise management"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import (
    ExerciseCreate,
    ExerciseUpdate,
    ExerciseResponse,
    ExerciseWithSolutionResponse,
    DifficultyLevel
)
from app.services.exercise_service import ExerciseService
from app.services.subject_service import SubjectService

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ExerciseResponse])
async def get_exercises(
    subject_id: int = Query(None, description="Filter by subject ID"),
    difficulty: DifficultyLevel = Query(None, description="Filter by difficulty level"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all exercises with optional filtering"""
    exercises = ExerciseService.get_all_exercises(
        db,
        subject_id=subject_id,
        difficulty=difficulty,
        skip=skip,
        limit=limit
    )
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseWithSolutionResponse)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Get a specific exercise with its solution"""
    exercise = ExerciseService.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {exercise_id} not found"
        )
    return exercise


@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db)):
    """Create a new exercise"""
    # Verify subject exists
    subject = SubjectService.get_subject_by_id(db, exercise.subject_id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {exercise.subject_id} not found"
        )
    
    new_exercise = ExerciseService.create_exercise(db, exercise)
    return new_exercise


@router.put("/{exercise_id}", response_model=ExerciseResponse)
async def update_exercise(
    exercise_id: int,
    exercise_update: ExerciseUpdate,
    db: Session = Depends(get_db)
):
    """Update an exercise"""
    exercise = ExerciseService.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {exercise_id} not found"
        )
    
    updated_exercise = ExerciseService.update_exercise(db, exercise_id, exercise_update)
    return updated_exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Delete an exercise"""
    exercise = ExerciseService.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {exercise_id} not found"
        )
    
    ExerciseService.delete_exercise(db, exercise_id)
    return None
