# menteedatahandler.py
from sqlalchemy.orm import Session
import bcrypt
from models import Mentee
from schemas import MenteeCreate

class MenteeDataHandler:
    @staticmethod
    def create_mentee(db: Session, mentee: MenteeCreate):
        # Hash the password
        hashed_password = bcrypt.hashpw(mentee.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create new mentee
        new_mentee = Mentee(
            username=mentee.username,
            email=mentee.email,
            password=hashed_password,
            interests=mentee.interests
        )
        
        db.add(new_mentee)
        db.commit()
        db.refresh(new_mentee)
        return new_mentee

    @staticmethod
    def get_all_mentees(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Mentee).offset(skip).limit(limit).all()

    @staticmethod
    def get_mentee_by_id(db: Session, mentee_id: int):
        return db.query(Mentee).filter(Mentee.id == mentee_id).first()
    
    @staticmethod
    def get_mentee_by_email(db: Session, email: str):
        return db.query(Mentee).filter(Mentee.email == email).first()
    
    @staticmethod
    def verify_login(db: Session, email: str, password: str):
        mentee = db.query(Mentee).filter(Mentee.email == email).first()
        if not mentee:
            return None
            
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), mentee.password.encode('utf-8')):
            return mentee
        return None