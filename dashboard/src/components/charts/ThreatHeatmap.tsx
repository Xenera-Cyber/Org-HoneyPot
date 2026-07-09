import useThreats from "../../hooks/useThreats";

export default function ThreatHeatmap() {

  const { heatmap } = useThreats();

  return (

    <div className="grid grid-cols-6 gap-3 pb-2">

      {heatmap.map((item) => (

        <div
          key={item.hour}
          className="
            rounded-xl
            border
            border-white/5
            bg-white/[0.03]
            p-4
            transition-all
            hover:border-cyan-500/30
          "
        >

          <div className="text-xs text-gray-500">

            {item.hour}

          </div>

          <div
            className="
              mt-3
              h-20
              rounded-lg
              bg-gradient-to-t
              from-cyan-600
              to-blue-400
            "
            style={{
              opacity: item.attacks / 100,
            }}
          />

          <div className="mt-3 text-center text-sm text-white">

            {item.attacks}

          </div>

        </div>

      ))}

    </div>

  );

}