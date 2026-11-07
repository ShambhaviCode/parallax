import {Server} from "lucide-react";
import type {Service} from "../types";
export default function Topology({services,onSelect}:{services:Service[];onSelect:(s:Service)=>void}) {
 const coords:Record<string,[number,number]>={edge:[12,50],basket:[43,23],stock:[43,77],payments:[80,50]};
 const nodes=services.map(s=>({...s,point:coords[s.id]||[50,50]}));
 return <div className="topology">
  <svg className="topology-lines" viewBox="0 0 600 260" preserveAspectRatio="none" aria-label="Service dependency paths">
   <path d="M95 130 C160 130 180 60 258 60"/><path d="M95 130 C160 130 180 200 258 200"/><path d="M95 130 L480 130"/><path d="M258 60 C350 60 380 130 480 130"/><path d="M258 200 C350 200 380 130 480 130"/>
  </svg>
  {nodes.map(s=><button key={s.id} className={`topo-node ${s.status}`} style={{left:`${s.point[0]}%`,top:`${s.point[1]}%`}} onClick={()=>onSelect(s)}><span className="topo-icon"><Server size={15}/></span><b>{s.name}</b><small><i/> {s.status==="healthy"?"Healthy":"Degraded"} · {s.p95_ms}ms</small></button>)}
 </div>
}
