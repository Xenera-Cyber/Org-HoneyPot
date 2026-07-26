import { useState } from "react";
import useSettings from "../../hooks/useSettings";
import { apiPost } from "../../lib/api";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";
import SettingsSelect from "./SettingsSelect";

function TestButton({
    channel,
    settings,
}: {
    channel: "slack" | "telegram";
    settings: ReturnType<typeof useSettings>;
}) {
    const [state, setState] = useState<"idle" | "sending" | "sent" | "error">(
        "idle"
    );
    const [error, setError] = useState<string | null>(null);

    async function send() {
        setState("sending");
        setError(null);
        const { ok, data } = await apiPost<{ ok: boolean; error?: string }>(
            "/api/notify",
            {
                channel,
                title: "XYNERA Test Alert",
                message: "This is a test notification from your dashboard's Settings page.",
                slackWebhook: settings.slackWebhook,
                telegramBotToken: settings.telegramBotToken,
                telegramChat: settings.telegramChat,
            }
        );
        if (ok && data?.ok) {
            setState("sent");
            setTimeout(() => setState("idle"), 2500);
        } else {
            setState("error");
            setError(data?.error ?? "Couldn't reach the dashboard API.");
        }
    }

    return (
        <div className="flex items-center gap-3">
            <button
                onClick={send}
                disabled={state === "sending"}
                className="rounded-lg bg-white/5 border border-white/10 px-3 py-1.5 text-xs font-medium text-gray-300 hover:bg-white/10 transition disabled:opacity-50"
            >
                {state === "sending" ? "Sending..." : "Send Test Alert"}
            </button>
            {state === "sent" && (
                <span className="text-xs text-green-400">Sent!</span>
            )}
            {state === "error" && (
                <span className="text-xs text-red-400">{error}</span>
            )}
        </div>
    );
}

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
                        description="Real browser notifications for new high-severity threats (uses the Notification API - your browser will ask to allow this once)."
                        checked={settings.desktopNotifications}
                        onChange={settings.setDesktopNotifications}
                    />

                    <SettingsToggle
                        label="Email Alerts"
                        description="Send critical events to email. Requires an SMTP relay, which isn't configured in this build - saved here for when one is added."
                        checked={settings.emailNotifications}
                        onChange={settings.setEmailNotifications}
                    />

                    <SettingsToggle
                        label="Telegram Alerts"
                        description="Send alerts through a Telegram bot."
                        checked={settings.telegramNotifications}
                        onChange={settings.setTelegramNotifications}
                    />

                    <SettingsToggle
                        label="Slack Alerts"
                        description="Forward alerts to a Slack workspace via incoming webhook."
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

                </div>

            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Telegram
                </h2>

                <div className="grid grid-cols-2 gap-6 items-end">

                    <SettingsInput
                        label="Bot Token"
                        value={settings.telegramBotToken}
                        onChange={settings.setTelegramBotToken}
                    />

                    <SettingsInput
                        label="Telegram Chat ID"
                        value={settings.telegramChat}
                        onChange={settings.setTelegramChat}
                    />

                </div>

                <div className="mt-3">
                    <TestButton channel="telegram" settings={settings} />
                </div>

            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Slack
                </h2>

                <SettingsInput
                    label="Slack Webhook URL"
                    value={settings.slackWebhook}
                    onChange={settings.setSlackWebhook}
                />

                <div className="mt-3">
                    <TestButton channel="slack" settings={settings} />
                </div>

            </div>

        </div>

    );

}
