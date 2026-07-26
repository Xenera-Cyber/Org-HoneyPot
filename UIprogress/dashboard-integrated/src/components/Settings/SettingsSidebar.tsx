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
  { name: "General", icon: <Settings size={18} /> },
  { name: "Honeypot", icon: <Server size={18} /> },
  { name: "AI", icon: <Brain size={18} /> },
  { name: "Dashboard", icon: <LayoutDashboard size={18} /> },
  { name: "Notifications", icon: <Bell size={18} /> },
  { name: "Security", icon: <Shield size={18} /> },
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
          className={`
            flex w-full items-center gap-3 rounded-lg px-4 py-3 text-left transition-all
            ${
              selected === item.name
                ? "bg-[var(--accent-primary)]/20 border border-[var(--accent-primary)] text-[var(--accent-primary)]"
                : "border border-[var(--border-subtle)] bg-[var(--bg-card)] text-[var(--text-secondary)] hover:bg-[var(--bg-hover)] hover:border-[var(--accent-primary)]/40 hover:text-[var(--text-primary)]"
            }
          `}
        >
          {item.icon}
          <span className="font-medium">{item.name}</span>
        </button>
      ))}
    </div>
  );
}