import { useEffect, useRef, useState } from "react";
import { Lock } from "lucide-react";
import useSettings from "../hooks/useSettings";

const ACTIVITY_EVENTS = ["mousemove", "keydown", "click", "scroll", "touchstart"];

/**
 * Real inactivity-based lock screen, driven by Settings > Security >
 * Auto Logout + Session Timeout. There's no authentication system in
 * this app (no login, no backend session), so "unlocking" is just a
 * click-through rather than re-entering credentials - but the inactivity
 * detection and lock/unlock behavior itself is genuinely functional,
 * not a static toggle.
 */
export default function SessionLockOverlay() {
  const { autoLogout, sessionTimeout } = useSettings();
  const [locked, setLocked] = useState(false);
  const lastActivity = useRef(Date.now());

  useEffect(() => {
    if (!autoLogout) {
      setLocked(false);
      return;
    }

    function markActive() {
      lastActivity.current = Date.now();
    }

    ACTIVITY_EVENTS.forEach((evt) =>
      window.addEventListener(evt, markActive, { passive: true })
    );

    const timeoutMs = Math.max(1, sessionTimeout) * 60 * 1000;
    const interval = setInterval(() => {
      if (Date.now() - lastActivity.current >= timeoutMs) {
        setLocked(true);
      }
    }, 1000);

    return () => {
      ACTIVITY_EVENTS.forEach((evt) =>
        window.removeEventListener(evt, markActive)
      );
      clearInterval(interval);
    };
  }, [autoLogout, sessionTimeout]);

  if (!locked) return null;

  return (
    <div className="fixed inset-0 z-[999] flex items-center justify-center bg-black/80 backdrop-blur-md">
      <div className="w-full max-w-sm rounded-2xl border border-white/10 bg-[var(--bg-panel)] p-8 text-center shadow-2xl">
        <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-blue-500/10 border border-blue-500/20">
          <Lock className="text-blue-400" size={24} />
        </div>
        <h2 className="text-lg font-semibold text-white">Session Locked</h2>
        <p className="mt-2 text-sm text-gray-400">
          Locked after {sessionTimeout} minutes of inactivity, per Settings
          &gt; Security.
        </p>
        <button
          onClick={() => {
            lastActivity.current = Date.now();
            setLocked(false);
          }}
          className="mt-6 w-full rounded-lg bg-blue-500/20 border border-blue-500/30 py-2 text-sm font-medium text-blue-300 hover:bg-blue-500/30 transition"
        >
          Continue
        </button>
      </div>
    </div>
  );
}
