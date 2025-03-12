# routers/mentor_router.py
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas import MentorCreate, MentorResponse, MentorLogin, MenteeResponse, MentorMenteeLink
from mentordatahandler import MentorDataHandler

router = APIRouter()

@router.post("/signup", response_model=MentorResponse, status_code=status.HTTP_201_CREATED)
def signup_mentor(mentor: MentorCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = MentorDataHandler.get_mentor_by_email(db, mentor.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the mentor
    new_mentor = MentorDataHandler.create_mentor(db, mentor)
    return new_mentor

@router.post("/login", response_model=MentorResponse)
def login_mentor(user_data: MentorLogin, db: Session = Depends(get_db)):
    # Verify credentials
    user = MentorDataHandler.verify_login(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.get("/", response_model=List[MentorResponse])
def get_all_mentors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    mentors = MentorDataHandler.get_all_mentors(db, skip, limit)
    return mentors

@router.get("/{mentor_id}", response_model=MentorResponse)
def get_mentor_by_id(mentor_id: int, db: Session = Depends(get_db)):
    mentor = MentorDataHandler.get_mentor_by_id(db, mentor_id)
    if mentor is None:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor

@router.post("/{mentor_id}/mentees", status_code=status.HTTP_201_CREATED)
def assign_mentee_to_mentor(mentor_id: int, link: MentorMenteeLink, db: Session = Depends(get_db)):
    # Verify mentor_id matches the one in the path
    if mentor_id != link.mentor_id:
        raise HTTPException(status_code=400, detail="Mentor ID mismatch")
    
    # Assign mentee to mentor
    success = MentorDataHandler.assign_mentee(db, link.mentor_id, link.mentee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mentor or mentee not found")
    
    return {"message": "Mentee assigned successfully"}

@router.get("/{mentor_id}/mentees", response_model=List[MenteeResponse])
def get_mentor_mentees(mentor_id: int, db: Session = Depends(get_db)):
    # Check if mentor exists
    mentor = MentorDataHandler.get_mentor_by_id(db, mentor_id)
    if mentor is None:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    # Get all mentees for the mentor
    mentees = MentorDataHandler.get_mentor_mentees(db, mentor_id)
    return mentees