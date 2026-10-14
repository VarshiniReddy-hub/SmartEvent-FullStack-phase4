from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


# =========================
# USER REGISTRATION
# =========================

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


# =========================
# USER RESPONSE
# =========================

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# =========================
# JWT TOKEN
# =========================

class Token(BaseModel):
    access_token: str
    token_type: str


# =========================
# EVENT CREATE
# =========================

class EventCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(min_length=5)
    category: Literal["Music", "Tech", "Sports", "Business"]
    location: str = Field(min_length=2, max_length=200)
    event_date: datetime
    ticket_price: float = Field(gt=0)
    banner_image: str | None = None
    total_tickets: int = Field(gt=0)


# =========================
# EVENT RESPONSE
# =========================

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    location: str
    event_date: datetime
    ticket_price: float
    banner_image: str | None
    total_tickets: int
    available_tickets: int
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# BOOKING CREATE
# =========================

class BookingCreate(BaseModel):
    event_id: int
    ticket_quantity: int = Field(gt=0, le=10)
    coupon_code: str | None = None


# =========================
# BOOKING RESPONSE
# =========================

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    ticket_quantity: int
    total_price: float
    coupon_id: int | None = None
    discount_amount: float = 0
    final_amount: float = 0
    booking_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# TICKET RESPONSE
# =========================

class TicketResponse(BaseModel):
    id: int
    booking_id: int
    ticket_code: str
    qr_code_url: str | None
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# NOTIFICATION RESPONSE
# =========================

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    booking_id: int
    payment_method: Literal["CARD", "UPI", "NET_BANKING", "SIMULATED"] = "SIMULATED"
    # Only for local demo testing; use real gateway verification in production.
    simulated_result: Literal["SUCCESS", "FAILED"] = "SUCCESS"

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    payment_method: str
    payment_status: str
    transaction_id: str | None
    amount: float
    created_at: datetime
    class Config:
        from_attributes = True

class CouponCreate(BaseModel):
    coupon_code: str = Field(min_length=3, max_length=50)
    discount_type: Literal["PERCENTAGE", "FIXED"]
    discount_value: float = Field(gt=0)
    minimum_booking_amount: float = Field(default=0, ge=0)
    expiry_date: datetime
    usage_limit: int = Field(gt=0)
    is_active: bool = True

class CouponValidate(BaseModel):
    coupon_code: str
    booking_amount: float = Field(gt=0)

class CouponResponse(BaseModel):
    id: int
    coupon_code: str
    discount_type: str
    discount_value: float
    minimum_booking_amount: float
    expiry_date: datetime
    usage_limit: int
    usage_count: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    event_id: int
    rating: int = Field(ge=1, le=5)
    review_text: str = Field(default="", max_length=2000)

class ReviewUpdate(BaseModel):
    rating: int = Field(ge=1, le=5)
    review_text: str = Field(default="", max_length=2000)

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    rating: int
    review_text: str
    created_at: datetime
    class Config:
        from_attributes = True
