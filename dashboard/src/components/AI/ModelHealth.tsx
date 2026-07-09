import {
    CheckCircle2,
    Cpu,
    Database,
    Shield,
    Clock3,
} from "lucide-react";

const metrics = [
    {
        title: "Inference Engine",
        value: "Healthy",
        icon: CheckCircle2,
        color: "text-green-400",
    },
    {
        title: "GPU Usage",
        value: "63%",
        icon: Cpu,
        color: "text-cyan-400",
    },
    {
        title: "Vector DB",
        value: "Online",
        icon: Database,
        color: "text-purple-400",
    },
    {
        title: "Guardrails",
        value: "Active",
        icon: Shield,
        color: "text-orange-400",
    },
    {
        title: "Latency",
        value: "118 ms",
        icon: Clock3,
        color: "text-cyan-400",
    },
];

export default function ModelHealth() {
    return (
        <div className="flex h-full flex-col justify-between">

            <div className="space-y-4">

                {metrics.map((metric) => {
                    const Icon = metric.icon;

                    return (
                        <div
                            key={metric.title}
                            className="rounded-xl border border-white/5 bg-[#0f172a] p-4 transition-all duration-300 hover:border-cyan-500/20"
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

            </div>

            <div className="mt-6 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-4">

                <div className="flex items-center gap-2">

                    <CheckCircle2
                        size={18}
                        className="text-emerald-400"
                    />

                    <span className="font-medium text-emerald-400">
                        AI System Stable
                    </span>

                </div>

                <p className="mt-2 text-sm text-gray-400">
                    No degraded models detected.
                    All inference services operating normally.
                </p>

            </div>

        </div>
    );
}