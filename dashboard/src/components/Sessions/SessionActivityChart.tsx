import ReactECharts from "echarts-for-react";

export default function SessionActivityChart() {

  const option = {

    backgroundColor: "transparent",

    tooltip: {
      trigger: "axis",
    },

    xAxis: {

      type: "category",

      data: [
        "18:00",
        "18:15",
        "18:30",
        "18:45",
        "19:00",
        "19:15",
        "19:30",
      ],

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

        data: [
          2,
          5,
          4,
          8,
          12,
          9,
          14,
        ],

        type: "line",

        smooth: true,

        areaStyle: {},

      },

    ],

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