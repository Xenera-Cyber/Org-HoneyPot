interface Props {
  label: string;
  value: string | number;
  onChange: (value: any) => void;
  type?: string;
  min?: number;
  max?: number;
  step?: number;
}

export default function SettingsInput({
  label,
  value,
  onChange,
  type = "text",
  min,
  max,
  step,
}: Props) {
  return (
    <div className="space-y-2">
      <label className="text-sm text-[var(--text-secondary)]">
        {label}
      </label>
      <input
        type={type}
        value={value}
        onChange={(e) => {
          const val = type === "number" ? Number(e.target.value) : e.target.value;
          onChange(val);
        }}
        min={min}
        max={max}
        step={step}
        className="w-full rounded-lg border border-[var(--border-medium)] bg-[var(--bg-input)] px-4 py-3 text-[var(--text-primary)] outline-none focus:border-[var(--accent-primary)] focus:ring-1 focus:ring-[var(--accent-primary)] transition-colors"
      />
    </div>
  );
}