import React, {useState} from "react";
import { token } from "../services/api";

export default function Login(){
  const [u,setU]=useState(""), [p,setP]=useState("");
  const handle=async(e)=>{ e.preventDefault(); try{ const res=await token(u,p); localStorage.setItem("token", res.data.access); alert("Logged in"); }catch(err){alert("Login failed")} }
  return (
    <form onSubmit={handle} className="max-w-md mx-auto mt-8 p-6 bg-white shadow rounded">
      <h2 className="text-xl mb-4">Login</h2>
      <input className="border p-2 w-full mb-2" placeholder="username" value={u} onChange={e=>setU(e.target.value)} />
      <input type="password" className="border p-2 w-full mb-2" placeholder="password" value={p} onChange={e=>setP(e.target.value)} />
      <button className="bg-blue-600 text-white px-4 py-2 rounded">Login</button>
    </form>
  );
}
