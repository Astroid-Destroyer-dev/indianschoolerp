from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, select
from pydantic import validator

class UserRole(str, Enum):
    admin = "admin"
    teacher = "teacher"
    staff = "staff"

class UserCreate(SQLModel):
    username: str
    password: str
    role: UserRole

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password: str
    role: UserRole
    is_active: bool = Field(default=True)

    @validator("role")
    def validate_admin_role(cls, v, values, **kwargs):
        if v == UserRole.admin:
            from sqlmodel import Session
            from app.db import engine
            with Session(engine) as session:
                existing_admin = session.exec(
                    select(User).where(User.role == UserRole.admin)
                ).first()
                if existing_admin:
                    raise ValueError("An admin user already exists")
        return v