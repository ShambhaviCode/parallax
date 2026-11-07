from datetime import datetime, timezone
from uuid import uuid4

def stamp():
    return datetime.now(timezone.utc).isoformat()

def event(state, actor, kind, message):
    item = {"id":f"EV-{uuid4().hex[:8].upper()}","at":stamp(),"actor":actor,"kind":kind,"message":message}
    state["events"].insert(0,item)
    state["events"] = state["events"][:100]
    return item

def run_investigation(state, incident):
    incident["last_investigated_at"] = stamp()
    incident["status"] = "investigating"
    event(state,"parallax-investigator","investigation.completed","Evidence review refreshed; three hypotheses retained with counter-evidence.")
    return {
        "summary":"Connection acquisition wait remains the strongest explanation. Payment degradation is not supported by current signals.",
        "leading_hypothesis":"H-01",
        "agents":[
            {"name":"Signal analyst","role":"Telemetry correlation","status":"complete","finding":"Pool utilization and queue wait rose together before upstream checkout errors."},
            {"name":"Trace analyst","role":"Dependency-path review","status":"complete","finding":"Slow spans originate in Stock Engine; Payments remains within baseline."},
            {"name":"Causal critic","role":"Counter-hypothesis review","status":"complete","finding":"A slow query is plausible but does not explain stable execution time after acquisition."}
        ]
    }

def run_experiment(state, incident):
    before = {"pool_limit":40,"pool_utilization":98,"acquisition_wait_ms":1240,"stock_p95_ms":2840,"checkout_error_rate":8.2}
    after = {"pool_limit":64,"pool_utilization":74,"acquisition_wait_ms":310,"stock_p95_ms":910,"checkout_error_rate":2.1}
    result = {
        "id":f"EXP-{uuid4().hex[:6].upper()}",
        "label":"Bounded pool-capacity counterfactual",
        "method":"Deterministic simulation: vary pool capacity while holding request load and query profile constant.",
        "before":before,"after":after,
        "interpretation":"The modeled acquisition wait and upstream error rate both fall when capacity increases. This supports H-01, but does not prove a production change is safe.",
        "supports":"H-01",
        "created_at":stamp(),
        "simulated":True
    }
    incident["experiment"] = result
    event(state,"counterfactual-lab","experiment.completed","Pool capacity counterfactual supports H-01 in the simulated environment.")
    return result

def make_report(incident, events):
    return {
        "product":"PARALLAX",
        "report_version":"1.0",
        "generated_at":stamp(),
        "simulation_notice":"This report contains simulated telemetry and modeled experiment results. No production system was changed.",
        "incident":incident,
        "related_events":[e for e in events if incident["id"] in e["message"] or e["kind"].startswith(("incident","investigation","experiment","decision"))][:30]
    }
