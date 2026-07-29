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
  const getFontSize = (val: string | number) => {
    const str = String(val);
    if (str.length > 12) return "text-xl";
    if (str.length > 7) return "text-2xl";
    if (str.length > 4) return "text-3xl";
    return "text-4xl";
  };

  return (
    <div className="rounded-xl border border-white/10 bg-[var(--bg-card)] p-6">
      <div className="flex justify-between">
        <div>
          <p className="text-sm text-gray-400">
            {title}
          </p>

          <h2
            className={`mt-2 font-bold ${getFontSize(value)} ${color}`}
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