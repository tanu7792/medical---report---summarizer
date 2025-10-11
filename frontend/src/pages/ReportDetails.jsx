import React, {useEffect, useState} from "react";
import { useParams } from "react-router-dom";
import axios from "axios";
import { createSummary } from "../services/api";

export default function ReportDetails(){
  const { id } = useParams();
  const [report,setReport]=useState(null);
  const [summary,setSummary]=useState(null);
  const token = localStorage.getItem("token")||"";
  useEffect(()=>{
    if(!token) return;
    axios.get(`http://127.0.0.1:8000/api/reports/${id}/`, { headers: { Authorization: `Bearer ${token}`}}).then(r=>setReport(r.data)).catch(()=>{});
  },[id]);
  const handleSumm=async()=>{
    try{
      const res = await createSummary(token, id);
      setSummary(res.data);
    }catch(e){console.error(e); alert("Summarize failed") }
  };
  return (
    <div className="max-w-4xl mx-auto bg-white p-6 shadow rounded">
      <h2 className="text-xl mb-4">Report</h2>
      <pre className="whitespace-pre-wrap bg-gray-50 p-4">{report ? (report.extracted_text || "No text extracted") : "Loading..."}</pre>
      <button className="mt-4 bg-indigo-600 text-white px-4 py-2 rounded" onClick={handleSumm}>Summarize & Analyze</button>
      {summary && (
        <div className="mt-6">
          <h3 className="text-lg">Summary</h3>
          <pre className="whitespace-pre-wrap bg-gray-50 p-4">{summary.summary_text}</pre>
          <h3 className="mt-4">Analysis</h3>
          <pre className="whitespace-pre-wrap bg-gray-50 p-4">{JSON.stringify(summary.analysis_parsed||summary.analysis_text, null, 2)}</pre>
          <h3 className="mt-4">Predicted Diseases</h3>
          <pre className="whitespace-pre-wrap bg-gray-50 p-4">{JSON.stringify(summary.predicted_diseases_parsed, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
