from flask import Flask, request, jsonify

from rag_engine import generate_deception
from threat_engine import get_threat_level
from attacker_profile import update_profile
from classifier import classify_command
from logger import log_event
from config import SERVER_HOST, SERVER_PORT


app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "AI Backend Running"})


@app.route("/process", methods=["POST"])
def process_command():

    data = request.json

    ip = data.get("ip")
    command = data.get("command")

    attack_type = classify_command(command)

    score = update_profile(ip, attack_type, command)

    threat_level = get_threat_level(score)

    log_event(
        f"IP: {ip} | CMD: {command} | TYPE: {attack_type} | SCORE: {score} | LEVEL: {threat_level}"
    )

    reply = generate_deception(command)

    return jsonify({
        "reply": reply,
        "attack_type": attack_type
    })


if __name__ == "__main__":
    app.run(host=SERVER_HOST, port=SERVER_PORT)
