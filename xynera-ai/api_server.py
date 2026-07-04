from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

from rag_engine import generate_deception
from threat_engine import get_threat_level
from attacker_profile import update_profile
from classifier import classify_command
from logger import log_event, log_ai_decision
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

    attack_type = classify_command(command)

    score = update_profile(ip, attack_type, command)

    threat_level = get_threat_level(score)

    log_ai_decision(
        session_id=payload.session_id or "UNKNOWN",
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
        username=payload.username
    )

    return ProcessResponse(
        reply=reply,
        attack_type=attack_type
    )


if __name__ == "__main__":
    uvicorn.run("api_server:app", host=SERVER_HOST, port=SERVER_PORT, reload=False)
