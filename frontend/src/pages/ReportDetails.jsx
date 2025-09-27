import React, {useEffect, useState} from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { summarizeReport } from "../services/api";

export default function ReportDetails(){
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [summary, setSummary] = useState("");
  const token = localStorage.getItem("token") || "";

  useEffect(()=>{
    async function load(){
      try{
        const res = await axios.get(`http://localhost:8000/api/reports/${id}/`, { headers:{ Authorization:`Bearer ${token}` }});
        setReport(res.data);
      }catch(e){ console.error(e); }
    }
    load();
  },[id]);

  const handleSumm = async ()=>{
    try{
      const res = await summarizeReport(token, id);
      setSummary(res.data.summary);
    }catch(e){ console.error(e); }
  };

  return (
    <div>
      <h2>Report</h2>
      <pre>{report ? report.extracted_text || "No text extracted" : "Loading..."}</pre>
      <button onClick={handleSumm}>Summarize</button>
      <h3>Summary</h3>
      <pre>{summary}</pre>
    </div>
  );
}
