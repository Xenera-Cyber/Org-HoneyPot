import type { ReactNode } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

interface Props {
    children: ReactNode;
}

export default function DashboardLayout({ children }: Props) {
    return (
        <div className="flex min-h-screen w-full bg-[#0a0e18] text-slate-100 antialiased">
            
            {/* SIDEBAR: Stays sticky/fixed to viewport height so it never cuts off */}
            <aside className="sticky top-0 h-screen shrink-0 border-r border-white/5 bg-[#0a0e18]">
                <Sidebar />
            </aside>

            {/* MAIN CONTAINER: Flexes, grows vertically with content, handles scroll accurately */}
            <div className="flex flex-1 flex-col min-w-0 bg-transparent">
                
                {/* TOP HEADER */}
                <header className="sticky top-0 z-50 border-b border-white/5 bg-[rgba(10,14,24,0.80)] backdrop-blur-2xl">
                    <Topbar />
                </header>

                {/* INNER CONTENT CONTAINER: Standard structural padding with natural scrolling */}
                <main className="flex-1 p-10">
                    {children}
                </main>
                
            </div>
        </div>
    );
}