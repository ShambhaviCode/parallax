import {useState} from "react";
import {Check,ShieldAlert,X} from "lucide-react";
export default function Modal({mode,busy,onClose,onConfirm}:{mode:"approved"|"rejected";busy:boolean;onClose:()=>void;onConfirm:(note:string)=>void}) {
 const [note,setNote]=useState(mode==="approved"?"Reviewed evidence and blast radius. Approve guarded remediation proposal.":"The current evidence is insufficient. Request further investigation.");
 const approving=mode==="approved";
 return <div className="modal-backdrop" onMouseDown={onClose}><section className="decision-modal" onMouseDown={e=>e.stopPropagation()} role="dialog" aria-modal="true" aria-labelledby="decision-title">
  <button className="modal-x" onClick={onClose} aria-label="Close"><X size={18}/></button>
  <div className={`modal-symbol ${approving?"ok":"no"}`}>{approving?<Check size={21}/>:<ShieldAlert size={21}/>}</div>
  <div className="eyebrow">HUMAN DECISION GATE</div><h2 id="decision-title">{approving?"Approve recovery proposal?":"Reject recovery proposal?"}</h2>
  <p>{approving?"This records your approval in the incident audit trail. PARALLAX will not execute a production change.":"This records the rejection and preserves your reasoning for the incident review."}</p>
  <label htmlFor="decision-note">Decision note</label><textarea id="decision-note" value={note} onChange={e=>setNote(e.target.value)} maxLength={500}/>
  <div className="modal-actions"><button className="button secondary" onClick={onClose}>Cancel</button><button className={`button ${approving?"primary":"danger"}`} disabled={busy||note.trim().length<4} onClick={()=>onConfirm(note)}>{busy?"Recording…":approving?"Confirm approval":"Confirm rejection"}</button></div>
 </section></div>
}
