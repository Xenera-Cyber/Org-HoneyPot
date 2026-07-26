import {
  Lock,
  Globe,
  Folder,
  Mail,
  Circle,
} from "lucide-react";

import useThreats from "../../hooks/useThreats";

const icons = {
  SSH: <Lock size={16} />,
  HTTP: <Globe size={16} />,
  FTP: <Folder size={16} />,
  SMTP: <Mail size={16} />,
  OTHER: <Circle size={16} />,
};

export default function AttackTypes() {

  const { attackTypes } = useThreats();

  return (

    <div className="space-y-6">

      {attackTypes.map((item) => (

        <div key={item.name}>

          <div className="mb-2 flex items-center justify-between">

            <div className="flex items-center gap-2 text-slate-300">

              {icons[item.name as keyof typeof icons]}

              <span>{item.name}</span>

            </div>

            <span className="font-semibold text-white">

              {item.percentage}%

            </span>

          </div>

          <div
            className="
              h-2.5
              overflow-hidden
              rounded-full
              bg-white/5
            "
          >

            <div
              className={`${item.color} h-full rounded-full transition-all duration-700`}
              style={{
                width: `${item.percentage}%`,
              }}
            />

          </div>

        </div>

      ))}

    </div>

  );

}