<<<<<<< HEAD
=======

>>>>>>> origin/main
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# =========================
# USER MODEL
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
<<<<<<< HEAD
    created_at = Column(DateTime, default=datetime.utcnow)
    location = Column(String(200), nullable=True)
    profile_picture = Column(String(500), nullable=True)
    role = Column(String(30), nullable=False, default="USER")
=======

    # Phase 2: Role
    role = Column(
        String(20),
        default="USER",
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)
>>>>>>> origin/main

    bookings = relationship(
        "Booking",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

<<<<<<< HEAD
=======
    organized_events = relationship(
        "Event",
        back_populates="organizer"
    )

>>>>>>> origin/main

# =========================
# EVENT MODEL
# =========================

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
<<<<<<< HEAD
=======

>>>>>>> origin/main
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    location = Column(String(200), nullable=False)
    event_date = Column(DateTime, nullable=False)
    ticket_price = Column(Float, nullable=False)
    banner_image = Column(String(500), nullable=True)

    total_tickets = Column(Integer, nullable=False)
    available_tickets = Column(Integer, nullable=False)

<<<<<<< HEAD
    created_at = Column(DateTime, default=datetime.utcnow)

=======
    # Phase 2: Organizer
    organizer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    # Phase 2: Event status
    event_status = Column(
        String(20),
        default="UPCOMING",
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    organizer = relationship(
        "User",
        back_populates="organized_events"
    )

>>>>>>> origin/main
    bookings = relationship(
        "Booking",
        back_populates="event"
    )


# =========================
# BOOKING MODEL
# =========================

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    ticket_quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
<<<<<<< HEAD
    coupon_id = Column(Integer, ForeignKey("coupons.id"), nullable=True)
    discount_amount = Column(Float, nullable=False, default=0.0)
    final_amount = Column(Float, nullable=False, default=0.0)
=======
>>>>>>> origin/main

    booking_status = Column(
        String(20),
        default="PENDING",
        nullable=False
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="bookings"
    )

    event = relationship(
        "Event",
        back_populates="bookings"
    )

    ticket = relationship(
        "Ticket",
        back_populates="booking",
        uselist=False,
        cascade="all, delete-orphan"
    )


# =========================
# TICKET MODEL
# =========================

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    booking_id = Column(
        Integer,
        ForeignKey("bookings.id"),
        unique=True,
        nullable=False
    )

    ticket_code = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    qr_code_url = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    booking = relationship(
        "Booking",
        back_populates="ticket"
    )


# =========================
# NOTIFICATION MODEL
# =========================

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)

    type = Column(
        String(20),
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="notifications"
    )
<<<<<<< HEAD

# =========================
# PAYMENT MODEL
# =========================
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, index=True)
    payment_method = Column(String(30), nullable=False)
    payment_status = Column(String(20), nullable=False, default="PENDING")
    transaction_id = Column(String(100), unique=True, nullable=True)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# COUPON MODEL
# =========================
class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    coupon_code = Column(String(50), unique=True, nullable=False, index=True)
    discount_type = Column(String(20), nullable=False)
    discount_value = Column(Float, nullable=False)
    minimum_booking_amount = Column(Float, nullable=False, default=0)
    expiry_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=False, default=1)
    usage_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# REVIEW MODEL
# =========================
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


# =========================
# PHASE 4: WISHLIST AND EVENT UPDATES
# =========================
class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EventUpdate(Base):
    __tablename__ = "event_updates"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    message = Column(Text, nullable=False)
    is_important = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class EventView(Base):
    __tablename__ = "event_views"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False, index=True)
    viewed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
=======
>>>>>>> origin/main
