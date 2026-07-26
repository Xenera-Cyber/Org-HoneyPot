import useThreats from "../../hooks/useThreats";

export default function ThreatIntelligenceSummary(){

    const {summary}=useThreats();

    return(

        <div className="space-y-7">

            <div className="grid grid-cols-2 gap-6">

                <Metric
                    label="Today's Attacks"
                    value={summary.todaysAttacks}
                />

                <Metric
                    label="Active Investigations"
                    value={summary.activeInvestigations}
                />

                <Metric
                    label="Critical Threats"
                    value={summary.criticalThreats}
                    danger
                />

                <Metric
                    label="Target Port"
                    value={summary.targetedPort}
                />

                <Metric
                    label="Threat Score"
                    value={summary.averageThreatScore}
                />

                <Metric
                    label="AI Confidence"
                    value={`${summary.aiConfidence}%`}
                    success
                />

            </div>

            <div>

                <div className="mb-3 flex justify-between">

                    <span className="text-sm text-slate-400">

                        Risk Index

                    </span>

                    <span className="font-semibold text-white">

                        {summary.riskIndex}%

                    </span>

                </div>

                <div className="h-3 rounded-full bg-white/5 overflow-hidden">

                    <div

                        className="
                        h-full
                        rounded-full
                        bg-gradient-to-r
                        from-cyan-400
                        via-blue-500
                        to-purple-500
                        transition-all
                        duration-700
                        "

                        style={{

                            width:`${summary.riskIndex}%`

                        }}

                    />

                </div>

            </div>

            <div className="grid grid-cols-2 gap-6">

                <Metric

                    label="Peak Attack Hour"

                    value={summary.peakHour}

                />

                <Metric

                    label="Top Origin"

                    value={summary.topOrigin}

                />

            </div>

        </div>

    )

}

interface MetricProps{

    label:string;

    value:string|number;

    danger?:boolean;

    success?:boolean;

}

function Metric({

    label,

    value,

    danger,

    success

}:MetricProps){

    return(

        <div
            className="
            rounded-2xl
            border
            border-white/5
            bg-white/[0.03]
            p-4
            "
        >

            <div className="text-xs uppercase tracking-wide text-slate-500">

                {label}

            </div>

            <div

                className={`
                mt-2
                text-2xl
                font-bold

                ${
                    danger
                    ? "text-red-400"
                    : success
                    ? "text-green-400"
                    : "text-white"
                }
                `}

            >

                {value}

            </div>

        </div>

    )

}