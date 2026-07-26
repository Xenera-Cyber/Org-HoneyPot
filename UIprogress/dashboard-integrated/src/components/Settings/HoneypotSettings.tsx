import { useEffect, useRef, useState } from "react";
import useSettings from "../../hooks/useSettings";
import { apiGet, apiPost } from "../../lib/api";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";

interface HoneypotBackendConfig {
    maxConcurrentSessions: number;
    sessionTimeoutMinutes: number;
    logRetentionDays: number;
    maxCommandsPerSession: number;
}

export default function HoneypotSettings() {

    const settings = useSettings();
    const [reachable, setReachable] = useState(false);
    const [saveState, setSaveState] = useState<
        "idle" | "saving" | "saved" | "error"
    >("idle");
    const seeded = useRef(false);

    async function refresh() {
        const data = await apiGet<HoneypotBackendConfig>(
            "/api/honeypot/config"
        );
        if (data) {
            setReachable(true);
            if (!seeded.current) {
                seeded.current = true;
                settings.setMaxConcurrentSessions(data.maxConcurrentSessions);
                settings.setSessionTimeoutMinutes(data.sessionTimeoutMinutes);
                settings.setLogRetentionDays(data.logRetentionDays);
                settings.setMaxCommandsPerSession(data.maxCommandsPerSession);
            }
        } else {
            setReachable(false);
        }
    }

    useEffect(() => {
        refresh();
        const interval = setInterval(refresh, 15000);
        return () => clearInterval(interval);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    async function applyToBackend() {
        setSaveState("saving");
        const { ok } = await apiPost<HoneypotBackendConfig>(
            "/api/honeypot/config",
            {
                maxConcurrentSessions: settings.maxConcurrentSessions,
                sessionTimeoutMinutes: settings.sessionTimeoutMinutes,
                logRetentionDays: settings.logRetentionDays,
                maxCommandsPerSession: settings.maxCommandsPerSession,
            }
        );
        if (ok) {
            setReachable(true);
            setSaveState("saved");
            setTimeout(() => setSaveState("idle"), 2500);
        } else {
            setSaveState("error");
        }
    }

    return (

        <div className="space-y-8">

            <div className="flex items-center justify-between rounded-xl border border-white/5 bg-white/[0.02] px-4 py-3">
                <div className="text-sm">
                    <span className="text-gray-400">dashboard_api / honeypot config: </span>
                    <span
                        className={
                            reachable
                                ? "font-medium text-green-400"
                                : "font-medium text-red-400"
                        }
                    >
                        {reachable ? "Connected" : "Not reachable"}
                    </span>
                </div>
                <button
                    onClick={refresh}
                    className="text-xs text-gray-400 hover:text-white transition"
                >
                    Refresh status
                </button>
            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Honeypot Services
                </h2>

                <div className="space-y-4">

                    <SettingsToggle
                        label="SSH Honeypot"
                        description="Enable SSH deception service."
                        checked={settings.sshEnabled}
                        onChange={settings.setSSHEnabled}
                    />

                    <SettingsToggle
                        label="HTTP Honeypot"
                        description="Enable fake web server. (Not yet implemented by the honeypot itself - reported as Offline on Monitoring either way.)"
                        checked={settings.httpEnabled}
                        onChange={settings.setHTTPEnabled}
                    />

                    <SettingsToggle
                        label="FTP Honeypot"
                        description="Enable FTP deception. (Not yet implemented by the honeypot itself - reported as Offline on Monitoring either way.)"
                        checked={settings.ftpEnabled}
                        onChange={settings.setFTPEnabled}
                    />

                </div>

            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Session Configuration
                </h2>

                <p className="mb-4 text-sm text-gray-500">
                    These are actually enforced by server.py - new connections
                    beyond the limit are rejected, idle sessions are
                    disconnected, and sessions are cut off past the command
                    cap.
                </p>

                <div className="grid grid-cols-2 gap-6">

                    <SettingsInput
                        label="Maximum Concurrent Sessions"
                        value={settings.maxConcurrentSessions}
                        type="number"
                        onChange={(v) =>
                            settings.setMaxConcurrentSessions(Number(v))
                        }
                    />

                    <SettingsInput
                        label="Session Timeout (minutes)"
                        value={settings.sessionTimeoutMinutes}
                        type="number"
                        onChange={(v) =>
                            settings.setSessionTimeoutMinutes(Number(v))
                        }
                    />

                    <SettingsInput
                        label="Log Retention (days)"
                        value={settings.logRetentionDays}
                        type="number"
                        onChange={(v) =>
                            settings.setLogRetentionDays(Number(v))
                        }
                    />

                    <SettingsInput
                        label="Maximum Commands Per Session"
                        value={settings.maxCommandsPerSession}
                        type="number"
                        onChange={(v) =>
                            settings.setMaxCommandsPerSession(Number(v))
                        }
                    />

                </div>

                <div className="mt-6 flex items-center gap-4">
                    <button
                        onClick={applyToBackend}
                        disabled={saveState === "saving"}
                        className="rounded-lg bg-blue-500/20 border border-blue-500/30 px-4 py-2 text-sm font-medium text-blue-300 hover:bg-blue-500/30 transition disabled:opacity-50"
                    >
                        {saveState === "saving" ? "Saving..." : "Save & Apply"}
                    </button>

                    {saveState === "saved" && (
                        <span className="text-sm text-green-400">
                            Applied - new connections will use these limits immediately.
                        </span>
                    )}
                    {saveState === "error" && (
                        <span className="text-sm text-red-400">
                            Couldn't reach dashboard_api.py - is it running?
                        </span>
                    )}
                </div>

            </div>

        </div>

    );

}
