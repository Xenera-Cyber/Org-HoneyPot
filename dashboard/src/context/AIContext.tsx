import {
  createContext,
  useContext,
} from "react";

// 1. DEFINED THE RECENT DECISION RECORD INTERFACE
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

// 2. EXTENDED THE MAIN CONTEXT INTERFACE
interface AIContextType {
  confidence: number;
  
  // ADDED CONFIDENCE BREAKDOWN INTERFACE EXTENSION
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
}

const AIContext = createContext<AIContextType | null>(null);

export function AIProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AIContext.Provider
      value={{
        confidence: 96,
        
        // ADDED THE CONFIDENCE BREAKDOWN METRIC MOCK DATA
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
          {
            id: 1,
            attack: "SSH Brute Force",
            time: "02:41:14",
            risk: "Critical",
            confidence: 98,
            kbHits: 42,
            responseTime: 208,
            guardrails: 3,
          },
          {
            id: 2,
            attack: "HTTP Directory Scan",
            time: "02:40:51",
            risk: "High",
            confidence: 91,
            kbHits: 25,
            responseTime: 214,
            guardrails: 1,
          },
          {
            id: 3,
            attack: "Credential Stuffing",
            time: "02:38:09",
            risk: "Critical",
            confidence: 99,
            kbHits: 61,
            responseTime: 196,
            guardrails: 4,
          },
          {
            id: 4,
            attack: "FTP Enumeration",
            time: "02:37:30",
            risk: "Medium",
            confidence: 78,
            kbHits: 16,
            responseTime: 241,
            guardrails: 0,
          },
        ],
      }}
    >
      {children}
    </AIContext.Provider>
  );
}

export function useAIContext() {
  const ctx = useContext(AIContext);

  if (!ctx)
    throw new Error(
      "useAIContext must be inside AIProvider"
    );

  return ctx;
}