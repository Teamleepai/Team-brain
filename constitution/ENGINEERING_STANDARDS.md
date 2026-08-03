# Engineering Standards

Governs system architecture. Subordinate to `MASTER_CONSTITUTION.md`.

## Modularity requirements

- Every service, module, or agent exposes a documented interface (API contract, schema, or protocol) — no reaching into another module's internals.
- Every component must be independently replaceable: swapping an implementation behind an interface should require zero changes to callers.
- Single responsibility per service. If describing a service needs "and," it's two services.
- Dependencies flow in one direction; circular dependencies between services are a build-blocking error, not a lint warning.

## Planning artifacts required before implementation

For any feature beyond a trivial bugfix, the following exist and are reviewed before code is written (full detail in `DEFINITION_OF_DONE.md`):

- PRD (goals, success metrics, personas)
- Architecture document (components, data flow, interfaces)
- Threat model and privacy model
- Permission model (which trust level, which roles)
- Data model / domain model
- API contract
- Failure mode analysis
- Rollback strategy

## Scale assumptions

Design for a future of millions of users even while building for the first ten. Concretely:

- No in-memory-only state that can't be reconstructed or sharded.
- No hardcoded single-tenant assumptions in multi-tenant-capable services.
- Rate limits, backpressure, and pagination are part of the initial design, not a v2 add-on.

## Coupling and dependency hygiene

- No hidden dependencies: if service A needs service B, that dependency is declared in the architecture doc and the API contract, not discovered at runtime.
- Prefer composition over inheritance; prefer explicit configuration over convention-based magic.
- Third-party dependencies require a one-line justification (what does it buy us that we couldn't build simply ourselves) recorded in the architecture doc.

## Review cadence

Architecture is revisited at every milestone (see `MASTER_CONSTITUTION.md` §19, Self-Review) — specifically checking for accidental coupling introduced since the last review, and for services whose responsibility has silently grown.
