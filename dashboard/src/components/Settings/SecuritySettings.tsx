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

            </div>

        </div>

    );

}