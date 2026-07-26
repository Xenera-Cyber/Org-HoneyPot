import useThreats from "../../hooks/useThreats";

export default function TopAttackSources(){

    const {sources}=useThreats();

    return(

        <div className="space-y-4 pb-2">

            {sources.map(source=>(

                <div
                    key={source.ip}
                    className="
                    rounded-2xl
                    border
                    border-white/5
                    bg-white/[0.03]
                    p-4
                    transition
                    hover:border-cyan-500/30
                    "
                >

                    <div className="flex justify-between">

                        <div>

                            <div className="font-semibold text-white">

                                {source.ip}

                            </div>

                            <div className="mt-1 text-sm text-gray-400">

                                {source.country} • {source.protocol}

                            </div>

                        </div>

                        <div className="text-right">

                            <div className="text-cyan-400 font-semibold">

                                {source.attacks}

                            </div>

                            <div className="text-xs text-gray-500">

                                attacks

                            </div>

                        </div>

                    </div>

                    <div className="mt-4">

                        <div className="flex justify-between mb-2">

                            <span className="text-xs text-gray-500">

                                Risk

                            </span>

                            <span className="text-xs text-red-400">

                                {source.risk}%

                            </span>

                        </div>

                        <div className="h-2 rounded-full bg-white/5 overflow-hidden">

                            <div
                                className="
                                h-full
                                rounded-full
                                bg-gradient-to-r
                                from-red-500
                                to-orange-400
                                transition-all
                                duration-700
                                "
                                style={{
                                    width:`${source.risk}%`
                                }}
                            />

                        </div>

                    </div>

                </div>

            ))}

        </div>

    )

}