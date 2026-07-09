import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

const data = [
  { name: "Recon", value: 28 },
  { name: "Privilege", value: 18 },
  { name: "Malware", value: 14 },
  { name: "Reverse Shell", value: 10 },
  { name: "SSH", value: 16 },
  { name: "Unknown", value: 14 },
];

const COLORS = [
  "#3B82F6", // Blue
  "#EF4444", // Red
  "#F59E0B", // Amber
  "#22C55E", // Green
  "#A855F7", // Purple
  "#6B7280", // Gray
];

export default function AttackPieChart() {
  return (
    /* Wrapper div gives ResponsiveContainer a reliable bounding box 
       so it doesn't cause wacky layout loops. */
    <div className="w-full h-[250px] flex items-center justify-center">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          {/* Pie settings updated to your wider donut configuration */}
          <Pie
            data={data}
            cx="40%" /* shifted slightly left to give room to the vertical right legend */
            cy="50%"
            innerRadius={58}
            outerRadius={86}
            paddingAngle={4}
            dataKey="value"
            
            /* ===== ANIMATION FIXES ===== */
            animationBegin={0}
            animationDuration={600}
            animationEasing="ease-out"
            animationMatchBy="index"
            // If it still jitters on data updates, uncomment the line below:
            // isAnimationActive={false}
          >
            {data.map((_, index) => (
              <Cell
                key={index}
                fill={COLORS[index % COLORS.length]}
                stroke="rgba(17, 23, 34, 0.85)" /* Blends flawlessly into your panel background */
                strokeWidth={2}
              />
            ))}
          </Pie>

          {/* Upgraded Tooltip with backdrop blur glassmorphism styles */}
          <Tooltip
            contentStyle={{
              background: "rgba(15,23,42,.85)",
              backdropFilter: "blur(20px)",
              borderRadius: 16,
              border: "1px solid rgba(255,255,255,.08)",
              color: "#fff",
            }}
          />

          {/* Legend typography color matched to #CBD5E1 */}
          <Legend
            verticalAlign="middle"
            align="right"
            layout="vertical"
            iconType="circle"
            wrapperStyle={{
              fontSize: "13px",
              paddingLeft: "10px",
              color: "#CBD5E1",
            }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}