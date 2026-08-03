# ADR-0002 — Postgres on Supabase as the memory substrate

**Date:** 2026-08-03

## Status

Accepted.

## Context

`MEMORY_ARCHITECTURE.md` is the most demanding document in the constitution from a storage perspective, and its requirements are unusually specific for a v1:

- Three structural layers — episodic (raw events), semantic (distilled facts and entities), procedural (prompt versions, playbooks, learned rules) — with different retention profiles.
- Provenance on every record: who or what created it, when, and from what source.
- Mandatory linking between related records, with orphan records treated as a data-quality defect.
- **Supersession rather than deletion**: when a fact changes, the old record is marked superseded and linked forward, preserving the audit trail.
- Explainable retrieval: any recommendation citing memory must be able to name the specific records it drew from.

Read together, those are the requirements of a relational store with strong referential integrity, not a document store. Supersession chains and mandatory bidirectional links are foreign keys. "Show me the exact records behind this recommendation" is a join.

Layered on top, `SECURITY_STANDARDS.md` requires encryption at rest, least privilege, role-based access control, audit logging of every agent action, and retention and deletion policies designed in from the first schema to support SOC 2 and GDPR-style data subject rights. `ADR-0005` requires tenant scoping in the first migration even though only one tenant will exist for months.

And the semantic layer needs similarity search, because "what do we know that is relevant to this meeting" is not a keyword query.

## Decision

**Postgres, hosted on Supabase**, as the single store backing all three memory layers for Phase 1 and Phase 2.

The specifics that matter:

- **pgvector** for semantic-layer embeddings, so similarity search and relational joins happen in one query against one store. Retrieval that must be explainable is far easier to build when the vector match and the provenance record are in the same transaction.
- **Row-Level Security as the enforcement layer** for tenant isolation and role-based access, not as a supplement to application checks but as the backstop beneath them. Application code will also scope every query; RLS ensures that a bug in application code is a failed query rather than a data leak. This is the defense-in-depth posture `SECURITY_STANDARDS.md` demands from its opening assumption that every system will eventually be attacked.
- **Repository-pattern data access.** No application code issues SQL directly. Every read and write goes through a repository module whose interface is the documented contract, per `ENGINEERING_STANDARDS.md`. This is what keeps the migration path below cheap.
- **Append-only audit and episodic tables.** Supersession is implemented as `superseded_by` pointers and validity timestamps, never as `UPDATE` over history. Audit records have no update path at all.
- Supabase Auth for identity, feeding the role assignments in the permission model.

## Alternatives considered

**Plain Postgres on Neon or RDS.** Genuinely close, and the honest observation is that Supabase's advantage here is convenience rather than capability — the substrate is identical. Rejected for Phase 1 because we would hand-build authentication, RLS policy conventions, and storage handling that arrive working, and there is no offsetting benefit at single-tenant scale. This is the alternative to revisit first if Supabase's platform constraints ever bind: the migration is a dump, a restore, and re-homing auth, because everything we depend on is standard Postgres.

**SQLite for Phase 1.** Zero infrastructure, fastest possible local iteration, and a real argument that Phase 1 has one user and does not need a server. Rejected on two grounds. It directly violates the design-for-scale rule in `ENGINEERING_STANDARDS.md`, which asks us to build for millions while serving ten. More concretely, it trades a small, immediate saving for a certain, larger, later cost: the migration to Postgres would land in Phase 2, exactly when we are also adding multi-user access control and draft execution. Deferring known work into a busier phase is how projects acquire the technical debt `PRODUCT_PHILOSOPHY.md` §2 forbids taking on intentionally.

**A document store (MongoDB, DynamoDB).** Rejected because our data is not document-shaped. The defining operations of the memory system are traversals — this decision superseded that one, this recommendation drew on those four records, this meeting produced these action items belonging to that project. Modeling supersession chains and mandatory link integrity in a store without foreign keys means implementing referential integrity in application code, which is precisely the kind of hidden, un-enforced invariant the engineering standards exist to prevent.

**A dedicated graph database alongside Postgres.** Superficially attractive given how link-centric the memory model is. Rejected as a premature second store: Postgres handles recursive traversal natively via recursive CTEs, and our graph is small and shallow for the foreseeable future. Introducing a second store means two consistency stories, two backup stories, and two failure modes, in exchange for query elegance we do not yet need. Revisit only against a measured performance bottleneck, per the no-premature-optimization rule.

**A dedicated vector database (Pinecone, Weaviate) for the semantic layer.** Rejected for the same reason. Splitting embeddings from their provenance records across two stores makes explainable retrieval — a hard constitutional requirement — meaningfully harder, because the vector match and the record it points at would no longer be joinable in one query. pgvector is sufficient at our scale, and consolidation is worth more than peak vector performance here.

## Tradeoffs

We accept a platform dependency on Supabase, including its availability, its pricing evolution, and its pace of Postgres version support. This is a real dependency and should be named as one rather than waved away.

We accept that Row-Level Security is powerful and easy to get subtly wrong. An RLS policy that is too permissive fails silently and looks exactly like a working system. This is the single most dangerous surface in the persistence design and it is treated as such in the testing strategy: RLS policies get their own adversarial test suite that attempts cross-tenant reads, not merely a check that legitimate reads succeed.

We accept that one store serving three memory layers with different access patterns will eventually strain. Episodic data is high-volume, append-heavy, and short-lived; procedural data is tiny, low-write, and permanent. Serving both from one Postgres instance is correct now and will not be correct forever.

## Future implications

Easier: transactional consistency across all three memory layers, explainable retrieval, referential integrity for links and supersession, tenant isolation via RLS, and a single operational surface to monitor and back up.

Harder: independently scaling the episodic layer's write throughput, and any future desire to run genuinely heavy analytical queries over historical events without affecting live traffic. Both have conventional answers — partitioning and archival for the former, a read replica or warehouse for the latter — and neither requires changing this decision.

## Migration path

Two migrations are worth pre-considering.

*Off Supabase, onto plain Postgres:* a dump and restore, plus re-implementing Supabase Auth's role assignment against another identity provider and porting RLS policies (which are standard Postgres and move as-is). Bounded work, measured in days rather than months, precisely because we are not using proprietary extensions.

*Splitting a layer out:* the repository pattern is what makes this cheap. Because no application code issues SQL, moving the episodic layer to a store better suited to high-volume append-only data means reimplementing one repository module against a new backend while its interface — and therefore every caller — stays unchanged. This is the modularity rule paying for itself.

## Technical debt

None incurred intentionally, but two items belong in the risk register with owners:

1. **RLS policy correctness** is security-critical and not self-evidently correct by reading it. Requires a dedicated adversarial test suite before any second user exists, and re-verification whenever a table is added.
2. **Retention and deletion policies** must be defined per memory category at schema-design time rather than retrofitted, per `MEMORY_ARCHITECTURE.md`. Writing the schema without them is the tempting shortcut here, and it is the one that turns into a compliance problem rather than a code problem.
