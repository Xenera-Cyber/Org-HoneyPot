import * as echarts from "echarts";
import ReactECharts from "echarts-for-react";
import { useEffect, useMemo, useRef, useState } from "react";
import { Locate } from "lucide-react";
import useSessions, { type Session } from "../../hooks/useSessions";
import useSettings from "../../hooks/useSettings";

// RISK MANAGEMENT UTILITY HELPERS
function getRiskColor(risk: number) {
  if (risk >= 90) return "#ef4444"; // red
  if (risk >= 75) return "#f97316"; // orange
  if (risk >= 50) return "#facc15"; // yellow
  return "#22c55e"; // green
}

function getRiskSize(risk: number) {
  if (risk >= 90) return 18;
  if (risk >= 75) return 15;
  if (risk >= 50) return 12;
  return 9;
}

// Bounds the map is allowed to pan/zoom within. Without this, pinch/scroll
// zoom has no floor or ceiling, so zooming out past the world map's own
// bounds (or zooming in far enough that the geo layer's internal tiling
// runs out) is what caused the "glitches or disappears" behavior.
const MIN_ZOOM = 1;
const MAX_ZOOM = 12;
const DEFAULT_ZOOM = 1.18;
const DEFAULT_CENTER: [number, number] = [10, 20];

interface AttackerPoint {
  ip: string;
  country: string;
  city: string;
  protocol: string;
  risk: number;
  sessionCount: number;
  timesSeenFromIp?: number;
  firstSeenFromIp?: string;
  longitude: number;
  latitude: number;
}

// Multiple sessions from the same IP/coordinate used to render as fully
// overlapping dots. Grouping them into one marker (with a real count) is
// both a visual fix and a more honest representation of "how many
// distinct attackers are we seeing" vs. "how many sessions total".
function groupByAttacker(sessions: Session[]): AttackerPoint[] {
  const byIp = new Map<string, AttackerPoint>();

  for (const s of sessions) {
    const existing = byIp.get(s.ip);
    if (existing) {
      existing.sessionCount += 1;
      existing.risk = Math.max(existing.risk, s.risk);
    } else {
      byIp.set(s.ip, {
        ip: s.ip,
        country: s.country,
        city: s.city,
        protocol: s.protocol,
        risk: s.risk,
        sessionCount: 1,
        timesSeenFromIp: s.timesSeenFromIp,
        firstSeenFromIp: s.firstSeenFromIp,
        longitude: s.longitude,
        latitude: s.latitude,
      });
    }
  }

  return Array.from(byIp.values());
}

export default function GeographicVisualization() {
  const [ready, setReady] = useState(false);
  const chartRef = useRef<ReactECharts | null>(null);
  const containerRef = useRef<HTMLDivElement | null>(null);
  const viewRef = useRef<{ zoom: number; center: [number, number] }>({
    zoom: DEFAULT_ZOOM,
    center: DEFAULT_CENTER,
  });

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

  // The chart container is inside a flex layout, so its size can change
  // without the window itself resizing (e.g. opening the sidebar, a panel
  // reflowing). echarts-for-react only listens for window resize by
  // default, so without this the canvas can end up stale/clipped after a
  // layout change - part of what read as "the map glitches".
  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver(() => {
      chartRef.current?.getEchartsInstance().resize();
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [ready]);

  const { sessions, honeypotLocation } = useSessions();
  const { showAttackRoutes, animations } = useSettings();

  const attackers = useMemo(() => groupByAttacker(sessions), [sessions]);

  if (!ready) {
    return (
      <div className="flex h-full items-center justify-center text-gray-400">
        Loading world map...
      </div>
    );
  }

  const scatterData = attackers.map((a) => ({
    name: a.country,
    value: [a.longitude, a.latitude, a.risk],
    ip: a.ip,
    city: a.city,
    protocol: a.protocol,
    risk: a.risk,
    sessionCount: a.sessionCount,
    timesSeenFromIp: a.timesSeenFromIp,
    firstSeenFromIp: a.firstSeenFromIp,
    itemStyle: {
      color: getRiskColor(a.risk),
      shadowBlur: 20,
      shadowColor: getRiskColor(a.risk),
    },
    symbolSize: getRiskSize(a.risk) + Math.min(10, a.sessionCount - 1) * 2,
  }));

  const attackLines = attackers.map((a) => ({
    coords: [
      [a.longitude, a.latitude],
      [honeypotLocation.longitude, honeypotLocation.latitude],
    ],
    lineStyle: {
      color: getRiskColor(a.risk),
      width: a.risk >= 90 ? 3 : a.risk >= 75 ? 2.5 : 2,
      opacity: 0.6,
      curveness: 0.25,
    },
  }));

  const honeypotMarker = [
    {
      name: honeypotLocation.name,
      value: [honeypotLocation.longitude, honeypotLocation.latitude, 100],
    },
  ];

  const option = {
    backgroundColor: "transparent",

    toolbox: { show: false },

    tooltip: {
      trigger: "item",
      formatter: (params: any) => {
        if (params.seriesType === "effectScatter") {
          if (params.data.ip) {
            const seenLine = params.data.timesSeenFromIp
              ? `Seen <b>${params.data.timesSeenFromIp}</b> time${
                  params.data.timesSeenFromIp === 1 ? "" : "s"
                } total${
                  params.data.firstSeenFromIp
                    ? ` &middot; first seen ${new Date(
                        params.data.firstSeenFromIp
                      ).toLocaleString()}`
                    : ""
                }<br/>`
              : "";
            return `
              <div style="min-width:200px; font-family: sans-serif; line-height: 1.6;">
                <b>${params.data.ip}</b><br/>
                ${params.data.city ? `${params.data.city}, ` : ""}${params.data.name}<br/><br/>
                Protocol: <b>${params.data.protocol}</b><br/>
                Sessions: <b>${params.data.sessionCount}</b><br/>
                ${seenLine}
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

    geo: {
      map: "world",
      roam: true,
      // Hard floor/ceiling on zoom - this is the actual fix for pinch-zoom
      // making the map disappear: without it, zooming out shrinks the map
      // arbitrarily small (looks like it vanished) and zooming in has no
      // ceiling either.
      scaleLimit: { min: MIN_ZOOM, max: MAX_ZOOM },
      zoom: viewRef.current.zoom,
      center: viewRef.current.center,
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
      select: { disabled: true },
    },

    series: [
      ...(showAttackRoutes
        ? [
            {
              type: "lines",
              coordinateSystem: "geo",
              zlevel: 2,
              effect: {
                show: animations,
                period: 4,
                constantSpeed: 35,
                trailLength: 0.45,
                symbol: "arrow",
                symbolSize: 8,
              },
              data: attackLines,
            },
          ]
        : []),

      {
        type: "effectScatter",
        coordinateSystem: "geo",
        showEffectOn: animations ? "render" : "emphasis",
        rippleEffect: { scale: 3, brushType: "stroke" },
        itemStyle: {},
        encode: {},
        data: scatterData,
      },

      {
        type: "effectScatter",
        coordinateSystem: "geo",
        showEffectOn: animations ? "render" : "emphasis",
        rippleEffect: { scale: 8, brushType: "stroke" },
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

    animation: animations,
    animationDuration: animations ? 1200 : 0,
    animationEasing: "cubicOut",
  };

  function onChartEvents() {
    return {
      georoam: (params: any) => {
        // Persist whatever zoom/center the user just set so the next
        // render (e.g. triggered by a data poll) starts from there
        // instead of snapping back to the default view - this is what
        // previously read as the map "glitching" during live updates.
        const instance = chartRef.current?.getEchartsInstance();
        if (!instance) return;
        const geoModel = (instance as any).getModel?.().getComponent?.("geo");
        const zoom = geoModel?.get?.("zoom") ?? params?.zoom;
        const center = geoModel?.get?.("center");
        if (typeof zoom === "number") {
          viewRef.current.zoom = Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, zoom));
        }
        if (Array.isArray(center) && center.length === 2) {
          viewRef.current.center = center as [number, number];
        }
      },
    };
  }

  function resetView() {
    viewRef.current = { zoom: DEFAULT_ZOOM, center: DEFAULT_CENTER };
    chartRef.current?.getEchartsInstance().setOption(
      {
        geo: { zoom: DEFAULT_ZOOM, center: DEFAULT_CENTER },
      },
      false
    );
  }

  return (
    <div className="flex h-full flex-col">
      {/* MAP CANVAS CONTAINER - overflow-hidden so pan/zoom can never
          visually spill outside the panel */}
      <div ref={containerRef} className="relative flex-1 min-h-0 overflow-hidden rounded-lg">
        <ReactECharts
          ref={chartRef}
          option={option}
          notMerge={false}
          lazyUpdate
          onEvents={onChartEvents()}
          style={{ width: "100%", height: "100%" }}
        />
        <button
          onClick={resetView}
          title="Reset map view"
          className="absolute bottom-3 right-3 flex items-center gap-1.5 rounded-lg border border-white/10 bg-black/50 px-2.5 py-1.5 text-xs text-gray-300 backdrop-blur transition hover:bg-black/70 hover:text-white"
        >
          <Locate size={13} />
          Reset View
        </button>
      </div>

      {/* LIVE SUMMARY */}
      <div className="flex justify-center gap-6 text-xs text-gray-500 pt-2 select-none">
        <span>
          <span className="text-white font-medium">{attackers.length}</span>{" "}
          unique attacker{attackers.length === 1 ? "" : "s"}
        </span>
        <span>
          <span className="text-white font-medium">{sessions.length}</span>{" "}
          total session{sessions.length === 1 ? "" : "s"}
        </span>
        <span>
          <span className="text-white font-medium">
            {new Set(sessions.map((s) => s.country)).size}
          </span>{" "}
          origin countr{new Set(sessions.map((s) => s.country)).size === 1 ? "y" : "ies"}
        </span>
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
