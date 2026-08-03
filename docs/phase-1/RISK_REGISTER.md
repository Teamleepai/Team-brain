# Phase 1 — Risk Register

**Date:** 2026-08-03
**Status:** Living document. Reviewed at every increment gate and at the milestone self-review.

`constitution/DEFINITION_OF_DONE.md` requires a living log of known risks with description, likelihood, impact, mitigation, owner, and status. `PRODUCT_PHILOSOPHY.md` §2 requires that every intentional shortcut or deferred hardening measure appear here with an owner and a removal date, so that nothing is known and forgotten.

Owners are **Founder** (business or product judgment) or **Implementation** (engineering, whoever holds the work). Removal dates are expressed as gates rather than calendar dates, because a date on a project with one contributor is a guess and a gate is a commitment.

---

## How to read severity

Severity here is graded by **damage to trust**, not by blast radius. That is deliberate and it is the correct frame for Phase 1. A cross-tenant data leak in a system with one tenant has near-zero blast radius and would still be catastrophic, because it would prove the isolation model was never real. Conversely an outage that the founder never notices costs almost nothing.

| Severity | Meaning |
|---|---|
| **Critical** | Would end or reset the phase, or prove a constitutional guarantee was never real |
| **High** | Would materially damage founder trust or require rework of something already built |
| **Medium** | Would degrade quality or cost real time, recoverable |
| **Low** | Annoyance, or a cost we accept knowingly |

---

## 1. Critical

| # | Risk | Likelihood | Mitigation | Owner | Closes at |
|---|---|---|---|---|---|
| R1 | **Authority layer erodes under delivery pressure.** Not a designed compromise but a small convenience: an agent given a tool "just for this", a proposal executed without a declared impact class, a gate bypassed in a hurry. Invisible in a demo and fatal to the trust framework, because every later phase's safety rests on this layer holding. | **High** — this is the single most likely serious failure, because the erosion is always locally reasonable | Gate fails closed on malformed proposals; refusals alert; the `rogue-cos` deliberately-misbehaving-agent suite proves refusal rather than proving good behavior; `TrustGate` and `AgentContract` treated as security-change surfaces requiring approval under `MASTER_CONSTITUTION.md` §11 | Implementation | Never closes. Re-verified at every increment gate and every milestone self-review. |
| R2 | **RLS policy misconfiguration.** A too-permissive policy fails *silently and permissively* and looks exactly like a working system. Nothing surfaces the defect, because legitimate reads keep working. | Medium | Two-org adversarial test matrix attempting cross-tenant reads; a metatest proving the adversarial suite would catch a deliberately broken policy; a build failure for any table added without an RLS policy | Implementation | Adversarial suite green before any second user exists (`ADR-0005`) |
| R3 | **Confidently wrong recommendation.** A briefing item that is fluent, specific, and false. Costs disproportionate trust because the founder cannot distinguish it from a correct one without checking, and checking is the cognitive load the product exists to remove. | Medium | Low-confidence facts excluded rather than hedged (`PRD.md` A3); every item cites evidence so verification is one click; the error-flag affordance; zero-misleading-items exit criterion that resets its own window on failure | Implementation | Phase exit criterion 2 satisfied |
| R4 | **Founder stops reading.** The failure that makes every other metric meaningless. A clean error record achieved because nobody looked is not a clean error record. | Medium | Open-rate and sustained-use metrics required *alongside* the error metric, never instead of it (`DEFINITION_OF_DONE.md` §5); item-count monitoring against firehose drift; two-minute readability target | Founder + Implementation | Phase exit criteria 1 and 5 satisfied together |

---

## 2. High

| # | Risk | Likelihood | Mitigation | Owner | Closes at |
|---|---|---|---|---|---|
| R5 | **Fixture-validated adapters.** No live credentials exist. All four adapters will be built against fixtures behind real interfaces, and fixtures lie about exactly what breaks adapters: pagination, rate limits, token expiry, malformed payloads, partial pages. Accepted technical debt, recorded per `PRODUCT_PHILOSOPHY.md` §2. | **High** — near-certain that something differs from fixtures | Live-credential validation is part of every increment's exit gate, explicitly not satisfied by fixture-passing tests (`DEFINITION_OF_DONE.md` §2) | Founder (credentials), Implementation (validation) | Each increment's live-credential gate |
| R6 | **A source silently stops ingesting.** Token revoked, OAuth scope changed, API deprecation. The briefing keeps arriving and is quietly incomplete. A correctness problem wearing an availability problem's clothes, and the most insidious item on this list because the product still *looks* healthy. | **High** over a long enough window | `consecutive_failures` on the watermark drives alerting; the briefing states the gap rather than silently omitting the source | Implementation | Alerting verified per increment |
| R7 | **`dedupe_key` derivation is unspecified.** The most consequential unresolved detail in the schema. Too strict and memory fills with near-duplicates; too loose and distinct facts collapse into one. Both degrade the briefing, and the second silently loses information. | **High** — it is currently undefined | Needs a written specification and its own test suite before distillation ships (`DATA_MODEL.md` §13) | Implementation | Before increment 1a distillation |
| R8 | **Briefing generation fails and the founder receives silence.** Silence is indistinguishable from "nothing mattered today", which is the worst failure mode available to a trust-building product — and once the briefing is trusted, silence conveys actively false information. | Medium | Failure notice on generation failure (`PRD.md` B1); alert on failure; alert on non-delivery by a deadline | Implementation | Failure-path test green in 1a |
| R9 | **Third-party personal data in call transcripts.** Customers and counterparties on recorded calls never consented to LEAP OS specifically, and call-recording consent law varies by jurisdiction. This is a legal exposure, not only a privacy-hygiene issue. | Medium | Treated at length in `PRIVACY_MODEL.md`; processor relationships disclosed; increment 1b should not ship before the consent position is settled | Founder | Before increment 1b |
| R10 | **Two permission systems in a stack.** The Agent SDK has its own tool-permission notion and ours sits above it. A mismatch could hide in the gap, and a gate tested only where it agrees with the layer beneath it has not been tested. | Medium | An explicit test proving our gate holds on a path where the SDK itself would have permitted the action (`TESTING_STRATEGY.md`) | Implementation | Test green in 1a |
| R30 | **Webhook-delivered transcripts have no gap detection.** `ADR-0008` makes Zoom ingestion push-based, which removes the watermark protection every other source has. If Zoom exhausts its delivery retries, the meeting is simply absent and nothing knows it existed. A reconciliation sweep over recent recordings is required, not optional. | **High** until the sweep exists | Periodic authenticated sweep comparing recent Zoom recordings against ingested `source_id`s, backfilling gaps (T18 in `THREAT_MODEL.md`) | Implementation | Sweep shipped and tested as part of increment 1b |
| R31 | **Zoom's native diarization is unvalidated.** Speaker misattribution turns a commitment made by someone else into one attributed to the founder, or vice versa. That is a confidently-wrong recommendation (R3) with a plausible-looking source behind it, which is the hardest kind to catch by reading the briefing. | Medium | Increment 1b's quality gate must check attribution accuracy specifically, not merely that transcripts arrive; Otter is the documented fallback if quality fails (`ADR-0008`) | Implementation | Increment 1b quality gate |
| R32 | **Forged Zoom webhook payloads.** A public endpoint accepting transcript events lets an attacker fabricate an entire episodic record including its provenance, manufacturing a sourced-looking commitment attributed to a real person. | Low, with verification; high impact without | Constant-time, fail-closed signature verification; the adapter re-fetches transcript content from Zoom with an authenticated token rather than trusting inline payload content, so a forged event with no real recording behind it dies at the fetch (T17) | Implementation | Verification tested with deliberately invalid signatures, in increment 1b |
| R11 | **Prompt injection via ingested content.** Email bodies, transcripts, and Slack messages are attacker-influenced text that reaches a model. | Medium | Tool absence rather than instruction is the defense — an agent does not hold a tool it is told not to use, it does not hold the tool; content passed as delimited data, never concatenated into instructions; a successful injection produces a gate refusal and an alert, making it a *detection event* rather than a breach | Implementation | Injection suite green in 1a; permanent thereafter |

---

## 3. Medium

| # | Risk | Likelihood | Mitigation | Owner | Closes at |
|---|---|---|---|---|---|
| R12 | **Voice transcript provider undetermined.** ASR quality, diarization, speaker attribution, and metadata differ enormously between providers, and those differences propagate into every downstream summary. Increment 1b cannot be more than a sketch until this is decided. | Certain until answered | `PRD.md` §10 open question 2 | Founder | Before increment 1b |
| R13 | **Increment ordering may be wrong.** The constitution devotes a full section to voice intelligence and no comparable detail to email, which reads as a signal that call intelligence is nearer the commercial core. If so, 1b should lead and validating the differentiated capability is being deferred. | Medium | `ADR-0006` open question, flagged rather than decided; architecture is indifferent to the order | Founder | Before increment 1a begins |
| R14 | **Prioritization degrades as memory grows.** The mechanism that produces a useful five-item briefing over two weeks of memory may produce a mediocre fifteen-item briefing over six months of it. | Medium, rising with time | Item count is a monitored secondary metric; growth past roughly twelve items is treated as regression, not success | Implementation | Monitored indefinitely |
| R15 | **Cost spike from a runaway loop or memory growth.** Agent loops that retry, or retrieval that grows with memory volume, can multiply token cost quietly. | Medium | `token_cost` and `generation_ms` recorded per briefing; cost anomaly alerting; cost is one of the eleven self-review dimensions | Implementation | Cost baseline and alert in 1a |
| R16 | **Embedding model and dimension are placeholders.** `vector(1536)` is a guess. Changing it later requires re-embedding everything, which is cheap now and expensive at volume. | Medium | `DATA_MODEL.md` §13 open question; decide before distillation ships | Implementation | Before increment 1a distillation |
| R17 | **Audit retention conflicts with deletion rights.** Audit records must survive for accountability while data subjects have deletion rights. Resolved in principle by redaction within audit records rather than removal, but the implementation is exacting and easy to get wrong in a way that only surfaces under a real request. | Medium | `PRIVACY_MODEL.md`; redaction path implemented and tested, not merely documented | Implementation | Before increment 1a ships to production |
| R18 | **Model API outage or rate limiting.** Distillation and briefing generation both depend on a single external model provider. | Medium | Graceful degradation per `FAILURE_MODES.md`; briefing states what it could not compute rather than omitting it silently | Implementation | Degradation path tested in 1a |
| R19 | **npm supply chain.** A TypeScript project's dependency surface is wide, and a compromised transitive dependency runs with the process's credentials. | Low per-incident, non-trivial cumulatively | Dependency justification rule enforced rather than nodded at (`ENGINEERING_STANDARDS.md`); lockfiles; automated advisory scanning in CI | Implementation | Scanning in CI before 1a ships |
| R20 | **Credential or PII leakage into logs and traces.** Message bodies and transcript text are exactly what a debugging session wants to log. | Medium | Redaction obligation enforced by lint rule plus a test asserting known-sensitive field names never appear in emitted output | Implementation | Redaction test green in 1a |
| R21 | **`payload` column-level encryption undecided.** Currently relying on at-rest encryption alone for message bodies and transcripts. Column-level encryption is stronger and complicates search. | Certain until answered | `DATA_MODEL.md` §13; decision belongs to `PRIVACY_MODEL.md` | Implementation | Before increment 1a ships to production |
| R22 | **Founder over-trust.** The mirror of R4. Acting on a wrong item without checking, precisely because the system has been reliable. Trust that outruns verification is a risk created *by* success. | Medium, rising as reliability improves | Every item cites evidence, making verification cheap; trust labels on every item; Phase 1 has no execution path, so the cost is bounded to a wasted action rather than an automated one | Founder | Never closes; the reason trust levels advance slowly |

---

## 4. Low, or knowingly accepted

| # | Risk | Position |
|---|---|---|
| R23 | **Supabase platform dependency.** Availability, pricing, and Postgres version support are outside our control. | Accepted. Mitigated by using only standard Postgres and pgvector, so migration is a dump, a restore, and re-homing auth (`ADR-0002`). |
| R24 | **Agent SDK vendor dependency.** Breaking changes, or opinions diverging from ours. | Accepted. Contained by the narrow substrate interface: replacing it means reimplementing one call while every guarantee stays put (`ADR-0003`). |
| R25 | **`episodic_record` partitioning deferred.** Monthly range partitioning would ease the 400-day retention sweep. | Accepted as premature at Phase 1 volume, but the retention job is materially simpler with it, so decide before volume arrives (`DATA_MODEL.md` §13). |
| R26 | **Non-reproducible agent output.** Identical inputs may yield differently-worded proposals, so golden-file testing of agent output is impossible. | Accepted, and correctly so. Assertions target structure and permissibility; prompt regression is statistical over an evaluation set (`ADR-0003`, `TESTING_STRATEGY.md`). |
| R27 | **Bus factor of one.** One contributor holds all context. | Accepted for Phase 1, and the reason the documentation standard is set where it is: `MASTER_CONSTITUTION.md` §17 requires that a developer understand the system from documentation alone, and this risk is why that requirement is not ceremonial. |
| R28 | **Error-flag signal pollution.** The flag endpoint is unauthenticated by deliberate choice (`ADR-0007`). Abuse yields false flags, which corrupt the phase's primary metric and, later, the learning loop's ground truth. | Accepted at Phase 1, where volume is low and flags are reviewed by hand. Bounded by single-use, item-scoped, expiring, rate-limited tokens. Must be re-evaluated **before** the learning loop is permitted to act on flags without review, because the exposure grows with the loop's authority rather than staying constant. |

### R29 — Erasure tooling is designed but unbuilt

**Severity: Medium. Owner: Implementation. Closes: before increment 1a reaches production with real third-party data.**

Phase 1 has a coherent erasure design (`PRIVACY_MODEL.md` §6) and no code implementing it. The first real request would therefore be handled by hand-written SQL, under time pressure, against a schema with two constraint interactions that specifically complicate erasure: the no-orphans trigger and the append-only audit table.

This is worth more attention than its severity suggests, because a minimal tested erasure path does double duty — it discharges a legal obligation and it *proves the retention design is coherent*. A retention policy that has never been executed is a retention policy nobody has checked.

---

## 5. Deferred to later phases

Recorded so that a later phase does not discover them as surprises. None is a Phase 1 obligation.

| # | Item | Arrives at | Note |
|---|---|---|---|
| D1 | **Approval-link security.** A naive click-to-approve URL in email is a credential in a mailbox: forwardable, logged by intermediate mail servers, replayable. Links must be single-use, short-expiry, and identity-bound, or approvals must move to an authenticated surface. | Phase 2 | Phase 1 avoids this entirely by having nothing to approve — the right way to defer a hard problem is not to have it yet, rather than to solve it badly (`ADR-0004`) |
| D2 | **Durable multi-step workflow state.** Unbuilt. Needed once approvals span days. | Phase 3 | `ADR-0003`. The strongest argument for revisiting LangGraph or similar. |
| D3 | **Multi-tenant operational surface.** Onboarding, provisioning, per-tenant configuration, cross-tenant admin tooling. | Phase 4 | The tenant-scoped schema buys the absence of a data migration, not the presence of a multi-tenant product (`ADR-0005`) |
| D4 | **Independent scaling of the episodic layer.** One Postgres instance serving three layers with very different access patterns is correct now and will not be correct forever. | Phase 3–4 | Repository pattern makes extraction a one-module change (`ADR-0002`) |
| D5 | **Closing the learning loop.** Phase 1 instruments for it — proposals and error flags are logged with enough structure to score — but does not act on it. | Phase 3 | `CONTINUOUS_IMPROVEMENT.md` |

---

## 6. Review discipline

This register is reviewed at every increment gate and at the milestone self-review. Three rules keep it honest:

A risk is not closed because it stopped being discussed. It is closed when its stated gate is satisfied, and the closure is recorded.

R1 and R22 never close. They are properties of building this kind of system, not defects to be fixed, and an register that eventually shows them resolved is a register that stopped being read.

New risks get added when discovered, including ones discovered by being hit. A register that only ever shrinks is being maintained as a status report rather than as an instrument.
