# backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import mentee_router, mentor_router

# Create tables in the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(mentee_router, prefix="/api/mentees", tags=["mentees"])
app.include_router(mentor_router, prefix="/api/mentors", tags=["mentors"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the MentorMatch API"}

@app.get("/test-cors")
async def test_cors():
    return {"message": "CORS is working!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)