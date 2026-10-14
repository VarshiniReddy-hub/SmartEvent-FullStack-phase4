from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Booking, Review, Event
from schemas import ReviewCreate, ReviewUpdate, ReviewResponse
from security import bearer_scheme, get_current_user_id
router = APIRouter(prefix="/api/v1/reviews", tags=["Reviews"])

@router.post("", response_model=ReviewResponse, status_code=201)
def create_review(data: ReviewCreate, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    uid = get_current_user_id(credentials)
    event = db.query(Event).filter(Event.id == data.event_id).first()
    if not event: raise HTTPException(status_code=404, detail="Event not found")
    if event.event_date > datetime.utcnow(): raise HTTPException(status_code=400, detail="Reviews are available after the event")
    attended = db.query(Booking).filter(Booking.user_id == uid, Booking.event_id == data.event_id, Booking.booking_status == "CONFIRMED").first()
    if not attended: raise HTTPException(status_code=403, detail="Only users with a confirmed booking can review this event")
    if db.query(Review).filter(Review.user_id == uid, Review.event_id == data.event_id).first(): raise HTTPException(status_code=409, detail="You have already reviewed this event")
    review = Review(user_id=uid, event_id=data.event_id, rating=data.rating, review_text=data.review_text.strip())
    db.add(review); db.commit(); db.refresh(review); return review

@router.get("/event/{event_id}")
def event_reviews(event_id: int, db: Session = Depends(get_db)):
    if not db.query(Event).filter(Event.id == event_id).first(): raise HTTPException(status_code=404, detail="Event not found")
    reviews = db.query(Review).filter(Review.event_id == event_id).order_by(Review.created_at.desc()).all()
    average = db.query(func.avg(Review.rating)).filter(Review.event_id == event_id).scalar()
    return {"average_rating": round(float(average), 2) if average is not None else None, "review_count": len(reviews), "reviews": reviews}

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_id: int, data: ReviewUpdate, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    uid = get_current_user_id(credentials); review = db.query(Review).filter(Review.id == review_id).first()
    if not review: raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != uid: raise HTTPException(status_code=403, detail="You can only edit your own review")
    review.rating = data.rating; review.review_text = data.review_text.strip(); db.commit(); db.refresh(review); return review

@router.delete("/{review_id}")
def delete_review(review_id: int, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    uid = get_current_user_id(credentials); review = db.query(Review).filter(Review.id == review_id).first()
    if not review: raise HTTPException(status_code=404, detail="Review not found")
    if review.user_id != uid: raise HTTPException(status_code=403, detail="You can only delete your own review")
    db.delete(review); db.commit(); return {"message": "Review deleted"}
