import {
  Server,
  Globe,
  FolderOpen,
  Cable,
  Bot,
  Database,
} from "lucide-react";

const services = [
  {
    icon: <Server size={18} />,
    name: "SSH Honeypot",
    status: "Running",
    detail: "3 Active Sessions",
    color: "bg-emerald-500",
  },
  {
    icon: <Globe size={18} />,
    name: "HTTP Honeypot",
    status: "Running",
    detail: "128 Requests",
    color: "bg-emerald-500",
  },
  {
    icon: <FolderOpen size={18} />,
    name: "FTP Honeypot",
    status: "Running",
    detail: "Idle",
    color: "bg-cyan-500",
  },
  {
    icon: <Cable size={18} />,
    name: "Telnet Honeypot",
    status: "Offline",
    detail: "Stopped",
    color: "bg-red-500",
  },
  {
    icon: <Bot size={18} />,
    name: "AI Engine",
    status: "Healthy",
    detail: "41 ms Response",
    color: "bg-blue-500",
  },
  {
    icon: <Database size={18} />,
    name: "SQLite Database",
    status: "Connected",
    detail: "Operational",
    color: "bg-purple-500",
  },
];

export default function HoneypotHealth() {
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
      {services.map((service) => (
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