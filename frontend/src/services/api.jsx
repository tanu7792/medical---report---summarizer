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

