"""Regression tests for the week-completion gating invariant and the
remediation -> practical-application learning flow.

Invariant: an incorrect answer must never reach a week's `end` node, so a week
can only be completed by answering every gating question correctly. Each wrong
answer routes: question -> `_rem` (worked example) -> `_app` (practical
application) -> back to the same question.
"""
from backend.app.models.curriculum import LearningNode


def _nodes_by_key(db):
    return {n.node_key: n for n in db.query(LearningNode).all()}


def _next_gate(nodes_by_key, start_key):
    """Follow remediation/application nodes from `start_key` (their 'proceed'
    button uses next_correct_key) to the first question/end gate reached."""
    seen = set()
    key = start_key
    while key and key not in seen:
        seen.add(key)
        node = nodes_by_key.get(key)
        if node is None:
            return None
        if node.node_type in ("question", "end"):
            return node
        key = node.next_correct_key
    return None


def _complete_week(client, db, start_key, end_key, track="FAR"):
    """Answer questions correctly from start to end by querying each question's correct_answer_idx."""
    nbk = _nodes_by_key(db)
    key, guard = start_key, 0
    while key and key != end_key and guard < 60:
        guard += 1
        node = nbk.get(key)
        correct_idx = node.correct_answer_idx if node else 0
        key = client.post(f"/api/v1/nodes/{key}/submit",
                          json={"index": correct_idx, "confidence": "high"}).json().get("next_node_key")
    return key


def test_wrong_answer_never_reaches_end_node(db):
    """Every question, across all tracks: a wrong answer leads (via rem/app) back
    to another question, never to an end node."""
    nbk = _nodes_by_key(db)
    offenders = []
    for q in nbk.values():
        if q.node_type != "question":
            continue
        gate = _next_gate(nbk, q.next_incorrect_key)
        if gate is None or gate.node_type != "question":
            offenders.append((q.node_key, q.next_incorrect_key,
                              gate.node_key if gate else None,
                              gate.node_type if gate else None))
    assert not offenders, f"Questions whose wrong path reaches a non-question gate: {offenders}"


def test_every_question_has_worked_example_then_application(db):
    """The reported UX fix: each question's wrong path is
    question -> `_rem` (remediation) -> `_app` (application) -> back to question."""
    nbk = _nodes_by_key(db)
    questions = [n for n in nbk.values() if n.node_type == "question"]
    assert questions, "no question nodes seeded"
    for q in questions:
        rem_key, app_key = f"{q.node_key}_rem", f"{q.node_key}_app"
        assert q.next_incorrect_key == rem_key, f"{q.node_key} wrong path != {rem_key}"
        assert rem_key in nbk and nbk[rem_key].node_type == "remediation"
        assert app_key in nbk and nbk[app_key].node_type == "application"
        # remediation proceeds to the practical application, which returns to the question
        assert nbk[rem_key].next_correct_key == app_key
        assert nbk[app_key].next_correct_key == q.node_key


def test_application_node_api_shape(client):
    """The application node is served with practical-application content and
    routes back to its originating question."""
    res = client.get("/api/v1/nodes/FAR_w1_q0_app")
    assert res.status_code == 200
    data = res.json()
    assert data["node_type"] == "application"
    assert data["next_node_key"] == "FAR_w1_q0"   # 'Return to Question'
    assert data["remediation_html"]               # has real content, not empty


def test_worked_example_node_proceeds_to_application(client):
    rem = client.get("/api/v1/nodes/FAR_w1_q0_rem").json()
    assert rem["node_type"] == "remediation"
    assert rem["next_node_key"] == "FAR_w1_q0_app"  # 'Proceed to Practical Application'
    assert rem["remediation_html"]


def test_wrong_answer_routes_to_remediation(client, db):
    nbk = _nodes_by_key(db)
    node = nbk["FAR_w1_q0"]
    wrong_idx = (node.correct_answer_idx + 1) % len(node.options_json)

    res = client.post("/api/v1/nodes/FAR_w1_q0/submit", json={"index": wrong_idx, "confidence": "high"})
    body = res.json()
    assert body["is_correct"] is False
    assert body["next_node_key"] == "FAR_w1_q0_rem"


def test_visit_end_node_does_not_grant_completion(client, db):
    """The /visit endpoint is a UX acknowledgement only; it must never complete a
    week -- neither with zero work nor after only a wrong answer."""
    nbk = _nodes_by_key(db)
    node = nbk["FAR_w1_q0"]
    wrong_idx = (node.correct_answer_idx + 1) % len(node.options_json)

    client.post("/api/v1/auth/user/reset")

    res = client.post("/api/v1/nodes/FAR_w1_end/visit")
    assert res.json()["completed"] is False
    assert client.get("/api/v1/courses/FAR/syllabus").json()[0]["status"] != "completed"

    client.post("/api/v1/nodes/FAR_w1_q0/submit", json={"index": wrong_idx, "confidence": "high"})
    res = client.post("/api/v1/nodes/FAR_w1_end/visit")
    assert res.json()["completed"] is False
    assert client.get("/api/v1/courses/FAR/syllabus").json()[0]["status"] != "completed"

    client.post("/api/v1/auth/user/reset")


def test_correct_answers_complete_week_and_unlock_next(client, db):
    """Completion is earned purely by correct answers (submit-side), no /visit."""
    client.post("/api/v1/auth/user/reset")
    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    last = _complete_week(client, db, syl[0]["start_node_key"], "FAR_w1_end")
    assert last == "FAR_w1_end"

    syl = client.get("/api/v1/courses/FAR/syllabus").json()
    assert syl[0]["status"] == "completed"
    assert syl[1]["status"] in ("unlocked", "in-progress")
    assert syl[2]["status"] == "locked"
    client.post("/api/v1/auth/user/reset")
