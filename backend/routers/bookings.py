import os
import uuid

import qrcode
<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
=======
from fastapi import APIRouter, Depends, HTTPException, status
>>>>>>> origin/main
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
<<<<<<< HEAD
from models import Booking, Event, User, Notification, Ticket, Coupon
from schemas import BookingCreate, BookingResponse
from datetime import datetime
from security import bearer_scheme, get_current_user_id
from sqlalchemy import update
from routers.phase4 import manager


async def broadcast_availability(event_id: int, available_tickets: int):
    await manager.broadcast(event_id, {"event_id": event_id, "available_tickets": available_tickets, "sold_out": available_tickets <= 0})

=======
from models import Booking, Event, User, Notification, Ticket
from schemas import BookingCreate, BookingResponse
from security import bearer_scheme, get_current_user_id


>>>>>>> origin/main
router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"]
)


<<<<<<< HEAD
=======
# =========================
# CREATE BOOKING
# =========================

>>>>>>> origin/main
@router.post(
    "",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_booking(
    booking_data: BookingCreate,
<<<<<<< HEAD
    background_tasks: BackgroundTasks,
=======
>>>>>>> origin/main
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
<<<<<<< HEAD
    user_id = get_current_user_id(credentials)
=======
    # Get logged-in user
    user_id = get_current_user_id(
        credentials=credentials,
        db=db
    )
>>>>>>> origin/main

    # Check user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check event
    event = db.query(Event).filter(
        Event.id == booking_data.event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

<<<<<<< HEAD
    # Atomically reserve tickets to prevent two concurrent requests overselling.
    reservation = db.query(Event).filter(
        Event.id == event.id,
        Event.available_tickets >= booking_data.ticket_quantity
    ).update(
        {Event.available_tickets: Event.available_tickets - booking_data.ticket_quantity},
        synchronize_session=False
    )
    if reservation != 1:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Not enough tickets available"
        )
    db.refresh(event)

    # Calculate total and validate an optional coupon.
    total_price = event.ticket_price * booking_data.ticket_quantity
    coupon = None
    discount_amount = 0.0
    if booking_data.coupon_code:
        coupon = db.query(Coupon).filter(
            Coupon.coupon_code == booking_data.coupon_code.strip().upper()
        ).first()
        if not coupon or not coupon.is_active:
            raise HTTPException(status_code=400, detail="Invalid or inactive coupon")
        if coupon.expiry_date < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Coupon has expired")
        if coupon.usage_count >= coupon.usage_limit:
            raise HTTPException(status_code=400, detail="Coupon usage limit reached")
        if total_price < coupon.minimum_booking_amount:
            raise HTTPException(status_code=400, detail=f"Minimum booking amount is ₹{coupon.minimum_booking_amount:.2f}")
        discount_amount = total_price * coupon.discount_value / 100 if coupon.discount_type == "PERCENTAGE" else coupon.discount_value
        discount_amount = min(discount_amount, total_price)
        coupon.usage_count += 1

    # Booking remains pending until payment succeeds.
=======
    # Check if event is cancelled
    if event.event_status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book a cancelled event"
        )

    # Check ticket quantity
    if booking_data.ticket_quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticket quantity must be greater than 0"
        )

    # Check ticket availability
    if event.available_tickets < booking_data.ticket_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough tickets available"
        )

    # Calculate total price
    total_price = (
        event.ticket_price *
        booking_data.ticket_quantity
    )

    # Create booking
>>>>>>> origin/main
    new_booking = Booking(
        user_id=user_id,
        event_id=event.id,
        ticket_quantity=booking_data.ticket_quantity,
        total_price=total_price,
<<<<<<< HEAD
        coupon_id=coupon.id if coupon else None,
        discount_amount=round(discount_amount, 2),
        final_amount=round(total_price - discount_amount, 2),
        booking_status="PENDING"
=======
        booking_status="CONFIRMED"
    )

    # Reduce available tickets
    event.available_tickets -= (
        booking_data.ticket_quantity
>>>>>>> origin/main
    )

    db.add(new_booking)

<<<<<<< HEAD
    # Get booking ID before creating ticket
=======
    # Get booking ID
>>>>>>> origin/main
    db.flush()

    # =========================
    # GENERATE QR TICKET
    # =========================

    ticket_code = (
        f"SME-{uuid.uuid4().hex[:12].upper()}"
    )

    os.makedirs(
        "static/qrcodes",
        exist_ok=True
    )

    qr_file_name = f"{ticket_code}.png"

    qr_file_path = os.path.join(
        "static",
        "qrcodes",
        qr_file_name
    )

    qr_data = (
        f"SmartEvent Ticket\n"
        f"Ticket Code: {ticket_code}\n"
        f"Booking ID: {new_booking.id}\n"
        f"Event ID: {event.id}"
    )

    qr_image = qrcode.make(qr_data)

    qr_image.save(qr_file_path)

    qr_code_url = (
        f"/static/qrcodes/{qr_file_name}"
    )

    # Create ticket record
    new_ticket = Ticket(
        booking_id=new_booking.id,
        ticket_code=ticket_code,
        qr_code_url=qr_code_url
    )

    db.add(new_ticket)

    # =========================
    # BOOKING NOTIFICATION
    # =========================

    notification = Notification(
        user_id=user_id,
<<<<<<< HEAD
        title="Booking Created",
=======
        title="Booking Confirmed",
>>>>>>> origin/main
        message=(
            f"Your booking for '{event.title}' "
            f"has been confirmed. "
            f"You booked "
            f"{booking_data.ticket_quantity} ticket(s). "
            f"Ticket Code: {ticket_code}"
        ),
        type="BOOKING",
        is_read=False
    )

    db.add(notification)

<<<<<<< HEAD
    # Save everything
    db.commit()

    db.refresh(new_booking)
    background_tasks.add_task(broadcast_availability, event.id, event.available_tickets)
=======
    # =========================
    # SAVE EVERYTHING
    # =========================

    db.commit()

    db.refresh(new_booking)
>>>>>>> origin/main

    return new_booking


<<<<<<< HEAD
=======
# =========================
# GET MY BOOKINGS
# =========================

>>>>>>> origin/main
@router.get(
    "/my-bookings",
    response_model=list[BookingResponse]
)
def get_my_bookings(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
<<<<<<< HEAD
    user_id = get_current_user_id(credentials)
=======
    user_id = get_current_user_id(
        credentials=credentials,
        db=db
    )
>>>>>>> origin/main

    bookings = (
        db.query(Booking)
        .filter(
            Booking.user_id == user_id
        )
        .order_by(
            Booking.created_at.desc()
        )
        .all()
    )

    return bookings


<<<<<<< HEAD
=======
# =========================
# GET SINGLE BOOKING
# =========================

>>>>>>> origin/main
@router.get(
    "/{booking_id}",
    response_model=BookingResponse
)
def get_booking(
    booking_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
<<<<<<< HEAD
    user_id = get_current_user_id(credentials)
=======
    user_id = get_current_user_id(
        credentials=credentials,
        db=db
    )
>>>>>>> origin/main

    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

<<<<<<< HEAD
=======
    # Check ownership
>>>>>>> origin/main
    if booking.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You are not allowed to access "
                "this booking"
            )
        )

    return booking


<<<<<<< HEAD
=======
# =========================
# CANCEL BOOKING
# =========================

>>>>>>> origin/main
@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingResponse
)
def cancel_booking(
    booking_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
<<<<<<< HEAD
    user_id = get_current_user_id(credentials)
=======
    user_id = get_current_user_id(
        credentials=credentials,
        db=db
    )
>>>>>>> origin/main

    booking = (
        db.query(Booking)
        .filter(
            Booking.id == booking_id
        )
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

    # Check ownership
    if booking.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You are not allowed to cancel "
                "this booking"
            )
        )

    # Already cancelled
    if booking.booking_status == "CANCELLED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking is already cancelled"
        )

<<<<<<< HEAD
    # Pending and confirmed bookings can be cancelled.
    if booking.booking_status not in ("CONFIRMED", "PENDING"):
        raise HTTPException(status_code=400, detail="This booking cannot be cancelled")
=======
    # Only confirmed bookings can be cancelled
    if booking.booking_status != "CONFIRMED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only confirmed bookings "
                "can be cancelled"
            )
        )
>>>>>>> origin/main

    # Restore event tickets
    event = (
        db.query(Event)
        .filter(
            Event.id == booking.event_id
        )
        .first()
    )

    if event:
        event.available_tickets += (
            booking.ticket_quantity
        )

    # Update booking status
    booking.booking_status = "CANCELLED"

    # Booking cancellation notification
    notification = Notification(
        user_id=user_id,
        title="Booking Cancelled",
        message=(
            f"Your booking #{booking.id} "
            f"has been cancelled."
        ),
        type="BOOKING",
        is_read=False
    )

    db.add(notification)

    db.commit()

    db.refresh(booking)

    return booking