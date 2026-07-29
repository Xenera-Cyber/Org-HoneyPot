import os
import time
import logging
import threading
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

# How often (seconds) the background thread pings the AI backend.
HEALTH_CHECK_INTERVAL = 5

# Persistent connection pooling
_session = requests.Session()

# ------------------------------------------------------------------
# Thread-safe backend availability state
#
# _backend_available  – threading.Event; set() when reachable,
#                       clear() when offline. Readers call .is_set()
#                       which is GIL-atomic and needs no extra lock.
# _last_backend_state – tracks the previous poll result so we only
#                       log on transitions, never on steady-state.
# _monitor_thread     – reference to the daemon thread; kept so the
#                       thread is not silently garbage-collected.
# ------------------------------------------------------------------
_backend_available: threading.Event = threading.Event()
_last_backend_state: Optional[bool] = None
_monitor_thread: Optional[threading.Thread] = None


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


def check_ai_backend() -> bool:
    """
    Quick health check against the AI backend's /health endpoint.
    Returns True when the backend responds with HTTP 200, False otherwise.
    Reused by the background health monitor loop.
    """
    try:
        resp = _session.get(AI_HEALTH_URL, timeout=5)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ------------------------------------------------------------------
# Background Health Monitor
# ------------------------------------------------------------------

def _health_monitor_loop() -> None:
    """
    Daemon thread body: polls check_ai_backend() every HEALTH_CHECK_INTERVAL
    seconds and updates _backend_available accordingly.

    Logs exactly one message per state transition:
      - Offline → "AI Backend Offline → Switching to Fallback"
      - Online  → "AI Backend Online → AI Routing Restored"

    The log is intentionally silent while the state is unchanged to
    avoid console spam.
    """
    global _last_backend_state
    while True:
        available = check_ai_backend()
        if available != _last_backend_state:
            if available:
                _backend_available.set()
                logger.info(
                    "[AI Health Monitor] AI Backend Online → AI Routing Restored"
                )
            else:
                _backend_available.clear()
                logger.warning(
                    "[AI Health Monitor] AI Backend Offline → Switching to Fallback"
                )
            _last_backend_state = available
        time.sleep(HEALTH_CHECK_INTERVAL)


def start_health_monitor() -> None:
    """
    Launch the background AI-backend health-monitor daemon thread.

    Safe to call multiple times — if the thread is already alive the
    call is a no-op, so server.py does not need to guard against it.

    The monitor runs as a daemon thread, so it terminates automatically
    when the main process exits without needing explicit cleanup.
    """
    global _monitor_thread
    if _monitor_thread is not None and _monitor_thread.is_alive():
        return
    _monitor_thread = threading.Thread(
        target=_health_monitor_loop,
        daemon=True,
        name="ai-health-monitor",
    )
    _monitor_thread.start()
    logger.info("[AI Health Monitor] Background health monitor started.")


def send_to_ai(ip: str, command: str, history=None, attack_type=None, **kwargs) -> Dict[str, Any]:
    """
    Sends the attacker's command to the Xynera AI backend.

    NOTE: intentionally does NOT return hostname/username — the
    attacker-visible shell identity is fixed for the life of a session
    (see session_manager.py) and must never be driven by AI output.
    Only personality_name is returned, as analyst/logging metadata.

    Fast-path: if the health monitor has marked the backend as offline,
    return the fallback immediately without attempting any network I/O.
    This keeps attacker sessions responsive and burns no retry budget
    while the backend is known to be down.
    """
    # Fast-path: backend is currently marked offline — skip network I/O.
    if not _backend_available.is_set():
        return get_offline_fallback(attack_type, 0)

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

