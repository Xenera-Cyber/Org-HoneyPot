import { type ReactElement } from "react";
import {
  Server,
  Globe,
  FolderOpen,
  Cable,
  Bot,
  Database,
} from "lucide-react";
import useMonitoring from "../../hooks/useMonitoring";
import useAI from "../../hooks/useAI";

const ICONS: Record<string, ReactElement> = {
  "SSH Honeypot": <Server size={18} />,
  "HTTP Honeypot": <Globe size={18} />,
  "FTP Honeypot": <FolderOpen size={18} />,
  "SMTP Honeypot": <Cable size={18} />,
  "Telnet Honeypot": <Cable size={18} />,
  "Database Honeypot": <Database size={18} />,
};

function dotColor(status: string) {
  if (status === "Running") return "bg-emerald-500";
  if (status === "Idle") return "bg-amber-500";
  return "bg-red-500";
}

export default function HoneypotHealth() {
  const { honeypots } = useMonitoring();
  const { ragStatus, responseTime, engineOnline } = useAI();

  const rows = [
    ...honeypots.map((h) => ({
      icon: ICONS[h.name] ?? <Server size={18} />,
      name: h.name,
      status: h.status,
      detail:
        h.status === "Offline"
          ? "Not running"
          : `${h.sessions} Active Session${h.sessions === 1 ? "" : "s"}`,
      color: dotColor(h.status),
    })),
    {
      icon: <Bot size={18} />,
      name: "AI Engine",
      status: engineOnline ? "Healthy" : "Offline",
      detail: engineOnline ? `${responseTime} ms Response` : "No live traffic",
      color: engineOnline ? "bg-blue-500" : "bg-red-500",
    },
    {
      icon: <Database size={18} />,
      name: "xynera-ai RAG Backend",
      status: ragStatus,
      detail: ragStatus === "Healthy" ? "Operational" : "Not reachable",
      color: ragStatus === "Healthy" ? "bg-purple-500" : "bg-red-500",
    },
  ];

  return (
    <div
      className="
        space-y-3
        h-full
        overflow-y-auto
        hide-scrollbar
        pr-2
      "
    >
      {rows.map((service) => (
        <div
          key={service.name}
          className="
            flex
            items-center
            justify-between
            rounded-2xl
            border
            border-white/5
            bg-white/[0.03]
            px-4
            py-3
            transition-all
            duration-300
            hover:bg-white/[0.05]
            hover:border-blue-400/20
          "
        >
          <div className="flex items-center gap-3">
            <div
              className="
                h-10
                w-10
                rounded-xl
                bg-white/5
                flex
                items-center
                justify-center
                text-slate-200
              "
            >
              {service.icon}
            </div>

            <div>
              <div className="font-medium text-white">
                {service.name}
              </div>

              <div className="text-xs text-gray-400">
                {service.detail}
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div
              className={`h-2.5 w-2.5 rounded-full ${service.color}`}
            />

            <span className="text-sm text-gray-300">
              {service.status}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}
