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

def test_guest_session_migration(client):
    # Test migrating guest history into account
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

def test_qr_session_generation_and_login(client):
    # Test QR auth token generation
    res = client.post("/api/v1/auth/qr-session")
    assert res.status_code == 200
    data = res.json()
    assert "qr_token" in data
    assert "qr_url" in data

    # Test scanning/validating QR token
    token = data["qr_token"]
    res_qr = client.get(f"/api/v1/auth/qr-login?qr_token={token}")
    assert res_qr.status_code == 200
    qr_data = res_qr.json()
    assert "access_token" in qr_data
