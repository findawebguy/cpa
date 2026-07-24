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
start_key = syllabus[0]["start_node_key"] or "FAR_w1_q0"
print(f"\n[4] INSPECT WEEK 1 Q1 ({start_key})")
r = requests.get(f"{BASE}/nodes/{start_key}", headers=headers)
q1 = r.json()
check("q1 is question type", q1["node_type"] == "question")
check("q1 has options", len(q1["options"]) >= 2)
print(f"  concept: {q1['concept_name']}")

# 5. Wrong answer to q1
print(f"\n[5] WRONG ANSWER TO Q1 ({start_key}) (index=1)")
r = requests.post(f"{BASE}/nodes/{start_key}/submit", headers=headers, json={"index": 1, "confidence": "high"})
result = r.json()
check("q1 answer incorrect", result["is_correct"] is False)
check("Routes to remediation", "rem" in result["next_node_key"] or "q" in result["next_node_key"])
check("Mastery decreased", result["mastery_delta"] < 0)

# 6. Syllabus after wrong q1
print("\n[6] SYLLABUS AFTER WRONG Q1 - WEEK 2 MUST BE LOCKED")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 1 in-progress", syllabus[0]["status"] == "in-progress")
check("Week 2 still locked", syllabus[1]["status"] == "locked")

# 7. View remediation
rem_key = result["next_node_key"]
print(f"\n[7] VIEW REMEDIATION {rem_key}")
r = requests.get(f"{BASE}/nodes/{rem_key}", headers=headers)
rem1 = r.json()
check("Remediation type node", rem1.get("node_type") == "remediation")
print(f"  next_node_key: {rem1.get('next_node_key')}")

# 8. Retry correct answer for Q1
print(f"\n[8] RETRY CORRECT ANSWER FOR {start_key}")
r = requests.post(f"{BASE}/nodes/{start_key}/submit", headers=headers, json={"index": 0, "confidence": "high"})
result = r.json()
check("Answer correct", result["is_correct"] is True)

# 9. Syllabus - Week 2 still locked
print("\n[9] SYLLABUS - WEEK 2 MUST STILL BE LOCKED (W1 not finished)")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 2 still locked after Q1", syllabus[1]["status"] == "locked")

# 10. Complete remaining Week 1 nodes dynamically
current_key = result.get("next_node_key")
print(f"\n[10-12] FINISHING REMAINING WEEK 1 QUESTIONS STARTING AT {current_key}")
while current_key and current_key != "FAR_w1_end":
    r_sub = requests.post(f"{BASE}/nodes/{current_key}/submit", headers=headers, json={"index": 0, "confidence": "high"})
    res_sub = r_sub.json()
    current_key = res_sub.get("next_node_key")
    if not res_sub.get("is_correct") and current_key:
        r_sub = requests.post(f"{BASE}/nodes/{current_key}/submit", headers=headers, json={"index": 0, "confidence": "high"})
        res_sub = r_sub.json()
        current_key = res_sub.get("next_node_key")

# 13. Visit the end node to record completion
end_key = "FAR_w1_end"
print(f"\n[13] VISIT END NODE {end_key}")
r = requests.post(f"{BASE}/nodes/{end_key}/visit", headers=headers)
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
w2_start = syllabus[1]["start_node_key"] or "FAR_w2_q0"
print(f"\n[15] INSPECT WEEK 2 CONTENT QUALITY ({w2_start})")
r = requests.get(f"{BASE}/nodes/{w2_start}", headers=headers)
w2q1 = r.json()
print(f"  concept: {w2q1['concept_name']}")
print(f"  scenario: {w2q1['scenario_content'][:120]}...")
print(f"  options count: {len(w2q1['options'])}")
for i, opt in enumerate(w2q1["options"]):
    print(f"    [{i}] {opt['text'][:80]}")
check("W2 Q1 has professional content", len(w2q1["scenario_content"]) > 20)
check("W2 Q1 has 2+ options", len(w2q1["options"]) >= 2)

# 16. Answer W2 Q0 correctly
print(f"\n[16] ANSWER {w2_start} CORRECTLY")
r = requests.post(f"{BASE}/nodes/{w2_start}/submit", headers=headers, json={"index": 0, "confidence": "medium"})
result = r.json()
check("W2 Q0 correct", result["is_correct"] is True)
next_key = result["next_node_key"]

# 17. CRITICAL: Week 3 must NOT be unlocked yet
print("\n[17] SYLLABUS - WEEK 3 MUST STILL BE LOCKED (only W2 Q0 done)")
r = requests.get(f"{BASE}/courses/FAR/syllabus", headers=headers)
syllabus = r.json()
check("Week 2 NOT completed", syllabus[1]["status"] != "completed", f"got {syllabus[1]['status']}")
check("Week 3 locked", syllabus[2]["status"] == "locked", f"got {syllabus[2]['status']}")

# 18. Complete remaining Week 2 nodes
current_key = next_key
print(f"\n[18-20] FINISHING REMAINING WEEK 2 QUESTIONS STARTING AT {current_key}")
while current_key and current_key != "FAR_w2_end":
    r_sub = requests.post(f"{BASE}/nodes/{current_key}/submit", headers=headers, json={"index": 0, "confidence": "high"})
    res_sub = r_sub.json()
    current_key = res_sub.get("next_node_key")

# 21. Visit end node
end_w2_key = "FAR_w2_end"
print(f"\n[21] VISIT END NODE {end_w2_key}")
r = requests.post(f"{BASE}/nodes/{end_w2_key}/visit", headers=headers)
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
