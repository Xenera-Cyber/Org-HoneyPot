import { Bell, Search } from "lucide-react";

export default function Topbar(){

    return(

        <header
            className="
                h-20
                px-8
                flex
                items-center
                justify-between
                border-b
                border-white/10
                glass
            "
        >

            <div>

                <h2 className="text-xl font-semibold">

                    Security Operations Dashboard

                </h2>

                <p className="text-sm text-gray-400">

                    Real-time Honeypot Monitoring

                </p>

            </div>

            <div className="flex items-center gap-4">

                <div
                    className="
                        flex
                        items-center
                        gap-2
                        bg-white/5
                        border
                        border-white/10
                        rounded-xl
                        px-4
                        py-2
                    "
                >

                    <Search size={18}/>

                    <input

                        placeholder="Search..."

                        className="
                            bg-transparent
                            outline-none
                            text-sm
                            placeholder:text-gray-500
                        "

                    />

                </div>

                <button
                    className="
                        p-3
                        rounded-xl
                        bg-white/5
                        border
                        border-white/10
                        hover:bg-blue-500/10
                        transition
                    "
                >

                    <Bell size={18}/>

                </button>

                <div
                    className="
                        w-10
                        h-10
                        rounded-full
                        bg-blue-500
                        flex
                        items-center
                        justify-center
                        font-semibold
                    "
                >

                    R

                </div>

            </div>

        </header>

    )

}