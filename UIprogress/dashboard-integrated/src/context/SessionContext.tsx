import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { apiGet } from "../lib/api";
import { useSettingsContext } from "./SettingsContext";

export interface Session {
  id: string;
  ip: string;
  country: string;
  city: string;
  latitude: number;
  longitude: number;
  protocol: "SSH" | "HTTP" | "FTP";
  honeypot: string;
  started: string;
  duration: number;
  commands: number;
  risk: number;
  status: "ACTIVE" | "IDLE" | "TERMINATED";
  // How many times (across all sessions, live+historical) this source IP
  // has connected, and when it was first seen - lets the UI distinguish
  // a first-time scanner from a repeat attacker.
  timesSeenFromIp?: number;
  firstSeenFromIp?: string;
}

export interface HoneypotLocation {
  name: string;
  latitude: number;
  longitude: number;
}

export interface ActivityPoint {
  time: string;
  count: number;
}

interface SessionContextType {
  sessions: Session[];
  activeSessions: number;
  totalToday: number;
  averageDuration: number;
  aiFlagged: number;
  honeypotLocation: HoneypotLocation;

  aiDecision: string;
  aiConfidence: number;
  predictedAttack: string;
  responseTime: number;

  totalCommandsProcessed: number;
  activityTimeline: ActivityPoint[];

  // true once we've successfully pulled real data from the XYNERA honeypot
  isLive: boolean;
  lastUpdated: Date | null;
}

// Shape returned by GET /api/sessions on dashboard_api.py
interface SessionsApiResponse {
  sessions: Session[];
  activeSessions: number;
  totalToday: number;
  averageDuration: number;
  aiFlagged: number;
  honeypotLocation: HoneypotLocation;
  aiDecision: string;
  aiConfidence: number;
  predictedAttack: string;
  responseTime: number;
  totalCommandsProcessed: number;
  activityTimeline: ActivityPoint[];
}

const SessionContext = createContext<SessionContextType | null>(null);

const DEMO_HONEYPOT_LOCATION: HoneypotLocation = {
  name: "XYNERA Honeypot",
  latitude: 28.6139,
  longitude: 77.209,
};

const DEMO_SESSIONS: Session[] = [
  {
    id: "1",
    ip: "185.194.21.54",
    country: "Russia",
    city: "Moscow",
    latitude: 55.7558,
    longitude: 37.6173,
    protocol: "SSH",
    honeypot: "Ubuntu SSH",
    started: "18:42",
    duration: 14,
    commands: 28,
    risk: 94,
    status: "ACTIVE",
  },
  {
    id: "2",
    ip: "103.54.11.19",
    country: "China",
    city: "Beijing",
    latitude: 39.9042,
    longitude: 116.4074,
    protocol: "HTTP",
    honeypot: "Apache HTTP",
    started: "18:35",
    duration: 8,
    commands: 16,
    risk: 81,
    status: "ACTIVE",
  },
  {
    id: "3",
    ip: "78.24.55.211",
    country: "Germany",
    city: "Berlin",
    latitude: 52.52,
    longitude: 13.405,
    protocol: "FTP",
    honeypot: "FTP Server",
    started: "18:20",
    duration: 23,
    commands: 49,
    risk: 72,
    status: "IDLE",
  },
  {
    id: "4",
    ip: "54.32.18.5",
    country: "USA",
    city: "Virginia",
    latitude: 38.9072,
    longitude: -77.0369,
    protocol: "SSH",
    honeypot: "Ubuntu SSH",
    started: "18:08",
    duration: 37,
    commands: 102,
    risk: 98,
    status: "ACTIVE",
  },
];

const DEMO_ACTIVITY_TIMELINE: ActivityPoint[] = Array.from(
  { length: 12 },
  (_, i) => ({
    time: `${(i * 15).toString().padStart(2, "0")}m`,
    count: Math.floor(Math.random() * 10) + 1,
  })
);

export function SessionProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const { refreshRate, autoRefresh, graphHistoryHours } = useSettingsContext();

  const [sessions, setSessions] = useState<Session[]>(DEMO_SESSIONS);
  const [totalToday, setTotalToday] = useState(431);
  const [averageDuration, setAverageDuration] = useState(12);
  const [aiDecision, setAiDecision] = useState("Credential Harvesting");
  const [aiConfidence, setAiConfidence] = useState(96);
  const [predictedAttack, setPredictedAttack] = useState("Reverse Shell");
  const [responseTime, setResponseTime] = useState(82);
  const [honeypotLocation, setHoneypotLocation] = useState<HoneypotLocation>(
    DEMO_HONEYPOT_LOCATION
  );
  const [totalCommandsProcessed, setTotalCommandsProcessed] = useState(4218);
  const [activityTimeline, setActivityTimeline] = useState<ActivityPoint[]>(
    DEMO_ACTIVITY_TIMELINE
  );
  const [isLive, setIsLive] = useState(false);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  // Poll the real honeypot backend. Falls back to (and stays on) the demo
  // dataset above whenever dashboard_api.py isn't reachable. Interval and
  // on/off are controlled from Settings > General so the whole app slows
  // down/pauses together instead of each page picking its own cadence.
  useEffect(() => {
    if (!autoRefresh) return;
    let cancelled = false;

    async function poll() {
      const data = await apiGet<SessionsApiResponse>(
        `/api/sessions?historyHours=${graphHistoryHours}`
      );
      if (cancelled) return;

      if (data) {
        setSessions(data.sessions);
        setTotalToday(data.totalToday);
        setAverageDuration(data.averageDuration);
        setAiDecision(data.aiDecision);
        setAiConfidence(data.aiConfidence);
        setPredictedAttack(data.predictedAttack);
        setResponseTime(data.responseTime);
        setHoneypotLocation(data.honeypotLocation);
        setTotalCommandsProcessed(data.totalCommandsProcessed);
        setActivityTimeline(data.activityTimeline);
        setIsLive(true);
        setLastUpdated(new Date());
      } else {
        setIsLive(false);
      }
    }

    poll();
    const interval = setInterval(poll, Math.max(1000, refreshRate * 1000));
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [refreshRate, autoRefresh, graphHistoryHours]);

  // Demo-mode simulation: only animates the placeholder sessions while we
  // haven't heard back from a real backend yet, so the UI still feels alive
  // during local development without the honeypot running.
  useEffect(() => {
    if (isLive || !autoRefresh) return;
    const interval = setInterval(() => {
      setSessions((old) =>
        old.map((session) => ({
          ...session,
          duration: session.duration + 1,
          commands: session.commands + Math.floor(Math.random() * 3),
        }))
      );
    }, 5000);

    return () => clearInterval(interval);
  }, [isLive, autoRefresh]);

  const activeSessions = sessions.filter((s) => s.status === "ACTIVE").length;
  const aiFlagged = sessions.filter((s) => s.risk > 80).length;

  return (
    <SessionContext.Provider
      value={{
        sessions,
        activeSessions,
        totalToday,
        averageDuration,
        aiFlagged,
        honeypotLocation,
        aiDecision,
        aiConfidence,
        predictedAttack,
        responseTime,
        totalCommandsProcessed,
        activityTimeline,
        isLive,
        lastUpdated,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export function useSessionContext() {
  const context = useContext(SessionContext);

  if (!context) {
    throw new Error(
      "useSessionContext must be used inside SessionProvider"
    );
  }

  return context;
}
