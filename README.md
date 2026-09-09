# College Event Management System - FastAPI Backend

A production-ready, modular REST API backend built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL**, tailored specifically for the College Event Management System frontend.

---

## Features

- **Multi-Role Authentication**: JWT-based authentication for Students (`user`), Event Organizers (`organizer`), and System Administrators (`admin`).
- **PostgreSQL Database Support**: Enterprise-ready database pooling with automatic schema generation and instant mock-data seeding.
- **Resilient Fallback**: Automatic fallback to SQLite if PostgreSQL is not yet started, enabling immediate zero-friction local development.
- **Event Lifecycle Management**: Full CRUD for events with category filtering, search, attendee tracking, and capacity enforcement.
- **Automated Digital Tickets**: Generates verifiable digital ticket codes (`TCK-XXXXXX`), seat allocation, and attendee roster CSV export.
- **Interactive Dashboards & Analytics**: Endpoints delivering metrics, monthly registration trends, category distributions, and organizer stats.
- **CORS Configured**: Pre-configured for seamless connection with Vite React frontend (`http://localhost:5173`).

---

## Pre-configured Demo Accounts

On initial launch, the system automatically creates the following demo accounts matching the frontend:

| Role | Email | Password | Name |
| :--- | :--- | :--- | :--- |
| **Student / Attendee** | `zeenat@college.edu` | `user123` | Zeenat |
| **Event Organizer** | `organizer@college.edu` | `org123` | Event Club |
| **System Administrator** | `admin@college.edu` | `admin123` | Admin |

---

## Getting Started

### 1. Prerequisites
- Python 3.10+ installed
- PostgreSQL installed and running (Optional: local SQLite fallback activates automatically if PostgreSQL is unavailable)

### 2. Create Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure PostgreSQL Database
1. In your PostgreSQL client (psql, pgAdmin, or DBeaver), create the database:
   ```sql
   CREATE DATABASE college_events;
   ```
2. Check or edit the `.env` file with your PostgreSQL credentials:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/college_events
   FALLBACK_TO_SQLITE=True
   SECRET_KEY=college-event-secret-key-super-secure-change-in-production-2025
   CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000
   ```

### 4. Run the Backend Server
```bash
python run.py
```
Or directly with Uvicorn:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend server will start on: **`http://127.0.0.1:8000`**

---

## Interactive API Documentation

Once the server is running, explore and test the endpoints directly from your browser:
- **Swagger UI (Interactive)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints Summary

### Authentication (`/api/auth`)
- `POST /api/auth/login`: Authenticate and receive JWT token + user profile.
- `POST /api/auth/register`: Register a new student or organizer.
- `POST /api/auth/forgot-password`: Request password reset instructions.
- `GET /api/auth/me`: Get current authenticated user details.

### Events (`/api/events`)
- `GET /api/events`: List events (supports `category`, `status`, and `search` query parameters).
- `GET /api/events/{id}`: Retrieve detailed event information.
- `POST /api/events`: Create a new event.
- `PUT /api/events/{id}`: Update an event.
- `DELETE /api/events/{id}`: Remove an event.
- `GET /api/events/categories`: Retrieve list of all available categories.

### Registrations & Tickets (`/api/registrations`)
- `GET /api/registrations/my`: Get registrations for current student.
- `POST /api/registrations`: Register for an event and generate ticket code.
- `GET /api/registrations/event/{id}`: List attendee roster for an event.
- `GET /api/registrations/event/{id}/export`: Download attendees roster as a CSV file.
- `GET /api/registrations/pending`: List pending registrations across organizer events.
- `PATCH /api/registrations/{id}/status`: Approve or decline a registration.
- `DELETE /api/registrations/{id}`: Cancel registration.

### User Management (`/api/users`)
- `GET /api/users`: List all users (Admin view).
- `GET /api/users/{id}`: Get user details.
- `PATCH /api/users/{id}/status`: Toggle Active/Inactive status.
- `DELETE /api/users/{id}`: Delete user.

### Analytics (`/api/analytics`)
- `GET /api/analytics/organizer-stats`: 4 metrics cards and monthly registration trends.
- `GET /api/analytics/admin-stats`: System KPIs, 6-month performance trend, and category breakdown.

### Notifications (`/api/notifications`)
- `GET /api/notifications`: Retrieve notifications feed.
- `PATCH /api/notifications/read-all`: Mark all notifications as read.
- `PATCH /api/notifications/{id}/read`: Mark specific notification as read.