# Architecture Decision Records

`MASTER_CONSTITUTION.md` §3 requires a written justification for every architectural decision, and §17 specifies what that justification must contain. This directory holds those records.

An ADR is written **before** implementation, reviewed critically, and then treated as immutable history. When a decision changes, write a new ADR that supersedes the old one — do not edit the original. This mirrors the supersession-over-deletion rule in `MEMORY_ARCHITECTURE.md`: the reasoning trail is the asset, and a decision quietly rewritten is a decision that will be re-litigated for free later.

## Index

| ADR | Decision | Status |
|---|---|---|
| [0001](ADR-0001-language-and-runtime.md) | TypeScript on Node as the primary language and runtime | Accepted |
| [0002](ADR-0002-persistence.md) | Postgres on Supabase as the memory substrate | Accepted |
| [0003](ADR-0003-agent-runtime.md) | Claude Agent SDK as the agent execution substrate | Accepted |
| [0004](ADR-0004-briefing-delivery-surface.md) | Email as the Phase 1 briefing delivery surface | Accepted |
| [0005](ADR-0005-tenancy-model.md) | Single active tenant, tenant-scoped schema from the first migration | Accepted |
| [0006](ADR-0006-phase-1-data-sources.md) | Three Phase 1 data sources, delivered as three sequential increments | Accepted, one open question |

## Required sections

Every ADR carries exactly these headings, taken from `MASTER_CONSTITUTION.md` §17:

- **Status** — Proposed, Accepted, Superseded by ADR-NNNN, or Rejected
- **Context** — the forces at play, including which constitutional requirements constrain the choice
- **Decision** — what was chosen, stated plainly enough to implement against
- **Alternatives considered** — each option that was genuinely weighed, and why it lost. An ADR with no rejected alternatives is a record of a decision that was never actually made.
- **Tradeoffs** — what this costs us, stated honestly. If a decision has no downside, the analysis is incomplete.
- **Future implications** — what this makes easier and harder later
- **Migration path** — how we would get off this choice if it proves wrong, and roughly what that costs
- **Technical debt** — what shortcuts, if any, this incurs. Anything logged here must also appear in the risk register with an owner and a removal date, per `PRODUCT_PHILOSOPHY.md` §2.
