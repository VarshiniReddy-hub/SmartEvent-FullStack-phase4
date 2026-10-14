import json
from sqlalchemy import func, or_
from ai_service import get_ai_response
from openai import OpenAIError
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from database import get_db, SessionLocal
from models import User, Event, Booking, Wishlist, EventUpdate, EventView
from security import bearer_scheme, get_current_user_id

router = APIRouter(prefix="/api/v1", tags=["Phase 4"])

def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    user_id = get_current_user_id(credentials)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

class ProfileUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=100)
    location: Optional[str] = Field(default=None, max_length=200)
    profile_picture: Optional[str] = Field(default=None, max_length=500)

class UpdateCreate(BaseModel):
    message: str = Field(min_length=2, max_length=2000)
    is_important: bool = False

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)

class ConnectionManager:
    def __init__(self):
        self.connections = {}
    async def connect(self, event_id, websocket):
        await websocket.accept()
        self.connections.setdefault(event_id, []).append(websocket)
    def disconnect(self, event_id, websocket):
        if event_id in self.connections and websocket in self.connections[event_id]:
            self.connections[event_id].remove(websocket)
    async def broadcast(self, event_id, data):
        for socket in list(self.connections.get(event_id, [])):
            try:
                await socket.send_json(data)
            except Exception:
                self.disconnect(event_id, socket)

manager = ConnectionManager()

@router.websocket("/ws/events/{event_id}/availability")
async def availability_socket(websocket: WebSocket, event_id: int):
    db = SessionLocal()
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            await websocket.close(code=1008)
            return
        await manager.connect(event_id, websocket)
        await websocket.send_json({"event_id": event.id, "available_tickets": event.available_tickets})
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(event_id, websocket)
    finally:
        db.close()

@router.get("/events/{event_id}/availability")
def ticket_availability(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event: raise HTTPException(404, "Event not found")
    return {"event_id": event.id, "available_tickets": event.available_tickets, "sold_out": event.available_tickets <= 0}

@router.post("/events/{event_id}/view", status_code=201)
def record_event_view(event_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event: raise HTTPException(404, "Event not found")
    db.add(EventView(user_id=user.id, event_id=event_id))
    db.commit()
    return {"message": "Event view recorded"}

@router.get("/recommendations")
def recommendations(user: User = Depends(current_user), db: Session = Depends(get_db)):
    viewed_ids = [x[0] for x in db.query(EventView.event_id).filter(EventView.user_id == user.id).all()]
    booked_categories = [x[0] for x in db.query(Event.category).join(Booking, Booking.event_id == Event.id).filter(Booking.user_id == user.id).distinct().all()]
    query = db.query(Event).filter(Event.event_date >= datetime.utcnow(), Event.available_tickets > 0)
    if booked_categories:
        query = query.filter(Event.category.in_(booked_categories))
    events = query.order_by(Event.available_tickets.asc(), Event.event_date.asc()).limit(8).all()
    if not events:
        events = db.query(Event).filter(Event.event_date >= datetime.utcnow(), Event.available_tickets > 0).order_by(Event.event_date.asc()).limit(8).all()
    trending = db.query(Event).outerjoin(Booking, Booking.event_id == Event.id).filter(Event.event_date >= datetime.utcnow()).group_by(Event.id).order_by(func.count(Booking.id).desc()).limit(8).all()
    return {"recommended": events, "trending": trending, "based_on_views": len(viewed_ids)}

@router.get("/wishlist")
def get_wishlist(user: User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(Event).join(Wishlist, Wishlist.event_id == Event.id).filter(Wishlist.user_id == user.id).order_by(Wishlist.created_at.desc()).all()

@router.post("/wishlist/{event_id}", status_code=201)
def add_wishlist(event_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if not db.query(Event).filter(Event.id == event_id).first(): raise HTTPException(404, "Event not found")
    saved = db.query(Wishlist).filter(Wishlist.user_id == user.id, Wishlist.event_id == event_id).first()
    if saved: return {"message": "Event already saved"}
    db.add(Wishlist(user_id=user.id, event_id=event_id)); db.commit()
    return {"message": "Event added to wishlist"}

@router.delete("/wishlist/{event_id}")
def remove_wishlist(event_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    saved = db.query(Wishlist).filter(Wishlist.user_id == user.id, Wishlist.event_id == event_id).first()
    if not saved: raise HTTPException(404, "Wishlist item not found")
    db.delete(saved); db.commit()
    return {"message": "Event removed from wishlist"}

@router.get("/events/{event_id}/updates")
def list_event_updates(event_id: int, db: Session = Depends(get_db)):
    if not db.query(Event).filter(Event.id == event_id).first(): raise HTTPException(404, "Event not found")
    return db.query(EventUpdate).filter(EventUpdate.event_id == event_id).order_by(EventUpdate.created_at.desc()).all()

@router.post("/events/{event_id}/updates", status_code=201)
def create_event_update(event_id: int, payload: UpdateCreate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if user.role not in ("ADMIN", "ORGANIZER"):
        raise HTTPException(403, "Only admins or organizers can post event updates")
    if not db.query(Event).filter(Event.id == event_id).first(): raise HTTPException(404, "Event not found")
    item = EventUpdate(event_id=event_id, message=payload.message, is_important=payload.is_important)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.patch("/profile")
def update_profile(payload: ProfileUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    if payload.username is not None:
        other = db.query(User).filter(User.username == payload.username, User.id != user.id).first()
        if other: raise HTTPException(409, "Username already exists")
        user.username = payload.username
    if payload.location is not None: user.location = payload.location
    if payload.profile_picture is not None: user.profile_picture = payload.profile_picture
    db.commit(); db.refresh(user)
    return {"id": user.id, "username": user.username, "email": user.email, "location": user.location, "profile_picture": user.profile_picture}

@router.get("/profile/summary")
def profile_summary(user: User = Depends(current_user), db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.user_id == user.id).all()
    return {"user": {"id": user.id, "username": user.username, "email": user.email, "location": user.location, "profile_picture": user.profile_picture}, "booking_count": len(bookings), "confirmed_bookings": sum(1 for b in bookings if b.booking_status == "CONFIRMED"), "tickets_booked": sum(b.ticket_quantity for b in bookings), "total_spent": round(sum((b.final_amount or b.total_price) for b in bookings if b.booking_status == "CONFIRMED"), 2)}

@router.post("/chat")
def chat(payload: ChatRequest, user: User = Depends(current_user), db: Session = Depends(get_db)):
    text = payload.message.lower()
    if any(word in text for word in ("my booking", "my ticket", "booking status")):
        rows = db.query(Booking, Event).join(Event, Booking.event_id == Event.id).filter(Booking.user_id == user.id).order_by(Booking.created_at.desc()).limit(10).all()
        items = [{"booking_id": b.id, "event": e.title, "status": b.booking_status, "quantity": b.ticket_quantity} for b,e in rows]
        return {"reply": f"You have {len(items)} recent booking(s).", "bookings": items, "suggestions": ["Trending events", "Find music events"]}
    query = db.query(Event).filter(Event.event_date >= datetime.utcnow(), Event.available_tickets > 0)
    if "music" in text: query = query.filter(Event.category.ilike("%music%"))
    elif "tech" in text or "technology" in text: query = query.filter(Event.category.ilike("%tech%"))
    elif "sport" in text: query = query.filter(Event.category.ilike("%sport%"))
    if "near me" in text and getattr(user, "location", None): query = query.filter(Event.location.ilike(f"%{user.location}%"))
    if "trending" in text or "popular" in text:
        events = db.query(Event).outerjoin(Booking, Booking.event_id == Event.id).filter(Event.event_date >= datetime.utcnow()).group_by(Event.id).order_by(func.count(Booking.id).desc()).limit(5).all()
    else:
        events = query.order_by(Event.event_date.asc()).limit(5).all()
    if events:
        return {"reply": "Here are some events that may match your request.", "events": [{"id": e.id, "title": e.title, "category": e.category, "location": e.location, "event_date": e.event_date.isoformat(), "ticket_price": e.ticket_price, "available_tickets": e.available_tickets} for e in events], "suggestions": ["Trending events", "My bookings", "Help with tickets"]}
    return {"reply": "I couldn't find matching upcoming events. Try a different category, location, or date. For ticket issues, open My Bookings and check the booking status.", "suggestions": ["Trending events", "My bookings", "Help with tickets"]}
