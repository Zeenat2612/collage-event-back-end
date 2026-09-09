from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(50), primary_key=True, index=True)
    user_id = Column(Integer, nullable=True, index=True)  # None means global
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    time_ago = Column(String(50), nullable=True, default="Just now")
    unread = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
