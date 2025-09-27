import React, {useState} from "react";
import { login } from "../services/api";

export default function Login(){
  const [u,setU] = useState(""); const [p,setP] = useState("");
  const [token,setToken] = useState(null);

  const handle = async (e) => {
    e.preventDefault();
    try{
      const res = await login(u,p);
      setToken(res.data.access);
      // record device
      await fetch("http://localhost:8000/api/devices/record/", {
        method:"POST",
        headers:{ "Content-Type":"application/json", "Authorization": `Bearer ${res.data.access}` },
        body: JSON.stringify({
          user_agent: navigator.userAgent,
          platform: navigator.platform,
          screen_width: window.screen.width,
          screen_height: window.screen.height,
          timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
        })
      });
      alert("Logged in and device recorded. Save token in app state for next calls.");
    }catch(e){
      alert("Login failed");
    }
  };

  return (
    <form onSubmit={handle}>
      <h2>Login</h2>
      <input value={u} onChange={e=>setU(e.target.value)} placeholder="username" />
      <input type="password" value={p} onChange={e=>setP(e.target.value)} placeholder="password" />
      <button type="submit">Login</button>
    </form>
  );
}
