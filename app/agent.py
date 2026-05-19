from dataclasses import dataclass, field
from typing import List, Dict
import time

from app.llm_client import call_llm
from app.logger import log_episode


@dataclass
class AgentState:
    user_id: str
    conversation_history: List[str] = field(default_factory=list)
    tool_outputs: Dict[str, str] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)


IRREVERSIBLE_ACTION_MAP = {
    "delete_logs": "Requires admin approval",
    "overwrite_eval_results": "Requires reviewer approval",
    "remove_audit_entries": "Blocked by default"
}


USER_MEMORY = {}


def run_agent(user_id: str, message: str) -> str:
    start_time = time.time()
    fallback_triggered = False

    USER_MEMORY.setdefault(user_id, [])
    USER_MEMORY[user_id].append(message)

    response = call_llm(message)

    if response.startswith("Fallback response"):
        fallback_triggered = True

    latency_ms = int((time.time() - start_time) * 1000)

    log_episode(
        user_id=user_id,
        question=message,
        response=response,
        cache_read_tokens=0,
        latency_ms=latency_ms,
        fallback_triggered=fallback_triggered
    )

    return response


def get_user_memory(user_id: str):
    return USER_MEMORY.get(user_id, [])