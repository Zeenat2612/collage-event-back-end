from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")  # 'user', 'organizer', 'admin'
    department = Column(String(100), nullable=True, default="")
    status = Column(String(50), nullable=False, default="Active")  # 'Active', 'Inactive'
    created_at = Column(DateTime, default=datetime.utcnow)
