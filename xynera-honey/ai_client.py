import requests
import time
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)

LOCAL_BACKEND = "http://10.200.200.30:5000/process"
REMOTE_BACKEND = "https://your-remote-ai-api/process"

TIMEOUT = 330


def clean_response(text):
    if not isinstance(text, str):
        return ""

    if text.startswith("```") and text.endswith("```"):
        text = text.strip("```")

    return text.strip()


def _post(url: str, payload: dict):
    start = time.perf_counter()

    response = requests.post(
        url,
        json=payload,
        timeout=TIMEOUT
    )

    elapsed = round((time.perf_counter() - start) * 1000)

    response.raise_for_status()

    data = response.json()

    data["response_time"] = elapsed

    return data


def send_to_ai(
    *,
    session_id: str,
    ip: str,
    username: str,
    hostname: str,
    cwd: str,
    command: str,
    history=None,
    attack_type=None,
    personality="default"
) -> Dict[str, Any]:

    payload = {
        "session": {
            "session_id": session_id,
            "ip": ip,
            "username": username,
            "hostname": hostname,
            "cwd": cwd,
            "command": command,
            "history": history or [],
            "attack_type": attack_type,
            "timestamp": time.time()
        },

        "ai": {
            "personality": personality
        }
    }

    logging.info(f"Sending AI Payload: {payload}")

    try:

        data = _post(LOCAL_BACKEND, payload)

        data["backend"] = "local"

        data["reply"] = clean_response(data.get("reply"))

        return data

    except Exception as e:

        logging.warning(f"Local backend failed: {e}")

    try:

        data = _post(REMOTE_BACKEND, payload)

        data["backend"] = "remote"

        data["reply"] = clean_response(data.get("reply"))

        return data

    except Exception as e:

        logging.error(f"Remote backend failed: {e}")

    return {

        "reply": "Command executed.",

        "backend": "offline",

        "personality": personality,

        "threat_score": 0,

        "confidence": 0,

        "attack_type": attack_type,

        "response_time": TIMEOUT * 1000,

        "rag": {
            "enabled": False,
            "documents_used": 0,
            "knowledge_hits": 0
        },

        "guardrails": {
            "blocked": False,
            "reason": None
        }
    }