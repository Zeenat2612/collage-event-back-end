from typing import Optional
from pydantic import BaseModel, computed_field

class EventBase(BaseModel):
    title: str
    date: str
    time: Optional[str] = "10:00 AM - 01:00 PM"
    venue: str
    category: str = "Technical"
    categoryColor: Optional[str] = "blue"
    image: Optional[str] = "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80"
    description: Optional[str] = ""
    speaker: Optional[str] = ""
    organizer: Optional[str] = "College Committee"
    capacity: int = 100
    status: str = "Upcoming"

class EventCreate(BaseModel):
    title: str
    date: Optional[str] = None
    time: Optional[str] = "10:00 AM - 01:00 PM"
    venue: Optional[str] = None
    dateVenue: Optional[str] = None  # e.g., '10 Jun 2025 | Main Auditorium'
    category: str = "Technical"
    categoryColor: Optional[str] = "blue"
    image: Optional[str] = "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80"
    description: Optional[str] = ""
    speaker: Optional[str] = ""
    organizer: Optional[str] = "Event Club"
    capacity: Optional[int] = 100
    maxCapacity: Optional[int] = None
    status: str = "Upcoming"

class EventUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    venue: Optional[str] = None
    dateVenue: Optional[str] = None
    category: Optional[str] = None
    categoryColor: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    speaker: Optional[str] = None
    organizer: Optional[str] = None
    capacity: Optional[int] = None
    maxCapacity: Optional[int] = None
    status: Optional[str] = None

class EventResponse(BaseModel):
    id: str
    title: str
    date: str
    time: Optional[str] = ""
    venue: str
    category: str
    categoryColor: Optional[str] = "blue"
    image: Optional[str] = ""
    description: Optional[str] = ""
    speaker: Optional[str] = ""
    organizer: Optional[str] = ""
    capacity: int
    registered: int
    status: str

    @computed_field
    def dateVenue(self) -> str:
        return f"{self.date} | {self.venue}"

    @computed_field
    def maxCapacity(self) -> int:
        return self.capacity

    @computed_field
    def registrations(self) -> int:
        return self.registered

    class Config:
        from_attributes = True
