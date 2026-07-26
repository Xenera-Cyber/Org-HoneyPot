import useThreats from "../../hooks/useThreats";

const severityColor = {
  LOW: "text-green-400 bg-green-500/10 border-green-500/20",
  MEDIUM: "text-yellow-400 bg-yellow-500/10 border-yellow-500/20",
  HIGH: "text-orange-400 bg-orange-500/10 border-orange-500/20",
  CRITICAL: "text-red-400 bg-red-500/10 border-red-500/20",
};

const statusColor = {
  Active: "bg-green-500",
  Monitoring: "bg-yellow-500",
  Blocked: "bg-red-500",
  Contained: "bg-cyan-500",
};

export default function LiveThreatTable() {

  const { liveThreats } = useThreats();

  return (

    <div className="space-y-3">

      {/* Header */}

      <div
        className="
          grid
          grid-cols-6
          px-5
          pb-2
          text-xs
          uppercase
          tracking-wider
          text-slate-500
        "
      >
        <div>Source</div>
        <div>Protocol</div>
        <div>Severity</div>
        <div>Confidence</div>
        <div>Status</div>
        <div>AI Action</div>
      </div>

      {liveThreats.map((threat) => (

        <div
          key={threat.id}
          className="
            grid
            grid-cols-6
            items-center
            rounded-2xl
            border
            border-white/5
            bg-white/[0.03]
            px-5
            py-4
            transition-all
            duration-300
            hover:border-cyan-500/20
            hover:bg-white/[0.05]
          "
        >

          {/* IP */}

          <div>

            <div className="font-medium text-white">

              {threat.ip}

            </div>

          </div>

          {/* Protocol */}

          <div>

            <span
              className="
                rounded-lg
                bg-cyan-500/10
                px-3
                py-1
                text-cyan-400
                text-xs
                font-medium
              "
            >
              {threat.protocol}
            </span>

          </div>

          {/* Severity */}

          <div>

            <span
              className={`
                rounded-lg
                border
                px-3
                py-1
                text-xs
                font-semibold
                ${severityColor[threat.severity]}
              `}
            >
              {threat.severity}
            </span>

          </div>

          {/* Confidence */}

          <div>

            <div className="flex items-center gap-3">

              <div
                className="
                  h-2
                  w-24
                  overflow-hidden
                  rounded-full
                  bg-white/5
                "
              >

                <div
                  className="
                    h-full
                    rounded-full
                    bg-gradient-to-r
                    from-cyan-400
                    to-blue-500
                    transition-all
                    duration-700
                  "
                  style={{
                    width: `${threat.confidence}%`,
                  }}
                />

              </div>

              <span className="text-sm text-white">

                {threat.confidence}%

              </span>

            </div>

          </div>

          {/* Status */}

          <div className="flex items-center gap-2">

            <div
              className={`
                h-2.5
                w-2.5
                rounded-full
                ${statusColor[threat.status as keyof typeof statusColor]}
              `}
            />

            <span className="text-sm text-slate-300">

              {threat.status}

            </span>

          </div>

          {/* Action */}

          <div>

            <span
              className="
                rounded-xl
                border
                border-cyan-500/20
                bg-cyan-500/10
                px-3
                py-1.5
                text-xs
                font-medium
                text-cyan-400
              "
            >
              {threat.action}
            </span>

          </div>

        </div>

      ))}

    </div>

  );

}