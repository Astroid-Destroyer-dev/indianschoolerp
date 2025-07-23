from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import validator
import re
from enum import Enum
from typing import List
from sqlmodel import Relationship


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class ClassModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str 

    sections: List["SectionModel"] = Relationship(back_populates="class_")

class SectionModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  
    
    class_id: int = Field(foreign_key="classmodel.id")
    class_: Optional[ClassModel] = Relationship(back_populates="sections")
    
class StudentCreate(SQLModel):
    name: str
    roll_no: str
    class_id: int = Field(default=None, foreign_key="classmodel.id")
    section_id: int = Field(default=None, foreign_key="sectionmodel.id")
    dob: str
    gender: Gender
    father_name: str
    mother_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    blood_group: Optional[str] = None
    admission_date: str
    aadhar_number: str

class user(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    role: str

class Student(SQLModel, table=True):
     id: Optional[int] = Field(default=None, primary_key=True)
     name: str
     roll_no: Optional[str]
     class_id: int = Field(default=None, foreign_key="classmodel.id")
     section_id: int = Field(default=None, foreign_key="sectionmodel.id")
     dob: str
     gender: Gender
     father_name: str
     mother_name: Optional[str] = None
     phone: str = None
     address: Optional[str] = None
     email: Optional[str] = None
     blood_group: Optional[str] = None
     admission_date: str
     aadhar_number: str
     progress: list["ProgressRecord"] = Relationship(back_populates="student")  # string reference

     @validator("aadhar_number")
     def aadhar_must_be_12_digits(cls, v):
         if not re.fullmatch(r"\d{12}", v):
             raise ValueError("Aadhar number must be exactly 12 digits")
         return v
     
     @validator("phone")
     def phone_must_be_10_digits(cls, v):
         if v and not re.fullmatch(r"\d{10}", v):
             raise ValueError("Phone number must be exactly 10 digits")
         return v