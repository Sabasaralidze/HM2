# Data Map

## Purpose

This document explains what data the HM2 AI agent system collects, stores, and protects.

| Data Type | Example | Purpose | Storage Location | Retention |
|---|---|---|---|---|
| User ID | user_123 | Separate users and test isolation | episode logs / memory | Until logs deleted |
| User message | "What is safety logging?" | Agent response generation | episode logs | Until logs deleted |
| Agent response | AI generated answer | Evaluation and debugging | episode logs | Until logs deleted |
| Latency | 520 ms | Reliability monitoring | episode logs | Until logs deleted |
| Fallback status | false | Resilience evidence | episode logs | Until logs deleted |
| Audit event | chat_request | Security monitoring | audit logs | Until logs deleted |

## PII Policy

The system should not log passwords, API keys, personal addresses, or private credentials.

## Environment Secrets

Secrets are stored in `.env` locally and `.env.example` is committed only as a template.

## User Isolation

User data is separated by `user_id`. The test file `tests/test_user_isolation.py` verifies that one user cannot access another user's memory.