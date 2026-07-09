import * as echarts from "echarts";
import ReactECharts from "echarts-for-react";
import { useEffect, useState } from "react";
import useSessions from "../../hooks/useSessions";

// RISK MANAGEMENT UTILITY HELPERS
function getRiskColor(risk: number) {
  if (risk >= 90) return "#ef4444";     // red
  if (risk >= 75) return "#f97316";     // orange
  if (risk >= 50) return "#facc15";     // yellow
  return "#22c55e";                     // green
}

function getRiskSize(risk: number) {
  if (risk >= 90) return 18;
  if (risk >= 75) return 15;
  if (risk >= 50) return 12;
  return 9;
}

export default function GeographicVisualization() {
  // ASYNCHRONOUS GEOJSON REGISTRATION STATE
  const [ready, setReady] = useState(false);

  useEffect(() => {
    fetch("/maps/world.geojson")
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load world.geojson");
        }
        return res.json();
      })
      .then((geojson) => {
        echarts.registerMap("world", geojson);
        setReady(true);
      })
      .catch((err) => {
        console.error("Map loading error:", err);
      });
  }, []);

  // EXTRACT LIVE DATA FLOW FROM HOOK
  const { sessions, honeypotLocation } = useSessions();

  // DONT RENDER ECHARTS UNTIL THE MAP IS LOADED
  if (!ready) {
    return (
      <div className="flex h-full items-center justify-center text-gray-400">
        Loading world map...
      </div>
    );
  }

  // SEVERITY DYNAMIC ATTACK NODES
  const scatterData = sessions.map((session) => ({
    name: session.country,
    value: [
      session.longitude,
      session.latitude,
      session.risk,
    ],
    ip: session.ip,
    protocol: session.protocol,
    risk: session.risk,
    itemStyle: {
      color: getRiskColor(session.risk),
      shadowBlur: 20,
      shadowColor: getRiskColor(session.risk),
    },
    symbolSize: getRiskSize(session.risk),
  }));

  // SEVERITY GRADED ATTACK TRAILS
  const attackLines = sessions.map((session) => ({
    coords: [
      [session.longitude, session.latitude],
      [honeypotLocation.longitude, honeypotLocation.latitude],
    ],
    lineStyle: {
      color: getRiskColor(session.risk),
      width:
        session.risk >= 90
          ? 3
          : session.risk >= 75
          ? 2.5
          : 2,
      opacity: 0.6,
      curveness: 0.25,
    },
  }));

  // GENERATE TARGET CORE NODE DATA
  const honeypotMarker = [
    {
      name: honeypotLocation.name,
      value: [
        honeypotLocation.longitude,
        honeypotLocation.latitude,
        100,
      ],
    },
  ];

  const option = {
    backgroundColor: "transparent",
    
    toolbox: {
      show: false,
    },

    // DYNAMIC HTML TOOLTIP POPUP CONTROLLER
    tooltip: {
      trigger: "item",
      formatter: (params: any) => {
        if (params.seriesType === "effectScatter") {
          if (params.data.ip) {
            return `
              <div style="min-width:180px; font-family: sans-serif; line-height: 1.5;">
                <b>${params.data.ip}</b><br/>
                ${params.data.name}<br/><br/>
                Protocol: <b>${params.data.protocol}</b><br/>
                Risk: <span style="color:${getRiskColor(params.data.risk)}; font-weight: bold;">
                  ${params.data.risk}%
                </span>
              </div>
            `;
          }
          return "<b>XYNERA Honeypot</b>";
        }
        return "";
      },
    },

    // MODERNIZED BLACK-OUT SOC MAP
    geo: {
      map: "world",
      roam: true,
      zoom: 1.18,
      silent: false,
      itemStyle: {
        areaColor: "#111827",
        borderColor: "#334155",
        borderWidth: 0.8,
      },
      emphasis: {
        itemStyle: {
          areaColor: "#1e40af",
          borderColor: "#38bdf8",
          borderWidth: 1.4,
        },
      },
      select: {
        disabled: true,
      },
    },

    // LAYERED COMPOSITION
    series: [
      /* CONTINUOUS INCOMING ATTACK ROUTES */
      {
        type: "lines",
        coordinateSystem: "geo",
        zlevel: 2,
        effect: {
          show: true,
          period: 4,
          constantSpeed: 35,
          trailLength: 0.45,
          symbol: "arrow",
          symbolSize: 8,
        },
        data: attackLines,
      },

      /* PULSING SEVERITY-DRIVEN ATTACK ORIGINS */
      {
        type: "effectScatter",
        coordinateSystem: "geo",
        rippleEffect: {
          scale: 3,
          brushType: "stroke",
        },
        itemStyle: {},
        encode: {},
        data: scatterData,
      },

      /* HIGH VISIBILITY XYNERA ANCHOR NODE */
      {
        type: "effectScatter",
        coordinateSystem: "geo",
        rippleEffect: {
          scale: 8,
          brushType: "stroke",
        },
        symbolSize: 20,
        itemStyle: {
          color: "#22c55e",
          shadowBlur: 35,
          shadowColor: "#22c55e",
        },
        label: {
          show: true,
          formatter: "XYNERA",
          position: "bottom",
          color: "#ffffff",
          fontWeight: "bold",
        },
        data: honeypotMarker,
      },
    ],

    // SMOOTH MOTION ANIMATION
    animation: true,
    animationDuration: 1200,
    animationEasing: "cubicOut",
  };

  return (
    <div className="flex h-full flex-col">
      {/* MAP CANVAS CONTAINER */}
      <div className="flex-1 min-h-0">
        <ReactECharts
          option={option}
          style={{
            width: "100%",
            height: "100%",
          }}
        />
      </div>

      {/* DYNAMIC THREAT STATUS LEGEND BAR */}
      <div className="mt-4 flex justify-center gap-6 text-xs text-gray-400 pb-2 select-none">
        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded-full bg-green-500" />
          Low
        </div>

        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded-full bg-yellow-400" />
          Medium
        </div>

        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded-full bg-orange-500" />
          High
        </div>

        <div className="flex items-center gap-2">
          <div className="h-3 w-3 rounded-full bg-red-500" />
          Critical
        </div>
      </div>
    </div>
  );
}