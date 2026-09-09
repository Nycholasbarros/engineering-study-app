"""Services for solution operations"""

from sqlalchemy.orm import Session
from app.models.models import Solution
from app.schemas.schemas import SolutionCreate, SolutionUpdate


class SolutionService:
    """Service for managing solutions"""

    @staticmethod
    def get_solution_by_exercise_id(db: Session, exercise_id: int):
        """Get a solution by exercise ID"""
        return db.query(Solution).filter(Solution.exercise_id == exercise_id).first()

    @staticmethod
    def get_solution_by_id(db: Session, solution_id: int):
        """Get a solution by ID"""
        return db.query(Solution).filter(Solution.id == solution_id).first()

    @staticmethod
    def create_solution(db: Session, solution: SolutionCreate):
        """Create a new solution"""
        db_solution = Solution(
            exercise_id=solution.exercise_id,
            step_by_step=solution.step_by_step,
            final_answer=solution.final_answer,
            explanation=solution.explanation,
            alternative_methods=solution.alternative_methods
        )
        db.add(db_solution)
        db.commit()
        db.refresh(db_solution)
        return db_solution

    @staticmethod
    def update_solution(db: Session, solution_id: int, solution_update: SolutionUpdate):
        """Update an existing solution"""
        db_solution = db.query(Solution).filter(Solution.id == solution_id).first()
        if db_solution:
            update_data = solution_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_solution, field, value)
            db.commit()
            db.refresh(db_solution)
        return db_solution

    @staticmethod
    def delete_solution(db: Session, solution_id: int):
        """Delete a solution"""
        db_solution = db.query(Solution).filter(Solution.id == solution_id).first()
        if db_solution:
            db.delete(db_solution)
            db.commit()
            return True
        return False
