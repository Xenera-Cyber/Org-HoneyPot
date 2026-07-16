import os
import time
import logging
import requests
from typing import Optional, Dict, Any

# Professional logging setup
logger = logging.getLogger("ai_client")
logging.basicConfig(level=logging.INFO)

AI_BACKEND_HOST = os.environ.get("AI_BACKEND_HOST", "127.0.0.1")
AI_BACKEND_PORT = os.environ.get("AI_BACKEND_PORT", "5000")
AI_BACKEND_URL = f"http://{AI_BACKEND_HOST}:{AI_BACKEND_PORT}/process"
AI_HEALTH_URL = f"http://{AI_BACKEND_HOST}:{AI_BACKEND_PORT}/health"

TIMEOUT = 5
MAX_RETRIES = 2
RETRY_BACKOFF = 0.5

# Persistent connection pooling
_session = requests.Session()


def clean_response(text: Optional[str]) -> Optional[str]:
    if not isinstance(text, str):
        return None
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text.strip("`").strip()
    return text if text else None


def get_offline_fallback(attack_type: Optional[str], elapsed_ms: int) -> Dict[str, Any]:
    """
    Safety net payload. Since a 5s timeout increases the odds of failing
    under load, this guarantees the caller doesn't encounter an
    AttributeError or KeyError when the backend is unreachable.
    """
    return {
        "reply": None,
        "backend": "offline",
        "attack_type": attack_type or "Unknown",
        "personality_name": None,
        "prediction": None,
        "response_time": elapsed_ms
    }


def check_ai_backend():
    """
    Quick health check against the AI backend's /health endpoint.
    Called once at server.py startup to warn if the AI side is unreachable.
    """
    try:
        resp = _session.get(AI_HEALTH_URL, timeout=5)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


def send_to_ai(ip: str, command: str, history=None, attack_type=None, **kwargs) -> Dict[str, Any]:
    """
    Sends the attacker's command to the Xynera AI backend.

    NOTE: intentionally does NOT return hostname/username — the
    attacker-visible shell identity is fixed for the life of a session
    (see session_manager.py) and must never be driven by AI output.
    Only personality_name is returned, as analyst/logging metadata.
    """
    if history:
        history = [entry["command"] if isinstance(entry, dict) else entry for entry in history]

    payload = {
        "ip": ip,
        "command": command,
        "history": history or [],
        "local_attack_type": attack_type,
        **kwargs
    }

    start_time = time.perf_counter()

    for attempt in range(MAX_RETRIES + 1):
        try:
            logger.info(f"Sending AI Payload: {payload}")

            response = _session.post(AI_BACKEND_URL, json=payload, timeout=TIMEOUT)
            elapsed = round((time.perf_counter() - start_time) * 1000)

            if response.status_code != 200:
                logger.error(f"Non-200 response from AI backend: {response.status_code}")
                return get_offline_fallback(attack_type, elapsed)

            data = response.json()

            # Response validation — guard against a malformed/non-dict
            # payload before calling .get() on it.
            if not isinstance(data, dict):
                logger.error("AI backend returned non-dict JSON")
                return get_offline_fallback(attack_type, elapsed)

            return {
                "reply": clean_response(data.get("reply")),
                "attack_type": data.get("attack_type", attack_type or "Unknown"),
                "personality_name": data.get("personality_name"),
                "prediction": data.get("prediction"),
                "backend": "local",
                "response_time": elapsed
            }

        except requests.exceptions.Timeout:
            elapsed = round((time.perf_counter() - start_time) * 1000)
            logger.error(f"Timeout hit after {elapsed}ms. Aborting loop to avoid server strain.")
            break

        except requests.exceptions.ConnectionError as e:
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF * (attempt + 1)
                logger.warning(f"Connection failed ({e}). Retrying in {wait}s ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            logger.error("Connection failed completely after retries.")

        except Exception as e:
            logger.error(f"Unexpected error processing AI response: {e}")
            break

    final_elapsed = round((time.perf_counter() - start_time) * 1000)
    return get_offline_fallback(attack_type, final_elapsed)