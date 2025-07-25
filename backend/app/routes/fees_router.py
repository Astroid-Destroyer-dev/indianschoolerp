from app.models.fees import FeeStructure, StudentFeeRecord
from app.models.fees import FeeStructureCreate, StudentFeePaymentCreate
from fastapi import APIRouter, Depends, HTTPException
from app.db import get_session
from sqlmodel import Session
from app.models.students import Student
from reportlab.lib.pagesizes import A4
from app.models.users import User
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import FileResponse, HTMLResponse  # Updated imports
from sqlalchemy import select   


router = APIRouter()

@router.post("/fee-structure")
def create_fee_structure(fee: FeeStructureCreate, session: Session = Depends(get_session)):
    # Add validation for reasonable fee amounts
    if fee.amount <= 0 or fee.amount > 1000000:  # adjust max limit as needed
        raise HTTPException(
            status_code=400,
            detail="Fee amount must be between 0 and 1,000,000"
        )

    new_fee = FeeStructure(**fee.dict())
    session.add(new_fee)
    session.commit()
    session.refresh(new_fee)
    return new_fee
@router.post("/fee-payment")
def record_fee_payment(payment: StudentFeePaymentCreate, session: Session = Depends(get_session)):
    # Check if receipt number already exists
    existing_payment = session.query(StudentFeeRecord).filter(
        StudentFeeRecord.receipt_number == payment.receipt_number
    ).first()
    
    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail=f"Receipt number {payment.receipt_number} already exists"
        )

    # Validate payment amount
    if payment.amount_paid <= 0:
        raise HTTPException(
            status_code=400,
            detail="Payment amount must be greater than 0"
        )

    new_payment = StudentFeeRecord(**payment.dict())
    session.add(new_payment)
    session.commit()
    session.refresh(new_payment)
    return new_payment
@router.get("/student/{student_id}/fee-dues")
def get_student_fee_dues(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch applicable fee structures
    fee_structures = session.query(FeeStructure).filter(FeeStructure.class_id == student.class_id).all()
    
    if not fee_structures:
        raise HTTPException(
            status_code=404, 
            detail=f"No fee structure found for class_id: {student.class_id}"
        )

    total_fee = sum(fee.amount for fee in fee_structures)

    # Fetch student payments
    payments = session.query(StudentFeeRecord).filter(StudentFeeRecord.student_id == student_id).all()
    total_paid = sum(payment.amount_paid for payment in payments)

    dues = total_fee - total_paid

    payment_details = [
           {
               "receipt_id": payment.receipt_number,
               "amount_paid": payment.amount_paid,
               "payment_date": payment.payment_date,
               "payment_mode": payment.payment_mode
           }
           for payment in payments
       ]

    return {
        "StudentID": student_id,
        "StudentName": student.name,
        "TotalFee": total_fee,
        "TotalPaid": total_paid,
        "DueAmount": dues,
        "FeeStructures": [
            {"id": fee.id, "amount": fee.amount, "fee_type": fee.fee_type}
            for fee in fee_structures
        ],
        "payments": payment_details
    }
@router.get("/fees/receipt/{receipt_number}", response_class=HTMLResponse)
def view_receipt(receipt_number: str, session: Session = Depends(get_session)):
    try:
        # Query student & receipt details
        stmt = select(StudentFeeRecord, User.username).join(
            User, StudentFeeRecord.user_id == User.id
        ).where(StudentFeeRecord.receipt_number == receipt_number)
        result = session.execute(stmt).fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Receipt not found")

        fee_record, uploaded_by = result
        student = session.query(Student).filter(Student.id == fee_record.student_id).first()

        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # Create template environment
        env = Environment(loader=FileSystemLoader('app'))
        template = env.get_template('receipt_template.html')

        # Render HTML directly
        html_content = template.render(
            student_id=student.id,
            student_name=student.name,
            father_name=student.father_name,
            receipt_number=fee_record.receipt_number,
            amount_paid=fee_record.amount_paid,
            payment_date=str(fee_record.payment_date),
            payment_mode=fee_record.payment_mode,
            uploaded_by=uploaded_by
        )
        
        return HTMLResponse(content=html_content, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))