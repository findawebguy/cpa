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
