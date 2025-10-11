import React, {useState} from "react";
import { uploadReport } from "../services/api";

export default function Upload(){
  const [file,setFile]=useState(null);
  const token = localStorage.getItem("token") || "";
  const submit = async (e) => {
    e.preventDefault();
    if(!file) return alert("select file");
    const fd = new FormData();
    fd.append("original_file", file);
    fd.append("title", file.name);
    try{
      const res = await uploadReport(token, fd);
      alert("Uploaded: " + res.data.id);
    }catch(err){ console.error(err); alert("Upload failed") }
  };
  return (
    <div className="max-w-2xl mx-auto bg-white p-6 shadow rounded">
      <h2 className="text-lg mb-4">Upload Report</h2>
      <input type="file" onChange={e=>setFile(e.target.files[0])} className="mb-4" />
      <button onClick={submit} className="bg-green-600 text-white px-4 py-2 rounded">Upload</button>
    </div>
  );
}
