import useSettings from "./useSettings";

export interface ThemeColors {
  textPrimary: string;
  textSecondary: string;
  gridColor: string;
  areaColor: string;
  lineColors: string[];
  barColors: string[];
  pieColors: string[];
}

export function useThemeColors(): ThemeColors {
  const { theme } = useSettings();

  const themes: Record<string, ThemeColors> = {
    dark: {
      textPrimary: "#f8fafc",
      textSecondary: "#94a3b8",
      gridColor: "rgba(255,255,255,0.05)",
      areaColor: "rgba(59, 130, 246, 0.1)",
      lineColors: ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6"],
      barColors: ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6"],
      pieColors: ["#3b82f6", "#ef4444", "#f59e0b", "#22c55e", "#8b5cf6", "#6b7280"],
    },
    light: {
      textPrimary: "#0f172a",
      textSecondary: "#475569",
      gridColor: "rgba(0,0,0,0.06)",
      areaColor: "rgba(59, 130, 246, 0.06)",
      lineColors: ["#2563eb", "#16a34a", "#d97706", "#dc2626", "#7c3aed"],
      barColors: ["#2563eb", "#16a34a", "#d97706", "#dc2626", "#7c3aed"],
      pieColors: ["#2563eb", "#dc2626", "#d97706", "#16a34a", "#7c3aed", "#64748b"],
    },
    ocean: {
      textPrimary: "#e0f2fe",
      textSecondary: "#7dd3fc",
      gridColor: "rgba(6, 182, 212, 0.15)",
      areaColor: "rgba(6, 182, 212, 0.12)",
      lineColors: ["#06b6d4", "#22d3ee", "#3b82f6", "#60a5fa", "#818cf8"],
      barColors: ["#06b6d4", "#22d3ee", "#3b82f6", "#60a5fa", "#818cf8"],
      pieColors: ["#06b6d4", "#3b82f6", "#22d3ee", "#60a5fa", "#818cf8", "#64748b"],
    },
    midnight: {
      textPrimary: "#ede9fe",
      textSecondary: "#a78bfa",
      gridColor: "rgba(139, 92, 246, 0.15)",
      areaColor: "rgba(139, 92, 246, 0.1)",
      lineColors: ["#8b5cf6", "#a78bfa", "#c084fc", "#7c3aed", "#6d28d9"],
      barColors: ["#8b5cf6", "#a78bfa", "#c084fc", "#7c3aed", "#6d28d9"],
      pieColors: ["#8b5cf6", "#7c3aed", "#a78bfa", "#c084fc", "#6d28d9", "#64748b"],
    },
    forest: {
      textPrimary: "#dcfce7",
      textSecondary: "#4ade80",
      gridColor: "rgba(34, 197, 94, 0.15)",
      areaColor: "rgba(34, 197, 94, 0.1)",
      lineColors: ["#22c55e", "#4ade80", "#86efac", "#16a34a", "#15803d"],
      barColors: ["#22c55e", "#4ade80", "#86efac", "#16a34a", "#15803d"],
      pieColors: ["#22c55e", "#16a34a", "#4ade80", "#86efac", "#15803d", "#64748b"],
    },
  };

  return themes[theme] || themes.dark;
}