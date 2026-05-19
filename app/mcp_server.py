import os
import json
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv

from app.models import ChatRequest
from app.agent import run_agent

load_dotenv()

app = FastAPI(title="HM2 Safety Audit MCP Server")

BEARER_TOKEN = os.getenv("BEARER_TOKEN", "my_secure_token")
AUDIT_LOG_FILE = "logs/audit_log.jsonl"


def write_audit_log(event_type: str, user_id: str, status: str):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "status": status
    }

    with open(AUDIT_LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def verify_token(authorization: str):
    if authorization != f"Bearer {BEARER_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized request")


@app.post("/chat")
def chat(request: ChatRequest, authorization: str = Header(None)):
    verify_token(authorization)

    try:
        response = run_agent(request.user_id, request.message)
        write_audit_log("chat_request", request.user_id, "success")
        return {"response": response}

    except Exception:
        write_audit_log("chat_request", request.user_id, "error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )