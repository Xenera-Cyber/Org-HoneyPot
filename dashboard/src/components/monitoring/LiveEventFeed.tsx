import {
  ShieldAlert,
  Bot,
  ScanSearch,
  Terminal,
  LogOut,
} from "lucide-react";

import useMonitoring from "../../hooks/useMonitoring";

export default function LiveEventFeed() {

  const { events } = useMonitoring();

  function icon(title: string) {

    if (title.includes("SSH"))
      return <ShieldAlert size={16} />;

    if (title.includes("Port"))
      return <ScanSearch size={16} />;

    if (title.includes("AI"))
      return <Bot size={16} />;

    if (title.includes("Shell"))
      return <Terminal size={16} />;

    return <LogOut size={16} />;
  }

  function color(title: string) {

    if (title.includes("SSH"))
      return "bg-cyan-500";

    if (title.includes("Port"))
      return "bg-amber-500";

    if (title.includes("AI"))
      return "bg-purple-500";

    if (title.includes("Shell"))
      return "bg-red-500";

    return "bg-green-500";
  }

  return (
    <div
      className="
      h-full
      overflow-y-auto
      hide-scrollbar
      pr-2
      space-y-4
      "
    >
      {events.map((event) => (

        <div
          key={event.id}
          className="
          group
          flex
          items-start
          gap-4
          rounded-2xl
          border
          border-white/5
          bg-white/[0.03]
          p-4
          transition-all
          duration-300
          hover:bg-white/[0.06]
          hover:border-cyan-500/20
          "
        >

          <div
            className={`
            h-10
            w-10
            rounded-xl
            flex
            items-center
            justify-center
            text-white
            ${color(event.title)}
            `}
          >
            {icon(event.title)}
          </div>

          <div className="flex-1">

            <div className="flex justify-between">

              <h4 className="font-semibold text-white">
                {event.title}
              </h4>

              <span className="text-xs text-gray-500">
                {event.time}
              </span>

            </div>

            <p className="mt-2 text-sm text-slate-400">
              {event.detail}
            </p>

          </div>

        </div>

      ))}
    </div>
  );
}