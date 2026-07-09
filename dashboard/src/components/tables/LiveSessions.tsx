const sessions = [
  {
    id: "SES-1024",
    ip: "192.168.20.15",
    threat: 18,
    status: "Active",
  },
  {
    id: "SES-1025",
    ip: "10.0.0.8",
    threat: 42,
    status: "Monitoring",
  },
  {
    id: "SES-1026",
    ip: "172.16.1.21",
    threat: 75,
    status: "High Risk",
  },
];

export default function LiveSessions() {
  return (
    <div className="overflow-x-auto px-6 py-4">
      {/* Table configured with border-separate to create standalone row spacing */}
      <table className="w-full text-sm text-left border-separate border-spacing-y-2">
        <thead>
          <tr>
            <th className="text-slate-400 font-medium tracking-wide uppercase text-xs pb-2 pl-4">
              Session
            </th>
            <th className="text-slate-400 font-medium tracking-wide uppercase text-xs pb-2">
              IP Address
            </th>
            <th className="text-slate-400 font-medium tracking-wide uppercase text-xs pb-2">
              Threat Score
            </th>
            <th className="text-slate-400 font-medium tracking-wide uppercase text-xs pb-2 pr-4 text-right">
              Status
            </th>
          </tr>
        </thead>

        <tbody>
          {sessions.map((session) => (
            <tr
              key={session.id}
              className="
                bg-white/[0.03]
                transition
                hover:bg-white/[0.06]
                rounded-xl
              "
            >
              {/* Individual cell padding and boundary rounding needed for border-separate layouts */}
              <td className="py-4 pl-4 first:rounded-l-xl text-white font-medium">
                {session.id}
              </td>
              <td className="py-4 text-slate-300">
                {session.ip}
              </td>
              <td className="py-4 font-mono text-slate-300">
                {session.threat}
              </td>
              <td className="py-4 pr-4 last:rounded-r-xl text-right">
                <span
                  className={`
                    rounded-full
                    px-3
                    py-1
                    text-xs
                    font-semibold
                    backdrop-blur-xl
                    ${
                      session.status === "High Risk"
                        ? "bg-red-500/10 text-red-400 border border-red-500/20"
                        : session.status === "Monitoring"
                        ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        : "bg-green-500/10 text-green-400 border border-green-500/20"
                    }
                  `}
                >
                  {session.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}