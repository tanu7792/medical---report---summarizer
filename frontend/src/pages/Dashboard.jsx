import React, {useState, useEffect} from "react";
import { listReports } from "../services/api";
import { Link } from "react-router-dom";

export default function Dashboard(){
  const [reports,setReports]=useState([]);
  const token = localStorage.getItem("token")||"";
  useEffect(()=>{ if(!token) return; listReports(token).then(r=>setReports(r.data)).catch(()=>{}); },[]);
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {reports.map(r=>(
        <div className="bg-white p-4 shadow rounded" key={r.id}>
          <div className="font-semibold">{r.title || r.original_file}</div>
          <div className="text-sm text-gray-500">{new Date(r.uploaded_at).toLocaleString()}</div>
          <div className="mt-2 space-x-2">
            <Link to={`/reports/${r.id}`} className="text-blue-600">View</Link>
          </div>
        </div>
      ))}
    </div>
  );
}
