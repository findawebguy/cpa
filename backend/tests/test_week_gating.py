"""Regression tests for the week-completion gating invariant.

Bug: a user could complete a week (reach its 'end' node) while answering a
question WRONG, because incorrect-answer routing skipped forward or pointed
straight at the end node. These tests lock in the invariant that an 'end' node
is only reachable by answering every gating question correctly.
"""
from backend.app.models.curriculum import LearningNode


def _next_gate(nodes_by_key, start_key):
    """Follow a chain of remediation nodes from `start_key` (the frontend 'Proceed'
    button uses a remediation's next_correct_key) and return the first
    question/end node encountered -- the next real gate a user must clear."""
    seen = set()
    key = start_key
    while key and key not in seen:
        seen.add(key)
        node = nodes_by_key.get(key)
        if node is None:
            return None
        if node.node_type in ("question", "end"):
            return node
        key = node.next_correct_key  # remediation -> proceed
    return None


def test_wrong_answer_never_reaches_end_node(db):
    """For EVERY question node across all tracks, a wrong answer must lead
    (possibly via remediation) back to another question -- never to an end node."""
    nodes = db.query(LearningNode).all()
    nodes_by_key = {n.node_key: n for n in nodes}

    offenders = []
    for q in nodes:
        if q.node_type != "question":
            continue
        gate = _next_gate(nodes_by_key, q.next_incorrect_key)
        if gate is None or gate.node_type != "question":
            offenders.append((q.node_key, q.next_incorrect_key,
                              gate.node_key if gate else None,
                              gate.node_type if gate else None))

    assert not offenders, (
        "These questions let a wrong answer reach a non-question gate (end node "
        "or dead end): " + str(offenders)
    )


def test_far_w2_wrong_q1_routes_back_not_forward(client):
    """The reported bug: wrong far_w2_q1 must route to remediation that returns
    to far_w2_q1 -- it must NOT skip forward to far_w2_q2 or far_w2_end."""
    res = client.post("/api/v1/nodes/far_w2_q1/submit", json={"index": 1, "confidence": "medium"})
    assert res.status_code == 200
    body = res.json()
    assert body["is_correct"] is False
    assert body["next_node_key"] == "far_w2_rem1"

    rem = client.get("/api/v1/nodes/far_w2_rem1").json()
    assert rem["next_node_key"] == "far_w2_q1"  # loops back, does not skip to q2/end


def test_aud_wrong_answer_does_not_complete_week(client):
    res = client.post("/api/v1/nodes/q1_aud/submit", json={"index": 1, "confidence": "medium"})
    assert res.json()["next_node_key"] == "q1_aud"  # retry, not finish_aud

    syl = client.get("/api/v1/courses/AUD/syllabus").json()
    assert syl[0]["status"] != "completed"


def test_reg_wrong_answer_does_not_complete_week(client):
    res = client.post("/api/v1/nodes/q1_reg/submit", json={"index": 1, "confidence": "medium"})
    assert res.json()["next_node_key"] == "q1_reg"  # retry, not finish_reg

    syl = client.get("/api/v1/courses/REG/syllabus").json()
    assert syl[0]["status"] != "completed"


def test_far_week2_end_to_end_gating(client):
    """End-to-end reproduction of the user's scenario: completing week 1, then
    getting a week-2 question wrong must NOT complete week 2. Only correctly
    answering both week-2 questions completes it."""
    client.post("/api/v1/auth/user/reset")

    # Complete Week 1 by answering the core questions correctly.
    assert client.post("/api/v1/nodes/q1/submit", json={"index": 0, "confidence": "medium"}).json()["next_node_key"] == "q2"
    assert client.post("/api/v1/nodes/q2/submit", json={"index": 1, "confidence": "medium"}).json()["next_node_key"] == "q3"
    assert client.post("/api/v1/nodes/q3/submit", json={"index": 0, "confidence": "medium"}).json()["next_node_key"] == "finish_w1"

    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[0]["status"] == "completed"            # Week 1 done (correct final answer)
    assert syl[1]["status"] in ("unlocked", "in-progress")  # Week 2 unlocked

    # Answer far_w2_q1 WRONG -> week 2 must stay incomplete, week 3 stays locked.
    client.post("/api/v1/nodes/far_w2_q1/submit", json={"index": 1, "confidence": "medium"})
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[1]["status"] != "completed"
    assert syl[2]["status"] == "locked"

    # Now answer both week-2 questions correctly -> week 2 completes, week 3 unlocks.
    assert client.post("/api/v1/nodes/far_w2_q1/submit", json={"index": 0, "confidence": "medium"}).json()["next_node_key"] == "far_w2_q2"
    # get q2 wrong first -> still not complete
    client.post("/api/v1/nodes/far_w2_q2/submit", json={"index": 1, "confidence": "medium"})
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[1]["status"] != "completed"
    # then correct
    assert client.post("/api/v1/nodes/far_w2_q2/submit", json={"index": 0, "confidence": "medium"}).json()["next_node_key"] == "far_w2_end"

    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[1]["status"] == "completed"
    assert syl[2]["status"] in ("unlocked", "in-progress")

    client.post("/api/v1/auth/user/reset")


def test_visit_end_node_does_not_grant_completion(client):
    """The /visit endpoint is a UX acknowledgement only -- it must never mark a
    week complete. Crafted jumps to an end node (with zero work, or after only a
    wrong answer) must leave the week incomplete."""
    client.post("/api/v1/auth/user/reset")

    # (a) Zero work: jump straight to a week-3 end node.
    res = client.post("/api/v1/nodes/far_w3_end/visit")
    assert res.json()["completed"] is False
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[2]["status"] != "completed"

    # (b) After only a WRONG answer: attempt far_w3_q1 wrong, then visit the end.
    client.post("/api/v1/nodes/far_w3_q1/submit", json={"index": 1, "confidence": "high"})
    res = client.post("/api/v1/nodes/far_w3_end/visit")
    assert res.json()["completed"] is False
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[2]["status"] != "completed"

    client.post("/api/v1/auth/user/reset")


def test_correct_final_answer_completes_week_without_visit(client):
    """Completion is earned by the correct final answer alone (submit-side),
    with no /visit call needed."""
    client.post("/api/v1/auth/user/reset")
    # Reach + clear Week 1 so Week 3's gate isn't relevant; test Week 1 directly.
    client.post("/api/v1/nodes/q1/submit", json={"index": 0, "confidence": "medium"})
    client.post("/api/v1/nodes/q2/submit", json={"index": 1, "confidence": "medium"})
    res = client.post("/api/v1/nodes/q3/submit", json={"index": 0, "confidence": "medium"})
    assert res.json()["next_node_key"] == "finish_w1"

    # No /visit call -- week must already be complete from the correct final answer.
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[0]["status"] == "completed"
    client.post("/api/v1/auth/user/reset")
