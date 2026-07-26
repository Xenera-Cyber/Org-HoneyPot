import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Monitoring from "./pages/Monitoring";
import Threats from "./pages/Threats";
import Sessions from "./pages/Sessions";
import Settings from "./pages/Settings";
import AIIntelligence from "./pages/AIIntelligence";

import { SettingsProvider } from "./context/SettingsContext";
import { SessionProvider } from "./context/SessionContext";
import { MonitoringProvider } from "./context/MonitoringContext";
import { ThreatProvider } from "./context/ThreatContext";
import { AIProvider } from "./context/AIContext";
import NotificationWatcher from "./components/NotificationWatcher";
import SessionLockOverlay from "./components/SessionLockOverlay";

// All data providers live here, above the router, instead of each page
// mounting (and un-mounting/resetting) its own copy. That means:
//  - Settings (theme, refresh rate, feature toggles) apply everywhere.
//  - Session/Monitoring/Threat/AI polling keeps running - and keeps its
//    data - as you navigate between pages, instead of restarting from
//    demo data on every route change.
function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SettingsProvider>
      <SessionProvider>
        <MonitoringProvider>
          <ThreatProvider>
            <AIProvider>
              <NotificationWatcher />
              <SessionLockOverlay />
              {children}
            </AIProvider>
          </ThreatProvider>
        </MonitoringProvider>
      </SessionProvider>
    </SettingsProvider>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Providers>
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
      </Providers>
    </BrowserRouter>
  );
}

export default App;
