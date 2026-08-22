import "./App.css";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Workspace from "./pages/Workspace";

export default function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<Workspace />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}