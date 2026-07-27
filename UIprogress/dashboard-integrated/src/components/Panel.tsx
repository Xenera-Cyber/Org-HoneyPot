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
        border-[var(--border-subtle)]
        bg-[var(--bg-panel)]
        overflow-hidden
        ${className}
      `}
    >
      <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-6 py-5">
        <h2 className="text-lg font-semibold text-[var(--text-primary)]">
          {title}
        </h2>
        <div className="h-2 w-2 rounded-full bg-[var(--accent-primary)]" />
      </div>
      <div className="flex-1 min-h-0 overflow-hidden p-6">
        {children}
      </div>
    </div>
  );
}