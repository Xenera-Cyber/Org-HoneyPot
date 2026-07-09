import DashboardLayout from "../layout/DashboardLayout";
import Panel from "../components/Panel";
import { MonitoringProvider } from "../context/MonitoringContext";

import ResourceUsage from "../components/monitoring/ResourceUsage";
import LiveEventFeed from "../components/monitoring/LiveEventFeed";
import HoneypotStatus from "../components/monitoring/HoneypotStatus";
import ActiveServices from "../components/monitoring/ActiveServices";
import SystemUptime from "../components/monitoring/SystemUptime";

export default function Monitoring() {
  return (
    <DashboardLayout>
      <MonitoringProvider>
        <div className="space-y-7">

          {/* Header */}
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">
                Monitoring
              </h1>
              <p className="mt-1 text-gray-400">
                Live operational monitoring of XYNERA services
              </p>
            </div>

            {/* LIVE INDICATOR WITH HOVER GLOW */}
            <div
              className="
                flex
                items-center
                gap-3
                rounded-xl
                border
                border-green-500/20
                bg-green-500/10
                px-5
                py-3
                transition-all
                duration-300
                hover:border-green-400/40
                hover:bg-green-500/15
                hover:shadow-[0_0_20px_rgba(34,197,94,0.25)]
              "
            >
              <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse" />
              <span className="font-medium text-green-400">
                LIVE
              </span>
            </div>
          </div>

          {/* ================= SYSTEM HEALTH (Green Glow) ================= */}
          <div className="group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(34,197,94,0.12)]">
            <Panel
              title="System Health Overview"
              className="min-h-[170px] transition-all duration-300 group-hover:border-green-500/30"
            >
              <SystemUptime />
            </Panel>
          </div>

          {/* ================= ROW 1 ================= */}
          <div className="grid grid-cols-12 gap-6">
            
            {/* Resource Usage - Amber / Orange Glow */}
            <div className="col-span-4 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(245,158,11,0.12)]">
              <Panel
                title="Resource Usage"
                className="h-[360px] transition-all duration-300 group-hover:border-amber-500/30"
              >
                <ResourceUsage />
              </Panel>
            </div>

            {/* Live Event Feed - Blue Glow */}
            <div className="col-span-8 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(59,130,246,0.12)]">
              <Panel
                title="Live Event Feed"
                className="h-[360px] transition-all duration-300 group-hover:border-blue-500/30"
              >
                <LiveEventFeed />
              </Panel>
            </div>
          </div>

          {/* ================= ROW 2 ================= */}
          <div className="grid grid-cols-12 gap-6">
            
            {/* Honeypot Status - Emerald Glow */}
            <div className="col-span-6 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(16,185,129,0.12)]">
              <Panel
                title="Honeypot Status"
                className="h-[380px] transition-all duration-300 group-hover:border-emerald-500/30"
              >
                <HoneypotStatus />
              </Panel>
            </div>

            {/* Active Services - Cyan Glow */}
            <div className="col-span-6 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(6,182,212,0.12)]">
              <Panel
                title="Active Services"
                className="h-[380px] transition-all duration-300 group-hover:border-cyan-500/30"
              >
                <ActiveServices />
              </Panel>
            </div>
          </div>

        </div>
      </MonitoringProvider>
    </DashboardLayout>
  );
}