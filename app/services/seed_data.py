import logging
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.event import Event
from app.models.registration import Registration
from app.models.notification import Notification
from app.services.auth_service import get_password_hash

logger = logging.getLogger("uvicorn")

def seed_database(db: Session):
    # Check if data already seeded
    existing_user = db.query(User).filter(User.email == "zeenat@college.edu").first()
    if existing_user:
        logger.info("Database already seeded with demo records.")
        return

    logger.info("Seeding database with initial users, events, and registrations...")

    # 1. Seed Users
    users = [
        User(
            name="Zeenat",
            email="zeenat@college.edu",
            hashed_password=get_password_hash("user123"),
            role="user",
            department="Computer Science",
            status="Active"
        ),
        User(
            name="Event Club",
            email="organizer@college.edu",
            hashed_password=get_password_hash("org123"),
            role="organizer",
            department="Cultural Committee",
            status="Active"
        ),
        User(
            name="Admin",
            email="admin@college.edu",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            department="System Administration",
            status="Active"
        ),
        User(
            name="Aarav Sharma",
            email="aarav@gmail.com",
            hashed_password=get_password_hash("user123"),
            role="user",
            department="Information Technology",
            status="Active"
        ),
        User(
            name="Priya Verma",
            email="priya@gmail.com",
            hashed_password=get_password_hash("user123"),
            role="user",
            department="Electronics",
            status="Active"
        ),
        User(
            name="Rohan Patel",
            email="rohan@gmail.com",
            hashed_password=get_password_hash("org123"),
            role="organizer",
            department="Tech Society",
            status="Active"
        ),
        User(
            name="Sneha Gupta",
            email="sneha@gmail.com",
            hashed_password=get_password_hash("user123"),
            role="user",
            department="Mechanical",
            status="Inactive"
        ),
        User(
            name="Vikram Malhotra",
            email="vikram@gmail.com",
            hashed_password=get_password_hash("org123"),
            role="organizer",
            department="Sports Council",
            status="Active"
        )
    ]
    db.add_all(users)
    db.commit()

    # Retrieve student id for registrations
    zeenat = db.query(User).filter(User.email == "zeenat@college.edu").first()
    zeenat_id = zeenat.id if zeenat else 1

    # 2. Seed Events
    events = [
        Event(
            id="evt-1",
            title="Tech Talk 2025",
            date="10 Jun 2025",
            time="10:00 AM - 01:00 PM",
            venue="Main Auditorium",
            date_venue="10 Jun 2025 | Main Auditorium",
            category="Technical",
            category_color="blue",
            image="https://images.unsplash.com/photo-1540575467063-178a50c2df87?auto=format&fit=crop&w=800&q=80",
            description="Explore the frontiers of Artificial Intelligence, Quantum Computing, and Next-Gen Software Engineering with top industry thought leaders.",
            speaker="Dr. Arvind Rao, Principal AI Scientist",
            organizer="CS Department",
            capacity=300,
            registered=245,
            status="Ongoing"
        ),
        Event(
            id="evt-2",
            title="Cultural Fest",
            date="15 Jun 2025",
            time="04:30 PM - 10:00 PM",
            venue="College Ground",
            date_venue="15 Jun 2025 | College Ground",
            category="Cultural",
            category_color="rose",
            image="https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=800&q=80",
            description="An electrifying celebration of music, dance, theater, and artistic expression featuring inter-collegiate band performances.",
            speaker="College Cultural Committee",
            organizer="Arts Club",
            capacity=1200,
            registered=980,
            status="Draft"
        ),
        Event(
            id="evt-3",
            title="AI Workshop",
            date="20 Jun 2025",
            time="09:30 AM - 04:00 PM",
            venue="Seminar Hall",
            date_venue="20 Jun 2025 | Seminar Hall",
            category="Workshop",
            category_color="emerald",
            image="https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=800&q=80",
            description="Hands-on masterclass building production-ready LLM agents, RAG architectures, and fine-tuning open-source models.",
            speaker="Prof. Neha Verma, AI Lab Director",
            organizer="Tech Society",
            capacity=80,
            registered=76,
            status="Upcoming"
        ),
        Event(
            id="evt-4",
            title="Sports Meet",
            date="25 Jun 2025",
            time="07:30 AM - 05:00 PM",
            venue="Sports Complex",
            date_venue="25 Jun 2025 | Sports Complex",
            category="Sports",
            category_color="amber",
            image="https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=800&q=80",
            description="Annual intra-university track and field championships, football tournament, and badminton singles.",
            speaker="Sports Council",
            organizer="Sports Club",
            capacity=500,
            registered=410,
            status="Ongoing"
        ),
        Event(
            id="evt-5",
            title="Literary Symposium",
            date="28 Jun 2025",
            time="11:00 AM - 03:00 PM",
            venue="Auditorium B",
            date_venue="28 Jun 2025 | Auditorium B",
            category="Literary",
            category_color="purple",
            image="https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=800&q=80",
            description="Debate championship, poetry slam, and author interaction on contemporary literature and creative writing.",
            speaker="Literary Circle",
            organizer="Literary Club",
            capacity=150,
            registered=110,
            status="Upcoming"
        )
    ]
    db.add_all(events)
    db.commit()

    # 3. Seed Registrations
    registrations = [
        Registration(
            id="reg-1",
            event_id="evt-1",
            user_id=zeenat_id,
            user_name="Zeenat",
            user_email="zeenat@college.edu",
            title="Tech Talk 2025",
            date="10 Jun 2025",
            venue="Main Auditorium",
            status="Confirmed",
            ticket_code="TCK-892401",
            seat="Row C - Seat 14"
        ),
        Registration(
            id="reg-2",
            event_id="evt-3",
            user_id=zeenat_id,
            user_name="Zeenat",
            user_email="zeenat@college.edu",
            title="AI Workshop",
            date="20 Jun 2025",
            venue="Seminar Hall",
            status="Pending",
            ticket_code="TCK-441029",
            seat="Waitlist #3"
        ),
        Registration(
            id="reg-3",
            event_id="evt-4",
            user_id=zeenat_id,
            user_name="Zeenat",
            user_email="zeenat@college.edu",
            title="Sports Meet",
            date="25 Jun 2025",
            venue="Sports Complex",
            status="Confirmed",
            ticket_code="TCK-673199",
            seat="Track 4 - Bib #108"
        ),
        Registration(
            id="reg-4",
            event_id="evt-3",
            user_id=4,
            user_name="Ananya Roy",
            user_email="ananya@college.edu",
            title="AI Workshop",
            date="20 Jun 2025",
            venue="Seminar Hall",
            status="Pending",
            ticket_code="TCK-554102",
            seat="Waitlist #4"
        ),
        Registration(
            id="reg-5",
            event_id="evt-1",
            user_id=5,
            user_name="Rahul Joshi",
            user_email="rahul@college.edu",
            title="Tech Talk 2025",
            date="10 Jun 2025",
            venue="Main Auditorium",
            status="Pending",
            ticket_code="TCK-712830",
            seat="Row D - Seat 5"
        ),
        Registration(
            id="reg-6",
            event_id="evt-2",
            user_id=6,
            user_name="Kavita Nair",
            user_email="kavita@college.edu",
            title="Cultural Fest",
            date="15 Jun 2025",
            venue="College Ground",
            status="Pending",
            ticket_code="TCK-990184",
            seat="General Area"
        )
    ]
    db.add_all(registrations)
    db.commit()

    # 4. Seed Notifications
    notifications = [
        Notification(
            id="notif-1",
            user_id=zeenat_id,
            title="Registration Confirmed",
            message="Your seat for Tech Talk 2025 has been confirmed.",
            time_ago="10m ago",
            unread=True
        ),
        Notification(
            id="notif-2",
            user_id=zeenat_id,
            title="Event Reminder",
            message="AI Workshop starts in 2 days at Seminar Hall.",
            time_ago="2h ago",
            unread=True
        ),
        Notification(
            id="notif-3",
            user_id=None,
            title="New Event Published",
            message="Cultural Fest 2025 schedule has been updated.",
            time_ago="1d ago",
            unread=False
        )
    ]
    db.add_all(notifications)
    db.commit()

    logger.info("Database seeding completed successfully.")
