from pydantic import BaseModel
from typing import Optional
from enum import Enum
from app.models.students import Gender


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    roll_no: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    dob: Optional[str] = None
    gender: Optional[Gender] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    blood_group: Optional[str] = None
    admission_date: Optional[str] = None
    aadhar_number: Optional[str] = None
