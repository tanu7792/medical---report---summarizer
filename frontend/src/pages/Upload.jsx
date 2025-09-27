import React, {useState} from "react";
import { uploadReport } from "../services/api";

export default function Upload(){
  const [file,setFile] = useState(null);
  const [token,setToken] = useState(localStorage.getItem("token") || "");

  const submit = async (e)=>{
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
    <div>
      <h2>Upload Report</h2>
      <input type="text" placeholder="Token" value={token} onChange={e=>setToken(e.target.value)} />
      <input type="file" onChange={e=>setFile(e.target.files[0])} />
      <button onClick={submit}>Upload</button>
    </div>
  );
}
