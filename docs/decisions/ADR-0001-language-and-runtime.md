# ADR-0001 — TypeScript on Node as the primary language and runtime

**Date:** 2026-08-03

## Status

Accepted.

## Context

LEAP OS needs one primary language, chosen once, early, and deliberately. This is among the least reversible decisions in the project: it constrains hiring, library availability, the shape of every interface, and how much friction stands between a design document and working code.

Three constitutional requirements bear directly on the choice:

- `ENGINEERING_STANDARDS.md` requires that every component expose a documented interface and be independently replaceable, with no reaching into another module's internals. A language whose type system can *enforce* that boundary is worth more here than one where the boundary is a convention maintained by discipline.
- `CODING_STANDARDS.md` requires explicit over implicit, and no reliance on subtle language behavior or implicit type coercion.
- The Phase 1 through Phase 3 workload, per `ROADMAP.md`, is overwhelmingly integration and orchestration: Google Workspace, Slack, CRM systems, transcript sources, email delivery. It is not model training.

That last point is the crux. It is tempting to select a language on the strength of its machine-learning ecosystem, because "AI operating system" sounds like a machine-learning project. It is not one, at least not for years. LEAP OS *consumes* hosted frontier models through an API; it does not train, fine-tune, or serve them. The engineering bottleneck for the entire visible roadmap is talking reliably to a dozen SaaS APIs, modeling organizational memory, and enforcing a permission system — none of which benefit from NumPy.

## Decision

**TypeScript in strict mode, running on the current Node LTS**, as the single primary language across the backend, the agent orchestration layer, and the eventual executive dashboard.

Specifically:

- `strict: true` with `noUncheckedIndexedAccess` and `exactOptionalPropertyTypes` enabled. A type system used loosely provides documentation without enforcement, which is the worst of both worlds.
- Runtime validation at every trust boundary (external API responses, ingested content, environment configuration) using a schema library, because TypeScript types vanish at runtime and every one of those boundaries is untrusted per `SECURITY_STANDARDS.md`.
- Shared type definitions between the backend and any future frontend, so an API contract change breaks the build rather than production.

## Alternatives considered

**Python with FastAPI.** The strongest option on paper for anything ML-adjacent, and genuinely better if voice and transcript processing become original research rather than API consumption. Rejected because it optimizes for a workload we do not have: our voice intelligence (`MASTER_CONSTITUTION.md` §13) is transcript analysis performed by a frontier model, not a model we build. Against that, Python gives up compile-time enforcement of the module boundaries the engineering standards are built around, and leaves a language seam between the backend and the Phase 2 dashboard. Reconsidered if and when we own a model.

**Python core with a TypeScript frontend.** Best-tool-per-job, and a very common shape. Rejected because it places a serialization boundary at precisely the seam where we least want one: between the agent layer that produces recommendations and the surface that renders them with trust levels, evidence links, and approval affordances. That boundary is where `UX_PRINCIPLES.md` demands the most fidelity — every recommendation must carry its trust level and its provenance intact. Two toolchains, two dependency stories, and two deployment pipelines is a real tax to pay for a Phase 1 with one user, and the tax is paid every day thereafter.

**Go.** Excellent for the eventual high-throughput ingestion path, and the best of these options for operational simplicity. Rejected for Phase 1: the integration ecosystem for the specific SaaS products we need is thinner, the Claude Agent SDK is not a first-class citizen, and the iteration speed penalty during a phase whose entire purpose is learning what the product should be is the wrong trade.

## Tradeoffs

We are accepting a genuinely weaker data and ML toolchain. If Phase 3's voice intelligence work turns into real model evaluation at volume — scoring thousands of calls against a rubric, statistical analysis of prompt regressions — we will feel the absence of the Python data stack, and we will be writing analysis code that would have been shorter elsewhere.

We are also accepting Node's operational characteristics: a single-threaded event loop that punishes accidental CPU-bound work, and a dependency ecosystem with a wide supply-chain surface. The first is a design constraint to respect; the second requires the dependency justification rule from `ENGINEERING_STANDARDS.md` to be enforced rather than nodded at.

## Future implications

Easier: every SaaS integration in the roadmap, the Claude Agent SDK and MCP connector ecosystem, end-to-end type safety from database row to rendered briefing, and a single CI pipeline.

Harder: heavy numerical or statistical work, and anything requiring true parallel CPU throughput in-process.

## Migration path

We are not betting the architecture on this. `ENGINEERING_STANDARDS.md` requires every component to sit behind an interface and be independently replaceable, which means a workload that outgrows TypeScript can be extracted into its own service in another language behind a documented API contract without touching its callers. The likely first candidate is transcript or evaluation batch processing, and extracting it is the *sanctioned* path rather than a workaround — it requires a new ADR, not an exception.

Wholesale migration of the core is not a scenario we are planning for; if it ever became necessary, the interface-driven structure means it would proceed service by service rather than as a single rewrite.

## Technical debt

None incurred intentionally.

One standing obligation: any future service written in a second language adds a toolchain, a dependency story, and a deployment pipeline permanently. That cost must be justified in its own ADR against the option of solving the problem in TypeScript, and "the ecosystem is nicer" is not sufficient on its own.
