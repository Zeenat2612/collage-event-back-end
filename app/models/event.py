from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime
from app.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String(50), primary_key=True, index=True)  # e.g., 'evt-1', 'evt-2'
    title = Column(String(200), nullable=False, index=True)
    date = Column(String(100), nullable=False)  # e.g., '10 Jun 2025'
    time = Column(String(100), nullable=True, default="10:00 AM - 01:00 PM")
    venue = Column(String(200), nullable=False)
    date_venue = Column(String(250), nullable=True)  # Helper for Organizer list
    category = Column(String(50), nullable=False, default="Technical", index=True)
    category_color = Column(String(50), nullable=True, default="blue")
    image = Column(Text, nullable=True, default="https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80")
    description = Column(Text, nullable=True)
    speaker = Column(String(200), nullable=True)
    organizer = Column(String(150), nullable=True, default="College Committee")
    organizer_id = Column(Integer, nullable=True)
    capacity = Column(Integer, nullable=False, default=100)
    registered = Column(Integer, nullable=False, default=0)
    status = Column(String(50), nullable=False, default="Upcoming")  # 'Ongoing', 'Upcoming', 'Draft', 'Completed'
    created_at = Column(DateTime, default=datetime.utcnow)
