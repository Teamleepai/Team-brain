# Phase 1 — Definition of Done

**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

The Phase-1-specific instantiation of `constitution/DEFINITION_OF_DONE.md`. That document defines the general gates; this one says exactly what satisfies them here, and is the checklist the milestone self-review runs against.

---

## 1. Planning artifacts

`MASTER_CONSTITUTION.md` §6 forbids production code until these exist and have been critically reviewed. Status as of this document's date:

| Artifact | File | Status |
|---|---|---|
| PRD — goals, metrics, personas | `PRD.md` | Drafted, awaiting review |
| Architecture document | `ARCHITECTURE.md` | Drafted, awaiting review |
| Threat model | `THREAT_MODEL.md` | Drafted, awaiting review |
| Privacy model | `PRIVACY_MODEL.md` | Drafted, awaiting review |
| Permission model | `PERMISSION_MODEL.md` | Drafted, awaiting review |
| Data model | `DATA_MODEL.md` | Drafted, awaiting review |
| Domain model | `DOMAIN_MODEL.md` | Drafted, awaiting review |
| API contracts | `API_CONTRACTS.md` | Drafted, awaiting review |
| Workflow diagrams | `WORKFLOWS.md` | Drafted, awaiting review |
| Memory architecture impact | `DATA_MODEL.md` §§6–8, `DOMAIN_MODEL.md` | Drafted |
| Agent architecture impact | `ARCHITECTURE.md` §5, `API_CONTRACTS.md` §5 | Drafted |
| Testing strategy | `TESTING_STRATEGY.md` | Drafted, awaiting review |
| Deployment strategy | `DEPLOYMENT_STRATEGY.md` | Drafted, awaiting review |
| Observability strategy | `OBSERVABILITY_STRATEGY.md` | Drafted, awaiting review |
| Rollback strategy | `ROLLBACK_STRATEGY.md` | Drafted, awaiting review |
| Failure mode analysis | `FAILURE_MODES.md` | Drafted, awaiting review |
| Risk register | `RISK_REGISTER.md` | Drafted, awaiting review |
| Architectural decisions | `../decisions/ADR-0001` … `ADR-0007` | Accepted |
| Definition of done | this file | Drafted |

**Gate:** every row reads reviewed, and the six open questions in `PRD.md` §10 are answered or explicitly deferred with a recorded reason. Implementation does not begin before this gate. Drafted is not reviewed, and the distinction is the entire point of §6 — a plan written and never challenged is a plan that will be challenged by production instead.

## 2. Per-increment completeness

Each increment from `ADR-0006` ships independently and must satisfy all of the following before the next begins.

### Code and structure

- [ ] Meets `CODING_STANDARDS.md`: no placeholder implementations, no dead code, public interfaces documented, functions small and modules single-responsibility.
- [ ] Every module matches the interface in `API_CONTRACTS.md`. A divergence updates that document in the same change.
- [ ] No SQL outside `memory/repositories` (`ADR-0002`).
- [ ] No circular dependencies between modules (build-blocking, per `ENGINEERING_STANDARDS.md`).
- [ ] No secrets, credentials, or PII anywhere in the diff or in commit history.

### Tests

Per `TESTING_STRATEGY.md`, which specifies the mechanics. The gates here are the ones whose absence would let a constitutional guarantee ship unproven:

- [ ] Unit, integration, and end-to-end tests present and passing.
- [ ] **Trust gate truth table covered exhaustively** — every impact class against every trust level.
- [ ] **Gate refusal proven with a deliberately misbehaving agent** configured to attempt an action above its level. A gate exercised only by well-behaved agents has not been tested.
- [ ] **Two-permission-system seam tested** — the gate holds on a path where the SDK itself would have permitted the action.
- [ ] **RLS adversarial suite passing** — cross-tenant reads attempted against a synthetic second organization and failing. RLS fails permissively and silently, so a policy exercised by one tenant has never been tested.
- [ ] **Prompt injection tests passing** — instruction-shaped text in ingested content leaves agent behavior unchanged, and any escalation attempt produces a gate refusal.
- [ ] Idempotency proven: overlapping ingestion windows create no duplicates; briefing generation is idempotent per `(org, recipient, date)`.
- [ ] Invariant tests: no orphan semantic records, supersession completeness, `dedupe_key` behavior.
- [ ] Failure injection: 429, 5xx, malformed payloads, and auth failure from each source, with the watermark never advancing past unprocessed data.
- [ ] Performance baselines recorded with regression thresholds.

### Security and privacy

- [ ] Security review completed (`SECURITY_STANDARDS.md`), mandatory because every increment touches customer data and credentials.
- [ ] Threat model updated for anything the increment introduces.
- [ ] Secret scanning passing in CI.
- [ ] Log and trace redaction verified by test: known-sensitive field names never appear in emitted output.
- [ ] Retention and deletion policy implemented for every new table, not merely documented (`DATA_MODEL.md` §12).

### Operations

- [ ] Documentation updated in the same change, never deferred.
- [ ] Structured log events, metrics, and traces in place per `OBSERVABILITY_STRATEGY.md`.
- [ ] Alerts configured for the increment's new failure modes, and each alert is actionable. Alert fatigue undermines the trust framework, so a non-actionable alert is a defect.
- [ ] Rollback path documented and, where the trigger is unambiguous, automated (`ROLLBACK_STRATEGY.md`).
- [ ] **Live-credential validation completed.** Fixture-passing tests do not satisfy this. Fixtures lie about pagination, rate limits, and auth edge cases, which is precisely where adapters break.

### Trust

- [ ] The agent's declared trust level is recorded in its contract and justified.
- [ ] No increment raises a trust level. Phase 1 stays at 0–1 throughout; a trust-level change is a separate approval event (`PERMISSION_MODEL.md`).

### Per-increment quality gate

Each increment's briefing contribution is reviewed for attributable quality before the next increment begins — the mechanism `ADR-0006` relies on to keep regressions diagnosable by source. Concretely: at least five consecutive briefings including the new source, with any misleading item traced to its originating adapter.

## 3. Phase exit criteria

With all three increments live, from `PRD.md` §9:

1. [ ] Fourteen consecutive weekdays of briefings delivered and opened, no gap greater than one day.
2. [ ] **Zero misleading recommendations flagged in that window.** Failing this resets the window, which is intentional.
3. [ ] Novel-priority rate at or above one item per briefing on average.
4. [ ] Self-reported time saved at or above twenty minutes per day.
5. [ ] Briefing open rate at or above 90% within three hours of delivery.
6. [ ] All Section 2 checklists satisfied for every increment.
7. [ ] Milestone self-review completed (Section 4).
8. [ ] No unresolved critical items in `RISK_REGISTER.md`.

Criterion 2 is the one that matters. The others measure whether the product is used; that one measures whether it deserves to be.

## 4. Milestone self-review

`MASTER_CONSTITUTION.md` §19 requires review across eleven dimensions before a milestone is declared complete. Findings are recorded even when they do not block this milestone, because the ones that do not block Phase 1 are the ones that shape Phase 2.

| Dimension | The Phase 1 question worth actually asking |
|---|---|
| Architecture | Has the authority layer been eroded anywhere? Any agent holding a tool it should not, any proposal reaching an effect without a declared impact class? |
| Security | Has anything reduced the blast radius of a compromised credential, or only assumed it? |
| Scalability | Which assumption breaks first at 100× the episodic volume, and do we know the answer or are we guessing? |
| Maintainability | Could someone else implement Phase 2 from these documents without asking me questions? |
| Performance | Do baselines exist with thresholds, or only numbers nobody compares against? |
| Usability | Is the briefing actually read in under two minutes on a phone, observed rather than assumed? |
| Business impact | Did cross-source synthesis surface priorities the founder would not have reached alone? If not, the product thesis needs revisiting before Phase 2. |
| AI safety | Every gate refusal in the window reviewed: bug, injection attempt, or model error? |
| Cost | Cost per briefing, and its trajectory as memory grows. |
| Observability | Can every briefing item be traced to its agent, records, and trust level on demand? |
| Documentation | Does every document still describe what was built, or has the code drifted? |

## 5. What explicitly does not count as done

Worth stating, because each is a plausible way to declare victory early:

- **Adapters passing fixture tests.** Fixtures are a development convenience, not evidence.
- **A briefing that renders.** Rendering is not the deliverable; a correct, prioritized, trusted briefing is.
- **Zero errors because the founder stopped reading.** Criterion 2 is meaningless without criterion 5. Both are required, and they are required together for exactly this reason.
- **The gate never refusing anything.** That is consistent with a working gate and equally consistent with a gate that is never consulted. Only the deliberately-misbehaving-agent test distinguishes them.
- **Documentation written after implementation.** `MASTER_CONSTITUTION.md` §6 makes plans a precondition, not a deliverable. A plan reverse-engineered from code is a description, not a design.
