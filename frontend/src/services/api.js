import axios from "axios";
const API = axios.create({ baseURL: "http://127.0.0.1:8000/api/" });

export async function register(u,p,e){
  return axios.post("http://127.0.0.1:8000/api/auth/register/", {username:u,password:p,email:e});
}
export async function token(u,p){
  return axios.post("http://127.0.0.1:8000/api/auth/token/", {username:u,password:p});
}
export async function uploadReport(token, formData){
  return API.post("reports/", formData, { headers: { Authorization: `Bearer ${token}`, "Content-Type":"multipart/form-data" }});
}
export async function listReports(token){
  return API.get("reports/", { headers: { Authorization: `Bearer ${token}` }});
}
export async function createSummary(token, reportId){
  return API.post("summaries/", { report: reportId }, { headers: { Authorization: `Bearer ${token}` }});
}
export async function listSummaries(token){ return API.get("summaries/", { headers: { Authorization: `Bearer ${token}` } });}
import axios from "axios";
const API = axios.create({ baseURL: "http://127.0.0.1:8000/api/" });

export async function register(u,p,e){
  return axios.post("http://127.0.0.1:8000/api/auth/register/", {username:u,password:p,email:e});
}
export async function token(u,p){
  return axios.post("http://127.0.0.1:8000/api/auth/token/", {username:u,password:p});
}
export async function uploadReport(token, formData){
  return API.post("reports/", formData, { headers: { Authorization: `Bearer ${token}`, "Content-Type":"multipart/form-data" }});
}
export async function listReports(token){
  return API.get("reports/", { headers: { Authorization: `Bearer ${token}` }});
}
export async function createSummary(token, reportId){
  return API.post("summaries/", { report: reportId }, { headers: { Authorization: `Bearer ${token}` }});
}
export async function listSummaries(token){ return API.get("summaries/", { headers: { Authorization: `Bearer ${token}` } });}
