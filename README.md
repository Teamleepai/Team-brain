# Team-brain

Working repository for **LEAP OS** — an AI-native operating system that acts as an executive Chief of Staff for founders and leadership teams. It observes work, organizes knowledge, identifies opportunities, recommends actions, and earns the autonomy to execute them.

No implementation has begun. Phase 1 is in planning, per `MASTER_CONSTITUTION.md` §6.

## Repository layout

| Directory | Contents |
|---|---|
| [`constitution/`](constitution/) | The standards. How LEAP OS is designed, built, secured, and shipped. Changes rarely. |
| [`docs/decisions/`](docs/decisions/) | Architecture Decision Records — every major choice, its alternatives, and its costs. |
| [`docs/phase-1/`](docs/phase-1/) | Planning artifacts for the Chief of Staff MVP. |

## Start here

**Understanding the project:** [`constitution/MASTER_CONSTITUTION.md`](constitution/MASTER_CONSTITUTION.md) — the founding directive, linking out to all fourteen standards documents.

**Understanding what is being built first:** [`docs/phase-1/README.md`](docs/phase-1/README.md) — the Chief of Staff MVP, its scope, its increments, and the open questions.

**Understanding why it is built this way:** [`docs/decisions/`](docs/decisions/) — start with `ADR-0003` (the authority boundary the whole architecture rests on) and `ADR-0006` (a recorded scope disagreement and its resolution).

## Current state

| | |
|---|---|
| **Phase** | 1 — Chief of Staff MVP |
| **Trust levels** | 0–1: observe and recommend only. No execution, no drafts. |
| **Stack** | TypeScript on Node, Postgres on Supabase, Claude Agent SDK |
| **Sources** | Gmail, Google Calendar, voice transcripts, Slack — three sequential increments |
| **Surface** | One email each weekday morning |
| **Status** | Planning artifacts drafted, awaiting critical review. Implementation gated on that review. |

## The idea the architecture rests on

> **The model decides what to propose. Deterministic code decides what is permitted.**

Trust levels, tool scoping, approval gates, and audit completeness live in plain TypeScript that agents run inside of and cannot reach around. An agent produces a *proposal*, never an effect. One deterministic code path leads from proposal to effect, and it is the same function that writes the audit record — so an unlogged action is not something the system can express.
