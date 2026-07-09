import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

interface ThreatStats {
  threatScore: number;
  activeThreats: number;
  blockedIPs: number;
  aiConfidence: number;
}

interface HeatmapPoint {
  hour: string;
  attacks: number;
}

interface SeverityPoint {
  time: string;
  low: number;
  medium: number;
  high: number;
  critical: number;
}

interface AttackSource {
  ip: string;
  country: string;
  protocol: string;
  attacks: number;
  risk: number;
}

interface AttackType {
  name: string;
  percentage: number;
  color: string;
}

interface LiveThreat {
  id: number;
  ip: string;
  protocol: string;
  severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  confidence: number;
  status: string;
  action: string;
}

export interface ThreatSummary {
  todaysAttacks: number;
  activeInvestigations: number;
  criticalThreats: number;
  targetedPort: string;
  averageThreatScore: number;
  aiConfidence: number;
  riskIndex: number;
  peakHour: string;
  topOrigin: string;
}

interface ThreatContextData extends ThreatStats {
  heatmap: HeatmapPoint[];
  severity: SeverityPoint[];
  sources: AttackSource[];
  attackTypes: AttackType[];
  liveThreats: LiveThreat[];
  summary: ThreatSummary;
}

const ThreatContext = createContext<ThreatContextData | null>(null);

const initialHeatmap = Array.from({ length: 24 }, (_, i) => ({
  hour: `${i.toString().padStart(2, "0")}:00`,
  attacks: Math.floor(Math.random() * 90) + 10,
}));

const severityData = Array.from({ length: 12 }, (_, i) => ({
  time: `${(i * 2).toString().padStart(2, "0")}:00`,
  low: Math.floor(Math.random() * 10) + 5,
  medium: Math.floor(Math.random() * 8) + 3,
  high: Math.floor(Math.random() * 6) + 2,
  critical: Math.floor(Math.random() * 3),
}));

const sourceData = [
  {
    ip: "185.194.12.55",
    country: "RU",
    protocol: "SSH",
    attacks: 84,
    risk: 94,
  },
  {
    ip: "103.44.12.17",
    country: "CN",
    protocol: "HTTP",
    attacks: 71,
    risk: 88,
  },
  {
    ip: "91.77.13.201",
    country: "US",
    protocol: "FTP",
    attacks: 53,
    risk: 74,
  },
  {
    ip: "178.14.2.16",
    country: "DE",
    protocol: "SMTP",
    attacks: 42,
    risk: 69,
  },
  {
    ip: "43.201.87.2",
    country: "IN",
    protocol: "SSH",
    attacks: 36,
    risk: 61,
  },
];

const attackTypeData = [
  {
    name: "SSH",
    percentage: 46,
    color: "bg-cyan-500",
  },
  {
    name: "HTTP",
    percentage: 28,
    color: "bg-green-500",
  },
  {
    name: "FTP",
    percentage: 14,
    color: "bg-yellow-500",
  },
  {
    name: "SMTP",
    percentage: 8,
    color: "bg-orange-500",
  },
  {
    name: "OTHER",
    percentage: 4,
    color: "bg-purple-500",
  },
];

const liveThreatData: LiveThreat[] = [
  {
    id: 1,
    ip: "185.194.12.55",
    protocol: "SSH",
    severity: "HIGH",
    confidence: 97,
    status: "Active",
    action: "Deploy Deception",
  },
  {
    id: 2,
    ip: "103.44.12.17",
    protocol: "HTTP",
    severity: "MEDIUM",
    confidence: 91,
    status: "Monitoring",
    action: "Observe",
  },
  {
    id: 3,
    ip: "91.77.13.201",
    protocol: "FTP",
    severity: "LOW",
    confidence: 82,
    status: "Contained",
    action: "Sandbox",
  },
  {
    id: 4,
    ip: "178.14.2.16",
    protocol: "SMTP",
    severity: "CRITICAL",
    confidence: 99,
    status: "Blocked",
    action: "Isolate",
  },
];

const statusCycle: string[] = ["Active", "Monitoring", "Contained", "Blocked"];
const severityCycle: ("LOW" | "MEDIUM" | "HIGH" | "CRITICAL")[] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];

export function ThreatProvider({ children }: { children: ReactNode }) {
  const [stats, setStats] = useState<ThreatContextData>({
    threatScore: 82,
    activeThreats: 37,
    blockedIPs: 142,
    aiConfidence: 96,
    heatmap: initialHeatmap,
    severity: severityData,
    sources: sourceData,
    attackTypes: attackTypeData,
    liveThreats: liveThreatData,
    summary: {
      todaysAttacks: 238,
      activeInvestigations: 31,
      criticalThreats: 9,
      targetedPort: "22 (SSH)",
      averageThreatScore: 81.2,
      aiConfidence: 93,
      riskIndex: 86,
      peakHour: "14:00",
      topOrigin: "185.194.x.x",
    },
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setStats((prev) => ({
        threatScore: Math.max(
          10,
          Math.min(100, prev.threatScore + Math.floor(Math.random() * 5 - 2))
        ),

        activeThreats: Math.max(
          0,
          prev.activeThreats + Math.floor(Math.random() * 5 - 2)
        ),

        blockedIPs: prev.blockedIPs + Math.floor(Math.random() * 3),

        aiConfidence: Math.max(
          90,
          Math.min(100, prev.aiConfidence + (Math.random() * 0.6 - 0.3))
        ),

        heatmap: prev.heatmap.map((item) => ({
          ...item,
          attacks: Math.max(0, item.attacks + Math.floor(Math.random() * 11 - 5)),
        })),

        severity: prev.severity.map((item) => ({
          ...item,
          low: Math.max(0, item.low + Math.floor(Math.random() * 3 - 1)),
          medium: Math.max(0, item.medium + Math.floor(Math.random() * 3 - 1)),
          high: Math.max(0, item.high + Math.floor(Math.random() * 3 - 1)),
          critical: Math.max(0, item.critical + Math.floor(Math.random() * 3 - 1)),
        })),

        sources: prev.sources.map((item) => ({
          ...item,
          attacks: Math.max(0, item.attacks + Math.floor(Math.random() * 5 - 2)),
          risk: Math.max(30, Math.min(100, item.risk + Math.floor(Math.random() * 5 - 2))),
        })),

        attackTypes: prev.attackTypes.map((item) => ({
          ...item,
          percentage: Math.max(
            2,
            Math.min(60, item.percentage + Math.floor(Math.random() * 5 - 2))
          ),
        })),

        liveThreats: prev.liveThreats.map((item) => {
          const shouldChangeState = Math.random() > 0.7;
          
          let nextStatus = item.status;
          let nextSeverity = item.severity;

          if (shouldChangeState) {
            const currentStatusIndex = statusCycle.indexOf(item.status);
            const nextStatusIndex = (currentStatusIndex + 1) % statusCycle.length;
            nextStatus = statusCycle[nextStatusIndex];

            const currentSeverityIndex = severityCycle.indexOf(item.severity);
            const nextSeverityIndex = (currentSeverityIndex + (Math.random() > 0.5 ? 1 : -1) + severityCycle.length) % severityCycle.length;
            nextSeverity = severityCycle[nextSeverityIndex];
          }

          return {
            ...item,
            confidence: Math.max(
              70,
              Math.min(100, item.confidence + Math.floor(Math.random() * 3 - 1))
            ),
            status: nextStatus,
            severity: nextSeverity,
          };
        }),

        summary: {
          ...prev.summary,
          todaysAttacks: prev.summary.todaysAttacks + (Math.random() < 0.35 ? 1 : 0),
          activeInvestigations: Math.max(
            0,
            prev.summary.activeInvestigations + Math.floor(Math.random() * 3) - 1
          ),
          criticalThreats: Math.max(
            0,
            prev.summary.criticalThreats + Math.floor(Math.random() * 3) - 1
          ),
          averageThreatScore: Number(
            (prev.summary.averageThreatScore + (Math.random() * 4 - 2)).toFixed(1)
          ),
          aiConfidence: Math.min(
            99,
            Math.max(80, prev.summary.aiConfidence + Math.floor(Math.random() * 3) - 1)
          ),
          riskIndex: Math.min(
            100,
            Math.max(60, prev.summary.riskIndex + Math.floor(Math.random() * 5) - 2)
          ),
        },
      }));
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <ThreatContext.Provider value={stats}>
      {children}
    </ThreatContext.Provider>
  );
}

export function useThreatContext() {
  const context = useContext(ThreatContext);
  if (!context) {
    throw new Error("useThreatContext must be used inside ThreatProvider");
  }
  return context;
}