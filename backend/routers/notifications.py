<<<<<<< HEAD
from fastapi import APIRouter, Depends, HTTPException
=======
from fastapi import APIRouter, Depends, HTTPException, status
>>>>>>> origin/main
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models import Notification
from schemas import NotificationResponse
from security import bearer_scheme, get_current_user_id


router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notifications"]
)


<<<<<<< HEAD
# Get all notifications
=======
# =========================
# GET MY NOTIFICATIONS
# =========================

>>>>>>> origin/main
@router.get(
    "",
    response_model=list[NotificationResponse]
)
def get_my_notifications(
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

    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id
        )
        .order_by(
            Notification.created_at.desc()
        )
        .all()
    )

    return notifications


<<<<<<< HEAD
# Get unread notification count
=======
# =========================
# GET UNREAD COUNT
# =========================

>>>>>>> origin/main
@router.get(
    "/unread-count"
)
def get_unread_count(
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

    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        .count()
    )

    return {
        "unread_count": count
    }


<<<<<<< HEAD
# Mark notification as read
@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse
=======
# =========================
# MARK NOTIFICATION AS READ
# =========================

@router.patch(
    "/{notification_id}/read"
>>>>>>> origin/main
)
def mark_notification_as_read(
    notification_id: int,
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

    notification = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
        .first()
    )

    if not notification:
        raise HTTPException(
<<<<<<< HEAD
            status_code=404,
=======
            status_code=status.HTTP_404_NOT_FOUND,
>>>>>>> origin/main
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

<<<<<<< HEAD
    return notification

@router.patch("/read-all")
def mark_all_as_read(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    user_id = get_current_user_id(credentials)
    db.query(Notification).filter(Notification.user_id == user_id, Notification.is_read == False).update({Notification.is_read: True})
    db.commit()
    return {"message": "All notifications marked as read"}
=======
    return notification
>>>>>>> origin/main
