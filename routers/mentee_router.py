# routers/mentee_router.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import MenteeCreate, MenteeResponse, MenteeLogin, MentorResponse
from menteedatahandler import MenteeDataHandler

router = APIRouter()

@router.post("/signup", response_model=MenteeResponse, status_code=status.HTTP_201_CREATED)
def signup_mentee(mentee: MenteeCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = MenteeDataHandler.get_mentee_by_email(db, mentee.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the mentee
    new_mentee = MenteeDataHandler.create_mentee(db, mentee)
    return new_mentee

@router.post("/login", response_model=MenteeResponse)
def login_mentee(user_data: MenteeLogin, db: Session = Depends(get_db)):
    # Verify credentials
    user = MenteeDataHandler.verify_login(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/", response_model=List[MenteeResponse])
def get_all_mentees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    mentees = MenteeDataHandler.get_all_mentees(db, skip, limit)
    return mentees

@router.get("/{mentee_id}", response_model=MenteeResponse)
def get_mentee_by_id(mentee_id: int, db: Session = Depends(get_db)):
    mentee = MenteeDataHandler.get_mentee_by_id(db, mentee_id)
    if mentee is None:
        raise HTTPException(status_code=404, detail="Mentee not found")
    return mentee

@router.get("/{mentee_id}/mentors", response_model=List[MentorResponse])
def get_mentee_mentors(mentee_id: int, db: Session = Depends(get_db)):
    mentee = MenteeDataHandler.get_mentee_by_id(db, mentee_id)
    if mentee is None:
        raise HTTPException(status_code=404, detail="Mentee not found")
    
    return mentee.mentors