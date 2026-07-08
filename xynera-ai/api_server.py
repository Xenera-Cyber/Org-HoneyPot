from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from rag_engine import generate_deception
from threat_engine import get_threat_level
from attacker_profile import update_profile, update_profile_response, get_detailed_profile, get_session_data
from classifier import classify_command
from logger import log_event, log_ai_decision, log_ai_analysis, log_centralized_event
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


@app.get("/health")
async def health():
    return {"status": "AI Backend Running"}


@app.post("/process", response_model=ProcessResponse)
async def process_command(payload: ProcessRequest):
    ip = payload.ip
    command = payload.command

    classification = classify_command(command, ip=ip)
    attack_type = classification["attack_type"]
    session_id = classification["session_id"]
    score = classification["risk_score"]
    threat_level = classification["threat_level"]

    # Dynamic data generation and command history tracking
    commands_history = (payload.history or []) + [command]
    get_session_data(session_id, commands=commands_history)

    # Track detailed stats by passing payload.cwd and the updated score
    update_profile(ip, attack_type, command, cwd=payload.cwd, score=score)

    log_ai_decision(
        session_id=session_id,
        command=command,
        attack_type=attack_type,
        risk_score=score,
        threat_level=threat_level
    )

    reply = await generate_deception(
        command=command,
        history=payload.history,
        cwd=payload.cwd,
        attack_type=attack_type,
        hostname=payload.hostname,
        username=payload.username,
        session_id=session_id
    )

    # Track response outcome (success/failure)
    update_profile_response(ip, reply)

    # Calculate advanced attacker profiling metrics
    detailed = get_detailed_profile(ip, score, threat_level)
    if detailed:
        curiosity = detailed["curiosity"]
        engagement = detailed["engagement"]
        behaviour = detailed["behaviour"]

        # Log advanced AI analysis
        log_ai_analysis(
            session_id=session_id,
            command=command,
            ai_decision=reply or "None",
            confidence_score=0.95,
            conversation_id=session_id,
            interaction_count=curiosity["commands_executed"],
            prediction_result=attack_type,
            prediction_confidence=0.90,
            risk_score=score,
            threat_level=threat_level
        )

        # Log centralized system event
        warning_msg = "High Threat Level" if threat_level in ["HIGH", "CRITICAL"] else None
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

    return ProcessResponse(
        reply=reply,
        attack_type=attack_type
    )


if __name__ == "__main__":
    uvicorn.run("api_server:app", host=SERVER_HOST, port=SERVER_PORT, reload=False)
