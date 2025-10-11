import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Login from "./pages/Login";
import ReportDetails from "./pages/ReportDetails";

export default function App(){
  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow p-4 flex justify-between">
        <div className="font-bold text-lg">Medical Report Summarizer</div>
        <div className="space-x-4">
          <Link to="/" className="text-sm">Dashboard</Link>
          <Link to="/upload" className="text-sm">Upload</Link>
          <Link to="/login" className="text-sm">Login</Link>
        </div>
      </nav>
      <main className="p-6"><Routes>
        <Route path="/" element={<Dashboard/>}/>
        <Route path="/upload" element={<Upload/>}/>
        <Route path="/reports/:id" element={<ReportDetails/>}/>
        <Route path="/login" element={<Login/>}/>
      </Routes></main>
    </div>
  );
}

frontend/src/services/api.js
import axios from "axios";
const API = axios.create({ baseURL: "http://127.0.0.1:8000/api/" });

export async function register(u,p,e){
  return API.post("auth/register/", {username:u,password:p,email:e});
}
export async function token(u,p){
  return API.post("auth/token/", {username:u,password:p});
}
export async function uploadReport(token, formData){
  return API.post("reports/", formData, { headers:{ Authorization:`Bearer ${token}`, "Content-Type":"multipart/form-data" }});
}
export async function listReports(token){
  return API.get("reports/", { headers:{ Authorization:`Bearer ${token}` }});
}
export async function getReport(token,id){
  return API.get(`reports/${id}/`, { headers:{ Authorization:`Bearer ${token}` }});
}
export async function summarizeReport(token, id){
  return API.post(`reports/${id}/summarize/`, {}, { headers:{ Authorization:`Bearer ${token}` }});
}
