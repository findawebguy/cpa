def test_register_and_login(client):
    email = "newstudent@cpa.com"
    password = "securepassword123"

    # Register
    res = client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == email

    # Login
    res_login = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert res_login.status_code == 200
    data_login = res_login.json()
    assert "access_token" in data_login

def test_user_profile(client):
    res = client.get("/api/v1/auth/user/profile")
    assert res.status_code == 200
    data = res.json()
    assert "readiness_score" in data
    assert "streak_days" in data

def test_update_user_profile(client):
    new_email = "updated_student@cpa.com"
    res = client.put("/api/v1/auth/user/profile", json={"email": new_email})
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == new_email

def test_guest_session_migration(client):
    payload = {
        "guest_progress": [
            {"node_key": "q1", "mastery_level": 75.0, "streak_days": 2},
            {"node_key": "q2", "mastery_level": 80.0, "streak_days": 2}
        ],
        "tbs_code": "tbs-1",
        "tbs_rows": [
            {"account": "Insurance Expense", "debit": 3000, "credit": 0}
        ]
    }
    res = client.post("/api/v1/auth/migrate-guest-session", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["migrated_nodes"] >= 0

def test_qr_session_generation_and_watcher(client):
    # 1. Desktop generates QR session token
    res = client.post("/api/v1/auth/qr-session")
    assert res.status_code == 200
    data = res.json()
    token = data["qr_token"]

    # 2. Desktop watcher polls before scan -> scanned should be False
    res_watcher_before = client.get(f"/api/v1/auth/qr-status?qr_token={token}")
    assert res_watcher_before.status_code == 200
    assert res_watcher_before.json()["scanned"] is False

    # 3. Mobile phone scans QR code (hits qr-login endpoint)
    res_qr = client.get(f"/api/v1/auth/qr-login?qr_token={token}")
    assert res_qr.status_code == 200
    assert "access_token" in res_qr.json()

    # 4. Desktop watcher polls after scan -> scanned should be True!
    res_watcher_after = client.get(f"/api/v1/auth/qr-status?qr_token={token}")
    assert res_watcher_after.status_code == 200
    status_data = res_watcher_after.json()
    assert status_data["scanned"] is True
    assert status_data["access_token"] == token

def test_reset_user_progress(client):
    # Attempt a question first
    client.post("/api/v1/nodes/q1/submit", json={"index": 0, "confidence": "high"})
    
    # Call reset endpoint
    res = client.post("/api/v1/auth/user/reset")
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # Verify profile stats reset to 0
    prof = client.get("/api/v1/auth/user/profile").json()
    assert prof["total_attempted"] == 0

def test_logout_user(client):
    res = client.post("/api/v1/auth/logout")
    assert res.status_code == 200
    assert res.json()["status"] == "success"


