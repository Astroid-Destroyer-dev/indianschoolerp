from sqlmodel import SQLModel, Field
from typing import Optional


class ProgressRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    academic_year: str
    class_id: int = Field(foreign_key="classmodel.id")
    section_id: int = Field(foreign_key="sectionmodel.id")
    result_status: str  # 'Passed', 'Failed', 'Promoted'
    total_marks: Optional[int] = None
    percentage: Optional[float] = None
    remarks: Optional[str] = None
