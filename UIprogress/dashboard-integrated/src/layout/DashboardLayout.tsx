import type { ReactNode } from "react";
import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

interface Props {
  children: ReactNode;
}

export default function DashboardLayout({ children }: Props) {
  return (
    <div className="flex min-h-screen w-full bg-[var(--bg-app)] text-[var(--text-primary)] antialiased">
      <aside className="sticky top-0 h-screen shrink-0 border-r border-[var(--border-subtle)] bg-[var(--bg-app)]">
        <Sidebar />
      </aside>
      <div className="flex flex-1 flex-col min-w-0 bg-transparent">
        <header className="sticky top-0 z-50 border-b border-[var(--border-subtle)] bg-[var(--bg-header)] backdrop-blur-2xl">
          <Topbar />
        </header>
        <main className="flex-1 p-10">
          {children}
        </main>
      </div>
    </div>
  );
}