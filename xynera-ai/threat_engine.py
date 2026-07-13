from collections import deque


class ThreatEngine:
    def __init__(self):
        self.base_weights = {
            "Reconnaissance": 4,
            "System Enumeration": 5,
            "Network/User Enumeration": 6,
            "Privilege Enumeration": 8,
            "Malware Download Attempt": 10,
            "Privilege Escalation Attempt": 15,
            "Persistence Attempt": 18,
            "Reverse Shell Attempt": 22,
            "C2 / Backdoor Attempt": 25,
            "System Destruction Attempt": 30,
            "Suspicious Script Execution": 12,
            "Unknown": 3,
        }

        self.sequence_multipliers = {
            ("Reconnaissance", "Malware Download Attempt"): 1.6,
            ("Reconnaissance", "Privilege Enumeration"): 1.4,
            ("Privilege Enumeration", "Privilege Escalation Attempt"): 1.8,
            ("Malware Download Attempt", "Persistence Attempt"): 1.7,
            ("Reverse Shell Attempt", "C2 / Backdoor Attempt"): 2.0,
        }

        self.attack_history = {}

    def get_threat_level(self, score: int, attack_type=None, ip: str = None) -> dict:
        if isinstance(attack_type, dict):
            attack_type = attack_type.get("attack_type", "Unknown")

        base_score = score

        if ip and attack_type:
            if ip not in self.attack_history:
                self.attack_history[ip] = deque(maxlen=5)
            self.attack_history[ip].append(attack_type)

        multiplier = 1.0

        if ip and len(self.attack_history.get(ip, [])) >= 2:
            last_two = tuple(list(self.attack_history[ip])[-2:])
            multiplier = self.sequence_multipliers.get(last_two, 1.0)

        final_score = int(base_score * multiplier)

        if final_score >= 70:
            level = "CRITICAL"
            indicator = "🔴"
        elif final_score >= 45:
            level = "HIGH"
            indicator = "🟠"
        elif final_score >= 25:
            level = "MEDIUM"
            indicator = "🟡"
        else:
            level = "LOW"
            indicator = "🟢"

        return {
            "score": final_score,
            "risk_level": level,
            "final_score": final_score,
            "threat_level": level,
            "base_score": base_score,
            "multiplier": round(multiplier, 2),
            "severity_indicator": indicator,
        }


threat_engine = ThreatEngine()


def get_threat_level(score: int, attack_type=None, ip: str = None) -> dict:
    return threat_engine.get_threat_level(score, attack_type, ip)
