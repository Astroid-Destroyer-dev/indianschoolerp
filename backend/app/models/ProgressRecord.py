from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.students import Student

class ProgressRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    student_id: int = Field(foreign_key="student.id")
    academic_year: str 
    
    class_name: str 
    section: str
    result_status: str  
    remarks: Optional[str] = None

    total_marks: Optional[int] = None
    percentage: Optional[float] = None

    student: Optional["Student"] = Relationship(back_populates="progress")
