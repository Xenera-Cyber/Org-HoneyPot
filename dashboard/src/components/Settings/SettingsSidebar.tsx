import {
    Settings,
    Brain,
    Shield,
    Server,
    Bell,
    LayoutDashboard,
} from "lucide-react";

interface Props {
    selected: string;
    onSelect: (tab: string) => void;
}

const items = [
    {
        name: "General",
        icon: <Settings size={18} />,
    },
    {
        name: "Honeypot",
        icon: <Server size={18} />,
    },
    {
        name: "AI",
        icon: <Brain size={18} />,
    },
    {
        name: "Dashboard",
        icon: <LayoutDashboard size={18} />,
    },
    {
        name: "Notifications",
        icon: <Bell size={18} />,
    },
    {
        name: "Security",
        icon: <Shield size={18} />,
    },
];

export default function SettingsSidebar({
    selected,
    onSelect,
}: Props) {
    return (
        <div className="space-y-2">
            {items.map((item) => (
                <button
                    key={item.name}
                    onClick={() => onSelect(item.name)}
                    className={`flex w-full items-center gap-3 rounded-lg px-4 py-3 text-left transition ${
                        selected === item.name
                            ? "bg-cyan-500/20 border border-cyan-500 text-cyan-400"
                            : "border border-slate-700 bg-slate-900 text-gray-300 hover:bg-slate-800 hover:border-cyan-500/40 hover:text-white"
                    }`}
                >
                    {item.icon}
                    {item.name}
                </button>
            ))}
        </div>
    );
}