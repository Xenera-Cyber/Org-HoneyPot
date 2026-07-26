import { Shield, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";

const tips = [
  {
    title: "Enable Multi-Factor Authentication",
    description:
      "MFA drastically reduces the success rate of password-based attacks and credential theft.",
  },
  {
    title: "Rotate SSH Keys Regularly",
    description:
      "Frequent key rotation limits exposure if credentials become compromised.",
  },
  {
    title: "Disable Root Login",
    description:
      "Blocking direct root SSH access significantly reduces brute-force attack success.",
  },
  {
    title: "Segment Honeypot Networks",
    description:
      "Isolating deception environments prevents attackers from pivoting into production systems.",
  },
  {
    title: "Keep Honeypots Updated",
    description:
      "Updated deception services remain believable and resistant to unintended exploitation.",
  },
  {
    title: "Monitor Failed Logins",
    description:
      "A sudden increase in failed authentication attempts often indicates reconnaissance activity.",
  },
  {
    title: "Limit Open Ports",
    description:
      "Reducing unnecessary exposed services lowers the overall attack surface.",
  },
  {
    title: "Use Strong Password Policies",
    description:
      "Long, randomly generated passwords greatly reduce brute-force effectiveness.",
  },
];

export default function SecurityTip() {
  const [tip, setTip] = useState(tips[0]);

  useEffect(() => {
    const random = Math.floor(Math.random() * tips.length);
    setTip(tips[random]);
  }, []);

  return (
    <div className="flex h-full flex-col justify-between rounded-2xl border border-blue-500/15 bg-gradient-to-r from-[#111827] via-[#0f172a] to-[#111827] p-6">

      <div className="flex items-center justify-between">

        <div className="flex items-center gap-3">

          <div className="rounded-xl bg-blue-500/10 p-3">
            <Shield className="text-blue-400" size={28} />
          </div>

          <div>
            <p className="text-sm text-blue-400 font-medium">
              AI Security Insight
            </p>

            <h3 className="text-xl font-bold text-white">
              {tip.title}
            </h3>
          </div>

        </div>

        <RefreshCw
          className="text-blue-400"
          size={18}
        />

      </div>

      <p className="mt-6 max-w-3xl text-slate-300 leading-8 text-lg">
        {tip.description}
      </p>

      <div className="mt-8 flex items-center justify-between border-t border-white/5 pt-4">

        <span className="text-xs uppercase tracking-widest text-slate-500">
          Changes every visit
        </span>

        <span className="text-xs text-blue-400">
          Powered by XYNERA AI
        </span>

      </div>

    </div>
  );
}