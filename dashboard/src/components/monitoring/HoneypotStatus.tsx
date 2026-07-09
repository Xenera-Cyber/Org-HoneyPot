import {
  Terminal,
  Globe,
  FolderOpen,
  Mail,
  Cable,
  Database,
} from "lucide-react";

import useMonitoring from "../../hooks/useMonitoring";

export default function HoneypotStatus() {

  const { honeypots } = useMonitoring();

  function getIcon(name: string) {

    if (name.includes("SSH")) return <Terminal size={18} />;

    if (name.includes("HTTP")) return <Globe size={18} />;

    if (name.includes("FTP")) return <FolderOpen size={18} />;

    if (name.includes("SMTP")) return <Mail size={18} />;

    if (name.includes("Telnet")) return <Cable size={18} />;

    return <Database size={18} />;

  }

  function getColor(status: string) {

    switch (status) {

      case "Running":
        return "bg-green-500";

      case "Idle":
        return "bg-yellow-500";

      default:
        return "bg-red-500";

    }

  }

  return (

    <div className="h-full overflow-y-auto hide-scrollbar pr-2 space-y-3">

      {honeypots.map((hp) => (

        <div
          key={hp.name}
          className="
            flex
            items-center
            justify-between
            rounded-2xl
            border
            border-white/5
            bg-white/[0.03]
            p-4
            transition-all
            duration-300
            hover:bg-white/[0.05]
          "
        >

          <div className="flex items-center gap-4">

            <div
              className="
                h-11
                w-11
                rounded-xl
                bg-white/5
                flex
                items-center
                justify-center
                text-slate-200
              "
            >
              {getIcon(hp.name)}
            </div>

            <div>

              <h4 className="font-medium text-white">

                {hp.name}

              </h4>

              <p className="text-xs text-gray-500">

                Port {hp.port} • {hp.sessions} Active Session{hp.sessions !== 1 ? "s" : ""}

              </p>

            </div>

          </div>

          <div className="flex items-center gap-2">

            <div
              className={`h-2.5 w-2.5 rounded-full ${getColor(hp.status)}`}
            />

            <span className="text-sm text-slate-300">

              {hp.status}

            </span>

          </div>

        </div>

      ))}

    </div>

  );

}