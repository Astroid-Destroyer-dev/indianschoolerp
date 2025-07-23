from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.models.students import ClassModel, SectionModel
from app.db import get_session

router = APIRouter(tags=["Classes and Sections"])

@router.post("/classes/", response_model=ClassModel)
def create_class(class_: ClassModel, session: Session = Depends(get_session)):
    db_class = ClassModel(name=class_.name)
    session.add(db_class)
    session.commit()
    session.refresh(db_class)
    return db_class

@router.get("/classes/", response_model=List[ClassModel])
def get_classes(session: Session = Depends(get_session)):
    classes = session.exec(select(ClassModel)).all()
    return classes

@router.post("/sections/", response_model=SectionModel)
def create_section(section: SectionModel, session: Session = Depends(get_session)):
    # Verify class exists
    class_ = session.exec(select(ClassModel).where(ClassModel.id == section.class_id)).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    
    db_section = SectionModel(name=section.name, class_id=section.class_id)
    session.add(db_section)
    session.commit()
    session.refresh(db_section)
    return db_section

@router.get("/sections/{class_id}", response_model=List[SectionModel])
def get_sections(class_id: int, session: Session = Depends(get_session)):
    sections = session.exec(select(SectionModel).where(SectionModel.class_id == class_id)).all()
    return sections