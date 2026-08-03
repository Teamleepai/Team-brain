# Phase 1 — Chief of Staff MVP

**Status:** Planning complete, awaiting critical review. **No implementation has begun**, per `MASTER_CONSTITUTION.md` §6.

One agent observes Gmail, Google Calendar, voice call transcripts, and Slack, builds structured organizational memory, and delivers one email each weekday morning saying what matters today, what is waiting, and what was committed but not done. It recommends. It does not act.

Trust Levels 0–1 (`MASTER_CONSTITUTION.md` §10). One user, one tenant, tenant-scoped schema.

---

## Reading order

If you read three documents, read the first three.

| # | Document | What it answers |
|---|---|---|
| 1 | [`PRD.md`](PRD.md) | What we are building, for whom, why, and how we will know it worked |
| 2 | [`ARCHITECTURE.md`](ARCHITECTURE.md) | How it is structured, and where authority lives |
| 3 | [`DOMAIN_MODEL.md`](DOMAIN_MODEL.md) | The concepts and their invariants, before any SQL |
| 4 | [`DATA_MODEL.md`](DATA_MODEL.md) | The schema, its constraints, and retention |
| 5 | [`API_CONTRACTS.md`](API_CONTRACTS.md) | Every module interface |
| 6 | [`WORKFLOWS.md`](WORKFLOWS.md) | End-to-end flows, including failure paths |
| 7 | [`PERMISSION_MODEL.md`](PERMISSION_MODEL.md) | Roles, agent scoping, and the gate truth table |
| 8 | [`THREAT_MODEL.md`](THREAT_MODEL.md) | What can go wrong adversarially |
| 9 | [`PRIVACY_MODEL.md`](PRIVACY_MODEL.md) | Personal data, lawful basis, subject rights |
| 10 | [`FAILURE_MODES.md`](FAILURE_MODES.md) | What breaks, how we detect it, what the founder sees |
| 11 | [`TESTING_STRATEGY.md`](TESTING_STRATEGY.md) | How each guarantee is proven |
| 12 | [`OBSERVABILITY_STRATEGY.md`](OBSERVABILITY_STRATEGY.md) | Logs, metrics, traces, alerts |
| 13 | [`DEPLOYMENT_STRATEGY.md`](DEPLOYMENT_STRATEGY.md) | How changes reach production |
| 14 | [`ROLLBACK_STRATEGY.md`](ROLLBACK_STRATEGY.md) | How we get back |
| 15 | [`RISK_REGISTER.md`](RISK_REGISTER.md) | Known risks with owners |
| 16 | [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md) | The checklist that closes the phase |

Decisions are in [`../decisions/`](../decisions/). `ADR-0003` and `ADR-0006` are the two worth reading in full: the first establishes the authority boundary the architecture is built on, the second records a scope disagreement and its resolution.

## A note on the state of these documents

They have been through one adversarial cross-review pass, and it found real defects rather than typos. Two were schema bugs that would have failed at runtime: a unique constraint on `dedupe_key` that would have rejected the first supersession, and a check constraint that made it impossible to invalidate a hallucinated fact with no replacement. Others were contradictions between documents — an append-only audit table that also had to permit PII redaction, an episodic deletion rule that would have violated the no-orphans invariant, a trust level typed as a compile-time constant in a system promising instant revocation, and a gate specified as pure in one document and asynchronous in another. All are fixed, and the fixes are visible in the affected documents rather than quietly applied.

This is what the review gate in `MASTER_CONSTITUTION.md` §6 is for, and it is the argument for the gate: every one of those defects was cheap to fix on paper and would have been a migration, an incident, or a false guarantee if found later.

## The one idea to hold onto

> **The model decides what to propose. Deterministic code decides what is permitted.**

Every constitutional guarantee — trust levels, tool scoping, approval gates, audit completeness — lives in plain TypeScript that the agent runs inside of and cannot reach around. An agent's output is a *proposal*, never an effect. There is exactly one code path from proposal to effect, it is deterministic, and it is the same function that writes the audit record, so an unlogged effect is not expressible.

This resolves what looks at first like a contradiction between `PRODUCT_PHILOSOPHY.md` §7 (deterministic behavior over hidden magic) and using a generative model at all. The constitution asks for predictable *authority*, not identical tokens. See `ADR-0003`.

## Delivery increments

Per `ADR-0006`, sequential rather than simultaneous, so a briefing-quality regression is attributable to a source rather than guessed at.

| Increment | Source | Blocked on |
|---|---|---|
| **1a** | Gmail + Google Calendar | Nothing (subject to increment ordering, below) |
| **1b** | Voice call transcripts | Transcript provider decision |
| **1c** | Slack | Channel scope decision |

## Open questions for the founder

Answers to 1 and 2 change what gets built first. The rest can be answered as their increment approaches.

| # | Question | Blocks |
|---|---|---|
| 1 | **Should voice transcripts (1b) come before Google Workspace (1a)?** The constitution devotes a full section to voice intelligence and no comparable detail to email, which reads as a signal that call intelligence is closer to the commercial core. If so, the differentiated capability should be validated first. Architecture is indifferent; only the order changes. | Increment ordering |
| 2 | Which voice transcript provider? ASR quality, speaker attribution, and available metadata vary enormously between them, and those differences propagate into every downstream summary. | 1b beyond a sketch |
| 3 | Briefing delivery time and timezone. It must land before the first meeting; a briefing that arrives at 11am is worthless. | 1a scheduling |
| 4 | Transactional email provider. I will choose unless you have a preference. | 1a delivery |
| 5 | Which Slack channels are in scope? Default is none, opted in explicitly. | 1c |
| 6 | Is there an existing CRM worth knowing about for Phase 3 sequencing? | Nothing in Phase 1 |

## What Phase 1 is deliberately not

No chat interface. No drafting. No actions of any kind. No dashboard. No multi-user. No self-improvement loop yet, though everything is instrumented so Phase 3 can close it.

Each of these is a plausible next step that would compromise the phase. The full reasoning is in `PRD.md` §3.

## Before implementation begins

`MASTER_CONSTITUTION.md` §6 requires these documents to be critically reviewed, not merely written. `DEFINITION_OF_DONE.md` §1 is the gate. Drafted is not reviewed, and a plan that was never challenged will be challenged by production instead.
