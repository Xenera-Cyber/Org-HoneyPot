import type { ReactNode } from "react";

interface Props {
  title: string;
  value: string;
  subtitle: string;
  icon: ReactNode;
  color: string;
}

export default function ThreatStatCard({
  title,
  value,
  subtitle,
  icon,
  color,
}: Props) {
  return (
    <div
      className="
        rounded-3xl
        border
        border-white/10
        bg-white/[0.04]
        backdrop-blur-3xl
        p-6
        transition-all
        hover:border-blue-500/20
      "
    >
      <div className="flex items-center justify-between">

        <div>

          <div className="text-sm text-gray-400">
            {title}
          </div>

          <div
            className={`mt-3 text-3xl font-bold ${color}`}
          >
            {value}
          </div>

          <div className="mt-1 text-xs text-gray-500">
            {subtitle}
          </div>

        </div>

        <div className={color}>
          {icon}
        </div>

      </div>
    </div>
  );
}