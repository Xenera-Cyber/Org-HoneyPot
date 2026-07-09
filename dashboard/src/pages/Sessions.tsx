import DashboardLayout from "../layout/DashboardLayout";
import Panel from "../components/Panel";

import { SessionProvider } from "../context/SessionContext";
import useSessions from "../hooks/useSessions";

import SessionStatCard from "../components/Sessions/SessionStatCard";
import GeographicVisualization from "../components/Sessions/GeographicVisualization";
import SessionActivityChart from "../components/Sessions/SessionActivityChart";

// IMPORTED ICONS
import {
  Activity,
  Clock3,
  Flag,
  Brain,
  Sparkles,
  ShieldAlert,
  Gauge,
  Cpu,
} from "lucide-react";

function SessionContent() {
  // DESTRUCTURED ALL VALUES FROM HOOK
  const {
    activeSessions,
    totalToday,
    averageDuration,
    aiFlagged,
    aiDecision,
    aiConfidence,
    predictedAttack,
    responseTime,
  } = useSessions();

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold text-white">
          Sessions
        </h1>
        <p className="mt-1 text-gray-400">
          Live Honeypot Session Monitoring
        </p>
      </div>

      {/* TOP STAT CARDS WITH DYNAMIC GLOW HOVER EFFECTS & EQUAL HEIGHTS */}
      <div className="grid grid-cols-4 gap-6 items-stretch">
        
        {/* Active Sessions - Cyan Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(6,182,212,0.15)] border border-transparent hover:border-cyan-500/30">
          <SessionStatCard
            title="Active Sessions"
            value={`${activeSessions}`}
            subtitle="Currently Connected"
            color="text-cyan-400"
            icon={<Activity size={34} />}
          />
        </div>

        {/* Total Today - Green Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(34,197,94,0.15)] border border-transparent hover:border-green-500/30">
          <SessionStatCard
            title="Total Today"
            value={`${totalToday}`}
            subtitle="Past 24 Hours"
            color="text-green-400"
            icon={<Flag size={34} />}
          />
        </div>

        {/* Average Duration - Orange Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(249,115,22,0.15)] border border-transparent hover:border-orange-500/30">
          <SessionStatCard
            title="Average Duration"
            value={`${averageDuration}m`}
            subtitle="Per Session"
            color="text-orange-400"
            icon={<Clock3 size={34} />}
          />
        </div>

        {/* AI Flagged - Red Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(239,68,68,0.15)] border border-transparent hover:border-red-500/30">
          <SessionStatCard
            title="AI Flagged"
            value={`${aiFlagged}`}
            subtitle="High Risk"
            color="text-red-400"
            icon={<Brain size={34} />}
          />
        </div>

        {/* Current AI Decision - Cyan Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(6,182,212,0.15)] border border-transparent hover:border-cyan-500/30">
          <SessionStatCard
            title="Current AI Decision"
            value={aiDecision}
            subtitle="Current Classification"
            color="text-cyan-400"
            icon={<Sparkles size={34} />}
          />
        </div>

        {/* AI Confidence - Green Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(34,197,94,0.15)] border border-transparent hover:border-green-500/30">
          <SessionStatCard
            title="AI Confidence"
            value={`${aiConfidence}%`}
            subtitle="Decision Confidence"
            color="text-green-400"
            icon={<Gauge size={34} />}
          />
        </div>

        {/* Predicted Next Attack - Orange Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(249,115,22,0.15)] border border-transparent hover:border-orange-500/30">
          <SessionStatCard
            title="Predicted Next Attack"
            value={predictedAttack}
            subtitle="AI Prediction"
            color="text-orange-400"
            icon={<ShieldAlert size={34} />}
          />
        </div>

        {/* Response Time - Purple Glow */}
        <div className="group h-full transition-all duration-300 rounded-xl hover:shadow-[0_0_25px_rgba(168,85,247,0.15)] border border-transparent hover:border-purple-500/30">
          <SessionStatCard
            title="Response Time"
            value={`${responseTime} ms`}
            subtitle="Inference Latency"
            color="text-purple-400"
            icon={<Cpu size={34} />}
          />
        </div>
      </div>

      {/* BOTTOM VISUALIZATION PANELS */}
      <div className="grid grid-cols-12 gap-6">
        
        {/* Geographic Visualization - Cyan Glow */}
        <div className="col-span-8 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(6,182,212,0.12)]">
          <Panel
            title="Geographic Visualization"
            className="h-[500px] transition-all duration-300 group-hover:border-cyan-500/30"
          >
            <GeographicVisualization />
          </Panel>
        </div>

        {/* Session Activity - Purple Glow */}
        <div className="col-span-4 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(168,85,247,0.12)]">
          <Panel
            title="Session Activity"
            className="h-[500px] transition-all duration-300 group-hover:border-purple-500/30"
          >
            <SessionActivityChart />
          </Panel>
        </div>

      </div>

    </div>
  );
}

export default function Sessions() {
  return (
    <DashboardLayout>
      <SessionProvider>
        <SessionContent />
      </SessionProvider>
    </DashboardLayout>
  );
}