import type {Overview} from "./types";
const API = import.meta.env.VITE_API_URL || "http://localhost:8100";
async function request<T>(path:string, init?:RequestInit):Promise<T>{
  const response = await fetch(`${API}${path}`,{...init,headers:{"Content-Type":"application/json",...(init?.headers||{})}});
  if(!response.ok){let message = `Request failed (${response.status})`;try{const data=await response.json();message=data.detail||message}catch{}throw new Error(message)}
  return response.json();
}
export const api = {
  overview:()=>request<Overview>("/api/overview"),
  investigate:(id:string)=>request<any>(`/api/incidents/${id}/investigate`,{method:"POST"}),
  experiment:(id:string)=>request<any>(`/api/incidents/${id}/experiment`,{method:"POST"}),
  decide:(id:string,decision:"approved"|"rejected",note:string)=>request<any>(`/api/incidents/${id}/decision`,{method:"POST",body:JSON.stringify({decision,note})}),
  scenario:(scenario:string)=>request<any>("/api/demo/scenario",{method:"POST",body:JSON.stringify({scenario})}),
  reset:()=>request<any>("/api/demo/reset",{method:"POST"}),
  report:(id:string,format:"markdown"|"json")=>fetch(`${API}/api/incidents/${id}/report?format=${format}`)
};
