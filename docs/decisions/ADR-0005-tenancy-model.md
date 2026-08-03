# ADR-0005 — Single active tenant, tenant-scoped schema from the first migration

**Date:** 2026-08-03

## Status

Accepted.

## Context

Phase 1 has exactly one user: the founder. Phase 2 adds the leadership team. Phase 4 adds external enterprise customers with isolation guarantees and per-tenant configuration, per `ROADMAP.md`.

Two constitutional requirements pull in opposite directions here, and the decision is about where to land between them.

`ENGINEERING_STANDARDS.md` requires designing for a future of millions of users while building for the first ten, and specifically forbids hardcoded single-tenant assumptions in services that will need to be multi-tenant. `SECURITY_STANDARDS.md` requires role-based access control and least privilege.

Against that, `PRODUCT_PHILOSOPHY.md` forbids premature optimization and adding complexity that is not earned, and `UX_PRINCIPLES.md` implies Phase 1 should be small enough to actually ship and get used for two consecutive weeks.

The resolution turns on a distinction the philosophy document supports but does not spell out: *schema shape* and *feature surface* have very different reversal costs. Adding an onboarding flow later is additive work. Adding a tenant column to a populated schema later is a data migration touching every table, every query, and every RLS policy at the same time as we are adding real multi-user access control.

## Decision

**One active tenant, with tenant scoping present in the schema from the first migration.**

- Every domain table carries an `org_id` from migration one. No exceptions, including tables that appear obviously global.
- Row-Level Security policies enforce `org_id` scoping on every table from the start, per `ADR-0002`. They are written and tested against a second, synthetic organization that exists only in tests — so isolation is *proven* rather than merely *intended* long before a real second tenant exists.
- Every user record belongs to an org and carries a role. Phase 1 has one org with one user in an owner role, which exercises the full path without the full surface.
- The repository layer takes tenant context as a required argument rather than reading it from ambient state. A function that cannot be called without a tenant context cannot forget one.
- **Not built:** onboarding flows, tenant provisioning UI, per-tenant configuration, billing, invitations, cross-tenant admin tooling. These are feature surface and they wait until they are needed.

The shape is multi-tenant. The surface is single-user. That asymmetry is the whole decision.

## Alternatives considered

**Single-user with no tenancy concept at all.** The simplest thing that works for Phase 1, and defensible if the product thesis were more speculative. Rejected because it converts an avoidable future migration into a certain one, and schedules it for the worst possible moment: Phase 2, concurrently with introducing draft execution, approval workflows, and real multi-user access control. Retrofitting tenant isolation into a system that is simultaneously gaining its first real permission boundaries is how cross-tenant data leaks happen. The cost of avoiding this now is roughly one column, one policy template, and one function argument.

**Full multi-tenant from Phase 1 — onboarding, provisioning, per-tenant configuration, isolation guarantees.** Rejected as textbook premature complexity. Every hour spent on tenant provisioning in Phase 1 is an hour not spent finding out whether the daily briefing is worth reading, which is the only question Phase 1 exists to answer. Building customer-facing tenancy before the product thesis is validated on a single user optimizes for a scale we have not earned.

**Multi-user within one org for Phase 1** (the founder plus the leadership team immediately). Genuinely tempting, because it exercises RBAC for real and surfaces hard problems — shared versus private memory, per-user data visibility — early rather than late. Rejected for Phase 1 scope, but this is the *next* increment rather than a rejected direction, and it arrives in Phase 2 by design. The tenant-scoped schema is what makes that arrival cheap.

## Tradeoffs

Every query, every repository method, and every policy carries tenant-scoping discipline from day one, for a system with one tenant. That is real ongoing friction paid against a benefit that does not materialize for months. The mitigation is that the discipline is *structural* rather than remembered: RLS enforces it at the database, and required function arguments enforce it at the call site. Discipline that depends on a developer remembering is discipline that fails; discipline the compiler and the database enforce is free after the first day.

There is also a subtler cost worth naming. Having tenant scoping in place creates a temptation to treat the system as multi-tenant-ready in a stronger sense than it is. It is not: no onboarding, no per-tenant configuration, no tested behavior under concurrent tenant load, no cross-tenant operational tooling. Phase 4 is still real work. What has been bought is the absence of a data migration, not the presence of a multi-tenant product.

## Future implications

Easier: adding the leadership team in Phase 2 is a matter of adding user records and exercising roles that already exist. Adding external customers in Phase 4 requires building provisioning and configuration surfaces, but no schema migration and no rewrite of data access.

Harder: nothing structural. The friction is a constant small tax rather than a growing one.

## Migration path

There is no migration to plan for in the expected direction — that is the point of the decision. In the unexpected direction, if LEAP OS turned out to be a permanently single-tenant internal tool, the `org_id` columns would simply remain unused and cost nothing but a small amount of visual noise. The asymmetry of those two outcomes is what makes this the right call: being wrong in one direction costs a column, being wrong in the other costs a migration during the busiest phase.

## Technical debt

None incurred intentionally.

One risk-register item: **RLS isolation must be verified adversarially against a synthetic second organization before any real second user exists.** A tenant-scoped schema whose policies have only ever been exercised by a single tenant provides the appearance of isolation without evidence of it, and the appearance is more dangerous than the absence, because it stops anyone from checking.
