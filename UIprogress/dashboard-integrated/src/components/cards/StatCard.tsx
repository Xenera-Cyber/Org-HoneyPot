import type { ReactNode } from "react";

interface StatCardProps {
  title: string;
  value: string;
  subtitle: string;
  icon: ReactNode;
}

export default function StatCard({
  title,
  value,
  subtitle,
  icon,
}: StatCardProps) {
  return (
    <div
      className="
      relative
      overflow-hidden
      rounded-3xl
      bg-white/[0.04]
      backdrop-blur-2xl
      border border-white/10
      shadow-[0_10px_40px_rgba(0,0,0,0.45)]
      transition-all
      duration-300
      hover:bg-white/[0.06]
      hover:border-blue-400/30
      hover:shadow-[0_0_40px_rgba(59,130,246,.18)]
      hover:-translate-y-1
      "
    >
      {/* Glow */}
      <div
        className="
        absolute
        -top-20
        -right-20
        w-40
        h-40
        rounded-full
        bg-blue-500/10
        blur-3xl
      "
      />

      {/* Top Content Area */}
      {/* Retained padding internally around elements since p-6 was moved inside the container flow */}
      <div className="relative flex justify-between items-start p-6">
        <div>
          <p className="text-sm text-gray-400">{title}</p>

          <h2 className="mt-3 text-5xl font-bold tracking-tight text-white">
            {value}
          </h2>

          <p className="mt-2 text-gray-500">{subtitle}</p>
        </div>

        {/* Icon Container */}
        <div
          className="
          w-12
          h-12
          rounded-2xl
          bg-blue-500/10
          backdrop-blur-xl
          border
          border-blue-400/20
          flex
          items-center
          justify-center
          text-blue-400
          shadow-[0_0_20px_rgba(59,130,246,.15)]
        "
        >
          {icon}
        </div>
      </div>

      {/* Bottom Accent */}
      <div
        className="
        absolute
        bottom-0
        left-0
        h-[3px]
        w-full
        bg-gradient-to-r
        from-cyan-400
        via-blue-500
        to-transparent
        "
      />
    </div>
  );
}