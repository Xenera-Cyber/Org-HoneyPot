import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

const data = [
  { time: "09:00", score: 12 },
  { time: "09:30", score: 18 },
  { time: "10:00", score: 24 },
  { time: "10:30", score: 17 },
  { time: "11:00", score: 36 },
  { time: "11:30", score: 42 },
  { time: "12:00", score: 58 },
  { time: "12:30", score: 48 },
  { time: "13:00", score: 67 },
  { time: "13:30", score: 74 },
];

export default function ThreatTimeline() {
  return (
    /* Changed container to h-[320px] and added px-6 py-5 padding */
    <div className="w-full h-[320px] px-6 py-5">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
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
            animationDuration={600}
            animationEasing="ease-out"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}