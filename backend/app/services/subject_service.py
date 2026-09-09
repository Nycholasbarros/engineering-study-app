"""Services for subject operations"""

from sqlalchemy.orm import Session
from app.models.models import Subject
from app.schemas.schemas import SubjectCreate, SubjectUpdate


class SubjectService:
    """Service for managing subjects"""

    @staticmethod
    def get_all_subjects(db: Session, skip: int = 0, limit: int = 100):
        """Get all subjects with pagination"""
        return db.query(Subject).offset(skip).limit(limit).all()

    @staticmethod
    def get_subject_by_id(db: Session, subject_id: int):
        """Get a subject by ID"""
        return db.query(Subject).filter(Subject.id == subject_id).first()

    @staticmethod
    def get_subject_by_code(db: Session, code: str):
        """Get a subject by code"""
        return db.query(Subject).filter(Subject.code == code).first()

    @staticmethod
    def create_subject(db: Session, subject: SubjectCreate):
        """Create a new subject"""
        db_subject = Subject(
            name=subject.name,
            description=subject.description,
            code=subject.code
        )
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return db_subject

    @staticmethod
    def update_subject(db: Session, subject_id: int, subject_update: SubjectUpdate):
        """Update an existing subject"""
        db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if db_subject:
            update_data = subject_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_subject, field, value)
            db.commit()
            db.refresh(db_subject)
        return db_subject

    @staticmethod
    def delete_subject(db: Session, subject_id: int):
        """Delete a subject"""
        db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if db_subject:
            db.delete(db_subject)
            db.commit()
            return True
        return False
