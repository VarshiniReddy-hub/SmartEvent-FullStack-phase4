import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Booking, Payment, Notification
from schemas import PaymentCreate, PaymentResponse
from security import bearer_scheme, get_current_user_id

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

@router.post("/checkout", response_model=PaymentResponse, status_code=201)
def checkout(data: PaymentCreate, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    user_id = get_current_user_id(credentials)
    booking = db.query(Booking).filter(Booking.id == data.booking_id, Booking.user_id == user_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.booking_status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Cancelled bookings cannot be paid")
    if db.query(Payment).filter(Payment.booking_id == booking.id, Payment.payment_status == "SUCCESS").first():
        raise HTTPException(status_code=400, detail="This booking has already been paid")
    success = data.simulated_result == "SUCCESS"
    payment = Payment(booking_id=booking.id, payment_method=data.payment_method, payment_status="SUCCESS" if success else "FAILED", transaction_id=f"SME-{uuid.uuid4().hex[:14].upper()}" if success else None, amount=booking.final_amount if booking.final_amount is not None else booking.total_price)
    if success:
        booking.booking_status = "CONFIRMED"
        message = f"Payment successful for booking #{booking.id}. Your tickets are confirmed."
        title = "Payment Successful"
    else:
        message = f"Payment failed for booking #{booking.id}. Please try again."
        title = "Payment Failed"
    db.add(payment)
    db.add(Notification(user_id=user_id, title=title, message=message, type="PAYMENT", is_read=False))
    db.commit(); db.refresh(payment)
    return payment

@router.get("/my-payments", response_model=list[PaymentResponse])
def my_payments(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    user_id = get_current_user_id(credentials)
    return db.query(Payment).join(Booking, Payment.booking_id == Booking.id).filter(Booking.user_id == user_id).order_by(Payment.created_at.desc()).all()
