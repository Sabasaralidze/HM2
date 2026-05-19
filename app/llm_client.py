from tenacity import retry, stop_after_attempt, wait_exponential


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8)
)
def call_llm(prompt: str) -> str:

    prompt_lower = prompt.lower()

    if "safety" in prompt_lower:
        return "Safety audit logging helps monitor AI system behavior."

    elif "token" in prompt_lower:
        return "Bearer token authentication improves secure API access."

    elif "pydantic" in prompt_lower:
        return "Pydantic is used for validation of structured input data."

    elif "errors" in prompt_lower or "sanitized" in prompt_lower:
        return "Sanitized errors hide internal implementation details."

    elif "backoff" in prompt_lower:
        return "Exponential backoff retries requests after failure."

    elif "user isolation" in prompt_lower:
        return "User isolation keeps separate user data secure."

    elif "episode log" in prompt_lower:
        return "Episode logs store request response latency information."

    elif ".env" in prompt_lower:
        return "Environment files contain secret private keys."

    elif "golden test" in prompt_lower:
        return "Golden test evaluation checks expected responses."

    elif "timeout" in prompt_lower:
        return "Timeout prevents long response delays."

    return "Fallback response: safe default answer."