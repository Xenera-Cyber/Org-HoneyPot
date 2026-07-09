import {
    PieChart,
    Pie,
    Cell,
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
} from "recharts";
import useAI from "../../hooks/useAI";

export default function AIConfidenceBreakdown() {
    const ai = useAI();
    const overall = ai.confidence;

    // Dynamically calculate radial chart slices based on current context state
    const radialData = [
        {
            name: "Confidence",
            value: overall,
        },
        {
            name: "Remaining",
            value: 100 - overall,
        },
    ];

    // Updated with reactive data directly from the AI Context Breakdown
    const breakdown = [
        {
            name: "Detection",
            confidence: ai.confidenceBreakdown.detection,
        },
        {
            name: "Classification",
            confidence: ai.confidenceBreakdown.classification,
        },
        {
            name: "RAG",
            confidence: ai.confidenceBreakdown.rag,
        },
        {
            name: "Prediction",
            confidence: ai.confidenceBreakdown.prediction,
        },
        {
            name: "Response",
            confidence: ai.confidenceBreakdown.response,
        },
    ];

    return (
        <div className="flex h-full flex-col">

            <div className="h-56">

                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>

                        <Pie
                            data={radialData}
                            dataKey="value"
                            startAngle={90}
                            endAngle={-270}
                            innerRadius={70}
                            outerRadius={88}
                            stroke="none"
                        >
                            <Cell fill="#06b6d4" />
                            <Cell fill="#1e293b" />
                        </Pie>

                        <text
                            x="50%"
                            y="48%"
                            textAnchor="middle"
                            dominantBaseline="middle"
                            fill="#ffffff"
                            fontSize="32"
                            fontWeight="700"
                        >
                            {overall}%
                        </text>

                        <text
                            x="50%"
                            y="62%"
                            textAnchor="middle"
                            dominantBaseline="middle"
                            fill="#94a3b8"
                            fontSize="13"
                        >
                            Overall Confidence
                        </text>

                    </PieChart>
                </ResponsiveContainer>

            </div>

            <div className="flex-1">

                <ResponsiveContainer width="100%" height="100%">

                    <BarChart
                        layout="vertical"
                        data={breakdown}
                        margin={{
                            top: 10,
                            right: 20,
                            left: 20,
                            bottom: 0,
                        }}
                    >

                        <XAxis
                            type="number"
                            domain={[0, 100]}
                            hide
                        />

                        <YAxis
                            type="category"
                            dataKey="name"
                            tick={{
                                fill: "#94a3b8",
                                fontSize: 12,
                            }}
                            width={90}
                        />

                        <Tooltip />

                        <Bar
                            dataKey="confidence"
                            radius={[8, 8, 8, 8]}
                            fill="#06b6d4"
                        />

                    </BarChart>

                </ResponsiveContainer>

            </div>

        </div>
    );
}