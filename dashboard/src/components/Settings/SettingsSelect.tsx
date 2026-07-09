interface Props {
    label: string;
    value: string;
    options: string[];
    onChange: (value: string) => void;
}

export default function SettingsSelect({
    label,
    value,
    options,
    onChange,
}: Props) {

    return (

        <div className="space-y-2">

            <label className="text-sm text-gray-400">
                {label}
            </label>

            <select
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-500"
            >

                {options.map((option) => (

                    <option
                        key={option}
                        value={option}
                    >
                        {option}
                    </option>

                ))}

            </select>

        </div>

    );

}