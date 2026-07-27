import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";
import { apiGet, apiPost } from "../lib/api";
import { useSettingsContext } from "./SettingsContext";

export interface RecentDecision {
  id: number;
  attack: string;
  time: string;
  risk: "Critical" | "High" | "Medium" | "Low";
  confidence: number;
  kbHits: number;
  responseTime: number;
  guardrails: number;
}

export interface AIBackendConfig {
  personality: string;
  model: string;
  confidenceThreshold: number;
  temperature: number;
  maxContext: number;
  maxResponseLength: number;
  ragEnabled: boolean;
  guardrailsEnabled: boolean;
}

interface AIContextType {
  confidence: number;

  confidenceBreakdown: {
    detection: number;
    classification: number;
    rag: number;
    prediction: number;
    response: number;
  };

  personality: string;
  predictedAttack: string;
  kbHits: number;
  ragStatus: "Healthy" | "Slow" | "Offline";
  guardrailBlocks: number;
  responseTime: number;
  recentDecisions: RecentDecision[];

  isLive: boolean;
  engineOnline: boolean;

  // Live config of the xynera-ai backend (Settings > AI reads/writes this
  // for real instead of just holding local UI state).
  backendConfig: AIBackendConfig | null;
  backendReachable: boolean;
  refreshBackendConfig: () => Promise<void>;
  saveBackendConfig: (
    partial: Partial<AIBackendConfig>
  ) => Promise<{ ok: boolean; error?: string }>;
}

const AIContext = createContext<AIContextType | null>(null);

const DEMO_STATE: Omit<
  AIContextType,
  | "isLive"
  | "engineOnline"
  | "backendConfig"
  | "backendReachable"
  | "refreshBackendConfig"
  | "saveBackendConfig"
> = {
  confidence: 96,
  confidenceBreakdown: {
    detection: 96,
    classification: 91,
    rag: 84,
    prediction: 93,
    response: 88,
  },
  personality: "Adaptive Defender",
  predictedAttack: "Credential Stuffing",
  kbHits: 2384,
  ragStatus: "Healthy",
  guardrailBlocks: 14,
  responseTime: 214,
  recentDecisions: [
    { id: 1, attack: "SSH Brute Force", time: "02:41:14", risk: "Critical", confidence: 98, kbHits: 42, responseTime: 208, guardrails: 3 },
    { id: 2, attack: "HTTP Directory Scan", time: "02:40:51", risk: "High", confidence: 91, kbHits: 25, responseTime: 214, guardrails: 1 },
    { id: 3, attack: "Credential Stuffing", time: "02:38:09", risk: "Critical", confidence: 99, kbHits: 61, responseTime: 196, guardrails: 4 },
    { id: 4, attack: "FTP Enumeration", time: "02:37:30", risk: "Medium", confidence: 78, kbHits: 16, responseTime: 241, guardrails: 0 },
  ],
};

export function AIProvider({ children }: { children: React.ReactNode }) {
  const { refreshRate, autoRefresh } = useSettingsContext();
  const [state, setState] = useState(DEMO_STATE);
  const [isLive, setIsLive] = useState(false);
  const [engineOnline, setEngineOnline] = useState(false);
  const [backendConfig, setBackendConfig] = useState<AIBackendConfig | null>(
    null
  );
  const [backendReachable, setBackendReachable] = useState(false);

  useEffect(() => {
    if (!autoRefresh) return;
    let cancelled = false;

    async function poll() {
      const live = await apiGet<
        Omit<AIContextType, "isLive" | "engineOnline" | "backendConfig" | "backendReachable" | "refreshBackendConfig" | "saveBackendConfig"> & {
          engineOnline: boolean;
        }
      >("/api/ai");
      if (cancelled) return;

      if (live) {
        setState(live);
        setEngineOnline(live.engineOnline);
        setIsLive(true);
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
  }, [refreshRate, autoRefresh]);

  async function refreshBackendConfig() {
    const result = await apiGet<{
      reachable: boolean;
      config: AIBackendConfig | null;
    }>("/api/ai/config");
    if (result) {
      setBackendReachable(result.reachable);
      setBackendConfig(result.config);
    } else {
      setBackendReachable(false);
    }
  }

  async function saveBackendConfig(partial: Partial<AIBackendConfig>) {
    const { ok, data } = await apiPost<{
      reachable: boolean;
      config: AIBackendConfig | null;
      error?: string;
    }>("/api/ai/config", partial);

    if (ok && data) {
      setBackendReachable(data.reachable);
      setBackendConfig(data.config);
      return { ok: true };
    }

    setBackendReachable(false);
    return {
      ok: false,
      error:
        data?.error ??
        "Couldn't reach the AI backend (xynera-ai/api_server.py). Start it, then try again.",
    };
  }

  useEffect(() => {
    refreshBackendConfig();
    const interval = setInterval(refreshBackendConfig, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <AIContext.Provider
      value={{
        ...state,
        isLive,
        engineOnline,
        backendConfig,
        backendReachable,
        refreshBackendConfig,
        saveBackendConfig,
      }}
    >
      {children}
    </AIContext.Provider>
  );
}

export function useAIContext() {
  const ctx = useContext(AIContext);

  if (!ctx) throw new Error("useAIContext must be inside AIProvider");

  return ctx;
}
