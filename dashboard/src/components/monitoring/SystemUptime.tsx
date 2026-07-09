import useMonitoring from "../../hooks/useMonitoring";

export default function SystemUptime() {
  const { uptime } = useMonitoring();

  const days = Math.floor(uptime / 86400);
  const hours = Math.floor((uptime % 86400) / 3600);
  const minutes = Math.floor((uptime % 3600) / 60);

  return (
    <div className="grid grid-cols-6 gap-4 h-full">
      {/* 1. UPTIME */}
      <Card
        title="System Uptime"
        value={`${days}d ${hours}h ${minutes}m`}
        statusText="Active"
        dotColor="bg-green-500"
        valueColor="text-white"
      />

      {/* 2. MONITORING */}
      <Card
        title="Monitoring Engine"
        value="Healthy"
        statusText="Running"
        dotColor="bg-green-500"
        valueColor="text-green-400"
      />

      {/* 3. AI ENGINE */}
      <Card
        title="AI Engine"
        value="Online"
        statusText="Running"
        dotColor="bg-green-500"
        valueColor="text-cyan-400"
      />

      {/* 4. DATABASE */}
      <Card
        title="Database"
        value="Connected"
        statusText="Connected"
        dotColor="bg-green-500"
        valueColor="text-green-400"
      />

      {/* 5. API */}
      <Card
        title="API Gateway"
        value="Operational"
        statusText="Online"
        dotColor="bg-green-500"
        valueColor="text-emerald-400"
      />

      {/* 6. WEBSOCKET */}
      <Card
        title="WebSocket"
        value="Connected"
        statusText="Live"
        dotColor="bg-green-500"
        valueColor="text-indigo-400"
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