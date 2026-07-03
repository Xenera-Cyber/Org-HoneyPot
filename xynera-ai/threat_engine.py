from datetime import datetime
from collections import deque
import logging
from enum import Enum
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, asdict
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('threat_engine.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """Enumeration for threat severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatCategory(Enum):
    """Categories of threats that can be detected"""
    RECONNAISSANCE = "Reconnaissance"
    SYSTEM_ENUMERATION = "System Enumeration"
    NETWORK_USER_ENUMERATION = "Network/User Enumeration"
    PRIVILEGE_ENUMERATION = "Privilege Enumeration"
    MALWARE_DOWNLOAD = "Malware Download Attempt"
    PRIVILEGE_ESCALATION = "Privilege Escalation Attempt"
    PERSISTENCE = "Persistence Attempt"
    REVERSE_SHELL = "Reverse Shell Attempt"
    C2_BACKDOOR = "C2 / Backdoor Attempt"
    SYSTEM_DESTRUCTION = "System Destruction Attempt"
    SUSPICIOUS_SCRIPT = "Suspicious Script Execution"
    UNKNOWN = "Unknown"


class ThreatEngine:
    """Main threat detection and analysis engine"""
    
    def __init__(self):
        """Initialize threat engine with weights and multipliers"""
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
            "Unknown": 3
        }

        # Attack sequence multipliers for detecting attack chains
        self.sequence_multipliers = {
            ("Reconnaissance", "Malware Download Attempt"): 1.6,
            ("Reconnaissance", "Privilege Enumeration"): 1.4,
            ("Privilege Enumeration", "Privilege Escalation Attempt"): 1.8,
            ("Malware Download Attempt", "Persistence Attempt"): 1.7,
            ("Reverse Shell Attempt", "C2 / Backdoor Attempt"): 2.0,
            ("System Enumeration", "Privilege Escalation Attempt"): 1.5,
            ("Reconnaissance", "System Enumeration"): 1.3,
            ("Persistence Attempt", "C2 / Backdoor Attempt"): 1.9,
        }

        # Store attack history per IP (max 5 entries)
        self.attack_history = {}
        # Store threat statistics
        self.threat_statistics = {
            "total_threats": 0,
            "by_level": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
            "by_type": {}
        }

    def get_threat_level(
        self,
        score: int,
        attack_type: Optional[Union[str, Dict]] = None,
        ip: Optional[str] = None
    ) -> Dict:
        """
        Calculate threat level and score with contextual multipliers.
        
        Args:
            score: Base threat score (0-100)
            attack_type: Type of attack (string or dict from classifier)
            ip: Source IP address for tracking attack chains
            
        Returns:
            Dictionary with threat assessment details
        """
        base_score = score

        # Handle if attack_type is a dict (from classifier.py)
        if isinstance(attack_type, dict):
            attack_type = attack_type.get("attack_type", "Unknown")

        # Update attack history for sequence detection
        if ip and attack_type:
            if ip not in self.attack_history:
                self.attack_history[ip] = deque(maxlen=5)
            self.attack_history[ip].append(attack_type)
            logger.debug(f"Updated attack history for IP {ip}: {attack_type}")

        # Calculate sequence multiplier for attack chains
        multiplier = self.calculate_sequence_multiplier(ip)

        # Calculate final score
        final_score = min(100, int(base_score * multiplier))

        # Determine threat level
        level, indicator = self._classify_threat_level(final_score)

        # Update statistics
        self._update_statistics(level, attack_type)

        result = {
            "final_score": final_score,
            "threat_level": level,
            "base_score": base_score,
            "multiplier": round(multiplier, 2),
            "severity_indicator": indicator,
            "attack_type": attack_type,
            "source_ip": ip,
            "timestamp": datetime.now().isoformat()
        }

        logger.info(f"Threat assessment - IP: {ip}, Type: {attack_type}, Score: {final_score}, Level: {level}")
        return result

    def calculate_sequence_multiplier(self, ip: Optional[str]) -> float:
        """
        Calculate multiplier based on attack sequence/chain.
        
        Args:
            ip: Source IP address
            
        Returns:
            Sequence multiplier (1.0 or higher)
        """
        if not ip or ip not in self.attack_history:
            return 1.0

        history = self.attack_history[ip]
        if len(history) < 2:
            return 1.0

        # Check last two attacks in sequence
        last_two = tuple(list(history)[-2:])
        multiplier = self.sequence_multipliers.get(last_two, 1.0)
        
        logger.debug(f"Attack sequence {last_two} -> multiplier: {multiplier}")
        return multiplier

    def _classify_threat_level(self, score: int) -> Tuple[str, str]:
        """
        Classify threat level based on score.
        
        Args:
            score: Final threat score
            
        Returns:
            Tuple of (threat_level, severity_indicator)
        """
        if score >= 70:
            return "CRITICAL", "🔴"
        elif score >= 45:
            return "HIGH", "🟠"
        elif score >= 25:
            return "MEDIUM", "🟡"
        else:
            return "LOW", "🟢"

    def _update_statistics(self, level: str, attack_type: Optional[str] = None) -> None:
        """Update threat statistics."""
        self.threat_statistics["total_threats"] += 1
        self.threat_statistics["by_level"][level] += 1
        
        if attack_type:
            if attack_type not in self.threat_statistics["by_type"]:
                self.threat_statistics["by_type"][attack_type] = 0
            self.threat_statistics["by_type"][attack_type] += 1

    def get_attack_history(self, ip: str) -> List[str]:
        """
        Get attack history for a specific IP.
        
        Args:
            ip: Source IP address
            
        Returns:
            List of attacks from that IP
        """
        if ip not in self.attack_history:
            return []
        return list(self.attack_history[ip])

    def get_statistics(self) -> Dict:
        """
        Get threat statistics.
        
        Returns:
            Dictionary with threat statistics
        """
        return self.threat_statistics.copy()

    def get_top_threats(self, limit: int = 5) -> List[Tuple[str, int]]:
        """
        Get top threat types by frequency.
        
        Args:
            limit: Number of top threats to return
            
        Returns:
            List of (attack_type, count) tuples
        """
        threats = self.threat_statistics["by_type"]
        sorted_threats = sorted(threats.items(), key=lambda x: x[1], reverse=True)
        return sorted_threats[:limit]

    def reset_statistics(self) -> None:
        """Reset all statistics counters."""
        self.threat_statistics = {
            "total_threats": 0,
            "by_level": {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0},
            "by_type": {}
        }
        logger.info("Threat statistics reset")

    def clear_attack_history(self, ip: Optional[str] = None) -> None:
        """
        Clear attack history.
        
        Args:
            ip: Specific IP to clear, or None to clear all
        """
        if ip:
            if ip in self.attack_history:
                del self.attack_history[ip]
                logger.info(f"Cleared attack history for IP {ip}")
        else:
            self.attack_history.clear()
            logger.info("Cleared all attack history")

    def export_threat_report(self) -> str:
        """
        Export comprehensive threat report in JSON format.
        
        Returns:
            JSON string with threat statistics
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "statistics": self.threat_statistics,
            "top_threats": dict(self.get_top_threats(10)),
            "active_ips": list(self.attack_history.keys()),
            "ip_threat_counts": {
                ip: len(history) for ip, history in self.attack_history.items()
            }
        }
        return json.dumps(report, indent=2)


# Global threat engine instance
threat_engine = ThreatEngine()


def get_threat_level(
    score: int,
    attack_type: Optional[Union[str, Dict]] = None,
    ip: Optional[str] = None
) -> Dict:
    """
    Wrapper function to get threat level using global engine instance.
    
    Args:
        score: Base threat score
        attack_type: Type of attack
        ip: Source IP address
        
    Returns:
        Dictionary with threat assessment
    """
    return threat_engine.get_threat_level(score, attack_type, ip)


def get_attack_history(ip: str) -> List[str]:
    """Get attack history for an IP address."""
    return threat_engine.get_attack_history(ip)


def get_threat_statistics() -> Dict:
    """Get current threat statistics."""
    return threat_engine.get_statistics()


def get_top_threats(limit: int = 5) -> List[Tuple[str, int]]:
    """Get top threat types."""
    return threat_engine.get_top_threats(limit)


def reset_statistics() -> None:
    """Reset threat statistics."""
    threat_engine.reset_statistics()


def clear_attack_history(ip: Optional[str] = None) -> None:
    """Clear attack history."""
    threat_engine.clear_attack_history(ip)


def export_threat_report() -> str:
    """Export threat report."""
    return threat_engine.export_threat_report()
