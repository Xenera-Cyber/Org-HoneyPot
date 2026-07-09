import useSettings from "../../hooks/useSettings";

import SettingsToggle from "./SettingsToggle";
import SettingsInput from "./SettingsInput";
import SettingsSelect from "./SettingsSelect";

export default function AISettings() {

    const settings = useSettings();

    return (

        <div className="space-y-8">

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
                        description="Enable vector database retrieval."
                        checked={settings.ragEnabled}
                        onChange={settings.setRAGEnabled}
                    />

                    <SettingsToggle
                        label="Guardrails"
                        description="Block unsafe AI responses."
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
                        value="Balanced"
                        options={[
                            "Balanced",
                            "Aggressive",
                            "Stealth",
                            "Research",
                        ]}
                        onChange={() => {}}
                    />

                    <SettingsSelect
                        label="LLM Model"
                        value="Llama-3"
                        options={[
                            "Llama-3",
                            "Mistral",
                            "Gemma",
                            "GPT",
                        ]}
                        onChange={() => {}}
                    />

                    <SettingsInput
                        label="Confidence Threshold (%)"
                        value={85}
                        type="number"
                        onChange={() => {}}
                    />

                    <SettingsInput
                        label="Temperature"
                        value={0.3}
                        type="number"
                        onChange={() => {}}
                    />

                    <SettingsInput
                        label="Max Context Tokens"
                        value={4096}
                        type="number"
                        onChange={() => {}}
                    />

                    <SettingsInput
                        label="Max AI Response Length"
                        value={1024}
                        type="number"
                        onChange={() => {}}
                    />

                </div>

            </div>

        </div>

    );

}