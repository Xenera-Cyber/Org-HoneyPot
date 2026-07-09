interface PanelProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

export default function Panel({
  title,
  children,
  className = "",
}: PanelProps) {
  return (
    <div
      className={`
        flex
        flex-col
        rounded-2xl
        border
        border-white/10
        bg-[#171b24]
        overflow-hidden
        ${className}
      `}
    >
      <div className="flex items-center justify-between border-b border-white/5 px-6 py-5">
        <h2 className="text-lg font-semibold text-white">
          {title}
        </h2>

        <div className="h-2 w-2 rounded-full bg-blue-400" />
      </div>

      <div className="flex-1 min-h-0 overflow-hidden p-6">
        {children}
      </div>
    </div>
  );
}