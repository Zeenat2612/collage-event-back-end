from typing import Optional
from pydantic import BaseModel, computed_field

class RegistrationCreate(BaseModel):
    eventId: str
    userId: Optional[int] = None
    userName: Optional[str] = None
    userEmail: Optional[str] = None

class RegistrationStatusUpdate(BaseModel):
    status: str  # 'Confirmed', 'Pending', 'Declined', 'Cancelled'

class RegistrationResponse(BaseModel):
    id: str
    eventId: str
    title: str
    date: str
    status: str
    ticketCode: str
    venue: Optional[str] = ""
    seat: Optional[str] = "General Admission - Assigned at Entry"
    userName: Optional[str] = None
    userEmail: Optional[str] = None

    class Config:
        from_attributes = True

class AttendeeItem(BaseModel):
    id: str
    name: str
    event: str
    date: str
    status: str
