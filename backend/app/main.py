from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from .config import APP_NAME, VERSION, CORS_ORIGINS
from .store import read_state, write_state, reset_state, init_db
from .engine import event, run_investigation, run_experiment, make_report

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(title=APP_NAME, version=VERSION, description="Evidence-led incident investigation demo API.", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=False, allow_methods=["GET","POST"], allow_headers=["*"])

class ScenarioRequest(BaseModel):
    scenario: str = Field(pattern="^(connection_exhaustion|payment_latency|inventory_errors|healthy)$")

class DecisionRequest(BaseModel):
    decision: str = Field(pattern="^(approved|rejected)$")
    note: str = Field(min_length=4, max_length=500)


def current_incident(state, incident_id):
    incident = next((i for i in state["incidents"] if i["id"] == incident_id), None)
    if not incident:
        raise HTTPException(404, "Incident not found")
    return incident

@app.get("/api/health")
def health():
    return {"status":"ok","service":"parallax-api","version":VERSION,"timestamp":datetime.now(timezone.utc).isoformat()}

@app.get("/api/overview")
def overview():
    state = read_state()
    incident = state["incidents"][0]
    healthy = sum(1 for s in state["services"] if s["status"] == "healthy")
    return {
        "product":"PARALLAX","workspace":"Acme Commerce","active_incidents":sum(i["status"] not in ("resolved","rejected") for i in state["incidents"]),
        "services_healthy":healthy,"services_total":len(state["services"]),"slo_compliance":99.92 if healthy == 4 else 98.71,
        "mean_latency_ms":round(sum(s["p95_ms"] for s in state["services"])/len(state["services"])),
        "services":state["services"],"incident":incident,"events":state["events"][:8]
    }

@app.get("/api/services")
def services():
    return read_state()["services"]

@app.get("/api/incidents")
def incidents():
    return read_state()["incidents"]

@app.get("/api/incidents/{incident_id}")
def incident_detail(incident_id: str):
    state = read_state()
    return current_incident(state, incident_id)

@app.post("/api/incidents/{incident_id}/investigate")
def investigate(incident_id: str):
    state = read_state()
    incident = current_incident(state, incident_id)
    result = run_investigation(state, incident)
    write_state(state)
    return {"ok":True,"result":result,"incident":incident}

@app.post("/api/incidents/{incident_id}/experiment")
def experiment(incident_id: str):
    state = read_state()
    incident = current_incident(state, incident_id)
    result = run_experiment(state, incident)
    write_state(state)
    return {"ok":True,"experiment":result,"incident":incident}

@app.post("/api/incidents/{incident_id}/decision")
def decision(incident_id: str, body: DecisionRequest):
    state = read_state()
    incident = current_incident(state, incident_id)
    incident["decision"] = {"decision":body.decision,"note":body.note,"by":"Human operator","at":datetime.now(timezone.utc).isoformat()}
    incident["status"] = "approved" if body.decision == "approved" else "rejected"
    event(state,"human-operator",f"decision.{body.decision}",f"{body.decision.title()} recovery proposal for {incident_id}: {body.note}")
    write_state(state)
    return {"ok":True,"decision":incident["decision"]}

@app.get("/api/incidents/{incident_id}/report")
def report(incident_id: str, format: str = Query(default="json", pattern="^(json|markdown)$")):
    state = read_state()
    incident = current_incident(state, incident_id)
    data = make_report(incident,state["events"])
    if format == "json":
        return JSONResponse(data, headers={"Content-Disposition":f'attachment; filename="{incident_id}-report.json"'})
    h = incident["hypotheses"]
    lines = [
        f"# PARALLAX Incident Report · {incident_id}","",
        f"**Title:** {incident['title']}  ",
        f"**Severity:** {incident['severity']}  ",
        f"**Status:** {incident['status']}  ",
        f"**Generated:** {data['generated_at']}","",
        "> SIMULATION NOTICE: telemetry and experiment results are simulated. No production change was made.","",
        "## Impact",incident["impact"],"",
        "## Root-cause hypotheses"
    ]
    for item in h:
        lines += [f"### {item['id']} · {item['title']} ({item['score']:.0%} heuristic evidence score)",item["interpretation"],"**Supporting evidence**"] + [f"- {x}" for x in item["for"]] + ["**Counter-evidence**"] + [f"- {x}" for x in item["against"]] + [""]
    if incident.get("experiment"):
        ex = incident["experiment"]
        lines += ["## Counterfactual experiment",ex["method"],"",f"- Stock p95: {ex['before']['stock_p95_ms']} ms → {ex['after']['stock_p95_ms']} ms",f"- Acquisition wait: {ex['before']['acquisition_wait_ms']} ms → {ex['after']['acquisition_wait_ms']} ms",ex["interpretation"],""]
    rec = incident["recommendation"]
    lines += ["## Recovery proposal",f"**{rec['title']}**",rec["rationale"],""] + [f"{i+1}. {s}" for i,s in enumerate(rec["steps"])] + [""]
    decision_data = incident.get("decision")
    lines += ["## Human decision",f"**{decision_data['decision'].upper()}**" if decision_data else "Pending human review",decision_data["note"] if decision_data else "No decision recorded.",""]
    return PlainTextResponse("\n".join(lines), media_type="text/markdown", headers={"Content-Disposition":f'attachment; filename="{incident_id}-report.md"'})

@app.get("/api/audit")
def audit():
    return read_state()["events"]

@app.post("/api/demo/scenario")
def scenario(body: ScenarioRequest):
    state = read_state()
    services = {s["id"]:s for s in state["services"]}
    if body.scenario == "connection_exhaustion":
        services["stock"].update(status="degraded",p95_ms=2840,error_rate=18.6,cpu=76)
        services["edge"].update(status="degraded",p95_ms=540,error_rate=8.2)
        services["basket"].update(status="degraded",p95_ms=610,error_rate=5.4)
        message = "Connection-pool exhaustion scenario activated."
    elif body.scenario == "payment_latency":
        services["payments"].update(status="degraded",p95_ms=1480,error_rate=9.1,cpu=88)
        services["edge"].update(status="degraded",p95_ms=690,error_rate=6.2)
        message = "Payment latency scenario activated."
    elif body.scenario == "inventory_errors":
        services["stock"].update(status="degraded",p95_ms=420,error_rate=26.4,cpu=64)
        services["edge"].update(status="degraded",p95_ms=380,error_rate=9.8)
        message = "Stock Engine error-spike scenario activated."
    else:
        for service in state["services"]:
            service.update(status="healthy")
        services["edge"].update(p95_ms=42,error_rate=.2)
        services["basket"].update(p95_ms=68,error_rate=.4)
        services["stock"].update(p95_ms=74,error_rate=.3,cpu=38)
        services["payments"].update(p95_ms=91,error_rate=.7,cpu=52)
        message = "Healthy baseline restored."
    incident = state["incidents"][0]
    if body.scenario == "healthy":
        incident["status"] = "resolved"
    else:
        incident["status"] = "investigating"
        incident["decision"] = None
    event(state,"demo-controller","scenario.changed",message)
    write_state(state)
    return {"ok":True,"message":message,"services":state["services"]}

@app.post("/api/demo/reset")
def reset():
    state = reset_state()
    event(state,"demo-controller","demo.reset","Demo workspace reset to the seeded incident.")
    write_state(state)
    return {"ok":True,"message":"Demo workspace reset.","overview":state}
