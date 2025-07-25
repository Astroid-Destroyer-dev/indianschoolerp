from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.db import get_session
from app.models.students import Student
import pandas as pd
from io import BytesIO
from indic_transliteration.sanscript import transliterate
from indic_transliteration.sanscript import ITRANS, DEVANAGARI

router = APIRouter(tags=["Export to Excel"])

def transliterate_to_hindi(text):
    return transliterate(text, ITRANS, DEVANAGARI)

@router.get("/export/registration-format")
def export_registration_excel(session: Session = Depends(get_session)):
    students = session.query(Student).all()

    data = []
    for idx, student in enumerate(students, start=1):
        sr_number = f"{idx:04}"  # Format as 0001, 0002 etc.
        dob_parts = student.dob.split("-")  # Assuming 'YYYY-MM-DD'
        yyyy, mm, dd = dob_parts

        data.append({
            "SerialNumber": sr_number,
            "CandidateName": student.name,
            "FatherName": student.father_name,
            "MotherName": student.mother_name or "",
            "CandidateName_HIN": transliterate_to_hindi(student.name),
            "FatherName_HIN": transliterate_to_hindi(student.father_name),
            "MotherName_HIN": transliterate_to_hindi(student.mother_name) if student.mother_name else "",
            "DD": dd,
            "MM": mm,
            "YYYY": yyyy,
            "Sex": "M" if student.gender == "Male" else ("F" if student.gender == "Female" else "O"),
            "CasteCode": "",  
            "IsMinorityCode": "",
            "CandidateType1Code": "",
            "CandidateType2Code": "",
            "MediumCode": "",
            "Subject01Code": "",
            "Subject02Code": "",
            "Subject03Code": "",
            "Subject04Code": "",
            "Subject05Code": "",
            "Subject06Code": "",
            "Subject07Code": "",
            "SubjectVOCCode": "",
            "SubjectRevVOCCode": "",
            "MobileNumber": student.phone or "",
            "AadhaarNumber": student.aadhar_number,
            "EMAILID": student.email or "",
            "Address1": student.address or "",
            "Address2": "",
            "District": "",
            "PinCode": "",
            "UniqueIDClass08": "",
            "UdisePen": student.pen,  # Fill your School UDISE Pen
            "SrNumber": "",
        })

    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="RegistrationFormat")
    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="registration_format.xlsx"'
    }

    return Response(content=output.getvalue(), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers=headers)
