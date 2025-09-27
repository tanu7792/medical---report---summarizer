import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import ReportDetails from "./pages/ReportDetails";

export default function App() {
  return (
    <div style={{ padding: 20 }}>
      <nav>
        <Link to="/">Dashboard</Link>{" | "}
        <Link to="/upload">Upload</Link>{" | "}
        <Link to="/login">Login</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/reports/:id" element={<ReportDetails />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </div>
  );
}
