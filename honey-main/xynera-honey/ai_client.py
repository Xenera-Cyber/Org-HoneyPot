import requests

AI_BACKEND_URL = "http://10.200.200.30:5000/process"
TIMEOUT = 335


def clean_response(text):
    # ensure valid string
    if not isinstance(text, str):
        return None

    # remove markdown if present
    if text.startswith("```") and text.endswith("```"):
        text = text.strip("```")

    text = text.strip()

    # IMPORTANT: return None instead of empty string
    return text if text else None


def send_to_ai(ip, command, history=None, attack_type=None, cwd=None, hostname=None, username=None):
    try:
        payload = {
            "ip": ip,
            "command": command,
            "history": history or [],
            "local_attack_type": attack_type,
            "cwd": cwd,
            "hostname": hostname,
            "username": username
        }

        print(f"[AI REQUEST] {payload}")

        response = requests.post(
            AI_BACKEND_URL,
            json=payload,
            timeout=TIMEOUT
        )

        print(f"[AI STATUS] {response.status_code}")

        if response.status_code != 200:
            print("[AI ERROR] Non-200 response")
            return None

        try:
            data = response.json()
        except Exception:
            print("[AI ERROR] Invalid JSON")
            return None

        reply = data.get("reply")
        cleaned = clean_response(reply)

        return cleaned

    except requests.exceptions.Timeout:
        print("[AI ERROR] Timeout")
        return None

    except requests.exceptions.ConnectionError:
        print("[AI ERROR] Connection failed")
        return None

    except Exception as e:
        print(f"[AI ERROR] {e}")
        return None
