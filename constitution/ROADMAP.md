# Roadmap

Phased path from MVP to enterprise scale. Subordinate to `MASTER_CONSTITUTION.md`. This is a living document — update it as reality corrects the plan; do not treat it as fixed scope.

## Phase 0 — Foundation (this phase)

- Constitution and companion standards in place (this directory).
- Repository, environment, and CI/CD scaffolding.
- Core data model and memory architecture v1 (`MEMORY_ARCHITECTURE.md`).
- Security baseline: secrets management, RBAC skeleton, audit logging (`SECURITY_STANDARDS.md`).
- Observability baseline: structured logging and a minimal health dashboard.

**Exit criteria**: a new contributor (human or agent) can read this directory and understand what to build and how, without additional context.

## Phase 1 — Single-agent MVP (Trust Levels 0–1)

- One agent (Chief of Staff, observe + recommend only) ingesting a single data source (e.g. calendar + email).
- Executive briefing v1: highest priority work, emails awaiting response, personal reminders.
- No autonomous execution. Every output is a recommendation a human acts on manually.

**Exit criteria**: daily briefing is used by a real executive for two consecutive weeks with measurable time saved and no false/misleading recommendations.

## Phase 2 — Draft and approval workflows (Trust Levels 2–3)

- Agent roster expands to Email Intelligence, Meeting Intelligence, Messaging Intelligence.
- Draft generation (emails, follow-ups, summaries) with a lightweight approval UI (`UX_PRINCIPLES.md`).
- Approval-gated execution for a narrow, low-risk action set.
- Knowledge system v1: decisions, meetings, and projects tracked and linked.

**Exit criteria**: draft acceptance rate and approval turnaround are tracked and trending favorably; no security or privacy incidents.

## Phase 3 — Guarded autonomy (Trust Level 4)

- Selected, narrowly-scoped actions execute autonomously inside guardrails (e.g. auto-scheduling within pre-approved constraints).
- CRM Intelligence, Sales Coach, Voice QA agents come online with structured call intelligence (master §13).
- Continuous Improvement loop (`CONTINUOUS_IMPROVEMENT.md`) running on a real cadence with measured hypothesis-to-impact rate.

**Exit criteria**: autonomous actions show sustained accuracy with zero unrecovered incidents over a defined observation window before further trust expansion.

## Phase 4 — Organizational operating layer (Trust Level 5 for select workflows)

- Full agent ecosystem (`AI_AGENT_STANDARDS.md` roster) operating across functions.
- Cross-agent orchestration handling conflicting recommendations gracefully.
- Enterprise-readiness: multi-tenant scale, compliance certifications, formalized RBAC and approval configurability for enterprise customers.

**Exit criteria**: system demonstrably increases organizational intelligence and decision quality, measured, not just adopted.

## Phase 5 — Category-defining platform

- Third-party/agent extensibility, enterprise-grade customization of trust levels and workflows per customer.
- Sustained compounding value: the system's institutional memory and learned playbooks become a durable moat.

---

Each phase transition requires a milestone self-review (`DEFINITION_OF_DONE.md`) — advancing phases is a deliberate, evidenced decision, not a calendar-driven one.
