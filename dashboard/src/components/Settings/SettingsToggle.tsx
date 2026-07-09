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
        <div className="flex items-center justify-between rounded-xl border border-slate-700 bg-slate-900 px-5 py-4">

            <div>
                <h3 className="text-white font-medium">
                    {label}
                </h3>

                {description && (
                    <p className="mt-1 text-sm text-gray-400">
                        {description}
                    </p>
                )}
            </div>

            <button
                onClick={() => onChange(!checked)}
                className={`relative h-7 w-14 rounded-full transition-all duration-300 ${
                    checked
                        ? "bg-cyan-500"
                        : "bg-slate-700"
                }`}
            >
                <div
                    className={`absolute top-1 h-5 w-5 rounded-full bg-white transition-all duration-300 ${
                        checked
                            ? "left-8"
                            : "left-1"
                    }`}
                />
            </button>

        </div>
    );
}