def test_get_tbs_scenario(client):
    res = client.get("/api/v1/tbs/tbs-1")
    assert res.status_code == 200
    data = res.json()
    assert data["code"] == "tbs-1"
    assert "Exhibit A" in data["exhibit_html"]
    assert len(data["accounts_list"]) > 0

def test_submit_tbs_simulation(client):
    payload = {
        "rows": [
            {"account": "Insurance Expense", "debit": 3000, "credit": 0},
            {"account": "Prepaid Insurance", "debit": 0, "credit": 3000},
            {"account": "Accounts Receivable", "debit": 4500, "credit": 0},
            {"account": "Service Revenue", "debit": 0, "credit": 4500},
            {"account": "Depreciation Expense", "debit": 6200, "credit": 0},
            {"account": "Accumulated Depreciation", "debit": 0, "credit": 6200}
        ]
    }
    res = client.post("/api/v1/tbs/tbs-1/submit", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["is_balanced"] is True
    assert data["score"] == 100.0
    assert data["passed"] is True
