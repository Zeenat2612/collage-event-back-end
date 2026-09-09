import time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventUpdate, EventResponse

router = APIRouter(prefix="/events", tags=["Events"])

CATEGORIES_LIST = [
    "Technical",
    "Cultural",
    "Workshop",
    "Sports",
    "Literary",
    "Others"
]

@router.get("/categories", response_model=List[str])
def get_categories():
    return CATEGORIES_LIST

@router.get("", response_model=List[EventResponse])
def get_events(
    category: Optional[str] = Query(None, description="Filter by event category"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by event status"),
    search: Optional[str] = Query(None, description="Search query across title, venue, category"),
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if category and category.lower() != "all":
        query = query.filter(Event.category.ilike(category))

    if status_filter and status_filter.lower() != "all":
        query = query.filter(Event.status.ilike(status_filter))

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            (Event.title.ilike(term)) |
            (Event.venue.ilike(term)) |
            (Event.category.ilike(term)) |
            (Event.description.ilike(term))
        )

    events = query.order_by(Event.created_at.desc()).all()
    return events

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found."
        )
    return event

@router.post("", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    # Generate unique ID
    event_id = f"evt-{int(time.time() * 1000)}"

    # Parse date and venue if dateVenue provided
    date_val = event_data.date or "TBD"
    venue_val = event_data.venue or "Campus Ground"
    if event_data.dateVenue and " | " in event_data.dateVenue:
        parts = event_data.dateVenue.split(" | ", 1)
        date_val = parts[0].strip()
        venue_val = parts[1].strip()
    elif event_data.dateVenue:
        date_val = event_data.dateVenue

    capacity_val = event_data.maxCapacity or event_data.capacity or 100

    new_event = Event(
        id=event_id,
        title=event_data.title,
        date=date_val,
        time=event_data.time or "10:00 AM - 01:00 PM",
        venue=venue_val,
        date_venue=f"{date_val} | {venue_val}",
        category=event_data.category,
        category_color=event_data.categoryColor or "blue",
        image=event_data.image or "https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80",
        description=event_data.description or "",
        speaker=event_data.speaker or "Guest Speaker",
        organizer=event_data.organizer or "Event Club",
        capacity=capacity_val,
        registered=0,
        status=event_data.status or "Upcoming"
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: str, event_data: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found."
        )

    if event_data.title is not None:
        event.title = event_data.title
    if event_data.category is not None:
        event.category = event_data.category
    if event_data.status is not None:
        event.status = event_data.status
    if event_data.description is not None:
        event.description = event_data.description
    if event_data.speaker is not None:
        event.speaker = event_data.speaker
    if event_data.image is not None:
        event.image = event_data.image

    if event_data.maxCapacity is not None:
        event.capacity = event_data.maxCapacity
    elif event_data.capacity is not None:
        event.capacity = event_data.capacity

    if event_data.dateVenue:
        if " | " in event_data.dateVenue:
            p = event_data.dateVenue.split(" | ", 1)
            event.date = p[0].strip()
            event.venue = p[1].strip()
        else:
            event.date = event_data.dateVenue
        event.date_venue = event_data.dateVenue
    else:
        if event_data.date is not None:
            event.date = event_data.date
        if event_data.venue is not None:
            event.venue = event_data.venue
        event.date_venue = f"{event.date} | {event.venue}"

    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id '{event_id}' not found."
        )
    db.delete(event)
    db.commit()
    return None
