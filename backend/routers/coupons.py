from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models import Coupon
from schemas import CouponCreate, CouponResponse, CouponValidate
from security import bearer_scheme, get_current_user_id
router = APIRouter(prefix="/api/v1/coupons", tags=["Coupons"])

@router.post("", response_model=CouponResponse, status_code=201)
def create_coupon(data: CouponCreate, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    get_current_user_id(credentials)
    code = data.coupon_code.strip().upper()
    if db.query(Coupon).filter(Coupon.coupon_code == code).first():
        raise HTTPException(status_code=409, detail="Coupon code already exists")
    if data.discount_type == "PERCENTAGE" and data.discount_value > 100:
        raise HTTPException(status_code=400, detail="Percentage discount cannot exceed 100")
    coupon = Coupon(coupon_code=code, discount_type=data.discount_type, discount_value=data.discount_value, minimum_booking_amount=data.minimum_booking_amount, expiry_date=data.expiry_date, usage_limit=data.usage_limit, is_active=data.is_active)
    db.add(coupon); db.commit(); db.refresh(coupon); return coupon

@router.post("/validate")
def validate_coupon(data: CouponValidate, db: Session = Depends(get_db)):
    coupon = db.query(Coupon).filter(Coupon.coupon_code == data.coupon_code.strip().upper()).first()
    if not coupon or not coupon.is_active: raise HTTPException(status_code=400, detail="Invalid or inactive coupon")
    if coupon.expiry_date < datetime.utcnow(): raise HTTPException(status_code=400, detail="Coupon has expired")
    if coupon.usage_count >= coupon.usage_limit: raise HTTPException(status_code=400, detail="Coupon usage limit reached")
    if data.booking_amount < coupon.minimum_booking_amount: raise HTTPException(status_code=400, detail=f"Minimum booking amount is ₹{coupon.minimum_booking_amount:.2f}")
    discount = data.booking_amount * coupon.discount_value / 100 if coupon.discount_type == "PERCENTAGE" else coupon.discount_value
    discount = min(discount, data.booking_amount)
    return {"valid": True, "coupon_id": coupon.id, "coupon_code": coupon.coupon_code, "discount_amount": round(discount, 2), "final_amount": round(data.booking_amount-discount, 2)}

@router.get("", response_model=list[CouponResponse])
def list_coupons(db: Session = Depends(get_db)):
    return db.query(Coupon).filter(Coupon.is_active == True).all()
