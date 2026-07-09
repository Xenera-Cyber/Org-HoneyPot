import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

export interface EventLog {
  id: number;
  time: string;
  title: string;
  detail: string;
  type: string;
}

export interface Honeypot {
  name: string;
  port: number;
  sessions: number;
  status: "Running" | "Idle" | "Offline";
}

export interface Service {
  name: string;
  status: "Running" | "Idle" | "Offline";
  latency: string;
}

interface MonitoringData {
  cpu: number;
  memory: number;
  disk: number;

  upload: number;
  download: number;

  uptime: number;

  events: EventLog[];

  honeypots: Honeypot[];

  services: Service[];
}

const MonitoringContext = createContext<MonitoringData | null>(null);

const eventTitles = [
  "SSH Login Attempt",
  "Port Scan Started",
  "Reverse Shell Detected",
  "AI Generated Deception",
  "Session Terminated",
  "Credential Harvest Attempt",
  "Privilege Escalation",
  "Command Executed",
];

const eventDetails = [
  "192.168.20.18",
  "192.168.20.41",
  "Fake filesystem deployed",
  "/bin/bash outbound connection",
  "Session closed",
  "Hydra detected",
  "Nmap reconnaissance",
  "AI diverted attacker",
];

export function MonitoringProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [data, setData] = useState<MonitoringData>({
    cpu: 52,
    memory: 43,
    disk: 31,

    upload: 2.3,
    download: 8.4,

    uptime: 0,

    events: [
      {
        id: 1,
        time: new Date().toLocaleTimeString(),
        title: "Monitoring Started",
        detail: "XYNERA initialized successfully",
        type: "info",
      },
    ],

    honeypots: [
      {
        name: "SSH Honeypot",
        port: 2222,
        sessions: 4,
        status: "Running",
      },
      {
        name: "HTTP Honeypot",
        port: 8080,
        sessions: 9,
        status: "Running",
      },
      {
        name: "FTP Honeypot",
        port: 2121,
        sessions: 2,
        status: "Running",
      },
      {
        name: "SMTP Honeypot",
        port: 2525,
        sessions: 0,
        status: "Idle",
      },
      {
        name: "Telnet Honeypot",
        port: 2323,
        sessions: 1,
        status: "Running",
      },
      {
        name: "Database Honeypot",
        port: 3306,
        sessions: 3,
        status: "Running",
      },
    ],

    services: [
      {
        name: "SSH Service",
        status: "Running",
        latency: "8 ms",
      },
      {
        name: "HTTP Service",
        status: "Running",
        latency: "12 ms",
      },
      {
        name: "FTP Service",
        status: "Running",
        latency: "14 ms",
      },
      {
        name: "SMTP Service",
        status: "Idle",
        latency: "0 ms",
      },
    ],
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setData((prev) => {
        const event = {
          id: Date.now(),

          time: new Date().toLocaleTimeString(),

          title:
            eventTitles[
              Math.floor(Math.random() * eventTitles.length)
            ],

          detail:
            eventDetails[
              Math.floor(Math.random() * eventDetails.length)
            ],

          type: "event",
        };

        return {
          ...prev,

          cpu: Math.max(
            10,
            Math.min(95, prev.cpu + (Math.random() * 8 - 4))
          ),

          memory: Math.max(
            20,
            Math.min(90, prev.memory + (Math.random() * 4 - 2))
          ),

          disk: Math.max(
            20,
            Math.min(70, prev.disk + (Math.random() * 2 - 1))
          ),

          upload: Number((Math.random() * 5).toFixed(1)),

          download: Number((Math.random() * 10).toFixed(1)),

          uptime: prev.uptime + 1,

          events: [event, ...prev.events].slice(0, 20),

          honeypots: prev.honeypots.map((honeypot) => {
            let sessions = honeypot.sessions;

            if (honeypot.status !== "Offline") {
              sessions += Math.floor(Math.random() * 3) - 1;
              sessions = Math.max(0, sessions);
            }

            let status: Honeypot["status"] = honeypot.status;

            const random = Math.random();

            if (random < 0.03) {
              status = "Offline";
            } else if (random < 0.10) {
              status = "Idle";
            } else {
              status = "Running";
            }

            return {
              ...honeypot,
              sessions,
              status,
            };
          }),

          services: prev.services.map((service) => {
            let status: Service["status"] = service.status;

            const random = Math.random();

            if (random < 0.03) {
              status = "Offline";
            } else if (random < 0.10) {
              status = "Idle";
            } else {
              status = "Running";
            }

            return {
              ...service,
              status,
              latency: `${Math.floor(
                5 + Math.random() * 18
              )} ms`,
            };
          }),
        };
      });
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  return (
    <MonitoringContext.Provider value={data}>
      {children}
    </MonitoringContext.Provider>
  );
}

export function useMonitoringContext() {
  const context = useContext(MonitoringContext);

  if (!context) {
    throw new Error(
      "useMonitoringContext must be used inside MonitoringProvider"
    );
  }

  return context;
}