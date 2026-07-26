interface Props {
  label: string;
  description?: string;
  checked: boolean;
  onChange: (value: boolean) => void;
}

export default function SettingsToggle({
  label,
  description,
  checked,
  onChange,
}: Props) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-[var(--border-medium)] bg-[var(--bg-card)] px-5 py-4 transition-colors">
      <div>
        <h3 className="text-[var(--text-primary)] font-medium">
          {label}
        </h3>
        {description && (
          <p className="mt-1 text-sm text-[var(--text-secondary)]">
            {description}
          </p>
        )}
      </div>
      <button
        onClick={() => onChange(!checked)}
        className={`relative h-7 w-14 rounded-full transition-all duration-300 ${
          checked
            ? "bg-[var(--accent-primary)]"
            : "bg-[var(--border-medium)]"
        }`}
      >
        <div
          className={`absolute top-1 h-5 w-5 rounded-full bg-white shadow-sm transition-all duration-300 ${
            checked ? "left-8" : "left-1"
          }`}
        />
      </button>
    </div>
  );
}