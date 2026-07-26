import useMonitoring from "../../hooks/useMonitoring";
import useAI from "../../hooks/useAI";
import useSettings from "../../hooks/useSettings";

export default function SystemUptime() {
  const { uptime, isLive, honeypotOnline } = useMonitoring();
  const { engineOnline } = useAI();
  const { autoRefresh } = useSettings();

  const days = Math.floor(uptime / 86400);
  const hours = Math.floor((uptime % 86400) / 3600);
  const minutes = Math.floor((uptime % 3600) / 60);

  return (
    <div className="grid grid-cols-6 gap-4 h-full">
      {/* 1. UPTIME - dashboard_api.py process uptime */}
      <Card
        title="Dashboard API Uptime"
        value={`${days}d ${hours}h ${minutes}m`}
        statusText={isLive ? "Active" : "Demo Data"}
        dotColor={isLive ? "bg-green-500" : "bg-gray-500"}
        valueColor="text-white"
      />

      {/* 2. HONEYPOT SERVER - real heartbeat from server.py */}
      <Card
        title="Honeypot Server"
        value={honeypotOnline ? "Online" : "Offline"}
        statusText={honeypotOnline ? "Listening :2222" : "Not detected"}
        dotColor={honeypotOnline ? "bg-green-500" : "bg-red-500"}
        valueColor={honeypotOnline ? "text-green-400" : "text-red-400"}
      />

      {/* 3. AI ENGINE - real, based on classified traffic seen by dashboard_api */}
      <Card
        title="AI Engine"
        value={engineOnline ? "Online" : "Idle"}
        statusText={engineOnline ? "Running" : "No activity"}
        dotColor={engineOnline ? "bg-green-500" : "bg-gray-500"}
        valueColor={engineOnline ? "text-cyan-400" : "text-gray-400"}
      />

      {/* 4. LOG STORAGE - dashboard_api reads directly from logs/ on disk */}
      <Card
        title="Log Storage"
        value={isLive ? "Readable" : "Unreachable"}
        statusText={isLive ? "logs/*.json" : "No connection"}
        dotColor={isLive ? "bg-green-500" : "bg-red-500"}
        valueColor={isLive ? "text-green-400" : "text-red-400"}
      />

      {/* 5. API - this dashboard's own REST API */}
      <Card
        title="Dashboard API"
        value={isLive ? "Operational" : "Unreachable"}
        statusText={isLive ? "Online" : "Offline"}
        dotColor={isLive ? "bg-green-500" : "bg-red-500"}
        valueColor={isLive ? "text-emerald-400" : "text-red-400"}
      />

      {/* 6. POLLING - this dashboard uses HTTP polling, not a websocket */}
      <Card
        title="Live Polling"
        value={autoRefresh ? "Active" : "Paused"}
        statusText={autoRefresh ? "Auto-refresh on" : "Auto-refresh off"}
        dotColor={autoRefresh ? "bg-green-500" : "bg-amber-500"}
        valueColor={autoRefresh ? "text-indigo-400" : "text-amber-400"}
      />
    </div>
  );
}

function Card({
  title,
  value,
  statusText,
  dotColor,
  valueColor,
}: {
  title: string;
  value: string;
  statusText: string;
  dotColor: string;
  valueColor: string;
}) {
  return (
    <div
      className="
        h-full
        rounded-xl
        border
        border-white/[0.06]
        bg-white/[0.02]
        p-4
        flex
        flex-col
        justify-between
        transition-all
        hover:border-white/10
        hover:bg-white/[0.03]
      "
    >
      {/* Top micro-badge */}
      <div className="flex items-center gap-1.5 text-[11px] font-medium tracking-wider uppercase text-gray-500">
        <span className={`h-1.5 w-1.5 rounded-full ${dotColor} animate-pulse`} />
        {statusText}
      </div>

      {/* Dynamic Content Structure */}
      <div className="mt-2.5">
        <div className="text-xs font-medium text-gray-400/80 truncate">
          {title}
        </div>
        <div className={`mt-0.5 text-base font-bold tracking-tight ${valueColor} truncate`}>
          {value}
        </div>
      </div>
    </div>
  );
}
