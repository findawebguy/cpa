import requests
import json
import sys
import os
import time

# Target base URL is configurable so the same suite can run against the live
# site or a local dev server, e.g.:
#   CPA_BASE_URL=http://localhost:8005/cpa python qa_test_live.py
#   python qa_test_live.py http://localhost:8005/cpa
_DEFAULT_ROOT = "https://demo.i-te.am/cpa"
_root = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CPA_BASE_URL", _DEFAULT_ROOT)).rstrip("/")
BASE = _root if _root.endswith("/api/v1") else f"{_root}/api/v1"
print(f"Target BASE: {BASE}")
PASS_COUNT = 0
FAIL_COUNT = 0

def check(label, condition, detail=""):
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS: {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL: {label} {detail}")
    return condition

print("=" * 70)
print("CPA PLATFORM FULL QA TEST SUITE (LIVE SITE)")
print("=" * 70)

# 0. Wait for server to pick up new code
print("\n[0] Waiting 3s for live server to reload after git pull...")
time.sleep(3)

# 1. Login
print("\n[1] LOGIN")
r = requests.post(f"{BASE}/auth/login", json={"email": "student@cpa.com", "password": "pass123"})
print(f"  Status: {r.status_code}")
token_data = r.json()
token = token_data.get("access_token")
check("Login succeeded", token is not None)
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 1b. Reseed curriculum to get new node data
print("\n[1b] RESEED CURRICULUM (pick up new init_db.py data)")
r = requests.post(f"{BASE}/auth/admin/reseed", headers=headers)
print(f"  Status: {r.status_code}")
if r.status_code == 200:
    print(f"  Response: {r.json()}")
    check("Reseed succeeded", True)
else:
    print(f"  ERROR: {r.text}")
    check("Reseed succeeded", False, r.text)

# 2. Reset progress
print("\n[2] RESET ALL PROGRESS")
r = requests.post(f"{BASE}/auth/user/reset", headers=headers)
check("Reset succeeded", r.status_code == 200)

# 3. Check syllabus BEFORE any attempts
print("\n[3] SYLLABUS STATE AFTER RESET (BEFORE ANY ATTEMPTS)")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
for w in syllabus:
    print(f"  Week {w['week_number']}: status={w['status']}, nodes={w['node_count']}, start_key={w.get('start_node_key')}")

check("Week 1 is in-progress", syllabus[0]["status"] == "in-progress")
check("Week 2 is locked", syllabus[1]["status"] == "locked")
check("Week 2 has no start_key", syllabus[1]["start_node_key"] is None)
check("Week 2 has >2 nodes (not placeholder)", syllabus[1]["node_count"] > 2, f"got {syllabus[1]['node_count']}")

# 4. Inspect Week 1 Q1
print("\n[4] INSPECT WEEK 1 Q1")
r = requests.get(f"{BASE}/nodes/q1", headers=headers)
q1 = r.json()
check("q1 is question type", q1["node_type"] == "question")
check("q1 has 4 options", len(q1["options"]) == 4)
print(f"  concept: {q1['concept_name']}")

# 5. Wrong answer to q1
print("\n[5] WRONG ANSWER TO Q1 (index=1)")
r = requests.post(f"{BASE}/nodes/q1/submit", headers=headers, json={"index": 1, "confidence": "high"})
result = r.json()
check("q1 answer incorrect", result["is_correct"] is False)
check("Routes to remediation (rem1)", result["next_node_key"] == "rem1")
check("Mastery decreased", result["mastery_delta"] < 0)

# 6. Syllabus after wrong q1
print("\n[6] SYLLABUS AFTER WRONG Q1 - WEEK 2 MUST BE LOCKED")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 1 in-progress", syllabus[0]["status"] == "in-progress")
check("Week 2 still locked", syllabus[1]["status"] == "locked")

# 7. View remediation
print("\n[7] VIEW REMEDIATION rem1")
r = requests.get(f"{BASE}/nodes/rem1", headers=headers)
rem1 = r.json()
check("rem1 is remediation type", rem1["node_type"] == "remediation")
print(f"  next_node_key: {rem1.get('next_node_key')}")

# 8. Answer scaffolded q1_easy correctly
print("\n[8] VIEW AND ANSWER q1_easy")
r = requests.get(f"{BASE}/nodes/q1_easy", headers=headers)
q1e = r.json()
check("q1_easy is question type", q1e["node_type"] == "question")

r = requests.post(f"{BASE}/nodes/q1_easy/submit", headers=headers, json={"index": 0, "confidence": "medium"})
result = r.json()
check("q1_easy correct", result["is_correct"] is True)
check("Routes to q2", result["next_node_key"] == "q2")

# 9. Syllabus - Week 2 still locked (only q1_easy done, q2 & q3 remaining)
print("\n[9] SYLLABUS - WEEK 2 MUST STILL BE LOCKED")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 2 still locked after q1_easy", syllabus[1]["status"] == "locked")

# 10. Answer q2 correctly
print("\n[10] ANSWER Q2 CORRECTLY (index=1)")
r = requests.post(f"{BASE}/nodes/q2/submit", headers=headers, json={"index": 1, "confidence": "medium"})
result = r.json()
check("q2 correct", result["is_correct"] is True)

# 11. Syllabus - Week 2 still locked (q3 remaining)
print("\n[11] SYLLABUS - WEEK 2 MUST STILL BE LOCKED (q3 not done)")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 2 still locked after q2", syllabus[1]["status"] == "locked")

# 12. Answer q3 correctly
print("\n[12] ANSWER Q3 CORRECTLY (index=0)")
r = requests.post(f"{BASE}/nodes/q3/submit", headers=headers, json={"index": 0, "confidence": "medium"})
result = r.json()
check("q3 correct", result["is_correct"] is True)
check("Routes to finish_w1", result["next_node_key"] == "finish_w1")

# 13. Visit the end node to record completion
print("\n[13] VISIT END NODE finish_w1")
r = requests.post(f"{BASE}/nodes/finish_w1/visit", headers=headers)
visit_result = r.json()
check("End node visit recorded", visit_result.get("status") == "success")

# 14. Syllabus - Week 1 completed, Week 2 unlocked, Week 3 locked
print("\n[14] SYLLABUS - WEEK 1 COMPLETED, WEEK 2 UNLOCKED")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
for w in syllabus[:4]:
    print(f"  Week {w['week_number']}: status={w['status']}, start_key={w.get('start_node_key')}")
check("Week 1 completed", syllabus[0]["status"] == "completed")
check("Week 2 unlocked", syllabus[1]["status"] in ["unlocked", "in-progress"])
check("Week 3 locked", syllabus[2]["status"] == "locked")

# 15. Inspect Week 2 content quality
print("\n[15] INSPECT WEEK 2 CONTENT QUALITY")
r = requests.get(f"{BASE}/nodes/far_w2_q1", headers=headers)
w2q1 = r.json()
print(f"  concept: {w2q1['concept_name']}")
print(f"  scenario: {w2q1['scenario_content'][:120]}...")
print(f"  options count: {len(w2q1['options'])}")
for i, opt in enumerate(w2q1["options"]):
    print(f"    [{i}] {opt['text'][:80]}")
check("W2 Q1 has professional content (not generic)", "GAAP" not in w2q1["concept_name"] or "Statement" in w2q1["concept_name"] or "Cash Flow" in w2q1["concept_name"])
check("W2 Q1 has 3+ options", len(w2q1["options"]) >= 3)

# 16. Answer W2 Q1 correctly
print("\n[16] ANSWER far_w2_q1 CORRECTLY")
r = requests.post(f"{BASE}/nodes/far_w2_q1/submit", headers=headers, json={"index": 0, "confidence": "medium"})
result = r.json()
check("W2 Q1 correct", result["is_correct"] is True)
next_key = result["next_node_key"]
check("Routes to far_w2_q2 (not end)", next_key == "far_w2_q2", f"got {next_key}")

# 17. CRITICAL: Week 3 must NOT be unlocked yet
print("\n[17] SYLLABUS - WEEK 3 MUST STILL BE LOCKED (only W2 Q1 done)")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 2 NOT completed", syllabus[1]["status"] != "completed", f"got {syllabus[1]['status']}")
check("Week 3 locked", syllabus[2]["status"] == "locked", f"got {syllabus[2]['status']}")

# 18. Answer W2 Q2 WRONG
print("\n[18] ANSWER far_w2_q2 WRONG (index=1)")
r = requests.post(f"{BASE}/nodes/far_w2_q2/submit", headers=headers, json={"index": 1, "confidence": "medium"})
result = r.json()
check("W2 Q2 incorrect", result["is_correct"] is False)
next_key = result["next_node_key"]
print(f"  next_node_key: {next_key}")
check("Routes to remediation, not end", next_key != "far_w2_end", f"got {next_key}")

# 19. CRITICAL: Week 3 must STILL be locked (wrong answer, didn't reach end)
print("\n[19] SYLLABUS - WEEK 3 STILL LOCKED AFTER WRONG W2 Q2")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 2 in-progress (not completed)", syllabus[1]["status"] in ["in-progress"], f"got {syllabus[1]['status']}")
check("Week 3 still locked", syllabus[2]["status"] == "locked")

# 20. Now view remediation and re-answer Q2 correctly
print("\n[20] REMEDIATE AND RE-ANSWER far_w2_q2 CORRECTLY")
if next_key and "rem" in next_key:
    r = requests.get(f"{BASE}/nodes/{next_key}", headers=headers)
    rem = r.json()
    print(f"  Remediation: {rem['concept_name']}")
    check("Remediation node is remediation type", rem["node_type"] == "remediation")

# Re-answer q2 (routing from remediation leads back to q2)
r = requests.post(f"{BASE}/nodes/far_w2_q2/submit", headers=headers, json={"index": 0, "confidence": "high"})
result = r.json()
check("W2 Q2 correct on retry", result["is_correct"] is True)
check("Routes to end node", result["next_node_key"] == "far_w2_end")

# 21. Visit end node
print("\n[21] VISIT END NODE far_w2_end")
r = requests.post(f"{BASE}/nodes/far_w2_end/visit", headers=headers)
visit_result = r.json()
check("End node visit recorded", visit_result.get("status") == "success")

# 22. Week 2 completed, Week 3 unlocked
print("\n[22] FINAL SYLLABUS CHECK")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
for w in syllabus[:5]:
    print(f"  Week {w['week_number']}: status={w['status']}, start_key={w.get('start_node_key')}")
check("Week 2 completed", syllabus[1]["status"] == "completed")
check("Week 3 unlocked", syllabus[2]["status"] in ["unlocked", "in-progress"])
check("Week 4 locked", syllabus[3]["status"] == "locked")

# 23. User profile stats
print("\n[23] USER PROFILE STATS")
r = requests.get(f"{BASE}/auth/user/profile", headers=headers)
profile = r.json()
print(f"  email: {profile['user']['email']}")
print(f"  streak_days: {profile['streak_days']}")
print(f"  mastery_percent: {profile['mastery_percent']}")
print(f"  total_attempted: {profile['total_attempted']}")

# 24. Test Reset functionality
print("\n[24] TEST RESET FUNCTIONALITY")
r = requests.post(f"{BASE}/auth/user/reset", headers=headers)
check("Reset succeeded", r.status_code == 200)
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("After reset: Week 1 in-progress", syllabus[0]["status"] == "in-progress")
check("After reset: Week 2 locked", syllabus[1]["status"] == "locked")

print("\n" + "=" * 70)
print(f"QA TEST SUITE COMPLETE: {PASS_COUNT} PASSED, {FAIL_COUNT} FAILED")
print("=" * 70)

if FAIL_COUNT > 0:
    sys.exit(1)
