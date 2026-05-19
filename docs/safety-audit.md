# Safety Audit Report

Team members: Saba Saralidze, Luka Kikvadze, Luka Gorduladze  
Project: HM2 AI Safety Audit

## Overview

This report describes the safety, reliability, evaluation, and data governance work completed for our HM2 AI agent project. The goal of this audit is to show that the system is not only functional, but also safer to test, easier to monitor, and more controlled when handling user requests.

The project uses a small FastAPI-based agent service with logging, request validation, authentication, evaluation tests, and user-isolation checks. Since this is a homework project, the LLM response layer is implemented as a controlled mock client instead of depending on a real API key. This makes the project easier to run and verify without exposing secrets.

## Episode Log Quality

The system records each agent interaction in an episode log file. The logging function is implemented in `app/logger.py`, and the generated log entries are stored in `logs/episode_log.jsonl`.

Each log entry includes the main fields needed for tracing and debugging:

- `timestamp`
- `user_id`
- `question`
- `response`
- `cache_read_tokens`
- `latency_ms`
- `fallback_triggered`

This helps us understand when the agent was called, which user made the request, how long the response took, and whether a fallback response was used. The log format is JSONL, so each line is a separate structured record and can be checked automatically.

## Agent Architecture

The agent uses a simple tool-calling style architecture. The main flow is:

1. A user sends a request.
2. The MCP server validates the request.
3. The agent receives the message.
4. The LLM client produces a controlled response.
5. The response and metadata are written to the episode log.
6. The result is returned to the user.

The architecture is documented in `README.md`, and the main agent logic is implemented in `app/agent.py`.

The project includes an `AgentState` dataclass to describe the important parts of the agent state, such as the user id, conversation history, tool outputs, and permissions. The code also includes an irreversible action map for actions that should not happen without additional review, such as deleting logs or overwriting evaluation results.

## MCP Server Security

The MCP server is implemented in `app/mcp_server.py`. The server includes basic security controls to reduce unsafe or uncontrolled access.

Bearer token authentication is used before processing chat requests. This means a request must include the correct authorization header before the server accepts it.

Input validation is handled through Pydantic in `app/models.py`. The `ChatRequest` model checks that the request contains the expected fields before the agent runs.

The server also writes audit events to `logs/audit_log.jsonl`. These audit logs record important server-side events, including the event type, user id, timestamp, and status.

Error responses are sanitized. Instead of returning raw Python errors or stack traces to the user, the server returns a clean internal error message. This avoids exposing implementation details.

## Resilience Patterns

The LLM client is implemented in `app/llm_client.py`. The call function uses retry logic with exponential backoff through the `tenacity` library.

This means that if an LLM call fails, the system does not immediately stop. It retries in a controlled way, with waiting time between attempts. This pattern makes the system more reliable and prevents simple temporary failures from breaking the full workflow.

The project uses a mock LLM response function, so it can be tested without a real API key. This also avoids exposing secrets in the repository.

## Golden Test Set and Evaluation

The project includes a golden test set in `eval/golden_set.json`. It contains ten test questions related to the main safety and reliability topics of the system.

The evaluation script is implemented in `eval/run_golden_set.py`. It runs every golden question through the agent and checks whether the answer contains expected keywords. The evaluation results are saved in:

`eval/results/results.json`

The latest evaluation run passed all ten tests. This shows that the agent gives expected answers for the safety topics covered in the golden test set.

## Data Governance

The data governance evidence is documented in `docs/data-map.md`.

The system separates user data by `user_id`. This is important because one user should not be able to access another user’s conversation memory. The isolation behavior is tested in `tests/test_user_isolation.py`.

The project also avoids storing sensitive secrets in the repository. The `.env` file is ignored, and only `.env.example` is included as a safe template. This allows someone to understand which environment variables are needed without exposing real credentials.

The logs are designed for debugging and audit evidence. They should not contain API keys, passwords, or private credentials.

## Verification

The main verification commands used for this project are:

```bash
python eval/run_golden_set.py