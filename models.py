# models.py
from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from database import Base

# Association table for mentor-mentee relationship
mentor_mentee = Table(
    "mentor_mentee",
    Base.metadata,
    Column("mentor_id", Integer, ForeignKey("mentors.id"), primary_key=True),
    Column("mentee_id", Integer, ForeignKey("mentees.id"), primary_key=True)
)

class Mentor(Base):
    __tablename__ = "mentors"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    years_of_experience = Column(Integer, default=0)
    expertise = Column(ARRAY(String), nullable=True)
    photo_url = Column(String, nullable=True)  # New field for profile photo
    
    # Relationship with mentees (many-to-many)
    mentees = relationship("Mentee", secondary=mentor_mentee, back_populates="mentors")

class Mentee(Base):
    __tablename__ = "mentees"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    interests = Column(ARRAY(String), nullable=True)
    photo_url = Column(String, nullable=True)  # New field for profile photo
    
    # Relationship with mentors (many-to-many)
    mentors = relationship("Mentor", secondary=mentor_mentee, back_populates="mentees")