<<<<<<< HEAD
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Event, Booking
from schemas import EventCreate, EventResponse
router = APIRouter(prefix="/api/v1/events", tags=["Events"])

@router.post("", response_model=EventResponse, status_code=201)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    event = Event(title=event_data.title, description=event_data.description, category=event_data.category, location=event_data.location, event_date=event_data.event_date, ticket_price=event_data.ticket_price, banner_image=event_data.banner_image, total_tickets=event_data.total_tickets, available_tickets=event_data.total_tickets)
    db.add(event); db.commit(); db.refresh(event); return event

@router.get("", response_model=list[EventResponse])
def get_events(category: str | None = Query(default=None), search: str | None = Query(default=None), location: str | None = Query(default=None), start_date: datetime | None = Query(default=None), end_date: datetime | None = Query(default=None), min_price: float | None = Query(default=None, ge=0), max_price: float | None = Query(default=None, ge=0), sort_by: str = Query(default="date", pattern="^(date|price|popularity)$"), db: Session = Depends(get_db)):
    query = db.query(Event)
    if category: query = query.filter(Event.category == category)
    if search: query = query.filter(Event.title.ilike(f"%{search}%"))
    if location: query = query.filter(Event.location.ilike(f"%{location}%"))
    if start_date: query = query.filter(Event.event_date >= start_date)
    if end_date: query = query.filter(Event.event_date <= end_date)
    if min_price is not None: query = query.filter(Event.ticket_price >= min_price)
    if max_price is not None: query = query.filter(Event.ticket_price <= max_price)
    if sort_by == "price": query = query.order_by(Event.ticket_price.asc())
    elif sort_by == "popularity": query = query.outerjoin(Booking, (Booking.event_id == Event.id) & (Booking.booking_status == "CONFIRMED")).group_by(Event.id).order_by(func.count(Booking.id).desc(), Event.event_date.asc())
    else: query = query.order_by(Event.event_date.asc())
    return query.all()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event: raise HTTPException(status_code=404, detail="Event not found")
    return event
=======

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Event, Booking
from schemas import (
    EventCreate,
    EventResponse,
    EventUpdate,
    BookingResponse
)
from security import require_role


router = APIRouter(
    prefix="/api/v1/events",
    tags=["Events"]
)


# =========================
# CREATE EVENT
# ORGANIZER ONLY
# =========================

@router.post(
    "",
    response_model=EventResponse,
    status_code=201
)
def create_event(
    event_data: EventCreate,
    current_user=Depends(require_role("ORGANIZER")),
    db: Session = Depends(get_db)
):

    new_event = Event(
        title=event_data.title,
        description=event_data.description,
        category=event_data.category,
        location=event_data.location,
        event_date=event_data.event_date,
        ticket_price=event_data.ticket_price,
        banner_image=event_data.banner_image,
        total_tickets=event_data.total_tickets,
        available_tickets=event_data.total_tickets,
        organizer_id=current_user.id,
        event_status="UPCOMING"
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event


# =========================
# GET ALL EVENTS
# PUBLIC
# =========================

@router.get(
    "",
    response_model=list[EventResponse]
)
def get_events(
    category: str | None = Query(default=None),
    search: str | None = Query(default=None),
    db: Session = Depends(get_db)
):

    query = db.query(Event)

    if category:
        query = query.filter(
            Event.category == category
        )

    if search:
        query = query.filter(
            Event.title.ilike(f"%{search}%")
        )

    return query.order_by(
        Event.event_date.asc()
    ).all()


# =========================
# GET SINGLE EVENT
# =========================

@router.get(
    "/{event_id}",
    response_model=EventResponse
)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


# =========================
# UPDATE EVENT
# ORGANIZER ONLY
# =========================

@router.put(
    "/{event_id}",
    response_model=EventResponse
)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user=Depends(require_role("ORGANIZER")),
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only modify your own events"
        )

    if event.event_status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Cancelled events cannot be updated"
        )

    update_data = event_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        if field == "total_tickets":

            tickets_sold = (
                event.total_tickets -
                event.available_tickets
            )

            if value < tickets_sold:
                raise HTTPException(
                    status_code=400,
                    detail="Total tickets cannot be less than tickets already sold"
                )

            event.available_tickets = value - tickets_sold

        setattr(event, field, value)

    db.commit()
    db.refresh(event)

    return event


# =========================
# CANCEL EVENT
# ORGANIZER ONLY
# =========================

@router.patch(
    "/{event_id}/cancel",
    response_model=EventResponse
)
def cancel_event(
    event_id: int,
    current_user=Depends(require_role("ORGANIZER")),
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only cancel your own events"
        )

    if event.event_status == "CANCELLED":
        raise HTTPException(
            status_code=400,
            detail="Event is already cancelled"
        )

    event.event_status = "CANCELLED"

    db.commit()
    db.refresh(event)

    return event


# =========================
# GET ORGANIZER EVENTS
# ORGANIZER ONLY
# =========================

@router.get(
    "/organizer/my-events",
    response_model=list[EventResponse]
)
def get_my_events(
    current_user=Depends(require_role("ORGANIZER")),
    db: Session = Depends(get_db)
):

    events = (
        db.query(Event)
        .filter(Event.organizer_id == current_user.id)
        .order_by(Event.event_date.asc())
        .all()
    )

    return events


# =========================
# GET BOOKINGS FOR ORGANIZER EVENT
# ORGANIZER ONLY
# =========================

@router.get(
    "/organizer/{event_id}/bookings",
    response_model=list[BookingResponse]
)
def get_event_bookings(
    event_id: int,
    current_user=Depends(require_role("ORGANIZER")),
    db: Session = Depends(get_db)
):

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    if event.organizer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only view bookings for your own events"
        )

    bookings = (
        db.query(Booking)
        .filter(Booking.event_id == event_id)
        .all()
    )

    return bookings

>>>>>>> origin/main
