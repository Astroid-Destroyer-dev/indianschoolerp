from fastapi import FastAPI, Depends
from app.models.students import Student
from app.db import create_db_and_tables, get_session
from sqlmodel import Session, select
from typing import List
from app.routes import student, classes, user_routes
from app.routes import router_progression
from app.routes import export_to_excel
from app.routes.fees_router import fees_router 
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Indian School ERP",
    description="An Open Source School ERP System",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React Dev Server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(export_to_excel.router)
app.include_router(router_progression.router)
app.include_router(student.router)
app.include_router(classes.router)
app.include_router(user_routes.router)
app.include_router(fees_router, prefix="/fees", tags=["Fees Management"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/students/", response_model=Student)
def add_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.get("/students/", response_model=List[Student])
def list_students(session: Session = Depends(get_session)):
    students = session.exec(select(Student)).all()
    return students
