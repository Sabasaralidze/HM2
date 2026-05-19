# HM2 - AI Safety Audit

## Project Overview

This project demonstrates a minimal AI agent system with safety,
security, logging, resilience, and evaluation mechanisms.

---

# Agent Architecture

## Pattern Choice

Tool-calling AI agent architecture.

## Components

- FastAPI MCP Server
- Logging Layer
- Evaluation Layer
- LLM Client
- Security Middleware

## AgentState Dataclass

The system stores:

- user_id
- conversation_history
- tool_outputs
- permissions

## Irreversible Actions

The following actions are irreversible:

- deleting logs
- overwriting evaluation results
- removing audit entries

---

# Security Features

- Bearer token authentication
- Pydantic request validation
- Structured audit logging
- Sanitized error responses

---

# Resilience Features

- Timeout protection
- Exponential backoff retry

---

# Evaluation

Golden test evaluation included in:

```text
eval/run_golden_set.py
```

Results stored in:

```text
eval/results/
```