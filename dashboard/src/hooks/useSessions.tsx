import { useSessionContext } from "../context/SessionContext";

export default function useSessions() {
  return useSessionContext();
}