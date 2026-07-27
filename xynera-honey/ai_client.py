import os
import time
import random
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

# ==========================================================
# Timeout strategy
# ==========================================================
# Separate connect vs. read timeouts instead of one flat value:
#   - CONNECT_TIMEOUT: how long we wait for the TCP handshake. Kept
#     short -- if the backend process is down/unreachable, that fails
#     fast instead of tying up the honeypot's response to the attacker.
#   - READ_TIMEOUT: how long we wait for the backend to actually finish
#     generating a reply once connected. Kept longer, since a live but
#     briefly slow backend (e.g. under load) shouldn't be treated the
#     same as a dead one.
CONNECT_TIMEOUT = 2
READ_TIMEOUT = 6
TIMEOUT = (CONNECT_TIMEOUT, READ_TIMEOUT)

# ==========================================================
# Retry policy
# ==========================================================
MAX_RETRIES = 2
BASE_BACKOFF = 0.5
MAX_BACKOFF = 3.0

# Persistent connection pooling
_session = requests.Session()


def clean_response(text: Optional[str]) -> Optional[str]:
    if not isinstance(text, str):
        return None
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        text = text.strip("`").strip()
    return text if text else None


def get_offline_fallback(attack_type: Optional[str], elapsed_ms: int, reason: str = "offline") -> Dict[str, Any]:
    """
    Safety net payload. Since backend calls can fail in several distinct
    ways now (timeout, connection refused, non-retryable HTTP status,
    malformed JSON), `reason` records which one so callers/logs can tell
    them apart instead of every failure looking identical.
    """
    return {
        "reply": None,
        "backend": "offline",
        "reason": reason,
        "attack_type": attack_type or "Unknown",
        "personality_name": None,
        "prediction": None,
        "response_time": elapsed_ms
    }


def check_ai_backend():
    """
    Quick health check against the AI backend's /health endpoint.
    Called once at server.py startup to warn if the AI side is unreachable.
    Uses the short connect timeout only -- a health check should fail
    fast, not wait as long as a real command would.
    """
    try:
        resp = _session.get(AI_HEALTH_URL, timeout=CONNECT_TIMEOUT)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


def _compute_backoff(attempt: int) -> float:
    """
    Exponential backoff with jitter, capped at MAX_BACKOFF.

    Replaces the old flat linear wait (BASE_BACKOFF * (attempt + 1)) with
    one that grows faster on repeated failures (so a genuinely struggling
    backend gets breathing room instead of being hammered every ~0.5-1s),
    while jitter avoids every concurrent session retrying in lockstep.
    """
    backoff = min(BASE_BACKOFF * (2 ** attempt), MAX_BACKOFF)
    jitter = random.uniform(0, backoff * 0.25)
    return backoff + jitter


def _classify_status(status_code: int) -> str:
    """
    Buckets an HTTP status code into a retry decision instead of
    treating every non-200 identically:
      - 200            -> "success"
      - 429            -> "retryable"  (rate limited; backing off and
                           trying again is exactly the right response)
      - 500-599        -> "retryable"  (transient server-side failure)
      - other 4xx      -> "fatal"      (bad request/auth/not-found --
                           the same request will just fail again, so
                           retrying wastes time and hides the real bug)
    """
    if status_code == 200:
        return "success"
    if status_code == 429:
        return "retryable"
    if 500 <= status_code <= 599:
        return "retryable"
    return "fatal"


def _validate_ai_payload(data: Any, attack_type: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Validates and sanitizes the AI backend's JSON body beyond a bare
    isinstance(dict) check. Each field we actually consume downstream
    gets a type check; a wrong type (e.g. `reply` coming back as a list,
    `attack_type` as an int) is logged and coerced to a safe default
    rather than silently propagating into session/prompt logic.

    Returns None if `data` isn't even a dict (unrecoverable), otherwise
    a cleaned dict with `reply` / `attack_type` / `personality_name` /
    `prediction`.
    """
    if not isinstance(data, dict):
        return None

    reply = data.get("reply")
    if reply is not None and not isinstance(reply, str):
        logger.warning(f"AI backend returned non-string 'reply' ({type(reply).__name__}); discarding.")
        reply = None

    ai_attack_type = data.get("attack_type")
    if ai_attack_type is not None and not isinstance(ai_attack_type, str):
        logger.warning(f"AI backend returned non-string 'attack_type' ({type(ai_attack_type).__name__}); discarding.")
        ai_attack_type = None

    personality_name = data.get("personality_name")
    if personality_name is not None and not isinstance(personality_name, str):
        logger.warning(f"AI backend returned non-string 'personality_name' ({type(personality_name).__name__}); discarding.")
        personality_name = None

    prediction = data.get("prediction")
    if prediction is not None and not isinstance(prediction, (dict, str, int, float)):
        logger.warning(f"AI backend returned unexpected 'prediction' type ({type(prediction).__name__}); discarding.")
        prediction = None

    return {
        "reply": clean_response(reply),
        "attack_type": ai_attack_type or attack_type or "Unknown",
        "personality_name": personality_name,
        "prediction": prediction,
    }


def send_to_ai(ip: str, command: str, history=None, attack_type=None, **kwargs) -> Dict[str, Any]:
    """
    Sends the attacker's command to the Xynera AI backend.

    NOTE: intentionally does NOT return hostname/username — the
    attacker-visible shell identity is fixed for the life of a session
    (see session_manager.py) and must never be driven by AI output.
    Only personality_name is returned, as analyst/logging metadata.

    Retry policy (unified across all failure modes, MAX_RETRIES each):
      - Timeout                          -> retry with backoff
      - ConnectionError                  -> retry with backoff
      - HTTP 429 / 5xx ("retryable")     -> retry with backoff
                                            (honors Retry-After on 429s)
      - HTTP other 4xx ("fatal")         -> no retry, fail fast
      - Malformed / non-dict JSON        -> no retry, fail fast
      - Any other unexpected exception   -> no retry, fail fast
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
            logger.info(f"Sending AI Payload (attempt {attempt + 1}/{MAX_RETRIES + 1}): {payload}")

            response = _session.post(AI_BACKEND_URL, json=payload, timeout=TIMEOUT)
            elapsed = round((time.perf_counter() - start_time) * 1000)

            status_kind = _classify_status(response.status_code)

            if status_kind == "fatal":
                logger.error(f"Non-retryable status {response.status_code} from AI backend; giving up.")
                return get_offline_fallback(attack_type, elapsed, reason=f"http_{response.status_code}")

            if status_kind == "retryable":
                if attempt < MAX_RETRIES:
                    wait = _compute_backoff(attempt)
                    # Honor Retry-After on 429s if the backend sends one,
                    # rather than guessing at a backoff it may not want.
                    if response.status_code == 429:
                        retry_after = response.headers.get("Retry-After")
                        if retry_after:
                            try:
                                wait = max(wait, float(retry_after))
                            except ValueError:
                                pass
                    logger.warning(
                        f"Retryable status {response.status_code} from AI backend. "
                        f"Retrying in {wait:.2f}s ({attempt + 1}/{MAX_RETRIES})"
                    )
                    time.sleep(wait)
                    continue
                logger.error(f"Status {response.status_code} persisted after all retries.")
                return get_offline_fallback(attack_type, elapsed, reason=f"http_{response.status_code}")

            # status_kind == "success" (HTTP 200)
            try:
                data = response.json()
            except ValueError:
                logger.error("AI backend returned invalid/non-JSON body.")
                return get_offline_fallback(attack_type, elapsed, reason="invalid_json")

            validated = _validate_ai_payload(data, attack_type)
            if validated is None:
                logger.error("AI backend returned non-dict JSON.")
                return get_offline_fallback(attack_type, elapsed, reason="invalid_json")

            return {
                **validated,
                "backend": "local",
                "response_time": elapsed
            }

        except requests.exceptions.Timeout:
            elapsed = round((time.perf_counter() - start_time) * 1000)
            if attempt < MAX_RETRIES:
                wait = _compute_backoff(attempt)
                logger.warning(
                    f"Timeout after {elapsed}ms. Retrying in {wait:.2f}s ({attempt + 1}/{MAX_RETRIES})"
                )
                time.sleep(wait)
                continue
            logger.error(f"Timeout persisted after all retries ({elapsed}ms).")
            return get_offline_fallback(attack_type, elapsed, reason="timeout")

        except requests.exceptions.ConnectionError as e:
            if attempt < MAX_RETRIES:
                wait = _compute_backoff(attempt)
                logger.warning(f"Connection failed ({e}). Retrying in {wait:.2f}s ({attempt + 1}/{MAX_RETRIES})")
                time.sleep(wait)
                continue
            logger.error("Connection failed completely after retries.")
            break

        except Exception as e:
            logger.error(f"Unexpected error processing AI response: {e}")
            break

    final_elapsed = round((time.perf_counter() - start_time) * 1000)
    return get_offline_fallback(attack_type, final_elapsed, reason="exception")