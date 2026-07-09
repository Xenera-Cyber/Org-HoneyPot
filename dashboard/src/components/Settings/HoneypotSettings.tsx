import useSettings from "../../hooks/useSettings";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";

export default function HoneypotSettings() {

    const settings = useSettings();

    return (

        <div className="space-y-8">

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
                        description="Enable fake web server."
                        checked={settings.httpEnabled}
                        onChange={settings.setHTTPEnabled}
                    />

                    <SettingsToggle
                        label="FTP Honeypot"
                        description="Enable FTP deception."
                        checked={settings.ftpEnabled}
                        onChange={settings.setFTPEnabled}
                    />

                </div>

            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Session Configuration
                </h2>

                <div className="grid grid-cols-2 gap-6">

                    <SettingsInput
                        label="Maximum Concurrent Sessions"
                        value={50}
                        onChange={() => {}}
                    />

                    <SettingsInput
                        label="Session Timeout (minutes)"
                        value={30}
                        onChange={() => {}}
                    />

                    <SettingsInput
                        label="Log Retention (days)"
                        value={30}
                        onChange={() => {}}
                    />

                    <SettingsInput
                        label="Maximum Commands Per Session"
                        value={250}
                        onChange={() => {}}
                    />

                </div>

            </div>

        </div>

    );

}