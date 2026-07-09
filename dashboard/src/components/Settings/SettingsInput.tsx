interface Props {

    label: string;

    value: string | number;

    onChange: (value: any) => void;

    type?: string;

}

export default function SettingsInput({

    label,

    value,

    onChange,

    type = "text",

}: Props) {

    return (

        <div className="space-y-2">

            <label className="text-sm text-gray-400">
                {label}
            </label>

            <input
                type={type}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-white outline-none focus:border-cyan-500"
            />

        </div>

    );

}