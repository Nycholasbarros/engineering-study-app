"""Services for exercise operations"""

from sqlalchemy.orm import Session
from app.models.models import Exercise, DifficultyLevel
from app.schemas.schemas import ExerciseCreate, ExerciseUpdate


class ExerciseService:
    """Service for managing exercises"""

    @staticmethod
    def get_all_exercises(
        db: Session,
        subject_id: int = None,
        difficulty: str = None,
        skip: int = 0,
        limit: int = 100
    ):
        """Get all exercises with optional filtering"""
        query = db.query(Exercise)
        if subject_id:
            query = query.filter(Exercise.subject_id == subject_id)
        if difficulty:
            query = query.filter(Exercise.difficulty == difficulty)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_exercise_by_id(db: Session, exercise_id: int):
        """Get an exercise by ID"""
        return db.query(Exercise).filter(Exercise.id == exercise_id).first()

    @staticmethod
    def create_exercise(db: Session, exercise: ExerciseCreate):
        """Create a new exercise"""
        db_exercise = Exercise(
            subject_id=exercise.subject_id,
            title=exercise.title,
            description=exercise.description,
            difficulty=exercise.difficulty,
            statement=exercise.statement,
            expected_answer_type=exercise.expected_answer_type,
            tags=exercise.tags
        )
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        return db_exercise

    @staticmethod
    def update_exercise(db: Session, exercise_id: int, exercise_update: ExerciseUpdate):
        """Update an existing exercise"""
        db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if db_exercise:
            update_data = exercise_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_exercise, field, value)
            db.commit()
            db.refresh(db_exercise)
        return db_exercise

    @staticmethod
    def delete_exercise(db: Session, exercise_id: int):
        """Delete an exercise"""
        db_exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if db_exercise:
            db.delete(db_exercise)
            db.commit()
            return True
        return False
