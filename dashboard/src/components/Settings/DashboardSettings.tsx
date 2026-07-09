import useSettings from "../../hooks/useSettings";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";

export default function DashboardSettings() {
    const settings = useSettings();

    return (
        <div className="space-y-8">

            <div>
                <h2 className="mb-5 text-xl font-semibold text-white">
                    Dashboard Preferences
                </h2>

                <div className="grid grid-cols-2 gap-6">

                    <SettingsInput
                        label="Refresh Rate (seconds)"
                        value={settings.refreshRate}
                        type="number"
                        onChange={(v) =>
                            settings.setRefreshRate(Number(v))
                        }
                    />

                    <SettingsInput
                        label="Maximum Graph History"
                        value={24}
                        type="number"
                        onChange={() => {}}
                    />

                </div>
            </div>

            <div>
                <h2 className="mb-5 text-xl font-semibold text-white">
                    Display Options
                </h2>

                <div className="space-y-4">

                    <SettingsToggle
                        label="Auto Refresh"
                        description="Automatically refresh dashboard data."
                        checked={settings.autoRefresh}
                        onChange={settings.setAutoRefresh}
                    />

                    <SettingsToggle
                        label="Show Attack Routes"
                        description="Display animated attack paths on the world map."
                        checked={settings.showAttackRoutes}
                        onChange={settings.setShowAttackRoutes}
                    />

                    <SettingsToggle
                        label="Enable Animations"
                        description="Enable UI animations and transitions."
                        checked={settings.animations}
                        onChange={settings.setAnimations}
                    />

                    <SettingsToggle
                        label="Compact Mode"
                        description="Reduce dashboard spacing."
                        checked={settings.compactMode}
                        onChange={settings.setCompactMode}
                    />

                    <SettingsToggle
                        label="Show Last Updated"
                        description="Display timestamps on dashboard widgets."
                        checked={settings.showLastUpdated}
                        onChange={settings.setShowLastUpdated}
                    />

                </div>
            </div>

        </div>
    );
}