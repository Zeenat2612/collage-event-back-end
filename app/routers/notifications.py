from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=List[NotificationResponse])
def get_notifications(db: Session = Depends(get_db)):
    notifs = db.query(Notification).order_by(Notification.created_at.desc()).all()
    return [
        NotificationResponse(
            id=n.id,
            title=n.title,
            message=n.message,
            time=n.time_ago or "Recently",
            unread=n.unread
        )
        for n in notifs
    ]

@router.patch("/read-all")
def mark_all_as_read(db: Session = Depends(get_db)):
    db.query(Notification).update({Notification.unread: False})
    db.commit()
    return {"message": "All notifications marked as read."}

@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(notification_id: str, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found.")
    notif.unread = False
    db.commit()
    db.refresh(notif)
    return NotificationResponse(
        id=notif.id,
        title=notif.title,
        message=notif.message,
        time=notif.time_ago or "Recently",
        unread=notif.unread
    )
