import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Monitoring from "./pages/Monitoring";
import Threats from "./pages/Threats";
import Sessions from "./pages/Sessions";
import Settings from "./pages/Settings";
import AIIntelligence from "./pages/AIIntelligence";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={<Navigate to="/dashboard" replace />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/monitoring"
          element={<Monitoring />}
        />

        <Route
          path="/threats"
          element={<Threats />}
        />

        <Route
          path="/sessions"
          element={<Sessions />}
        />

        {/* CORRECTED ROUTE PATH TO MATCH THE SIDEBAR LINK */}
        <Route
          path="/ai"
          element={<AIIntelligence />}
        />

        <Route
          path="/settings"
          element={<Settings />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;