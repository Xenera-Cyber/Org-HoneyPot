import useSessions from "../../hooks/useSessions";

function statusStyle(status: string, risk: number) {
  if (status === "TERMINATED") {
    return "bg-white/5 text-slate-400 border border-white/10";
  }
  if (risk >= 70) {
    return "bg-red-500/10 text-red-400 border border-red-500/20";
  }
  if (risk >= 40) {
    return "bg-amber-500/10 text-amber-400 border border-amber-500/20";
  }
  return "bg-green-500/10 text-green-400 border border-green-500/20";
}

function statusLabel(status: string, risk: number) {
  if (status === "TERMINATED") return "Closed";
  if (status === "IDLE") return "Idle";
  if (risk >= 70) return "High Risk";
  if (risk >= 40) return "Monitoring";
  return "Active";
}

export default function LiveSessions() {
  const { sessions } = useSessions();
  const rows = sessions.slice(0, 8);

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
          {rows.length === 0 && (
            <tr>
              <td colSpan={4} className="py-6 text-center text-slate-500">
                No sessions yet - waiting for an attacker to connect.
              </td>
            </tr>
          )}
          {rows.map((session) => (
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
                {session.id.slice(0, 8)}
              </td>
              <td className="py-4 text-slate-300">
                {session.ip}
              </td>
              <td className="py-4 font-mono text-slate-300">
                {session.risk}
              </td>
              <td className="py-4 pr-4 last:rounded-r-xl text-right">
                <span
                  className={`rounded-full px-3 py-1 text-xs font-semibold backdrop-blur-xl ${statusStyle(
                    session.status,
                    session.risk
                  )}`}
                >
                  {statusLabel(session.status, session.risk)}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
