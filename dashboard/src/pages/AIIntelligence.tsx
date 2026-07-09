import DashboardLayout from "../layout/DashboardLayout";
import Panel from "../components/Panel";
import ModelHealth from "../components/AI/ModelHealth";
import AIConfidenceBreakdown from "../components/AI/AIConfidenceBreakdown";
import { AIProvider } from "../context/AIContext";
import useAI from "../hooks/useAI";

import AIStatCard from "../components/AI/AIStatCard";
import AIDecisionTimeline from "../components/AI/AIDecisionTimeline";

import {
    Brain,
    Shield,
    Database,
    Zap,
    Cpu,
    Sparkles,
    Radar,
} from "lucide-react";

function Content() {
    const ai = useAI();

    return (
        <div className="space-y-6">

            <div>
                <h1 className="text-3xl font-bold text-white">
                    AI Intelligence
                </h1>
                <p className="mt-1 text-gray-400">
                    Live AI Engine Monitoring
                </p>
            </div>

            {/* AI ENGINE METRICS GRID */}
            <div className="grid grid-cols-4 gap-6 items-stretch">
                
                {/* AI Confidence - Cyan Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(6,182,212,0.15)] border border-transparent hover:border-cyan-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="AI Confidence"
                            value={`${ai.confidence}%`}
                            subtitle="Prediction Confidence"
                            color="text-cyan-400"
                            icon={<Brain size={34}/>}
                        />
                    </div>
                </div>

                {/* Current Personality - Green Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(34,197,94,0.15)] border border-transparent hover:border-green-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="Current Personality"
                            value={ai.personality}
                            subtitle="Running Profile"
                            color="text-green-400"
                            icon={<Sparkles size={34}/>}
                        />
                    </div>
                </div>

                {/* Predicted Attack - Orange Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(249,115,22,0.15)] border border-transparent hover:border-orange-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="Predicted Attack"
                            value={ai.predictedAttack}
                            subtitle="Next Threat"
                            color="text-orange-400"
                            icon={<Radar size={34}/>}
                        />
                    </div>
                </div>

                {/* Knowledge Hits - Purple Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(168,85,247,0.15)] border border-transparent hover:border-purple-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="Knowledge Hits"
                            value={ai.kbHits}
                            subtitle="Vector Matches"
                            color="text-purple-400"
                            icon={<Database size={34}/>}
                        />
                    </div>
                </div>

                {/* RAG Retrieval - Green Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(34,197,94,0.15)] border border-transparent hover:border-green-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="RAG Retrieval"
                            value={ai.ragStatus}
                            subtitle="Vector Database"
                            color="text-green-400"
                            icon={<Shield size={34}/>}
                        />
                    </div>
                </div>

                {/* Guardrail Blocks - Red Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(239,68,68,0.15)] border border-transparent hover:border-red-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="Guardrail Blocks"
                            value={ai.guardrailBlocks}
                            subtitle="Blocked Prompts"
                            color="text-red-400"
                            icon={<Shield size={34}/>}
                        />
                    </div>
                </div>

                {/* Response Time - Cyan Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(6,182,212,0.15)] border border-transparent hover:border-cyan-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="Response Time"
                            value={`${ai.responseTime} ms`}
                            subtitle="Average"
                            color="text-cyan-400"
                            icon={<Zap size={34}/>}
                        />
                    </div>
                </div>

                {/* AI Engine Status - Green Glow */}
                <div className="group h-full flex flex-col transition-all duration-300 rounded-2xl hover:shadow-[0_0_25px_rgba(34,197,94,0.15)] border border-transparent hover:border-green-500/30">
                    <div className="w-full h-full flex flex-col [&>div]:h-full [&>div]:w-full [&>div]:flex [&>div]:flex-col [&>div]:justify-between">
                        <AIStatCard
                            title="AI Engine"
                            value="ONLINE"
                            subtitle="Status"
                            color="text-green-400"
                            icon={<Cpu size={34}/>}
                        />
                    </div>
                </div>
            </div>

            {/* FIRST ROW: DECISIONS & CONFIDENCE BREAKDOWN */}
            <div className="grid grid-cols-12 gap-6">
                
                {/* Recent AI Decisions - Cyan Glow Panel */}
                <div className="col-span-8 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(6,182,212,0.12)]">
                    <Panel
                        title="Recent AI Decisions"
                        className="h-[520px] transition-all duration-300 group-hover:border-cyan-500/30"
                    >
                        <AIDecisionTimeline />
                    </Panel>
                </div>

                {/* AI Confidence Breakdown - Purple Glow Panel */}
                <div className="col-span-4 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(168,85,247,0.12)]">
                    <Panel
                        title="AI Confidence Breakdown"
                        className="h-[520px] transition-all duration-300 group-hover:border-purple-500/30"
                    >
                        <AIConfidenceBreakdown />
                    </Panel>
                </div>
                
            </div>

            {/* SECOND ROW: FULL WIDTH MODEL HEALTH WITH SCROLLABLE INTERNAL VIEW */}
            <div className="grid grid-cols-12 gap-6">
                <div className="col-span-12 group transition-all duration-300 rounded-xl hover:shadow-[0_0_30px_rgba(34,197,94,0.12)]">
                    <Panel
                        title="Model Health"
                        className="h-[350px] transition-all duration-300 group-hover:border-green-500/30 overflow-y-auto custom-scrollbar"
                    >
                        <div className="h-full pr-2 overflow-y-auto">
                            <ModelHealth />
                        </div>
                    </Panel>
                </div>
            </div>

        </div>
    );
}

export default function AIIntelligence() {
    return (
        <DashboardLayout>
            <AIProvider>
                <Content/>
            </AIProvider>
        </DashboardLayout>
    );
}