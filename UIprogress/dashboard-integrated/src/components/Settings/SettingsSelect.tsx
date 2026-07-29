interface Props {
  label: string;
  value: string;
  options: string[] | { value: string; label: string }[];
  onChange: (value: string) => void;
}

export default function SettingsSelect({
  label,
  value,
  options,
  onChange,
}: Props) {
  const optionList = options.map((opt) =>
    typeof opt === "string" ? { value: opt, label: opt } : opt
  );

  return (
    <div className="space-y-2">
      <label className="text-sm text-[var(--text-secondary)]">
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full rounded-lg border border-[var(--border-medium)] bg-[var(--bg-input)] px-4 py-3 text-[var(--text-primary)] outline-none focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] transition-colors"
      >
        {optionList.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
}