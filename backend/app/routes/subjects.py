"""Routes for subject management"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.schemas import SubjectCreate, SubjectUpdate, SubjectResponse, SubjectDetailedResponse
from app.services.subject_service import SubjectService

router = APIRouter(
    prefix="/subjects",
    tags=["subjects"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[SubjectResponse])
async def get_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all subjects"""
    subjects = SubjectService.get_all_subjects(db, skip=skip, limit=limit)
    return subjects


@router.get("/{subject_id}", response_model=SubjectDetailedResponse)
async def get_subject(subject_id: int, db: Session = Depends(get_db)):
    """Get a specific subject with all its topics and formulas"""
    subject = SubjectService.get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {subject_id} not found"
        )
    return subject


@router.post("/", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    """Create a new subject"""
    # Check if subject with same code already exists
    existing = SubjectService.get_subject_by_code(db, subject.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Subject with code {subject.code} already exists"
        )
    
    new_subject = SubjectService.create_subject(db, subject)
    return new_subject


@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: int,
    subject_update: SubjectUpdate,
    db: Session = Depends(get_db)
):
    """Update a subject"""
    subject = SubjectService.get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {subject_id} not found"
        )
    
    updated_subject = SubjectService.update_subject(db, subject_id, subject_update)
    return updated_subject


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    """Delete a subject"""
    subject = SubjectService.get_subject_by_id(db, subject_id)
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subject with id {subject_id} not found"
        )
    
    SubjectService.delete_subject(db, subject_id)
    return None
