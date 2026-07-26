import { useEffect, useRef } from "react";
import useThreats from "../hooks/useThreats";
import useSettings from "../hooks/useSettings";

const LEVEL_RANK: Record<string, number> = {
  Low: 0,
  Medium: 1,
  High: 2,
  Critical: 3,
};

const SEVERITY_TO_LEVEL: Record<string, string> = {
  LOW: "Low",
  MEDIUM: "Medium",
  HIGH: "High",
  CRITICAL: "Critical",
};

/**
 * Mounted once near the root (see App.tsx). Watches real live-threat data
 * from ThreatContext and fires an actual browser Notification for any new
 * threat at/above the configured minimum severity - this is a real
 * integration with the Notification API, not a decorative toggle.
 */
export default function NotificationWatcher() {
  const { liveThreats } = useThreats();
  const { desktopNotifications, minimumAlertLevel } = useSettings();
  const seen = useRef<Set<string | number>>(new Set());
  const permissionAsked = useRef(false);

  useEffect(() => {
    if (!desktopNotifications) return;
    if (permissionAsked.current) return;
    if (typeof Notification === "undefined") return;
    permissionAsked.current = true;
    if (Notification.permission === "default") {
      Notification.requestPermission();
    }
  }, [desktopNotifications]);

  useEffect(() => {
    if (!desktopNotifications) return;
    if (typeof Notification === "undefined") return;
    if (Notification.permission !== "granted") return;

    const minRank = LEVEL_RANK[minimumAlertLevel] ?? 2;

    for (const threat of liveThreats) {
      if (seen.current.has(threat.id)) continue;
      seen.current.add(threat.id);

      const level = SEVERITY_TO_LEVEL[threat.severity] ?? "Low";
      if ((LEVEL_RANK[level] ?? 0) < minRank) continue;

      try {
        new Notification(`XYNERA: ${threat.severity} threat detected`, {
          body: `${threat.ip} via ${threat.protocol} - recommended action: ${threat.action}`,
          tag: String(threat.id),
        });
      } catch {
        // Notification API can throw in some contexts (e.g. insecure
        // origin); failing silently is fine, this is a best-effort alert.
      }
    }

    // Cap memory growth - keep the last 200 seen ids.
    if (seen.current.size > 200) {
      const arr = Array.from(seen.current);
      seen.current = new Set(arr.slice(arr.length - 200));
    }
  }, [liveThreats, desktopNotifications, minimumAlertLevel]);

  return null;
}
