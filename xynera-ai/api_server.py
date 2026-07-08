from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from rag_engine import generate_deception, generate_response
from threat_engine import get_threat_level
from attacker_profile import update_profile, update_profile_response, get_detailed_profile, get_session_data
from classifier import classify_command
from logger import log_event, log_ai_decision, log_ai_analysis, log_centralized_event, log_personality_integration
from personalities import get_personality
from config import SERVER_HOST, SERVER_PORT


app = FastAPI(title="Xynera AI Backend")


class ProcessRequest(BaseModel):
    ip: str
    command: str
    session_id: Optional[str] = None
    history: Optional[List[str]] = None
    local_attack_type: Optional[str] = None
    cwd: Optional[str] = None
    hostname: Optional[str] = None
    username: Optional[str] = None


class ProcessResponse(BaseModel):
    reply: Optional[str] = None
    attack_type: str
    personality_name: Optional[str] = None
    hostname: Optional[str] = None
    username: Optional[str] = None


@app.get("/health")
async def health():
    return {"status": "AI Backend Running"}


@app.post("/process", response_model=ProcessResponse)
async def process_command(payload: ProcessRequest):
    ip = payload.ip
    command = payload.command

    # 1. Classifier
    classification = classify_command(command, ip=ip)
    attack_type = classification["attack_type"]
    session_id = classification["session_id"]
    base_score = classification["risk_score"]
    confidence = classification.get("confidence", 0.90)

    # Dynamic data generation and command history tracking
    commands_history = (payload.history or []) + [command]
    get_session_data(session_id, commands=commands_history)

    # 2. Attacker Profile
    update_profile(ip, attack_type, command, cwd=payload.cwd, score=base_score)
    detailed_profile = get_detailed_profile(ip, base_score, classification.get("threat_level", "LOW"))

    # 3. Threat Engine
    threat_score = get_threat_level(base_score, attack_type=attack_type, ip=ip)

    # 4. Personalities
    personality = get_personality(detailed_profile, threat_score)

    # 5. RAG Engine -> 6. Guardrails (applied inside generate_response)
    reply = await generate_response(
        command=command,
        personality=personality,
        attacker_profile=detailed_profile,
        threat_score=threat_score,
        history=payload.history,
        cwd=payload.cwd,
        session_id=session_id
    )

    # Track response outcome (success/failure)
    update_profile_response(ip, reply)

    # Get updated profile after response outcome is tracked
    detailed_profile = get_detailed_profile(ip, threat_score["score"], threat_score["risk_level"])

    # 7. Logger
    log_personality_integration(
        session_id=session_id,
        command=command,
        response=reply or "None",
        personality=personality,
        threat_score=threat_score,
        attacker_profile=detailed_profile
    )

    log_ai_decision(
        session_id=session_id,
        command=command,
        attack_type=attack_type,
        risk_score=threat_score["score"],
        threat_level=threat_score["risk_level"]
    )

    curiosity = detailed_profile["curiosity"]
    log_ai_analysis(
        session_id=session_id,
        command=command,
        ai_decision=reply or "None",
        confidence_score=confidence,
        conversation_id=session_id,
        interaction_count=curiosity["commands_executed"],
        prediction_result=attack_type,
        prediction_confidence=confidence,
        risk_score=threat_score["score"],
        threat_level=threat_score["risk_level"]
    )

    warning_msg = "High Threat Level" if threat_score["risk_level"] in ["HIGH", "CRITICAL"] else None
    log_centralized_event(
        session_id=session_id,
        conversation_log=f"Attacker executed: {command}",
        ai_decision=reply or "None",
        system_event="AI Deception Generated",
        security_event=attack_type,
        warning=warning_msg,
        error=None,
        prediction=attack_type
    )

    # 8. Client Response
    return ProcessResponse(
        reply=reply,
        attack_type=attack_type,
        personality_name=personality.get("name", "Normal Server"),
        hostname=personality.get("hostname", "ubuntu-server"),
        username=personality.get("user", "ubuntu")
    )


if __name__ == "__main__":
    uvicorn.run("api_server:app", host=SERVER_HOST, port=SERVER_PORT, reload=False)
