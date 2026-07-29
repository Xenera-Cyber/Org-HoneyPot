import {
    CheckCircle2,
    AlertTriangle,
    Database,
    Shield,
    Clock3,
} from "lucide-react";
import useAI from "../../hooks/useAI";

export default function ModelHealth() {
    const {
        engineOnline,
        ragStatus,
        guardrailBlocks,
        responseTime,
        confidence,
        kbHits,
    } = useAI();

    const metrics = [
        {
            title: "Inference Engine",
            value: engineOnline ? "Healthy" : "Idle",
            icon: engineOnline ? CheckCircle2 : AlertTriangle,
            color: engineOnline ? "text-green-400" : "text-gray-400",
        },
        {
            title: "Detection Confidence",
            value: `${confidence}%`,
            icon: CheckCircle2,
            color:
                confidence >= 80
                    ? "text-cyan-400"
                    : confidence >= 50
                    ? "text-amber-400"
                    : "text-gray-400",
        },
        {
            title: "RAG / Vector DB",
            value: ragStatus,
            icon: Database,
            color: ragStatus === "Healthy" ? "text-purple-400" : "text-red-400",
        },
        {
            title: "Guardrail Blocks",
            value: String(guardrailBlocks),
            icon: Shield,
            color: guardrailBlocks > 0 ? "text-orange-400" : "text-gray-400",
        },
        {
            title: "Response Latency",
            value: responseTime ? `${responseTime} ms` : "--",
            icon: Clock3,
            color: "text-cyan-400",
        },
    ];

    const stable = engineOnline && confidence >= 50;

    return (
        <div className="flex h-full flex-col justify-between">

            <div className="space-y-4">

                {metrics.map((metric) => {
                    const Icon = metric.icon;

                    return (
                        <div
                            key={metric.title}
                            className="rounded-xl border border-white/5 bg-[var(--bg-card)] p-4 transition-all duration-300 hover:border-cyan-500/20"
                        >
                            <div className="flex items-center justify-between">

                                <div>

                                    <p className="text-sm text-gray-400">
                                        {metric.title}
                                    </p>

                                    <h2 className={`mt-1 text-xl font-semibold ${metric.color}`}>
                                        {metric.value}
                                    </h2>

                                </div>

                                <Icon
                                    size={28}
                                    className={metric.color}
                                />

                            </div>
                        </div>
                    );
                })}

                <p className="text-xs text-gray-500 px-1">
                    Knowledge base: {kbHits} documents
                </p>

            </div>

            <div
                className={`mt-6 rounded-xl border p-4 ${
                    stable
                        ? "border-emerald-500/20 bg-emerald-500/10"
                        : "border-amber-500/20 bg-amber-500/10"
                }`}
            >

                <div className="flex items-center gap-2">

                    {stable ? (
                        <CheckCircle2 size={18} className="text-emerald-400" />
                    ) : (
                        <AlertTriangle size={18} className="text-amber-400" />
                    )}

                    <span
                        className={`font-medium ${
                            stable ? "text-emerald-400" : "text-amber-400"
                        }`}
                    >
                        {stable ? "AI System Stable" : "Awaiting Live Traffic"}
                    </span>

                </div>

                <p className="mt-2 text-sm text-gray-400">
                    {stable
                        ? "No degraded models detected. All inference services operating normally."
                        : "No attacker activity classified yet, or the honeypot/AI backend isn't running."}
                </p>

            </div>

        </div>
    );
}
