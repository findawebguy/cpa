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
    # Submit incorrect answer on q1 -> routed to rem1
    res1 = client.post("/api/v1/nodes/q1/submit", json={"index": 1, "confidence": "high"})
    assert res1.json()["next_node_key"] == "rem1"

    # Submit incorrect answer on q1_easy -> routed back to q1
    res2 = client.post("/api/v1/nodes/q1_easy/submit", json={"index": 1, "confidence": "medium"})
    assert res2.json()["next_node_key"] == "q1"

    # Check syllabus - Week 2 MUST remain locked
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[1]["status"] == "locked"
    assert syl[1]["start_node_key"] is None

def test_get_node_security_strip(client):
    res = client.get("/api/v1/nodes/q1")
    assert res.status_code == 200
    data = res.json()
    assert data["node_key"] == "q1"
    # Ensure options do not expose isCorrect or explanation
    for opt in data["options"]:
        assert "isCorrect" not in opt
        assert "explanation" not in opt

def test_submit_node_answer(client):
    res = client.post("/api/v1/nodes/q1/submit", json={"index": 0, "confidence": "high"})
    assert res.status_code == 200
    data = res.json()
    assert data["is_correct"] is True
    assert data["mastery_delta"] == 10.0
    assert data["next_node_key"] == "q2"
