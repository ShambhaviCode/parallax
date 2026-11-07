import {useState} from "react";
import Landing from "./components/Landing";
import Console from "./components/Console";
export default function App(){
 const [screen,setScreen]=useState<"landing"|"console">("landing");
 return screen==="landing"?<Landing onLaunch={()=>{setScreen("console");window.scrollTo(0,0)}}/>:<Console onExit={()=>{setScreen("landing");window.scrollTo(0,0)}}/>;
}
