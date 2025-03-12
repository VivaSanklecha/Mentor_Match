# mentordatahandler.py
from sqlalchemy.orm import Session
import bcrypt
from models import Mentor, Mentee, mentor_mentee
from schemas import MentorCreate

class MentorDataHandler:
    @staticmethod
    def create_mentor(db: Session, mentor: MentorCreate):
        # Hash the password
        hashed_password = bcrypt.hashpw(mentor.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create new mentor
        new_mentor = Mentor(
            username=mentor.username,
            email=mentor.email,
            password=hashed_password,
            years_of_experience=mentor.years_of_experience,
            expertise=mentor.expertise
        )
        
        db.add(new_mentor)
        db.commit()
        db.refresh(new_mentor)
        return new_mentor

    @staticmethod
    def get_all_mentors(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Mentor).offset(skip).limit(limit).all()

    @staticmethod
    def get_mentor_by_id(db: Session, mentor_id: int):
        return db.query(Mentor).filter(Mentor.id == mentor_id).first()
    
    @staticmethod
    def get_mentor_by_email(db: Session, email: str):
        return db.query(Mentor).filter(Mentor.email == email).first()
    
    @staticmethod
    def verify_login(db: Session, email: str, password: str):
        mentor = db.query(Mentor).filter(Mentor.email == email).first()
        if not mentor:
            return None
            
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), mentor.password.encode('utf-8')):
            return mentor
        return None
    
    @staticmethod
    def assign_mentee(db: Session, mentor_id: int, mentee_id: int):
        # Check if mentor and mentee exist
        mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
        mentee = db.query(Mentee).filter(Mentee.id == mentee_id).first()
        
        if not mentor or not mentee:
            return False
            
        # Add mentee to mentor's mentees list
        mentor.mentees.append(mentee)
        db.commit()
        return True
    
    @staticmethod
    def get_mentor_mentees(db: Session, mentor_id: int):
        mentor = db.query(Mentor).filter(Mentor.id == mentor_id).first()
        if not mentor:
            return []
        return mentor.mentees