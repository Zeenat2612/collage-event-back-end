import sys
from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    print("--- Starting Backend API Verification ---")
    from app.database import SessionLocal
    from app.models.user import User
    from app.models.registration import Registration
    db = SessionLocal()
    db.query(Registration).filter(Registration.event_id == 'evt-3', Registration.user_email == 'zeenat@college.edu').delete()
    u = db.query(User).filter(User.email == 'zeenat@college.edu').first()
    if u:
        u.status = 'Active'
    db.commit()
    db.close()

    with TestClient(app) as client:
        # 1. Root & Health
        res = client.get("/")
        assert res.status_code == 200, f"Root failed: {res.text}"
        data = res.json()
        print(f"[PASS] Root endpoint working. DB dialect: {data.get('database')}")

        res = client.get("/health")
        assert res.status_code == 200
        print("[PASS] Health endpoint working.")

        # 2. Authentication: Student Login
        res = client.post("/api/auth/login", json={"email": "zeenat@college.edu", "password": "user123"})
        assert res.status_code == 200, f"Student login failed: {res.text}"
        auth_data = res.json()
        token = auth_data["access_token"]
        assert auth_data["user"]["name"] == "Zeenat"
        assert auth_data["user"]["role"] == "user"
        print("[PASS] Student Login verified (Zeenat).")

        # 3. Authentication: Organizer Login
        res = client.post("/api/auth/login", json={"email": "organizer@college.edu", "password": "org123"})
        assert res.status_code == 200, f"Organizer login failed: {res.text}"
        assert res.json()["user"]["role"] == "organizer"
        print("[PASS] Organizer Login verified.")

        # 4. Authentication: Admin Login
        res = client.post("/api/auth/login", json={"email": "admin@college.edu", "password": "admin123"})
        assert res.status_code == 200, f"Admin login failed: {res.text}"
        assert res.json()["user"]["role"] == "admin"
        print("[PASS] Admin Login verified.")

        # 5. Events List
        res = client.get("/api/events")
        assert res.status_code == 200, f"Get events failed: {res.text}"
        events = res.json()
        assert len(events) >= 5, f"Expected at least 5 events, got {len(events)}"
        evt1 = events[0]
        assert "id" in evt1 and "title" in evt1 and "dateVenue" in evt1 and "categoryColor" in evt1
        print(f"[PASS] Events endpoint verified ({len(events)} events loaded).")

        # 6. Event Filter by Category & Search
        res = client.get("/api/events?category=Technical")
        assert res.status_code == 200
        assert all(e["category"] == "Technical" for e in res.json())
        print("[PASS] Event Category Filter verified.")

        # 7. Registrations: My Registrations
        headers = {"Authorization": f"Bearer {token}"}
        res = client.get("/api/registrations/my", headers=headers)
        assert res.status_code == 200, f"My registrations failed: {res.text}"
        regs = res.json()
        assert len(regs) > 0
        assert "ticketCode" in regs[0]
        print(f"[PASS] My Registrations verified ({len(regs)} registrations found).")

        # 8. Event Booking / Registration Creation
        new_booking_payload = {
            "eventId": "evt-3",
            "userName": "Zeenat",
            "userEmail": "zeenat@college.edu"
        }
        res = client.post("/api/registrations", json=new_booking_payload, headers=headers)
        assert res.status_code == 201, f"Create registration failed: {res.text}"
        created_reg = res.json()
        assert created_reg["ticketCode"].startswith("TCK-")
        print(f"[PASS] Event Registration created with ticket code: {created_reg['ticketCode']}")

        # 9. Organizer Analytics
        res = client.get("/api/analytics/organizer-stats")
        assert res.status_code == 200
        org_stats = res.json()
        assert len(org_stats["stats"]) == 4
        assert len(org_stats["chartData"]) > 0
        print("[PASS] Organizer Analytics verified.")

        # 10. Admin Analytics
        res = client.get("/api/analytics/admin-stats")
        assert res.status_code == 200
        adm_stats = res.json()
        assert len(adm_stats["stats"]) == 4
        assert len(adm_stats["lineChartData"]) > 0
        assert len(adm_stats["categoryData"]) > 0
        print("[PASS] Admin Analytics verified.")

        # 11. User Management (Admin)
        res = client.get("/api/users")
        assert res.status_code == 200
        users = res.json()
        assert len(users) >= 3
        print(f"[PASS] Users Directory verified ({len(users)} users).")

        # Toggle User Status
        user_id = users[0]["id"]
        res = client.patch(f"/api/users/{user_id}/status")
        assert res.status_code == 200
        # Re-toggle back to Active so test suite remains idempotent
        client.patch(f"/api/users/{user_id}/status")
        print("[PASS] Toggle User Status verified.")

        # 12. Attendee CSV Export
        res = client.get("/api/registrations/event/evt-1/export")
        assert res.status_code == 200
        assert "text/csv" in res.headers.get("content-type", "")
        print("[PASS] Attendee CSV Export verified.")

        # 13. Notifications
        res = client.get("/api/notifications")
        assert res.status_code == 200
        notifs = res.json()
        assert len(notifs) > 0
        print(f"[PASS] Notifications verified ({len(notifs)} items).")

    print("--- ALL 13 VERIFICATION TESTS PASSED SUCCESSFULLY! ---")

if __name__ == "__main__":
    run_tests()
