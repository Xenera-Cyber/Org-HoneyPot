SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000

LOG_FILE = "ai_backend.log"
GROQ_MODEL = "llama-3.1-8b-instant"

import os

# Attempt to load using python-dotenv if installed
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass

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
                        