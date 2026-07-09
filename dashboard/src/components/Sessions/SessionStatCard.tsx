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
  return (
    <div
      className="
      rounded-2xl
      border
      border-white/10
      bg-[#171b24]
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
              className={`mt-2 text-4xl font-bold tracking-tight break-words ${color}`}
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