import {

LineChart,
Line,
XAxis,
YAxis,
Tooltip,
ResponsiveContainer,
CartesianGrid,

} from "recharts";

import useThreats from "../../hooks/useThreats";

export default function SeverityTimeline(){

    const {severity}=useThreats();

    return(

        <div className="h-[320px]">

            <ResponsiveContainer>

                <LineChart data={severity}>

                    <CartesianGrid
                        stroke="rgba(255,255,255,.05)"
                    />

                    <XAxis
                        dataKey="time"
                        tick={{
                            fill:"#94a3b8",
                            fontSize:11
                        }}
                    />

                    <YAxis
                        tick={{
                            fill:"#94a3b8",
                            fontSize:11
                        }}
                    />

                    <Tooltip/>

                    <Line

                        type="monotone"

                        dataKey="low"

                        stroke="#22c55e"

                        strokeWidth={2}

                        dot={false}

                    />

                    <Line

                        type="monotone"

                        dataKey="medium"

                        stroke="#eab308"

                        strokeWidth={2}

                        dot={false}

                    />

                    <Line

                        type="monotone"

                        dataKey="high"

                        stroke="#fb923c"

                        strokeWidth={2}

                        dot={false}

                    />

                    <Line

                        type="monotone"

                        dataKey="critical"

                        stroke="#ef4444"

                        strokeWidth={3}

                        dot={false}

                    />

                </LineChart>

            </ResponsiveContainer>

        </div>

    )

}