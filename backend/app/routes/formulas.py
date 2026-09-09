"""Routes for formula management"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import FormulaCreate, FormulaUpdate, FormulaResponse
from app.services.formula_service import FormulaService
from app.services.subject_service import SubjectService

router = APIRouter(
    prefix="/formulas",
    tags=["formulas"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[FormulaResponse])
async def get_formulas(
    subject_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all formulas with optional filtering by subject"""
    formulas = FormulaService.get_all_formulas(db, subject_id=subject_id, skip=skip, limit=limit)
    return formulas


@router.get("/{formula_id}", response_model=FormulaResponse)
async def get_formula(formula_id: int, db: Session = Depends(get_db)):
    """Get a specific formula"""
    formula = FormulaService.get_formula_by_id(db, formula_id)
    if not formula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Formula with id {formula_id} not found"
        )
    return formula


@router.post("/", response_model=FormulaResponse, status_code=status.HTTP_201_CREATED)
async def create_formula(formula: FormulaCreate, db: Session = Depends(get_db)):
    """Create a new formula"""
    # Verify subject exists
    subject = SubjectService.get_subject_by_id(db, formula.subject_id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {formula.subject_id} not found"
        )
    
    new_formula = FormulaService.create_formula(db, formula)
    return new_formula


@router.put("/{formula_id}", response_model=FormulaResponse)
async def update_formula(
    formula_id: int,
    formula_update: FormulaUpdate,
    db: Session = Depends(get_db)
):
    """Update a formula"""
    formula = FormulaService.get_formula_by_id(db, formula_id)
    if not formula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Formula with id {formula_id} not found"
        )
    
    updated_formula = FormulaService.update_formula(db, formula_id, formula_update)
    return updated_formula


@router.delete("/{formula_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_formula(formula_id: int, db: Session = Depends(get_db)):
    """Delete a formula"""
    formula = FormulaService.get_formula_by_id(db, formula_id)
    if not formula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Formula with id {formula_id} not found"
        )
    
    FormulaService.delete_formula(db, formula_id)
    return None
