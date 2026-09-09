from sqlalchemy import Column, Integer, String
from app.database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    event_id = Column(String(50), nullable=False, index=True)
