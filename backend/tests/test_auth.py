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
