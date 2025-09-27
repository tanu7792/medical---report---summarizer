import React, {useEffect, useState} from "react";
import { listReports } from "../services/api";
import { Link } from "react-router-dom";

export default function Dashboard(){
  const [reports,setReports] = useState([]);
  const token= localStorage.getItem("token") || "";

  useEffect(()=>{
    async function load(){
      try{
        const res = await listReports(token);
        setReports(res.data);
      }catch(e){ console.error(e) }
    }
    load();
  },[]);

  return (
    <div>
      <h2>Reports</h2>
      <ul>
        {reports.map(r => (
          <li key={r.id}>
            <Link to={`/reports/${r.id}`}>{r.title || r.original_file}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
