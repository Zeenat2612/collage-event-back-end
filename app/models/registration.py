from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(String(50), primary_key=True, index=True)  # e.g., 'reg-1'
    event_id = Column(String(50), nullable=False, index=True)
    user_id = Column(Integer, nullable=True, index=True)
    user_name = Column(String(100), nullable=True)
    user_email = Column(String(150), nullable=True)
    title = Column(String(200), nullable=False)
    date = Column(String(100), nullable=False)
    venue = Column(String(200), nullable=True)
    status = Column(String(50), nullable=False, default="Confirmed")  # 'Confirmed', 'Pending', 'Declined'
    ticket_code = Column(String(50), nullable=False, unique=True)  # 'TCK-XXXXXX'
    seat = Column(String(100), nullable=True, default="General Admission - Assigned at Entry")
    created_at = Column(DateTime, default=datetime.utcnow)
