import useSettings from "../../hooks/useSettings";
import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";
import SettingsSelect from "./SettingsSelect";

const themeOptions = [
  { value: "dark", label: "Dark" },
  { value: "light", label: "Light" },
  { value: "ocean", label: "Ocean" },
  { value: "midnight", label: "Midnight" },
  { value: "forest", label: "Forest" },
];

export default function GeneralSettings() {
  const settings = useSettings();

  return (
    <div className="space-y-8">
      <div>
        <h2 className="mb-5 text-xl font-semibold text-[var(--text-primary)]">
          Appearance
        </h2>
        <div className="grid grid-cols-2 gap-6">
          <SettingsSelect
            label="Theme"
            value={settings.theme}
            options={themeOptions}
            onChange={(v) =>
              settings.setTheme(v as "dark" | "light" | "ocean" | "midnight" | "forest")
            }
          />
          <SettingsSelect
            label="Language"
            value={settings.language}
            options={[
              { value: "English", label: "English" },
              { value: "Hindi", label: "Hindi" },
            ]}
            onChange={settings.setLanguage}
          />
          <SettingsSelect
            label="Timezone"
            value={settings.timezone}
            options={[
              { value: "UTC +05:30", label: "UTC +05:30" },
              { value: "UTC", label: "UTC" },
            ]}
            onChange={settings.setTimezone}
          />
          <SettingsInput
            label="Refresh Rate (sec)"
            value={settings.refreshRate}
            type="number"
            min={1}
            max={60}
            onChange={(v) => settings.setRefreshRate(Number(v))}
          />
        </div>
      </div>

      <div>
        <h2 className="mb-5 text-xl font-semibold text-[var(--text-primary)]">
          Preferences
        </h2>
        <div className="space-y-4">
          <SettingsToggle
            label="Auto Refresh"
            description="Automatically refresh dashboard data."
            checked={settings.autoRefresh}
            onChange={settings.setAutoRefresh}
          />
        </div>
      </div>
    </div>
  );
}