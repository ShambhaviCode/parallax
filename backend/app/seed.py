from datetime import datetime, timezone

def seed_state():
    now = datetime.now(timezone.utc).isoformat()
    services = [
        {"id":"edge","name":"Edge Gateway","kind":"edge","status":"healthy","p95_ms":42,"error_rate":0.2,"cpu":31,"memory":48,"depends_on":["basket","stock","payments"],"requests_per_min":18420},
        {"id":"basket","name":"Basket API","kind":"service","status":"healthy","p95_ms":68,"error_rate":0.4,"cpu":44,"memory":57,"depends_on":["stock"],"requests_per_min":7210},
        {"id":"stock","name":"Stock Engine","kind":"service","status":"degraded","p95_ms":2840,"error_rate":18.6,"cpu":76,"memory":69,"depends_on":[],"requests_per_min":6890},
        {"id":"payments","name":"Payments","kind":"service","status":"healthy","p95_ms":91,"error_rate":0.7,"cpu":52,"memory":61,"depends_on":[],"requests_per_min":4230},
    ]
    incident = {
        "id":"INC-2048",
        "title":"Inventory latency is cascading into checkout",
        "severity":"critical",
        "status":"investigating",
        "service_id":"stock",
        "service_name":"Stock Engine",
        "started_at":now,
        "duration":"18 min",
        "impact":"Checkout p95 is elevated; an estimated 23.8% of checkout requests are affected.",
        "summary":"The Stock Engine is acquiring database connections more slowly than it can release them. Queue wait has increased, and upstream checkout requests are accumulating.",
        "signals":[
            {"id":"SIG-01","label":"Stock Engine p95","value":"2.84 s","delta":"+684%","severity":"critical","source":"service.metrics.p95"},
            {"id":"SIG-02","label":"Checkout error rate","value":"8.2%","delta":"+7.6 pp","severity":"critical","source":"edge.metrics.http_5xx"},
            {"id":"SIG-03","label":"DB pool utilization","value":"98%","delta":"+41 pp","severity":"warning","source":"stock.db.pool_in_use"},
            {"id":"SIG-04","label":"Payment p95","value":"91 ms","delta":"within baseline","severity":"healthy","source":"payments.metrics.p95"}
        ],
        "timeline":[
            {"time":"14:02:11","kind":"deploy","title":"Release v2.8.1 completed","detail":"Stock Engine rollout reached 100%."},
            {"time":"14:05:34","kind":"alert","title":"Latency SLO breached","detail":"Stock Engine p95 crossed the 800 ms threshold."},
            {"time":"14:07:02","kind":"impact","title":"Checkout degradation detected","detail":"Edge Gateway 5xx rate increased to 8.2%."},
            {"time":"14:11:48","kind":"signal","title":"Connection pool saturation observed","detail":"98% of 40 available database connections are in use."}
        ],
        "hypotheses":[
            {"id":"H-01","title":"Stock DB connection pool exhaustion","score":0.86,"status":"leading","for":["Pool utilization reached 98%.","Queue wait increased 11× during the incident.","Latency spike follows the v2.8.1 rollout."],"against":["Database CPU remains below its saturation threshold."],"interpretation":"Strongest fit: acquisition wait explains the latency while stable query execution weakens the slow-query theory."},
            {"id":"H-02","title":"A slow query introduced in v2.8.1","score":0.61,"status":"plausible","for":["Deployment preceded the incident by three minutes.","Stock query p95 increased."],"against":["Query execution time is stable after a connection is acquired."],"interpretation":"The release is temporally correlated, but query execution itself does not explain most of the wait."},
            {"id":"H-03","title":"Payments degradation is backing up checkout","score":0.14,"status":"unlikely","for":["Checkout includes a payment dependency."],"against":["Payment p95 and error rate remain close to baseline."],"interpretation":"The dependency exists, but the observed payment signals do not support it as the initiating fault."}
        ],
        "experiment":None,
        "recommendation":{
            "title":"Increase the Stock Engine connection pool",
            "change":"Proposed change: max pool size 40 → 64",
            "risk":"low",
            "expected":"55–70% lower Stock Engine p95",
            "rationale":"If acquisition queueing is the dominant contributor, a bounded increase in available connections should reduce wait time. Monitor database active connections to avoid shifting the bottleneck.",
            "steps":["Raise the pool limit to 64 in a controlled environment.","Observe active DB connections and acquisition wait for three minutes.","Confirm checkout p95 returns below 500 ms; revert if DB saturation rises."]
        },
        "decision":None,
        "last_investigated_at":None
    }
    events = [
        {"id":"EV-001","at":now,"actor":"telemetry-watch","kind":"incident.detected","message":"Stock Engine p95 exceeded the incident threshold."},
        {"id":"EV-002","at":now,"actor":"impact-analyzer","kind":"impact.mapped","message":"Checkout path identified as the affected upstream journey."},
        {"id":"EV-003","at":now,"actor":"hypothesis-engine","kind":"hypotheses.ranked","message":"Three competing root-cause hypotheses ranked against available signals."}
    ]
    return {"services":services,"incidents":[incident],"events":events}
