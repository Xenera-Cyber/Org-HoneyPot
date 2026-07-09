import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

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
}

export interface HoneypotLocation {
  name: string;
  latitude: number;
  longitude: number;
}

// EXTENDED THE CONTEXT TYPE INTERFACE
interface SessionContextType {
  sessions: Session[];
  activeSessions: number;
  totalToday: number;
  averageDuration: number;
  aiFlagged: number;
  honeypotLocation: HoneypotLocation;
  
  // NEW METRICS
  aiDecision: string;
  aiConfidence: number;
  predictedAttack: string;
  responseTime: number;
}

const SessionContext = createContext<SessionContextType | null>(null);

export function SessionProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const honeypotLocation: HoneypotLocation = {
    name: "XYNERA Honeypot",
    latitude: 28.6139,
    longitude: 77.2090,
  };

  const [sessions, setSessions] = useState<Session[]>([
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
      latitude: 52.5200,
      longitude: 13.4050,
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
  ]);

  useEffect(() => {
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
  }, []);

  const activeSessions = sessions.filter((s) => s.status === "ACTIVE").length;
  const totalToday = 431;
  const averageDuration = 12;
  const aiFlagged = sessions.filter((s) => s.risk > 80).length;

  // ADDED NEW CONSTANTS
  const aiDecision = "Credential Harvesting";
  const aiConfidence = 96;
  const predictedAttack = "Reverse Shell";
  const responseTime = 82;

  return (
    // UPDATED PROVIDER VALUE
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