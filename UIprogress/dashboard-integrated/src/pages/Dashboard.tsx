import { useEffect, useState } from "react";
import LiveSessions from "../components/tables/LiveSessions";
import AttackDistribution from "../components/charts/AttackPieChart";
import ThreatTimeline from "../components/charts/ThreatTimeline";
import HoneypotHealth from "../components/cards/HoneypotHealth";
import DashboardLayout from "../layout/DashboardLayout";
import StatCard from "../components/cards/StatCard";
import Panel from "../components/Panel";

import useSessions from "../hooks/useSessions";
import useThreats from "../hooks/useThreats";
import useMonitoring from "../hooks/useMonitoring";
import useSettings from "../hooks/useSettings";

import {
  Shield,
  Activity,
  Bot,
  Server,
  Users,
} from "lucide-react";

function threatLevelLabel(score: number) {
  if (score >= 70) return { label: "CRITICAL", className: "text-red-400" };
  if (score >= 45) return { label: "HIGH", className: "text-orange-400" };
  if (score >= 25) return { label: "MEDIUM", className: "text-yellow-400" };
  return { label: "LOW", className: "text-green-400" };
}

export default function Dashboard() {
  const [time, setTime] = useState("");
  const { activeSessions, totalCommandsProcessed, isLive: sessionsLive } =
    useSessions();
  const { threatScore, isLive: threatsLive } = useThreats();
  const { honeypots, services, honeypotOnline } = useMonitoring();
  const { showLastUpdated } = useSettings();

  useEffect(() => {
    const updateTime = () => {
      setTime(
        new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);

    return () => clearInterval(interval);
  }, []);

  const threat = threatLevelLabel(threatScore);
  const isLive = sessionsLive || threatsLive;

  // Availability across everything the dashboard tracks (SSH honeypot +
  // whatever other services/honeypots are reporting in) - a genuine,
  // if simple, "System Health" figure instead of a hardcoded 98%.
  const allComponents = [...honeypots, ...services];
  const healthyCount = allComponents.filter(
    (c) => c.status !== "Offline"
  ).length;
  const healthPercent = allComponents.length
    ? Math.round((healthyCount / allComponents.length) * 100)
    : 100;
  const healthLabel =
    healthPercent >= 90 ? "Healthy" : healthPercent >= 60 ? "Degraded" : "Critical";

  return (
    <DashboardLayout>
      {/* CONTENT */}
      <div className="space-y-8">

        {/* STATUS BAR WITH GREEN GLOW HOVER */}
        <div
          className="
            flex
            items-center
            justify-between
            rounded-2xl
            border
            border-white/10
            bg-white/[0.045]
            backdrop-blur-2xl
            px-6
            py-4
            transition-all
            duration-300
            hover:border-green-500/30
            hover:bg-white/[0.06]
            hover:shadow-[0_0_25px_rgba(34,197,94,0.15)]
          "
        >
          <div className="flex items-center gap-4">
            <div
              className={`h-3 w-3 rounded-full animate-pulse ${
                honeypotOnline ? "bg-green-500" : "bg-gray-500"
              }`}
            />
            <div>
              <div
                className={`font-semibold ${
                  honeypotOnline ? "text-green-400" : "text-gray-400"
                }`}
              >
                {honeypotOnline ? "XYNERA ACTIVE" : isLive ? "XYNERA IDLE" : "DEMO MODE"}
              </div>
              {showLastUpdated && (
                <div className="text-sm text-gray-400">
                  Last Update: {time}
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-10 text-sm">
            <div>
              <span className="text-gray-500">Sessions</span>
              <span className="ml-2 font-semibold text-white">
                {activeSessions}
              </span>
            </div>
            <div>
              <span className="text-gray-500">Threat</span>
              <span className={`ml-2 font-semibold ${threat.className}`}>
                {threat.label}
              </span>
            </div>
            <div>
              <span className="text-gray-500">AI Decisions</span>
              <span className="ml-2 font-semibold text-blue-400">
                {totalCommandsProcessed}
              </span>
            </div>
            <div>
              <span className="text-gray-500">System</span>
              <span className="ml-2 font-semibold text-green-400">
                {healthLabel}
              </span>
            </div>
          </div>
        </div>

        {/* STAT CARDS */}
        <div className="grid grid-cols-5 gap-7 mt-2">
          <StatCard
            title="Active Sessions"
            value={String(activeSessions)}
            subtitle="Connected"
            icon={<Users />}
          />
          <StatCard
            title="Threat Level"
            value={threat.label}
            subtitle={`Score ${threatScore}`}
            icon={<Shield />}
          />
          <StatCard
            title="Threat Score"
            value={String(threatScore)}
            subtitle="Current"
            icon={<Activity />}
          />
          <StatCard
            title="AI Decisions"
            value={String(totalCommandsProcessed)}
            subtitle="Processed"
            icon={<Bot />}
          />
          <StatCard
            title="System Health"
            value={healthLabel}
            subtitle={`${healthPercent}%`}
            icon={<Server />}
          />
        </div>

        {/* MAIN GRID WITH CUSTOM GLOW ON PANELS */}
        <div className="grid grid-cols-12 gap-7 items-start">
          
          {/* Threat Timeline - Blue/Purple Glow */}
          <div className="col-span-8 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(59,130,246,0.12)]">
            <Panel title="Threat Timeline" className="h-[420px] transition-all duration-300 group-hover:border-blue-500/30">
              <ThreatTimeline />
            </Panel>
          </div>

          {/* Attack Distribution - Red Glow */}
          <div className="col-span-4 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(239,68,68,0.12)]">
            <Panel title="Attack Distribution" className="h-[420px] transition-all duration-300 group-hover:border-red-500/30">
              <AttackDistribution />
            </Panel>
          </div>
          
          <div className="col-span-12 h-2" />
          
          {/* Live Sessions - Neutral/Cyan Glow */}
          <div className="col-span-7 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(6,182,212,0.12)]">
            <Panel title="Live Sessions" className="h-[340px] transition-all duration-300 group-hover:border-cyan-500/30">
              <LiveSessions />
            </Panel>
          </div>

          {/* Honeypot Health - Emerald Glow */}
          <div className="col-span-5 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(16,185,129,0.12)]">
            <Panel title="Honeypot Health" className="h-[340px] transition-all duration-300 group-hover:border-emerald-500/30">
              <HoneypotHealth />
            </Panel>
          </div>
        </div>

      </div>
    </DashboardLayout>
  );
}
