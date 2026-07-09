import type { ReactNode } from "react";

interface Props {
  title: string;
  value: string | number;
  subtitle: string;
  color: string;
  icon: ReactNode;
}

export default function AIStatCard({
  title,
  value,
  subtitle,
  color,
  icon,
}: Props) {
  return (
    <div className="rounded-xl border border-white/10 bg-[#1b1f27] p-6">
      <div className="flex justify-between">
        <div>
          <p className="text-sm text-gray-400">
            {title}
          </p>

          <h2
            className={`mt-2 text-4xl font-bold ${color}`}
          >
            {value}
          </h2>

          <p className="mt-2 text-gray-500">
            {subtitle}
          </p>
        </div>

        <div className={color}>{icon}</div>
      </div>
    </div>
  );
}