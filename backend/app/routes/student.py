from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Optional

from app.models.students import Student, StudentCreate, ClassName
from app.db import get_session 

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=Student)
def create_student(student: StudentCreate, session: Session = Depends(get_session)):
    db_student = Student.from_orm(student)
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student

@router.get("/", response_model=List[Student])
def read_students(
    class_name: Optional[ClassName] = None,
    section: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Student)
    if class_name:
        query = query.where(Student.class_name == class_name)
    if section:
        query = query.where(Student.section == section)
    results = session.exec(query).all()
    return results

@router.get("/", response_model=List[Student])
def read_students(
    class_name: Optional[ClassName] = None,
    section: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Student)
    if class_name:
        query = query.where(Student.class_name == class_name)
    if section:
        query = query.where(Student.section == section)
    results = session.exec(query).all()
    return results

