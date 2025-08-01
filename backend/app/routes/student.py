from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Optional
from app.models.StudentUpdate import StudentUpdate
from app.models.students import Student, StudentCreate
from app.db import get_session 
from fastapi import HTTPException

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
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    query = select(Student)
    if class_id:
        query = query.where(Student.class_id == class_id)
    if section_id:
        query = query.where(Student.section_id == section_id)
    results = session.exec(query).all()
    return results

@router.put("/students/{student_id}")
def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_session)):
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)

    db.add(student)
    db.commit()
    db.refresh(student)

    return {"message": "Student updated successfully", "student": student}