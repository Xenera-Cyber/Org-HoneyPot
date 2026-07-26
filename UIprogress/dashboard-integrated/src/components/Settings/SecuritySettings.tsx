import useSettings from "../../hooks/useSettings";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";
import SettingsSelect from "./SettingsSelect";

export default function SecuritySettings() {

    const settings = useSettings();

    return (

        <div className="space-y-8">

            {/* Authentication */}

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Authentication
                </h2>

                <div className="space-y-4">

                    <SettingsToggle
                        label="Two-Factor Authentication"
                        description="Require OTP during administrator login."
                        checked={settings.twoFactor}
                        onChange={settings.setTwoFactor}
                    />

                    <SettingsToggle
                        label="Auto Logout"
                        description="Automatically logout inactive users."
                        checked={settings.autoLogout}
                        onChange={settings.setAutoLogout}
                    />

                    <SettingsInput
                        label="Session Timeout (minutes)"
                        value={settings.sessionTimeout}
                        type="number"
                        onChange={(v)=>
                            settings.setSessionTimeout(Number(v))
                        }
                    />

                </div>

            </div>

            {/* Access Control */}

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Access Control
                </h2>

                <div className="grid grid-cols-2 gap-6">

                    <SettingsInput
                        label="Allowed IP Address"
                        value={settings.allowedIP}
                        onChange={settings.setAllowedIP}
                    />

                    <SettingsSelect
                        label="User Role"
                        value={settings.defaultRole}
                        options={[
                            "Administrator",
                            "Analyst",
                            "Viewer",
                        ]}
                        onChange={settings.setDefaultRole}
                    />

                </div>

            </div>

            {/* Logging */}

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Audit Logging
                </h2>

                <div className="space-y-4">

                    <SettingsToggle
                        label="Enable Audit Logs"
                        description="Record every administrative action."
                        checked={settings.auditLogs}
                        onChange={settings.setAuditLogs}
                    />

                    <SettingsToggle
                        label="Failed Login Lockout"
                        description="Lock account after repeated failures."
                        checked={settings.lockout}
                        onChange={settings.setLockout}
                    />

                </div>

                {settings.auditLogs && (
                    <div className="mt-5 rounded-xl border border-white/5 bg-white/[0.02]">
                        <div className="flex items-center justify-between px-4 py-3 border-b border-white/5">
                            <span className="text-sm text-gray-400">
                                Recent settings changes ({settings.auditLog.length})
                            </span>
                            <button
                                onClick={settings.clearAuditLog}
                                className="text-xs text-gray-500 hover:text-white transition"
                            >
                                Clear
                            </button>
                        </div>
                        <div className="max-h-64 overflow-y-auto divide-y divide-white/5">
                            {settings.auditLog.length === 0 && (
                                <div className="px-4 py-4 text-sm text-gray-500">
                                    No changes recorded yet this session.
                                </div>
                            )}
                            {settings.auditLog.map((entry, i) => (
                                <div
                                    key={i}
                                    className="flex items-center justify-between px-4 py-2 text-sm"
                                >
                                    <span className="text-gray-300">
                                        Changed <span className="text-white font-medium">{entry.field}</span>{" "}
                                        to <span className="text-cyan-300">{entry.value}</span>
                                    </span>
                                    <span className="text-xs text-gray-500 shrink-0 ml-3">
                                        {entry.time}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

            </div>

        </div>

    );

}