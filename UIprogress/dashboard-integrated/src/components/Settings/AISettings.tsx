import { useEffect, useRef, useState } from "react";
import useSettings from "../../hooks/useSettings";
import useAI from "../../hooks/useAI";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";
import SettingsSelect from "./SettingsSelect";

export default function AISettings() {
    const settings = useSettings();
    const ai = useAI();

    const [saveState, setSaveState] = useState<
        "idle" | "saving" | "saved" | "error"
    >("idle");
    const [saveError, setSaveError] = useState<string | null>(null);
    const seeded = useRef(false);

    // Once, on first successful read of the real AI backend, pull its
    // current live config into these fields - so the form starts from
    // what the backend is actually running, not a stale local guess.
    useEffect(() => {
        if (seeded.current) return;
        if (!ai.backendReachable || !ai.backendConfig) return;
        seeded.current = true;

        const cfg = ai.backendConfig;
        settings.setPersonality(cfg.personality);
        settings.setModel(cfg.model);
        settings.setConfidenceThreshold(cfg.confidenceThreshold);
        settings.setTemperature(cfg.temperature);
        settings.setMaxContext(cfg.maxContext);
        settings.setMaxResponseLength(cfg.maxResponseLength);
        settings.setRAGEnabled(cfg.ragEnabled);
        settings.setGuardrailsEnabled(cfg.guardrailsEnabled);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [ai.backendReachable, ai.backendConfig]);

    async function applyToBackend() {
        setSaveState("saving");
        setSaveError(null);

        const result = await ai.saveBackendConfig({
            personality: settings.personality,
            model: settings.model,
            confidenceThreshold: settings.confidenceThreshold,
            temperature: settings.temperature,
            maxContext: settings.maxContext,
            maxResponseLength: settings.maxResponseLength,
            ragEnabled: settings.ragEnabled,
            guardrailsEnabled: settings.guardrailsEnabled,
        });

        if (result.ok) {
            setSaveState("saved");
            setTimeout(() => setSaveState("idle"), 2500);
        } else {
            setSaveState("error");
            setSaveError(result.error ?? "Failed to save.");
        }
    }

    return (

        <div className="space-y-8">

            <div className="flex items-center justify-between rounded-xl border border-white/5 bg-white/[0.02] px-4 py-3">
                <div className="text-sm">
                    <span className="text-gray-400">xynera-ai backend: </span>
                    <span
                        className={
                            ai.backendReachable
                                ? "font-medium text-green-400"
                                : "font-medium text-red-400"
                        }
                    >
                        {ai.backendReachable ? "Connected" : "Not reachable"}
                    </span>
                    {!ai.backendReachable && (
                        <span className="ml-2 text-xs text-gray-500">
                            (settings below will save locally and apply once it's running)
                        </span>
                    )}
                </div>
                <button
                    onClick={() => ai.refreshBackendConfig()}
                    className="text-xs text-gray-400 hover:text-white transition"
                >
                    Refresh status
                </button>
            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    AI Engine
                </h2>

                <div className="space-y-4">

                    <SettingsToggle
                        label="AI Engine"
                        description="Enable AI decision engine."
                        checked={settings.aiEnabled}
                        onChange={settings.setAIEnabled}
                    />

                    <SettingsToggle
                        label="RAG Retrieval"
                        description="Enable vector database retrieval. When off, the AI backend skips the LLM entirely and only uses the static knowledge base."
                        checked={settings.ragEnabled}
                        onChange={settings.setRAGEnabled}
                    />

                    <SettingsToggle
                        label="Guardrails"
                        description="Block responses that break character or leak real-looking credentials."
                        checked={settings.guardrailsEnabled}
                        onChange={settings.setGuardrailsEnabled}
                    />

                </div>

            </div>

            <div>

                <h2 className="mb-5 text-xl font-semibold text-white">
                    Model Configuration
                </h2>

                <div className="grid grid-cols-2 gap-6">

                    <SettingsSelect
                        label="AI Personality"
                        value={settings.personality}
                        options={[
                            "auto",
                            "Adaptive Defender",
                            "Aggressive",
                            "Stealth",
                            "Research",
                        ]}
                        onChange={settings.setPersonality}
                    />

                    <SettingsSelect
                        label="LLM Model"
                        value={settings.model}
                        options={[
                            "llama-3.3-70b-versatile",
                            "llama-3.1-8b-instant",
                            "mixtral-8x7b-32768",
                            "gemma2-9b-it",
                        ]}
                        onChange={settings.setModel}
                    />

                    <SettingsInput
                        label="Confidence Threshold (%)"
                        value={settings.confidenceThreshold}
                        type="number"
                        onChange={(v) =>
                            settings.setConfidenceThreshold(Number(v))
                        }
                    />

                    <SettingsInput
                        label="Temperature"
                        value={settings.temperature}
                        type="number"
                        onChange={(v) => settings.setTemperature(Number(v))}
                    />

                    <SettingsInput
                        label="Max Context Tokens"
                        value={settings.maxContext}
                        type="number"
                        onChange={(v) => settings.setMaxContext(Number(v))}
                    />

                    <SettingsInput
                        label="Max AI Response Length"
                        value={settings.maxResponseLength}
                        type="number"
                        onChange={(v) =>
                            settings.setMaxResponseLength(Number(v))
                        }
                    />

                </div>

                <div className="mt-6 flex items-center gap-4">
                    <button
                        onClick={applyToBackend}
                        disabled={saveState === "saving"}
                        className="rounded-lg bg-blue-500/20 border border-blue-500/30 px-4 py-2 text-sm font-medium text-blue-300 hover:bg-blue-500/30 transition disabled:opacity-50"
                    >
                        {saveState === "saving" ? "Saving..." : "Save & Apply to AI Backend"}
                    </button>

                    {saveState === "saved" && (
                        <span className="text-sm text-green-400">
                            Applied - the AI backend is now using these settings.
                        </span>
                    )}
                    {saveState === "error" && (
                        <span className="text-sm text-red-400">{saveError}</span>
                    )}
                </div>

            </div>

        </div>

    );

}
