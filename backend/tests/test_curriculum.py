def test_get_courses(client):
    res = client.get("/api/v1/courses")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 3
    track_codes = [c["code"] for c in data]
    assert "FAR" in track_codes
    assert "AUD" in track_codes
    assert "REG" in track_codes

def test_get_syllabus(client):
    res = client.get("/api/v1/courses/FAR/syllabus")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 7
    assert data[0]["week_number"] == 1
    # Week 1 should be unlocked, Week 2 locked
    assert data[0]["status"] in ["unlocked", "in-progress"]
    assert data[1]["status"] == "locked"

def test_remediation_does_not_unlock_week_2(client):
    client.post("/api/v1/auth/user/reset")
    # Submit incorrect answer on the first question -> routed to its worked-example remediation
    res1 = client.post("/api/v1/nodes/FAR_w1_q0/submit", json={"index": 1, "confidence": "high"})
    assert res1.json()["next_node_key"] == "FAR_w1_q0_rem"

    # The remediation proceeds to a practical application, which loops back to the question
    rem = client.get("/api/v1/nodes/FAR_w1_q0_rem").json()
    assert rem["next_node_key"] == "FAR_w1_q0_app"
    app = client.get("/api/v1/nodes/FAR_w1_q0_app").json()
    assert app["next_node_key"] == "FAR_w1_q0"

    # Check syllabus - Week 2 MUST remain locked (Week 1 not finished)
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[1]["status"] == "locked"
    assert syl[1]["start_node_key"] is None
    client.post("/api/v1/auth/user/reset")

def test_get_node_security_strip(client):
    res = client.get("/api/v1/nodes/FAR_w1_q0")
    assert res.status_code == 200
    data = res.json()
    assert data["node_key"] == "FAR_w1_q0"
    # Ensure options do not expose isCorrect or explanation
    for opt in data["options"]:
        assert "isCorrect" not in opt
        assert "explanation" not in opt

def test_submit_node_answer(client):
    client.post("/api/v1/auth/user/reset")
    res = client.post("/api/v1/nodes/FAR_w1_q0/submit", json={"index": 0, "confidence": "high"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_correct"] is True
    assert data["mastery_delta"] == 10.0
    assert data["next_node_key"] == "FAR_w1_q1"
    client.post("/api/v1/auth/user/reset")
