from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    r = client.get("/api/health/ready")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_report_lookup_flow():
    r = client.post("/api/reports", json={
    "phone": "5512345678", "country": "MX", "channel": "call",
    "reason": "threat", "details": "Exigieron depósito", "reporter_id": "t1"
    })
    assert r.status_code == 200
    rid = r.json()["report_id"]
    assert rid > 0


r2 = client.get("/api/risk/lookup", params={"phone": "5512345678", "country": "MX"})
assert r2.status_code == 200
data = r2.json()
assert 0.0 <= data["risk_score"] <= 1.0