import json
from datetime import datetime

LOG_FILE = "logs/episode_log.jsonl"


def log_episode(
    user_id,
    question,
    response,
    cache_read_tokens,
    latency_ms,
    fallback_triggered
):

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "question": question,
        "response": response,
        "cache_read_tokens": cache_read_tokens,
        "latency_ms": latency_ms,
        "fallback_triggered": fallback_triggered
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")