from fastapi import FastAPI, Depends
from app.models.students import Student
from app.db import create_db_and_tables, get_session
from sqlmodel import Session, select
from typing import List
from fastapi import FastAPI
from app.routes import student


app = FastAPI()
app.include_router(student.router)

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
