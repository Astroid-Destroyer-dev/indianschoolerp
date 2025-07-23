from sqlmodel import SQLModel, Session, create_engine
from app.models.students import Student

DATABASE_URL = "sqlite:///school.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
