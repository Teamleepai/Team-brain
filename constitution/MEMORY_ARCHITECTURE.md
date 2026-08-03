# Memory Architecture

Governs the organizational knowledge system. Subordinate to `MASTER_CONSTITUTION.md`.

## Purpose

LEAP OS's value compounds through memory. A system that forgets decisions, repeats mistakes, or fragments knowledge across silos cannot become an operating layer — it stays a chat window. Memory is a first-class subsystem, not a side effect of logging.

## What is remembered

Decisions, meeting outcomes, architecture, customers, projects, commits, bugs, prompt versions, experiments, failures, and lessons learned (master §12). Each category has:

- A canonical schema (what fields every record of that type has).
- A source of truth (which agent/system is authoritative for writes).
- A linking convention (how it references related records).

## Core rules

1. **Never create duplicate knowledge.** Before writing a new record, the Knowledge Manager agent checks for an existing record covering the same entity/decision/event and updates or links it instead of forking a duplicate.
2. **Always link related knowledge.** A decision links to the meeting it came from, the project it affects, and any prior decision it supersedes. Orphan records are a data-quality defect.
3. **Provenance is mandatory.** Every record stores who/what created it (human or agent), when, and from what source (transcript, commit, email, manual entry).
4. **Supersession over deletion.** When a decision or fact changes, the old record is marked superseded and linked forward — it is not deleted, preserving the audit trail (see `SECURITY_STANDARDS.md` on audit logging).

## Structural layers

- **Episodic layer**: raw events (meeting transcripts, commits, calls, messages) — high volume, short-to-medium retention per data policy.
- **Semantic layer**: distilled facts, decisions, and entities extracted from episodic events — long retention, deduplicated, linked.
- **Procedural layer**: prompt versions, playbooks, and learned automation rules — versioned, tested before promotion (see `CONTINUOUS_IMPROVEMENT.md`).

## Query and retrieval

Retrieval must be explainable: any recommendation citing "memory" must be able to show the specific record(s) it drew from. Silent, unexplainable retrieval is a violation of the transparency principle in `PRODUCT_PHILOSOPHY.md`.

## Data lifecycle

Retention, deletion, and export policies are defined per category at schema-design time, not retrofitted, to support compliance requirements in `SECURITY_STANDARDS.md`.
