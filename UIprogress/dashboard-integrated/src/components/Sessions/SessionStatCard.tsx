interface Props {
  title: string;
  value: string;
  subtitle: string;
  color: string;
  icon: React.ReactNode;
}

export default function SessionStatCard({
  title,
  value,
  subtitle,
  color,
  icon,
}: Props) {
  const getFontSize = (val: string) => {
    if (val.length > 12) return "text-xl";
    if (val.length > 7) return "text-2xl";
    if (val.length > 4) return "text-3xl";
    return "text-4xl";
  };

  return (
    <div
      className="
      rounded-2xl
      border
      border-white/10
      bg-[var(--bg-card)]
      p-6
      h-full
      flex
      flex-col
      "
    >
      {/* Changing this to flex-1 and a column layout ensures that 
        the internal space stretches cleanly to fill the container height.
      */}
      <div className="flex justify-between flex-1 flex-col sm:flex-row gap-4">
        <div className="flex flex-col justify-between h-full flex-1">
          <div>
            <p className="text-sm text-gray-400">
              {title}
            </p>
            <h2
              className={`mt-2 font-bold tracking-tight break-words ${getFontSize(value)} ${color}`}
            >
              {value}
            </h2>
          </div>
          
          <p className="mt-2 text-sm text-gray-500">
            {subtitle}
          </p>
        </div>

        <div className={`${color} shrink-0`}>
          {icon}
        </div>
      </div>
    </div>
  );
}