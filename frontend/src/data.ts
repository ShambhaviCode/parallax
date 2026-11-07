import type {Overview} from "./types";
export const fallback:Overview = {
 product:"PARALLAX",workspace:"Acme Commerce",active_incidents:1,services_healthy:1,services_total:4,slo_compliance:98.71,mean_latency_ms:1010,
 services:[
  {id:"edge",name:"Edge Gateway",kind:"edge",status:"degraded",p95_ms:540,error_rate:8.2,cpu:31,memory:48,depends_on:["basket","stock","payments"],requests_per_min:18420},
  {id:"basket",name:"Basket API",kind:"service",status:"degraded",p95_ms:610,error_rate:5.4,cpu:44,memory:57,depends_on:["stock"],requests_per_min:7210},
  {id:"stock",name:"Stock Engine",kind:"service",status:"degraded",p95_ms:2840,error_rate:18.6,cpu:76,memory:69,depends_on:[],requests_per_min:6890},
  {id:"payments",name:"Payments",kind:"service",status:"healthy",p95_ms:91,error_rate:.7,cpu:52,memory:61,depends_on:[],requests_per_min:4230}
 ],
 incident:{
  id:"INC-2048",title:"Inventory latency is cascading into checkout",severity:"critical",status:"investigating",service_id:"stock",service_name:"Stock Engine",duration:"18 min",impact:"Checkout p95 is elevated; an estimated 23.8% of checkout requests are affected.",summary:"The Stock Engine is acquiring database connections more slowly than it can release them. Queue wait has increased, and upstream checkout requests are accumulating.",
  signals:[{id:"SIG-01",label:"Stock Engine p95",value:"2.84 s",delta:"+684%",severity:"critical"},{id:"SIG-02",label:"Checkout error rate",value:"8.2%",delta:"+7.6 pp",severity:"critical"},{id:"SIG-03",label:"DB pool utilization",value:"98%",delta:"+41 pp",severity:"warning"},{id:"SIG-04",label:"Payment p95",value:"91 ms",delta:"baseline",severity:"healthy"}],
  timeline:[{time:"14:02:11",kind:"deploy",title:"Release v2.8.1 completed",detail:"Stock Engine rollout reached 100%."},{time:"14:05:34",kind:"alert",title:"Latency SLO breached",detail:"Stock Engine p95 crossed 800 ms."},{time:"14:07:02",kind:"impact",title:"Checkout degradation detected",detail:"Edge Gateway 5xx rate reached 8.2%."},{time:"14:11:48",kind:"signal",title:"Connection pool saturation",detail:"98% of 40 database connections are in use."}],
  hypotheses:[
   {id:"H-01",title:"Stock DB connection pool exhaustion",score:.86,status:"leading",for:["Pool utilization reached 98%.","Queue wait increased 11× during the incident.","Latency spike follows v2.8.1."],against:["Database CPU remains below saturation."],interpretation:"Acquisition wait explains the latency while stable query execution weakens the slow-query theory."},
   {id:"H-02",title:"A slow query introduced in v2.8.1",score:.61,status:"plausible",for:["Deployment preceded the incident by three minutes."],against:["Query execution time is stable after connection acquisition."],interpretation:"The release is temporally correlated, but query execution does not explain most of the wait."},
   {id:"H-03",title:"Payments degradation backing up checkout",score:.14,status:"unlikely",for:["Checkout includes a payment dependency."],against:["Payment p95 and error rate remain close to baseline."],interpretation:"The dependency exists, but current payment signals do not support it as the initiating fault."}
  ],
  experiment:null,
  recommendation:{title:"Increase the Stock Engine connection pool",change:"Max pool size 40 → 64",risk:"low",expected:"55–70% lower Stock Engine p95",rationale:"If acquisition queueing is dominant, a bounded capacity increase should reduce wait time. Monitor active database connections to avoid shifting the bottleneck.",steps:["Raise the pool limit to 64 in a controlled environment.","Observe active DB connections and acquisition wait for three minutes.","Confirm checkout p95 returns below 500 ms; revert if DB saturation rises."]},
  decision:null
 },
 events:[{id:"EV-001",actor:"telemetry-watch",kind:"incident.detected",message:"Stock Engine p95 exceeded the incident threshold."},{id:"EV-002",actor:"impact-analyzer",kind:"impact.mapped",message:"Checkout path identified as affected."},{id:"EV-003",actor:"hypothesis-engine",kind:"hypotheses.ranked",message:"Three competing hypotheses ranked against available signals."}]
 }
