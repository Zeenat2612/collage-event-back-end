import csv
import io
import random
import time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User
from app.schemas.registration import RegistrationCreate, RegistrationResponse, RegistrationStatusUpdate, AttendeeItem
from app.dependencies import get_current_user

router = APIRouter(prefix="/registrations", tags=["Registrations"])

@router.get("/my", response_model=List[RegistrationResponse])
def get_my_registrations(
    email: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    target_email = None
    if current_user:
        target_email = current_user.email
    elif email:
        target_email = email
    else:
        target_email = "zeenat@college.edu"

    registrations = db.query(Registration).filter(
        (Registration.user_email == target_email) | (Registration.user_id == (current_user.id if current_user else 1))
    ).order_by(Registration.created_at.desc()).all()

    # Map to schema response
    results = []
    for r in registrations:
        results.append(RegistrationResponse(
            id=r.id,
            eventId=r.event_id,
            title=r.title,
            date=r.date,
            status=r.status,
            ticketCode=r.ticket_code,
            venue=r.venue or "",
            seat=r.seat or "General Admission - Assigned at Entry",
            userName=r.user_name,
            userEmail=r.user_email
        ))
    return results

@router.post("", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def create_registration(
    data: RegistrationCreate,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(Event.id == data.eventId).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    user_email = (current_user.email if current_user else data.userEmail) or "zeenat@college.edu"
    user_name = (current_user.name if current_user else data.userName) or "Zeenat"
    user_id = current_user.id if current_user else data.userId

    # Check for duplicate registration
    existing = db.query(Registration).filter(
        Registration.event_id == event.id,
        Registration.user_email == user_email,
        Registration.status != "Cancelled"
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"You are already registered for '{event.title}'."
        )

    # Check capacity
    if event.registered >= event.capacity:
        assigned_status = "Pending"
        seat_assigned = f"Waitlist #{event.registered - event.capacity + 1}"
    else:
        assigned_status = "Confirmed"
        seat_assigned = f"Row {chr(65 + (event.registered // 20))} - Seat {(event.registered % 20) + 1}"

    # Generate ticket code
    ticket_code = f"TCK-{random.randint(100000, 999999)}"
    reg_id = f"reg-{int(time.time() * 1000)}"

    new_reg = Registration(
        id=reg_id,
        event_id=event.id,
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        title=event.title,
        date=event.date,
        venue=event.venue,
        status=assigned_status,
        ticket_code=ticket_code,
        seat=seat_assigned
    )
    db.add(new_reg)

    # Increment registered counter
    event.registered += 1
    db.commit()
    db.refresh(new_reg)

    return RegistrationResponse(
        id=new_reg.id,
        eventId=new_reg.event_id,
        title=new_reg.title,
        date=new_reg.date,
        status=new_reg.status,
        ticketCode=new_reg.ticket_code,
        venue=new_reg.venue or "",
        seat=new_reg.seat or "General Admission",
        userName=new_reg.user_name,
        userEmail=new_reg.user_email
    )

@router.get("/pending", response_model=List[AttendeeItem])
def get_pending_registrations(db: Session = Depends(get_db)):
    regs = db.query(Registration).filter(Registration.status == "Pending").all()
    results = []
    for r in regs:
        results.append(AttendeeItem(
            id=r.id,
            name=r.user_name or "Attendee",
            event=r.title,
            date=r.date,
            status=r.status
        ))
    return results

@router.get("/event/{event_id}", response_model=List[RegistrationResponse])
def get_event_attendees(event_id: str, db: Session = Depends(get_db)):
    regs = db.query(Registration).filter(Registration.event_id == event_id).all()
    return [
        RegistrationResponse(
            id=r.id,
            eventId=r.event_id,
            title=r.title,
            date=r.date,
            status=r.status,
            ticketCode=r.ticket_code,
            venue=r.venue or "",
            seat=r.seat or "",
            userName=r.user_name,
            userEmail=r.user_email
        )
        for r in regs
    ]

@router.get("/event/{event_id}/export")
def export_attendees_csv(event_id: str, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    regs = db.query(Registration).filter(Registration.event_id == event_id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Ticket Code", "Name", "Email", "Event", "Date", "Venue", "Seat", "Status"])
    for r in regs:
        writer.writerow([r.ticket_code, r.user_name, r.user_email, r.title, r.date, r.venue, r.seat, r.status])

    output.seek(0)
    filename = f"attendees_{event.title.replace(' ', '_').lower()}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.patch("/{registration_id}/status", response_model=RegistrationResponse)
def update_registration_status(
    registration_id: str,
    status_update: RegistrationStatusUpdate,
    db: Session = Depends(get_db)
):
    reg = db.query(Registration).filter(Registration.id == registration_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found.")

    reg.status = status_update.status
    db.commit()
    db.refresh(reg)

    return RegistrationResponse(
        id=reg.id,
        eventId=reg.event_id,
        title=reg.title,
        date=reg.date,
        status=reg.status,
        ticketCode=reg.ticket_code,
        venue=reg.venue or "",
        seat=reg.seat or "",
        userName=reg.user_name,
        userEmail=reg.user_email
    )

@router.delete("/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_registration(registration_id: str, db: Session = Depends(get_db)):
    reg = db.query(Registration).filter(Registration.id == registration_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found.")

    event = db.query(Event).filter(Event.id == reg.event_id).first()
    if event and event.registered > 0:
        event.registered -= 1

    db.delete(reg)
    db.commit()
    return None
