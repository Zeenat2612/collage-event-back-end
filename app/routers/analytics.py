from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.event import Event
from app.models.registration import Registration
from app.models.user import User
from app.schemas.analytics import (
    OrganizerAnalyticsResponse, AdminAnalyticsResponse, StatCard,
    MonthlyRegistrationPoint, AdminRegistrationTrendPoint, CategoryDistributionPoint
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])

CATEGORY_COLORS = {
    "Technical": "#3b82f6",
    "Cultural": "#ec4899",
    "Workshop": "#10b981",
    "Sports": "#f59e0b",
    "Literary": "#8b5cf6",
    "Others": "#64748b"
}

@router.get("/organizer-stats", response_model=OrganizerAnalyticsResponse)
def get_organizer_stats(db: Session = Depends(get_db)):
    total_events = db.query(Event).count()
    total_registrations = db.query(Registration).count()
    ongoing_events = db.query(Event).filter(Event.status.ilike("ongoing")).count()
    upcoming_events = db.query(Event).filter(Event.status.ilike("upcoming")).count()

    stats = [
        StatCard(
            id="stat-events",
            title="Total Events",
            value=total_events,
            icon="Calendar",
            change="+2 this month",
            theme="blue"
        ),
        StatCard(
            id="stat-reg",
            title="Total Registrations",
            value=total_registrations,
            icon="Users",
            change="+18% from last week",
            theme="green"
        ),
        StatCard(
            id="stat-ongoing",
            title="Ongoing Events",
            value=ongoing_events,
            icon="CheckCircle2",
            change="Active right now",
            theme="amber"
        ),
        StatCard(
            id="stat-upcoming",
            title="Upcoming Events",
            value=upcoming_events,
            icon="Clock",
            change="Next in 5 days",
            theme="purple"
        )
    ]

    chart_data = [
        MonthlyRegistrationPoint(month="Jan", count=32),
        MonthlyRegistrationPoint(month="Feb", count=48),
        MonthlyRegistrationPoint(month="Mar", count=72),
        MonthlyRegistrationPoint(month="Apr", count=64),
        MonthlyRegistrationPoint(month="May", count=128),
        MonthlyRegistrationPoint(month="Jun", count=max(184, total_registrations))
    ]

    return OrganizerAnalyticsResponse(
        stats=stats,
        chartData=chart_data
    )

@router.get("/admin-stats", response_model=AdminAnalyticsResponse)
def get_admin_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    total_events = db.query(Event).count()
    total_registrations = db.query(Registration).count()
    upcoming_events = db.query(Event).filter(Event.status.ilike("upcoming")).count()

    stats = [
        StatCard(
            id="adm-users",
            title="Total Users",
            value=max(150, total_users),
            icon="Users",
            change="+12 new today",
            theme="blue"
        ),
        StatCard(
            id="adm-events",
            title="Total Events",
            value=max(25, total_events),
            icon="Calendar",
            change="Across 6 departments",
            theme="teal"
        ),
        StatCard(
            id="adm-registrations",
            title="Total Registrations",
            value=max(320, total_registrations),
            icon="UserCheck",
            change="+24% growth",
            theme="amber"
        ),
        StatCard(
            id="adm-upcoming",
            title="Upcoming Events",
            value=max(8, upcoming_events),
            icon="TrendingUp",
            change="Scheduled this month",
            theme="purple"
        )
    ]

    line_chart_data = [
        AdminRegistrationTrendPoint(month="Jan", registrations=24),
        AdminRegistrationTrendPoint(month="Feb", registrations=46),
        AdminRegistrationTrendPoint(month="Mar", registrations=38),
        AdminRegistrationTrendPoint(month="Apr", registrations=54),
        AdminRegistrationTrendPoint(month="May", registrations=76),
        AdminRegistrationTrendPoint(month="Jun", registrations=95)
    ]

    # Category distribution
    cat_counts = db.query(Event.category, func.count(Event.id)).group_by(Event.category).all()
    total_cat_events = sum(count for _, count in cat_counts) or 1
    
    category_data = []
    for cat, count in cat_counts:
        pct = round((count / total_cat_events) * 100)
        color = CATEGORY_COLORS.get(cat, "#3b82f6")
        category_data.append(CategoryDistributionPoint(
            name=cat,
            percentage=pct,
            color=color
        ))
    
    if not category_data:
        category_data = [
            CategoryDistributionPoint(name="Technical", percentage=40, color="#3b82f6"),
            CategoryDistributionPoint(name="Cultural", percentage=25, color="#ec4899"),
            CategoryDistributionPoint(name="Workshop", percentage=15, color="#10b981"),
            CategoryDistributionPoint(name="Sports", percentage=10, color="#f59e0b"),
            CategoryDistributionPoint(name="Others", percentage=10, color="#8b5cf6")
        ]

    return AdminAnalyticsResponse(
        stats=stats,
        lineChartData=line_chart_data,
        categoryData=category_data
    )
