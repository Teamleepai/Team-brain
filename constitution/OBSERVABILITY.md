# Observability

Governs how LEAP OS makes its own behavior visible. Subordinate to `MASTER_CONSTITUTION.md`.

## Why this matters here specifically

An autonomous, multi-agent system that can't explain what it did, why, and under what trust level is not safe to grant autonomy to (see master §10, Trust Framework). Observability is the mechanism that makes trust-level advancement and revocation evidence-based rather than a gut call.

## Required signals

- **Structured logs** for every agent action: actor, trust level, inputs, outputs, decision rationale, approval chain, timestamp.
- **Metrics** per agent: recommendation acceptance rate, execution success/failure rate, time-to-approval, escalation rate.
- **Traces** across orchestration: a single user-visible outcome (e.g. the daily briefing) should be traceable back through every agent and data source that contributed to it.
- **System health dashboard**: uptime, latency, error rate, and queue depth per service — feeds directly into the executive dashboard's "system health" section (master §14).
- **Alerting**: any Trust Level 3+ action failure, any security-relevant event (`SECURITY_STANDARDS.md`), and any prompt regression trigger an alert, not just a log entry.

## Explainability requirement

Any recommendation or action must answer, on demand: what data was used, what agent produced it, what trust level authorized it, and what alternative was considered and rejected (if any). If a system can't answer this, it isn't ready to act at that trust level — dial it back to Recommend (Level 1) until it can.

## Retention

Observability data follows the same lifecycle discipline as `MEMORY_ARCHITECTURE.md` — retained long enough to support audits and trust-level review, with clear deletion policy for anything containing PII.
