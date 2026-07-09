import {
  Cpu,
  HardDrive,
  MemoryStick,
  Wifi,
} from "lucide-react";

import useMonitoring from "../../hooks/useMonitoring";

export default function ResourceUsage() {
  const {
    cpu,
    memory,
    disk,
    upload,
    download,
  } = useMonitoring();

  const stats = [
    {
      icon: <Cpu size={18} />,
      name: "CPU",
      value: Math.round(cpu),
      color: "from-cyan-400 to-blue-500",
    },
    {
      icon: <MemoryStick size={18} />,
      name: "Memory",
      value: Math.round(memory),
      color: "from-green-400 to-emerald-500",
    },
    {
      icon: <HardDrive size={18} />,
      name: "Disk",
      value: Math.round(disk),
      color: "from-purple-400 to-violet-500",
    },
  ];

  return (
    <div className="h-full overflow-y-auto hide-scrollbar pr-2">
      <div className="space-y-8">
        
        {/* Usage */}
        <div className="space-y-6">
          {stats.map((item) => (
            <div key={item.name}>
              <div className="mb-2 flex items-center justify-between">
                <div className="flex items-center gap-2 text-slate-300">
                  {item.icon}
                  <span>{item.name}</span>
                </div>
                <span className="font-semibold text-white">
                  {item.value}%
                </span>
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-white/5">
                <div
                  className={`h-full rounded-full bg-gradient-to-r ${item.color} transition-all duration-700`}
                  style={{
                    width: `${item.value}%`,
                  }}
                />
              </div>
            </div>
          ))}
        </div>

        {/* Network */}
        <div
          className="
            rounded-2xl
            border
            border-white/5
            bg-white/[0.03]
            p-5
          "
        >
          <div className="mb-4 flex items-center gap-2 text-slate-300">
            <Wifi size={18} />
            <span>Network</span>
          </div>

          <div className="flex justify-between">
            <div>
              <div className="text-xs text-gray-500">
                Upload
              </div>
              <div className="mt-1 text-lg font-semibold text-cyan-400">
                ↑ {upload.toFixed(1)} MB/s
              </div>
            </div>

            <div>
              <div className="text-xs text-gray-500">
                Download
              </div>
              <div className="mt-1 text-lg font-semibold text-green-400">
                ↓ {download.toFixed(1)} MB/s
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}