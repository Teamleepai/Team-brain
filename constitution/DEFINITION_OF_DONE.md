# Definition of Done

Governs when work is actually finished. Subordinate to `MASTER_CONSTITUTION.md`.

## Planning artifacts (required before implementation begins)

For any non-trivial feature:

- [ ] PRD: business goals, success metrics, user personas
- [ ] Architecture document
- [ ] Threat model
- [ ] Privacy model
- [ ] Permission model (trust level, roles)
- [ ] Data model / domain model
- [ ] API contracts
- [ ] Workflow diagrams
- [ ] Memory architecture impact (if applicable)
- [ ] Agent architecture impact (if applicable)
- [ ] Testing strategy
- [ ] Deployment strategy
- [ ] Observability strategy
- [ ] Rollback strategy
- [ ] Failure mode analysis
- [ ] Risk register entry
- [ ] Definition of done for this specific feature (below)

These are reviewed critically (see master §19, Self-Review) before implementation starts — not written retroactively to justify a decision already made.

## Implementation completeness checklist

- [ ] Code meets `CODING_STANDARDS.md`
- [ ] Unit, integration, E2E, performance, and failure tests exist and pass (`TESTING_STANDARDS.md`)
- [ ] Security review completed for anything touching data, credentials, or external communication (`SECURITY_STANDARDS.md`)
- [ ] Documentation updated in the same change
- [ ] Monitoring/alerting in place for new failure modes (`OBSERVABILITY.md`)
- [ ] Rollback plan documented and, where feasible, automated (`DEPLOYMENT.md`)
- [ ] Trust level assigned and justified if this introduces or changes agent autonomy (`AI_AGENT_STANDARDS.md`)
- [ ] No unresolved items in the risk register that block this specific release

## Risk register

A living log of known risks, each with: description, likelihood, impact, mitigation, owner, and status. Every intentional shortcut or deferred hardening measure from `PRODUCT_PHILOSOPHY.md` §2 lives here with a removal date — nothing is "known and forgotten."

## Milestone self-review gate

Before any milestone is declared complete, run the full self-review from master §19 (architecture, security, scalability, maintainability, performance, usability, business impact, AI safety, cost, observability, documentation) and record findings — even ones that don't block this milestone but should inform the next.
