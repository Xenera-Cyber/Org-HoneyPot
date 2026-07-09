import useSettings from "../../hooks/useSettings";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";
import SettingsSelect from "./SettingsSelect";

export default function NotificationSettings() {

    const settings = useSettings();

    return (

        <div className="space-y-8">

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Alert Channels
                </h2>

                <div className="space-y-4">

                    <SettingsToggle
                        label="Desktop Notifications"
                        description="Receive browser desktop alerts."
                        checked={settings.desktopNotifications}
                        onChange={settings.setDesktopNotifications}
                    />

                    <SettingsToggle
                        label="Email Alerts"
                        description="Send critical events to email."
                        checked={settings.emailNotifications}
                        onChange={settings.setEmailNotifications}
                    />

                    <SettingsToggle
                        label="Telegram Alerts"
                        description="Send alerts through Telegram Bot."
                        checked={settings.telegramNotifications}
                        onChange={settings.setTelegramNotifications}
                    />

                    <SettingsToggle
                        label="Slack Alerts"
                        description="Forward alerts to Slack workspace."
                        checked={settings.slackNotifications}
                        onChange={settings.setSlackNotifications}
                    />

                </div>

            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Alert Severity
                </h2>

                <div className="grid grid-cols-2 gap-6">

                    <SettingsSelect
                        label="Minimum Alert Level"
                        value={settings.minimumAlertLevel}
                        options={[
                            "Low",
                            "Medium",
                            "High",
                            "Critical",
                        ]}
                        onChange={settings.setMinimumAlertLevel}
                    />

                    <SettingsInput
                        label="Email Address"
                        value={settings.alertEmail}
                        onChange={settings.setAlertEmail}
                    />

                    <SettingsInput
                        label="Telegram Chat ID"
                        value={settings.telegramChat}
                        onChange={settings.setTelegramChat}
                    />

                    <SettingsInput
                        label="Slack Webhook URL"
                        value={settings.slackWebhook}
                        onChange={settings.setSlackWebhook}
                    />

                </div>

            </div>

        </div>

    );

}