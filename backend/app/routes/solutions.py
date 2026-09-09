"""Routes for solution management"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import SolutionCreate, SolutionUpdate, SolutionResponse
from app.services.solution_service import SolutionService
from app.services.exercise_service import ExerciseService

router = APIRouter(
    prefix="/solutions",
    tags=["solutions"],
    responses={404: {"description": "Not found"}},
)


@router.get("/exercise/{exercise_id}", response_model=SolutionResponse)
async def get_solution_by_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """Get solution for a specific exercise"""
    # Verify exercise exists
    exercise = ExerciseService.get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {exercise_id} not found"
        )
    
    solution = SolutionService.get_solution_by_exercise_id(db, exercise_id)
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solution for exercise {exercise_id} not found"
        )
    return solution


@router.get("/{solution_id}", response_model=SolutionResponse)
async def get_solution(solution_id: int, db: Session = Depends(get_db)):
    """Get a specific solution"""
    solution = SolutionService.get_solution_by_id(db, solution_id)
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solution with id {solution_id} not found"
        )
    return solution


@router.post("/", response_model=SolutionResponse, status_code=status.HTTP_201_CREATED)
async def create_solution(solution: SolutionCreate, db: Session = Depends(get_db)):
    """Create a new solution for an exercise"""
    # Verify exercise exists
    exercise = ExerciseService.get_exercise_by_id(db, solution.exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id {solution.exercise_id} not found"
        )
    
    # Check if solution already exists for this exercise
    existing_solution = SolutionService.get_solution_by_exercise_id(db, solution.exercise_id)
    if existing_solution:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Solution already exists for exercise {solution.exercise_id}"
        )
    
    new_solution = SolutionService.create_solution(db, solution)
    return new_solution


@router.put("/{solution_id}", response_model=SolutionResponse)
async def update_solution(
    solution_id: int,
    solution_update: SolutionUpdate,
    db: Session = Depends(get_db)
):
    """Update a solution"""
    solution = SolutionService.get_solution_by_id(db, solution_id)
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solution with id {solution_id} not found"
        )
    
    updated_solution = SolutionService.update_solution(db, solution_id, solution_update)
    return updated_solution


@router.delete("/{solution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_solution(solution_id: int, db: Session = Depends(get_db)):
    """Delete a solution"""
    solution = SolutionService.get_solution_by_id(db, solution_id)
    if not solution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solution with id {solution_id} not found"
        )
    
    SolutionService.delete_solution(db, solution_id)
    return None
