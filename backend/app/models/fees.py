from sqlmodel import SQLModel
from typing import Optional
from sqlmodel import Field
from datetime import date
from pydantic import BaseModel
from pydantic import BaseModel
from datetime import date

class FeeStructure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    class_id: int = Field(foreign_key="classmodel.id")
    section_id: Optional[int] = Field(default=None, foreign_key="sectionmodel.id")
    fee_type: str  # Example: Tuition, Transport, Exam, etc.
    amount: float


class StudentFeeRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="student.id")
    fee_structure_id: int = Field(foreign_key="feestructure.id")
    amount_paid: float
    payment_date: date = Field(default_factory=date.today)
    payment_mode: str  # Cash, UPI, Cheque etc.
    receipt_number: str
    user_id: int = Field(foreign_key="user.id")
  

class FeeStructureCreate(BaseModel):
    class_id: int
    section_id: Optional[int] = None  # If fees is for a section-specific
    fee_type: str  # e.g., Tuition, Transport, Exam Fee
    amount: float
    


class StudentFeePaymentCreate(BaseModel):
    student_id: int
    fee_structure_id: int
    amount_paid: float
    payment_date: Optional[date] = None
    payment_mode: str
    receipt_number: str
    user_id: int

    class Config:
        schema_extra = {
            "example": {
                "student_id": 1,
                "fee_structure_id": 1,
                "amount_paid": 5000,
                "payment_date": "2025-07-25",
                "payment_mode": "Cash",
                "receipt_number": "RCP-001",
                "user_id": 1
            }
        }



