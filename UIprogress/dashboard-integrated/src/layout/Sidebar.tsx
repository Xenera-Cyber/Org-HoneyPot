import {
  LayoutDashboard,
  Activity,
  Shield,
  Server,
  Settings,
  BrainCircuit, // IMPORTED ICON
} from "lucide-react";

import { NavLink } from "react-router-dom";

const menu = [
  {
    icon: <LayoutDashboard size={18} />,
    label: "Dashboard",
    path: "/dashboard",
  },
  {
    icon: <Activity size={18} />,
    label: "Monitoring",
    path: "/monitoring",
  },
  {
    icon: <Shield size={18} />,
    label: "Threats",
    path: "/threats",
  },
  {
    icon: <Server size={18} />,
    label: "Sessions",
    path: "/sessions",
  },
  // ADDED AI INTELLIGENCE NAVIGATION ITEM
  {
    icon: <BrainCircuit size={18} />,
    label: "AI Intelligence",
    path: "/ai",
  },
  {
    icon: <Settings size={18} />,
    label: "Settings",
    path: "/settings",
  },
];

export default function Sidebar() {
  return (
    <aside
      className="
      w-72
      h-screen
      bg-[rgba(8,12,20,.95)]
      backdrop-blur-3xl
      border-r
      border-white/5
      flex
      flex-col
      "
    >
      {/* Logo */}
      <div className="px-8 py-8">
        <h1 className="text-2xl font-bold tracking-wide text-blue-400">
          XYNERA
        </h1>
        <p className="mt-1 text-xs text-gray-500">
          Security Operations Center
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-5 space-y-2">
        {menu.map((item) => (
          <NavLink
            key={item.label}
            to={item.path}
            className={({ isActive }) =>
              `
              flex
              items-center
              gap-3
              px-5
              py-3
              rounded-xl
              transition-all
              ${
                isActive
                  ? "bg-blue-500/15 border border-blue-500/20 text-white shadow-[0_0_20px_rgba(59,130,246,.15)]"
                  : "text-gray-400 hover:bg-white/[0.04] hover:text-white"
              }
              `
            }
          >
            {item.icon}
            <span>
              {item.label}
            </span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}