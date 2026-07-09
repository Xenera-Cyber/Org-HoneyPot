import DashboardLayout from "../layout/DashboardLayout";
import Panel from "../components/Panel";

import { ThreatProvider } from "../context/ThreatContext";
import useThreats from "../hooks/useThreats";

import ThreatHeatmap from "../components/charts/ThreatHeatmap";
import TopAttackSources from "../components/threats/TopAttackSources";

import SeverityTimeline from "../components/threats/SeverityTimeline";
import ThreatIntelligenceSummary from "../components/threats/ThreatIntelligenceSummary";
import SecurityTip from "../components/threats/SecurityTip";

import LiveThreatTable from "../components/threats/ThreatLiveTable";
import AttackTypes from "../components/threats/AttackTypes";
import ThreatStatCard from "../components/threats/ThreatStatCard";

import {
  ShieldAlert,
  Activity,
  Ban,
  Brain,
} from "lucide-react";

function ThreatContent() {
  const {
    threatScore,
    activeThreats,
    blockedIPs,
    aiConfidence,
  } = useThreats();

  return (
    <div className="space-y-6">

      <div>
        <h1 className="text-3xl font-bold text-white">
          Threat Intelligence
        </h1>

        <p className="mt-1 text-gray-400">
          AI-driven threat analysis and attack intelligence
        </p>
      </div>

      <div className="grid grid-cols-4 gap-6">

        <ThreatStatCard
          title="Threat Score"
          value={`${threatScore}`}
          subtitle="Current Risk"
          color="text-red-400"
          icon={<ShieldAlert size={34} />}
        />

        <ThreatStatCard
          title="Active Threats"
          value={`${activeThreats}`}
          subtitle="Live Attacks"
          color="text-orange-400"
          icon={<Activity size={34} />}
        />

        <ThreatStatCard
          title="Blocked IPs"
          value={`${blockedIPs}`}
          subtitle="Today"
          color="text-cyan-400"
          icon={<Ban size={34} />}
        />

        <ThreatStatCard
          title="AI Confidence"
          value={`${aiConfidence.toFixed(1)}%`}
          subtitle="Detection Accuracy"
          color="text-green-400"
          icon={<Brain size={34} />}
        />

      </div>

      <div className="grid grid-cols-12 gap-6 items-stretch">

        {/* LEFT */}
        <div className="col-span-8 flex flex-col gap-6">

          {/* Threat Heatmap - Red Glow */}
          <div className="group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(239,68,68,0.12)]">
            <Panel
              title="Threat Heatmap"
              className="flex-1 min-h-[300px] flex flex-col transition-all duration-300 group-hover:border-red-500/30"
            >
              <div className="flex-1 overflow-y-auto custom-scrollbar pr-2">
                <ThreatHeatmap />
              </div>
            </Panel>
          </div>

          {/* Top Attack Sources - Orange Glow */}
          <div className="group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(249,115,22,0.12)]">
            <Panel
              title="Top Attack Sources"
              className="flex-1 min-h-[300px] flex flex-col transition-all duration-300 group-hover:border-orange-500/30"
            >
              <div className="flex-1 overflow-y-auto custom-scrollbar pr-2">
                <TopAttackSources />
              </div>
            </Panel>
          </div>

        </div>

        {/* RIGHT */}
        <div className="col-span-4 flex flex-col gap-6">

          {/* Threat Severity Timeline - Purple / Magenta Glow */}
          <div className="group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(168,85,247,0.12)]">
            <Panel
              title="Threat Severity Timeline"
              className="flex-1 min-h-[260px] transition-all duration-300 group-hover:border-purple-500/30"
            >
              <SeverityTimeline />
            </Panel>
          </div>

          {/* Threat Intelligence Summary - Blue Glow (Preserves context scroll layer) */}
          <div className="group flex-1 min-h-[360px] max-h-[360px] overflow-y-auto custom-scrollbar pr-1 transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(59,130,246,0.12)]">
            <Panel 
              title="Threat Intelligence Summary"
              className="transition-all duration-300 group-hover:border-blue-500/30"
            >
              <ThreatIntelligenceSummary />
            </Panel>
          </div>

          {/* Security Tip - Cyan Glow */}
          <div className="group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(6,182,212,0.12)]">
            <Panel
              title="Security Tip"
              className="flex-1 min-h-[300px] transition-all duration-300 group-hover:border-cyan-500/30"
            >
              <SecurityTip />
            </Panel>
          </div>

        </div>

      </div>

      {/* Live Threat Investigation - Crimson Red Glow */}
      <div className="group transition-all duration-300 rounded-xl hover:shadow-[0_0_35px_rgba(220,38,38,0.15)]">
        <Panel
          title="Live Threat Investigation"
          className="min-h-[430px] transition-all duration-300 group-hover:border-red-600/40"
        >
          <LiveThreatTable />
        </Panel>
      </div>

      {/* Attack Types - Fuchsia / Purple Glow */}
      <div className="group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(217,70,239,0.12)]">
        <Panel
          title="Attack Types"
          className="transition-all duration-300 group-hover:border-fuchsia-500/30"
        >
          <AttackTypes />
        </Panel>
      </div>

    </div>
  );
}

export default function Threats() {
  return (
    <DashboardLayout>
      <ThreatProvider>
        <ThreatContent />
      </ThreatProvider>
    </DashboardLayout>
  );
}