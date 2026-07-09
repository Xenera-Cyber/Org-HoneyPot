import {
  CheckCircle2,
  PauseCircle,
  XCircle,
} from "lucide-react";

import useMonitoring from "../../hooks/useMonitoring";

export default function ActiveServices() {
  const { services } = useMonitoring();

  function icon(status: string) {
    switch (status) {
      case "Running":
        return <CheckCircle2 className="text-green-400" size={18} />;
      case "Idle":
        return <PauseCircle className="text-yellow-400" size={18} />;
      default:
        return <XCircle className="text-red-400" size={18} />;
    }
  }

  return (
    <div className="h-full overflow-y-auto hide-scrollbar pr-2">
      <div className="space-y-3">
        {services.map((service) => (
          <div
            key={service.name}
            className="
            flex
            items-center
            justify-between
            rounded-xl
            border
            border-white/5
            bg-white/[0.03]
            p-4
            hover:bg-white/[0.05]
            transition-all
            "
          >
            <div className="flex items-center gap-3">
              {icon(service.status)}
              <div>
                <div className="font-medium text-white">
                  {service.name}
                </div>
                <div className="text-xs text-gray-500">
                  {service.latency}
                </div>
              </div>
            </div>

            <div
              className={`
              text-sm font-medium
              ${
                service.status === "Running"
                  ? "text-green-400"
                  : service.status === "Idle"
                  ? "text-yellow-400"
                  : "text-red-400"
              }
            `}
            >
              {service.status}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}