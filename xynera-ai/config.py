import os
import json

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
LOG_FILE = "ai_backend.log"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Custom manual parser fallback
if not GROQ_API_KEY:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    if key.strip() == "GROQ_API_KEY":
                        GROQ_API_KEY = val.strip().strip("'\"")
                        break

def get_dynamic_config():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dynamic_config.json")
    default_config = {
        "personality": "auto",
        "model": "llama-3.1-8b-instant",
        "confidenceThreshold": 85,
        "temperature": 0.1,
        "maxContext": 4096,
        "maxResponseLength": 1024,
        "ragEnabled": True,
        "guardrailsEnabled": True
    }
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return {**default_config, **json.load(f)}
        except Exception:
            return default_config
    return default_config

# Set static GROQ_MODEL variable for backward compatibility
GROQ_MODEL = get_dynamic_config()["model"]
                        