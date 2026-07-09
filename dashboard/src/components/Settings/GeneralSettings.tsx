import useSettings from "../../hooks/useSettings";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";
import SettingsSelect from "./SettingsSelect";

export default function GeneralSettings() {

    const settings = useSettings();

    return (

        <div className="space-y-8">

            <div className="grid grid-cols-2 gap-6">

                <SettingsSelect
                    label="Theme"
                    value={settings.theme}
                    options={[
                        "Dark",
                        "Light",
                    ]}
                    onChange={(v) =>
                        settings.setTheme(
                            v as "Dark" | "Light"
                        )
                    }
                />

                <SettingsSelect
                    label="Language"
                    value={settings.language}
                    options={[
                        "English",
                        "Hindi",
                    ]}
                    onChange={settings.setLanguage}
                />

                <SettingsSelect
                    label="Timezone"
                    value={settings.timezone}
                    options={[
                        "UTC +05:30",
                        "UTC",
                    ]}
                    onChange={settings.setTimezone}
                />

                <SettingsInput
                    label="Refresh Rate (sec)"
                    value={settings.refreshRate}
                    type="number"
                    onChange={(v) =>
                        settings.setRefreshRate(Number(v))
                    }
                />

            </div>

            <SettingsToggle
                label="Auto Refresh"

                description="Automatically refresh dashboard data."

                checked={settings.autoRefresh}

                onChange={settings.setAutoRefresh}
            />

        </div>

    );

}