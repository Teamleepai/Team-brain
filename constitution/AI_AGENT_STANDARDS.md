# AI Agent Standards

Governs the multi-agent architecture. Subordinate to `MASTER_CONSTITUTION.md`.

## Principle: ecosystem, not monolith

LEAP OS is not one large prompt. It is an orchestrated ecosystem of specialized agents, each with a narrow, clearly documented responsibility, coordinated by an orchestration layer (the "Chief of Staff" agent) that routes work, resolves conflicts, and enforces trust-level gating.

## Candidate agents (initial roster — expand deliberately, not by default)

| Agent | Responsibility |
|---|---|
| Chief of Staff | Orchestration, prioritization, routing between agents, daily briefing synthesis |
| Executive Assistant | Scheduling, follow-ups, task tracking |
| Meeting Intelligence | Transcript capture, summarization, action-item extraction |
| Email Intelligence | Triage, drafting, thread summarization |
| Messaging Intelligence | Slack/Teams triage, drafting, sentiment |
| CRM Intelligence | Pipeline hygiene, deal risk signals |
| Sales Coach | Call/deal coaching recommendations |
| Voice QA | Call transcript scoring, structured intelligence (see master §13) |
| Prompt Engineer | Prompt version management, evaluation, regression testing |
| Knowledge Manager | Deduplication, linking, memory hygiene (`MEMORY_ARCHITECTURE.md`) |
| Research Agent | Web/document research synthesis |
| Marketing / Finance / Legal / Operations / Project Manager agents | Domain-specific recommendation and drafting within their function |
| Developer Assistant / Infrastructure Engineer | Engineering-facing automation, CI/CD, infra recommendations |

Adding a new agent requires: a one-paragraph responsibility statement, a list of tools/data it needs (least privilege), its starting trust level, and confirmation that no existing agent's responsibility already covers it.

## Agent contract

Every agent must declare:

1. **Responsibility** — one sentence, single purpose.
2. **Inputs** — what data/events it consumes.
3. **Outputs** — what it produces (recommendation, draft, structured record, executed action).
4. **Trust level** — current level (0–5, see master §10) and the criteria to advance.
5. **Tools/permissions** — explicit least-privilege list.
6. **Escalation path** — what it does when uncertain (default: escalate to a lower trust level action, e.g. recommend instead of execute).

## Orchestration rules

- The orchestration layer (Chief of Staff) is the only agent permitted to route work between other agents; agents do not call each other directly without going through the orchestrator's logged routing.
- Conflicting recommendations from two agents are surfaced to the human, not silently resolved by the orchestrator picking one.
- No agent may act above its declared trust level, even if technically capable of the action.

## Advancing trust levels

An agent advances a trust level only after: a minimum volume of successful, human-verified outcomes at the current level; a documented failure-mode review with no unresolved critical failures; and explicit human sign-off recorded in the Knowledge System. Trust levels can be revoked instantly on regression — advancement is earned continuously, not granted permanently.
