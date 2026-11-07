export type Service = {id:string;name:string;kind:string;status:string;p95_ms:number;error_rate:number;cpu:number;memory:number;depends_on:string[];requests_per_min:number};
export type Hypothesis = {id:string;title:string;score:number;status:string;for:string[];against:string[];interpretation:string};
export type Incident = {id:string;title:string;severity:string;status:string;service_id:string;service_name:string;duration:string;impact:string;summary:string;signals:any[];timeline:any[];hypotheses:Hypothesis[];experiment:any;recommendation:any;decision:any};
export type Overview = {product:string;workspace:string;active_incidents:number;services_healthy:number;services_total:number;slo_compliance:number;mean_latency_ms:number;services:Service[];incident:Incident;events:any[]};
