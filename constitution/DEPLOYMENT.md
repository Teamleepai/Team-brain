# Deployment Strategy

Governs how changes reach production. Subordinate to `MASTER_CONSTITUTION.md`.

## Principles

- Every deployment is a high-impact action for customer-facing prompt/behavior changes (master §11) and requires the configured approval workflow.
- Deployments are incremental and reversible by default: feature-flagged or canaried, never a single all-at-once cutover for anything with customer or financial impact.
- No deployment ships without: passing test suite (`TESTING_STANDARDS.md`), a rollback plan, and an observability signal that would detect a regression within minutes, not days.

## Environments

- **Local/dev** — fast iteration, synthetic or anonymized data only.
- **Staging** — production-like, used for integration/E2E tests and simulation of agent autonomy upgrades.
- **Production** — canary → partial rollout → full rollout, gated by health metrics at each stage.

## Prompt and agent deployments specifically

Prompt changes and agent trust-level advancements follow the same rigor as code deployments: versioned, regression-tested against an evaluation set (`TESTING_STANDARDS.md`), and rolled out incrementally with the ability to instantly revert to the prior prompt version if metrics regress.

## Rollback

Every deployment's rollback path is defined before rollout, not improvised after an incident: what triggers a rollback, who/what can execute it, and how fast it can happen. Automated rollback triggers are preferred over manual ones wherever the trigger condition is unambiguous (e.g. error rate threshold breach).

## Change record

Every production deployment is logged as a knowledge-system record (`MEMORY_ARCHITECTURE.md`): what changed, why, who approved it, and its observed impact — feeding the Continuous Learning Engine (`CONTINUOUS_IMPROVEMENT.md`).
