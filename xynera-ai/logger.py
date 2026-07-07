import logging
import json

try:
    from config import LOG_FILE
except ImportError:
    LOG_FILE = "app.log"


logger = logging.getLogger("xynera")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE)

    formatter = logging.Formatter(
        "%(asctime)s - %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_event(message):
    """
    Basic event logging.
    Backward-compatible with existing modules.
    """
    logger.info(message)


def log_ai_decision(
    session_id,
    command,
    attack_type,
    risk_score,
    threat_level
):
    """
    Logs AI security decisions.
    """

    log_data = {
        "session_id": session_id,
        "command": command,
        "attack_type": attack_type,
        "risk_score": risk_score,
        "threat_level": threat_level
    }

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
    """
    Advanced AI analytics logging.
    """

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
    """
    Centralized logging for conversation,
    AI decisions, system events,
    security events and predictions.
    """

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


if __name__ == "__main__":

    log_event("Logger Test")

    log_ai_decision(
        session_id="A102",
        command="sudo su",
        attack_type="Privilege Escalation",
        risk_score=82,
        threat_level="HIGH"
    )

    log_ai_analysis(
        session_id="A102",
        command="sudo su",
        ai_decision="Privilege Escalation Detected",
        confidence_score=0.96,
        conversation_id="SESSION_001",
        interaction_count=7,
        prediction_result="Credential Access",
        prediction_confidence=0.89,
        risk_score=82,
        threat_level="HIGH"
    )

    log_centralized_event(
        session_id="SESSION_101",
        conversation_log="Attacker executed sudo su",
        ai_decision="Privilege Escalation Attempt",
        system_event="AI Response Generated",
        security_event="Privilege Escalation",
        warning="High Risk Command",
        error=None,
        prediction="Credential Access"
    )

    print("Centralized Logging Test Successful.")