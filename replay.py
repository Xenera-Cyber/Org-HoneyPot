"""
replay.py

Thin wrapper around ai_client.py's AI-backend communication helpers.

This module previously duplicated ai_client.py's send_to_ai()/clean_response()
implementation verbatim. That duplication has been removed (Baseline V3.2
integration) so replay/testing tooling always uses the same retry, offline
fallback, and response-validation logic as the live honeypot instead of a
copy that can silently drift out of sync.
"""

from ai_client import (
    AI_BACKEND_URL,
    AI_HEALTH_URL,
    TIMEOUT,
    clean_response,
    send_to_ai,
    check_ai_backend,
    get_offline_fallback,
)

__all__ = [
    "AI_BACKEND_URL",
    "AI_HEALTH_URL",
    "TIMEOUT",
    "clean_response",
    "send_to_ai",
    "check_ai_backend",
    "get_offline_fallback",
]
