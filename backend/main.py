import asyncio
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, SessionLocal, Base
import models

from routers.auth import router as auth_router
from routers.events import router as events_router
from routers.bookings import router as bookings_router
from routers.tickets import router as tickets_router
from routers.notifications import router as notifications_router
<<<<<<< HEAD
from routers.payments import router as payments_router
from routers.coupons import router as coupons_router
from routers.reviews import router as reviews_router
from routers.phase4 import router as phase4_router


Base.metadata.create_all(bind=engine)

# Lightweight SQLite migration for existing SmartEvent databases.
from sqlalchemy import inspect, text
with engine.begin() as connection:
    user_columns = {column["name"] for column in inspect(engine).get_columns("users")}
    if "location" not in user_columns:
        connection.execute(text("ALTER TABLE users ADD COLUMN location VARCHAR(200)"))
    if "profile_picture" not in user_columns:
        connection.execute(text("ALTER TABLE users ADD COLUMN profile_picture VARCHAR(500)"))
    if "role" not in user_columns:
        connection.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(30) NOT NULL DEFAULT 'USER'"))
    columns = {column["name"] for column in inspect(engine).get_columns("bookings")}
    if "coupon_id" not in columns:
        connection.execute(text("ALTER TABLE bookings ADD COLUMN coupon_id INTEGER"))
    if "discount_amount" not in columns:
        connection.execute(text("ALTER TABLE bookings ADD COLUMN discount_amount FLOAT NOT NULL DEFAULT 0"))
    if "final_amount" not in columns:
        connection.execute(text("ALTER TABLE bookings ADD COLUMN final_amount FLOAT NOT NULL DEFAULT 0"))
    connection.execute(text("UPDATE bookings SET final_amount = total_price WHERE final_amount = 0 AND total_price > 0"))

=======
from routers.organizer import router as organizer_router

Base.metadata.create_all(bind=engine)

>>>>>>> origin/main
os.makedirs(
    "static/qrcodes",
    exist_ok=True
)


async def event_reminder_checker():

    while True:

        try:

            db = SessionLocal()

            try:

                now = datetime.utcnow()
                reminder_limit = (
                    now + timedelta(hours=24)
                )

                upcoming_events = (
                    db.query(models.Event)
                    .filter(
                        models.Event.event_date > now,
                        models.Event.event_date <= reminder_limit
                    )
                    .all()
                )

                for event in upcoming_events:

                    bookings = (
                        db.query(models.Booking)
                        .filter(
                            models.Booking.event_id == event.id,
                            models.Booking.booking_status == "CONFIRMED"
                        )
                        .all()
                    )

                    for booking in bookings:

                        existing_notification = (
                            db.query(
                                models.Notification
                            )
                            .filter(
                                models.Notification.user_id
                                == booking.user_id,
                                models.Notification.type
                                == "EVENT",
                                models.Notification.title
                                == "Upcoming Event Reminder",
                                models.Notification.message.contains(
                                    f"'{event.title}'"
                                )
                            )
                            .first()
                        )

                        if existing_notification:
                            continue

                        notification = models.Notification(
                            user_id=booking.user_id,
                            title="Upcoming Event Reminder",
                            message=(
                                f"Your event '{event.title}' "
                                f"is happening within the next "
                                f"24 hours at {event.location}."
                            ),
                            type="EVENT",
                            is_read=False
                        )

                        db.add(notification)

                db.commit()

            finally:

                db.close()

        except Exception as error:

            print(
                "Event reminder checker error:",
                error
            )

        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):

    reminder_task = asyncio.create_task(
        event_reminder_checker()
    )

    yield

    reminder_task.cancel()

    try:
        await reminder_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="SmartEvent API",
    description="Event Discovery & Ticket Booking System",
    version="1.0.0",
    lifespan=lifespan
)


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(events_router)
app.include_router(bookings_router)
app.include_router(tickets_router)
app.include_router(notifications_router)
<<<<<<< HEAD
app.include_router(payments_router)
app.include_router(coupons_router)
app.include_router(reviews_router)
app.include_router(phase4_router)

=======
app.include_router(organizer_router)
>>>>>>> origin/main

@app.get("/")
def root():

    return {
        "message": "SmartEvent API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }