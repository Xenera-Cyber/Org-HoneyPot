import { useState } from "react";
import DashboardLayout from "../layout/DashboardLayout";
import Panel from "../components/Panel";

import { SettingsProvider } from "../context/SettingsContext";

import SettingsSidebar from "../components/Settings/SettingsSidebar";
import GeneralSettings from "../components/Settings/GeneralSettings";
import HoneypotSettings from "../components/Settings/HoneypotSettings";
import AISettings from "../components/Settings/AISettings";
import DashboardSettings from "../components/Settings/DashboardSettings";
import NotificationSettings from "../components/Settings/NotificationSettings";
import SecuritySettings from "../components/Settings/SecuritySettings";

export default function Settings() {
    const [selected, setSelected] = useState("General");

    return (
        <DashboardLayout>
            <SettingsProvider>
                <div className="space-y-6">

                    <div>
                        <h1 className="text-3xl font-bold text-white">
                            Settings
                        </h1>
                        <p className="mt-1 text-gray-400">
                            Configure XYNERA
                        </p>
                    </div>

                    <div className="grid grid-cols-12 gap-6">

                        {/* LEFT SIDEBAR CATEGORIES PANEL */}
                        <div className="col-span-3">
                            <Panel title="Categories">
                                <SettingsSidebar 
                                    selected={selected} 
                                    onSelect={setSelected} 
                                />
                            </Panel>
                        </div>

                        {/* RIGHT DYNAMIC SETTINGS CONTENT PANEL */}
                        <div className="col-span-9">
                            <Panel title={selected}>
                                {selected === "General" && <GeneralSettings />}
                                {selected === "Honeypot" && <HoneypotSettings />}
                                {selected === "AI" && <AISettings />}
                                {selected === "Dashboard" && <DashboardSettings />}
                                {selected === "Notifications" && <NotificationSettings />}
                                {selected === "Security" && <SecuritySettings />}
                                
                                {/* Fallback message for tabs that are not implemented yet */}
                                {selected !== "General" && 
                                 selected !== "Honeypot" && 
                                 selected !== "AI" && 
                                 selected !== "Dashboard" && 
                                 selected !== "Notifications" && 
                                 selected !== "Security" && (
                                    <div className="flex h-[300px] items-center justify-center text-gray-500">
                                        {selected} Settings Configuration Coming Soon
                                    </div>
                                )}
                            </Panel>
                        </div>

                    </div>

                </div>
            </SettingsProvider>
        </DashboardLayout>
    );
}