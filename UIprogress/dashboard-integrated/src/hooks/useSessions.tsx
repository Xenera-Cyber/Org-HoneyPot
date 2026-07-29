import { useSessionContext } from "../context/SessionContext";
export type { Session } from "../context/SessionContext";

export default function useSessions() {
  return useSessionContext();
}