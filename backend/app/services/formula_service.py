"""Services for formula operations"""

from sqlalchemy.orm import Session
from app.models.models import Formula
from app.schemas.schemas import FormulaCreate, FormulaUpdate


class FormulaService:
    """Service for managing formulas"""

    @staticmethod
    def get_all_formulas(db: Session, subject_id: int = None, skip: int = 0, limit: int = 100):
        """Get all formulas with optional filtering by subject"""
        query = db.query(Formula)
        if subject_id:
            query = query.filter(Formula.subject_id == subject_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_formula_by_id(db: Session, formula_id: int):
        """Get a formula by ID"""
        return db.query(Formula).filter(Formula.id == formula_id).first()

    @staticmethod
    def create_formula(db: Session, formula: FormulaCreate):
        """Create a new formula"""
        db_formula = Formula(
            subject_id=formula.subject_id,
            topic_id=formula.topic_id,
            name=formula.name,
            formula=formula.formula,
            description=formula.description,
            components=formula.components,
            usage_example=formula.usage_example,
            unit=formula.unit
        )
        db.add(db_formula)
        db.commit()
        db.refresh(db_formula)
        return db_formula

    @staticmethod
    def update_formula(db: Session, formula_id: int, formula_update: FormulaUpdate):
        """Update an existing formula"""
        db_formula = db.query(Formula).filter(Formula.id == formula_id).first()
        if db_formula:
            update_data = formula_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_formula, field, value)
            db.commit()
            db.refresh(db_formula)
        return db_formula

    @staticmethod
    def delete_formula(db: Session, formula_id: int):
        """Delete a formula"""
        db_formula = db.query(Formula).filter(Formula.id == formula_id).first()
        if db_formula:
            db.delete(db_formula)
            db.commit()
            return True
        return False
