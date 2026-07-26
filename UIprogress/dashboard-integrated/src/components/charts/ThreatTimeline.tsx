import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";
import useThreats from "../../hooks/useThreats";
import useSettings from "../../hooks/useSettings";

export default function ThreatTimeline() {
  const { scoreTimeline } = useThreats();
  const { animations } = useSettings();

  return (
    /* Changed container to h-[320px] and added px-6 py-5 padding */
    <div className="w-full h-[320px] px-6 py-5">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={scoreTimeline}>
          <CartesianGrid stroke="#1F2937" strokeDasharray="4 4" />

          <XAxis
            dataKey="time"
            stroke="#6B7280"
            tick={{ fill: "#9CA3AF", fontSize: 12 }}
          />

          <YAxis
            stroke="#6B7280"
            tick={{ fill: "#9CA3AF", fontSize: 12 }}
          />

          {/* Upgraded Tooltip with backdrop blur glassmorphism styles */}
          <Tooltip
            contentStyle={{
              background: "rgba(15,23,42,.85)",
              backdropFilter: "blur(20px)",
              border: "1px solid rgba(255,255,255,.08)",
              borderRadius: 16,
              color: "#fff",
            }}
          />

          {/* Configured Line with custom activeDot styling */}
          <Line
            type="monotone"
            dataKey="score"
            stroke="#3B82F6"
            strokeWidth={3}
            dot={false}
            activeDot={{
              r: 6,
              fill: "#60A5FA",
              stroke: "#fff",
              strokeWidth: 2,
            }}
            
            /* ===== SYNCED ANIMATION SETTINGS ===== */
            animationBegin={0}
            animationDuration={animations ? 600 : 0}
            animationEasing="ease-out"
            isAnimationActive={animations}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
