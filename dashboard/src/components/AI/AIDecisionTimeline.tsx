import useAI from "../../hooks/useAI";
import { ShieldAlert, Brain, Database, Clock3 } from "lucide-react";

const riskColor = (risk: string) => {
    switch (risk) {
        case "Critical":
            return "bg-red-500";
        case "High":
            return "bg-orange-500";
        case "Medium":
            return "bg-yellow-400";
        default:
            return "bg-green-500";
    }
};

export default function AIDecisionTimeline() {

    const { recentDecisions } = useAI();

    return (
        <div className="space-y-4 overflow-y-auto h-full pr-2">

            {recentDecisions.map((decision) => (

                <div
                    key={decision.id}
                    className="rounded-xl border border-slate-700 bg-slate-900/50 p-4 transition-all hover:border-cyan-500/40"
                >

                    <div className="flex justify-between items-center">

                        <div>

                            <div className="font-semibold text-white">
                                {decision.attack}
                            </div>

                            <div className="text-xs text-slate-400 mt-1">
                                {decision.time}
                            </div>

                        </div>

                        <span
                            className={`px-3 py-1 rounded-full text-xs font-semibold text-white ${riskColor(
                                decision.risk
                            )}`}
                        >
                            {decision.risk}
                        </span>

                    </div>

                    <div className="grid grid-cols-2 gap-4 mt-5 text-sm">

                        <div className="flex items-center gap-2 text-slate-300">
                            <Brain size={16} />
                            Confidence
                            <span className="ml-auto text-cyan-400">
                                {decision.confidence}%
                            </span>
                        </div>

                        <div className="flex items-center gap-2 text-slate-300">
                            <Database size={16} />
                            KB Hits
                            <span className="ml-auto text-green-400">
                                {decision.kbHits}
                            </span>
                        </div>

                        <div className="flex items-center gap-2 text-slate-300">
                            <ShieldAlert size={16} />
                            Guardrails
                            <span className="ml-auto text-orange-400">
                                {decision.guardrails}
                            </span>
                        </div>

                        <div className="flex items-center gap-2 text-slate-300">
                            <Clock3 size={16} />
                            Response
                            <span className="ml-auto text-purple-400">
                                {decision.responseTime} ms
                            </span>
                        </div>

                    </div>

                </div>

            ))}

        </div>
    );
}