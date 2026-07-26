import ReactECharts from "echarts-for-react";
import useSessions from "../../hooks/useSessions";
import useSettings from "../../hooks/useSettings";

export default function SessionActivityChart() {
  const { activityTimeline } = useSessions();
  const { animations } = useSettings();

  const option = {
    backgroundColor: "transparent",

    tooltip: {
      trigger: "axis",
    },

    xAxis: {
      type: "category",
      data: activityTimeline.map((p) => p.time),
      axisLine: {
        lineStyle: {
          color: "#64748b",
        },
      },
    },

    yAxis: {
      type: "value",
      splitLine: {
        lineStyle: {
          color: "#273244",
        },
      },
    },

    series: [
      {
        data: activityTimeline.map((p) => p.count),
        type: "line",
        smooth: true,
        areaStyle: {},
      },
    ],

    animation: animations,
  };

  return (
    <ReactECharts
      option={option}
      style={{
        width: "100%",
        height: "100%",
      }}
    />
  );
}
