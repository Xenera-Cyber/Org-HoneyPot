import logging
import json

try:
    from config import LOG_FILE
except ImportError:
    LOG_FILE = "app.log"


logger = logging.getLogger("xynera")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_event(message):
    logger.info(message)


def log_ai_decision(
    session_id,
    command,
    attack_type,
    risk_score,
    threat_level,
    personality=None,
    attacker_profile=None
):
    log_data = {
        "session_id": session_id,
        "command": command,
        "attack_type": attack_type,
        "risk_score": risk_score,
        "threat_level": threat_level
    }
    if personality:
        log_data["personality"] = personality
    if attacker_profile:
        log_data["attacker_profile"] = make_serializable(attacker_profile)

    logger.info(json.dumps(log_data))


def log_ai_analysis(
    session_id,
    command,
    ai_decision,
    confidence_score,
    conversation_id,
    interaction_count,
    prediction_result,
    prediction_confidence,
    risk_score,
    threat_level
):
    log_data = {
        "session_id": session_id,
        "command": command,
        "ai_decision": ai_decision,
        "confidence_score": confidence_score,
        "conversation_metadata": {
            "conversation_id": conversation_id,
            "interaction_count": interaction_count
        },
        "prediction_result": {
            "next_prediction": prediction_result,
            "prediction_confidence": prediction_confidence
        },
        "risk_score": risk_score,
        "threat_level": threat_level
    }
    logger.info(json.dumps(log_data, indent=4))


def log_centralized_event(
    session_id,
    conversation_log,
    ai_decision,
    system_event,
    security_event,
    error=None,
    warning=None,
    prediction=None
):
    log_data = {
        "session_id": session_id,
        "conversation_log": conversation_log,
        "ai_decision": ai_decision,
        "session_metadata": {
            "prediction": prediction
        },
        "system_event": system_event,
        "security_event": security_event,
        "warning": warning,
        "error": error
    }
    logger.info(json.dumps(log_data, indent=4))


def make_serializable(obj):
    if isinstance(obj, set):
        return list(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(x) for x in obj]
    return obj


def log_personality_integration(
    session_id,
    command,
    response,
    personality,
    threat_score,
    attacker_profile
):
    log_data = {
        "session_id": session_id,
        "query": command,
        "response": response,
        "selected_personality": make_serializable(personality),
        "threat_score": make_serializable(threat_score),
        "attacker_profile": make_serializable(attacker_profile)
    }
    logger.info(json.dumps(log_data, indent=4))
