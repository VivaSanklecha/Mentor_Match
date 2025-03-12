# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Mentee schemas
class MenteeBase(BaseModel):
    username: str
    email: EmailStr

class MenteeCreate(MenteeBase):
    password: str
    interests: List[str]
    photo_url: Optional[str] = None  # Optional photo URL

class MenteeResponse(MenteeBase):
    id: int
    interests: Optional[List[str]] = None
    photo_url: Optional[str] = None  # Include photo URL in response
    
    class Config:
        orm_mode = True

# Mentor schemas
class MentorBase(BaseModel):
    username: str
    email: EmailStr

class MentorCreate(MentorBase):
    password: str
    expertise: List[str]
    years_of_experience: int
    photo_url: Optional[str] = None  # Optional photo URL

class MentorResponse(MentorBase):
    id: int
    expertise: List[str]
    years_of_experience: int
    photo_url: Optional[str] = None  # Include photo URL in response
    
    class Config:
        orm_mode = True

# Login schemas
class MenteeLogin(BaseModel):
    email: EmailStr
    password: str

class MentorLogin(BaseModel):
    email: EmailStr
    password: str

# Relationship schema
class MentorMenteeLink(BaseModel):
    mentor_id: int
    mentee_id: int