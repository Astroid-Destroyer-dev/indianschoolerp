from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.models.Progression import ProgressRecord
from app.models.students import Student
from app.db import engine

router = APIRouter()

@router.post("/progression/promote/{student_id}")
def promote_student(student_id: int, academic_year: str, class_id: int, section_id: int, result_status: str):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        progress = ProgressRecord(
            student_id=student.id,
            academic_year=academic_year,
            class_id=class_id,
            section_id=section_id,
            result_status=result_status
        )
        student.class_id = class_id
        student.section_id = section_id

        session.add(progress)
        session.add(student)
        session.commit()
        session.refresh(progress)
        return {"msg": "Student promoted successfully", "progress": progress}

@router.get("/progression/history/{student_id}")
def progression_history(student_id: int):
    with Session(engine) as session:
        statement = select(ProgressRecord).where(ProgressRecord.student_id == student_id)
        records = session.exec(statement).all()
        return records
