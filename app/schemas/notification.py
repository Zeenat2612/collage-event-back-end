from typing import Optional
from pydantic import BaseModel

class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    time: str
    unread: bool

    class Config:
        from_attributes = True
