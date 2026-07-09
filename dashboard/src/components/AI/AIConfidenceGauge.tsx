import ReactECharts from "echarts-for-react";
import useAI from "../../hooks/useAI";

export default function AIConfidenceGauge() {

    const { confidence } = useAI();

    return (
        <ReactECharts
            style={{ height: "320px" }}
            option={{
                backgroundColor: "transparent",

                series: [
                    {
                        type: "gauge",

                        startAngle: 220,
                        endAngle: -40,

                        progress: {
                            show: true,
                            width: 18
                        },

                        axisLine: {
                            lineStyle: {
                                width: 18,
                                color: [
                                    [0.50, "#22c55e"],
                                    [0.75, "#facc15"],
                                    [0.90, "#fb923c"],
                                    [1, "#ef4444"]
                                ]
                            }
                        },

                        pointer: {
                            show: false
                        },

                        detail: {
                            formatter: "{value}%",
                            color: "#ffffff",
                            fontSize: 36
                        },

                        data: [
                            {
                                value: confidence
                            }
                        ]
                    }
                ]
            }}
        />
    );
}