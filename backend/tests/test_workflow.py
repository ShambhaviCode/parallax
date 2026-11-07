from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    assert client.get("/api/health").json()["status"] == "ok"

def test_overview_and_incident():
    overview = client.get("/api/overview").json()
    assert overview["services_total"] == 4
    assert overview["incident"]["id"] == "INC-2048"

def test_investigation_and_experiment():
    a = client.post("/api/incidents/INC-2048/investigate")
    assert a.status_code == 200
    b = client.post("/api/incidents/INC-2048/experiment")
    assert b.status_code == 200
    assert b.json()["experiment"]["simulated"] is True

def test_human_decision_is_audited():
    r = client.post("/api/incidents/INC-2048/decision", json={"decision":"approved","note":"Reviewed the evidence and risk."})
    assert r.status_code == 200
    assert r.json()["decision"]["decision"] == "approved"
    assert any(x["kind"] == "decision.approved" for x in client.get("/api/audit").json())

def test_report_markdown():
    r = client.get("/api/incidents/INC-2048/report?format=markdown")
    assert r.status_code == 200
    assert "SIMULATION NOTICE" in r.text

def test_scenario_reset():
    assert client.post("/api/demo/scenario", json={"scenario":"payment_latency"}).status_code == 200
    assert client.post("/api/demo/reset").status_code == 200
