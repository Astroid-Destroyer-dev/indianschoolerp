from sqlmodel import SQLModel, Session, create_engine
from typing import Generator

DATABASE_URL = "sqlite:///school.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
