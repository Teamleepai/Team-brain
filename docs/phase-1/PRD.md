# Phase 1 — Product Requirements Document

**Feature:** Chief of Staff agent, daily executive briefing, observe and recommend only
**Trust levels:** 0–1 (`MASTER_CONSTITUTION.md` §10)
**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

---

## 1. The problem

A founder's attention is fragmented across three systems that do not talk to each other: an inbox, a calendar, and the record of what was actually said on calls and in channels. The cost is not the time spent reading any one of them. The cost is the *reconstruction tax* — every morning, the founder rebuilds a mental model of what matters today from four or five partial sources, and every evening some portion of what mattered was never reconstructed at all.

The failures this produces are specific and expensive:

- A commitment made on a call on Tuesday is not honored, because it lived only in the call.
- An email from a customer sits four days because it arrived during a busy afternoon and fell below the fold.
- Two hours of the highest-leverage day of the week go to whatever was loudest rather than whatever was most important.
- A pattern across three customer conversations goes unnoticed because no single conversation contained it.

None of these are information-retrieval failures. The information was all available. They are *synthesis and prioritization* failures, and they are the specific failures LEAP OS Phase 1 targets.

## 2. What Phase 1 is

One agent — the Chief of Staff — observes three source families across four adapters (Gmail and Google Calendar, voice call transcripts, and Slack), builds structured organizational memory from what it sees, and delivers one email each morning that says: here is what matters today, here is what is waiting on you, and here is what you committed to that has not happened yet.

Throughout this document, "three sources" refers to the three families that define the delivery increments in `ADR-0006`; "four adapters" refers to the integrations implementing them, since Gmail and Calendar are separate APIs within increment 1a.

It recommends. It does not act. There is no draft, no send, no schedule, no delete. Every item is a recommendation the founder acts on manually, in the source system, via a link.

## 3. What Phase 1 is deliberately not

Naming these matters as much as naming the scope, because each is a plausible next step that would compromise the phase:

- **Not a chat interface.** There is no conversational surface. The briefing is a push, not a dialogue. Adding "ask a follow-up question" doubles the surface area and defers the only question Phase 1 asks.
- **Not drafting anything.** No draft replies, no suggested email text. Drafting is Trust Level 2 and it arrives in Phase 2.
- **Not taking any action.** No calendar changes, no sends, no CRM updates. See `ADR-0004` on why this also means no action links in the email.
- **Not a dashboard.** Deferred to Phase 2 (`ADR-0004`).
- **Not multi-user.** One founder, one org, though the schema is tenant-scoped (`ADR-0005`).
- **Not self-improving yet.** The continuous learning loop in `CONTINUOUS_IMPROVEMENT.md` requires scored outcomes at volume. Phase 1 *instruments* for it — every recommendation is logged with enough structure to score later — but does not close the loop.

## 4. Business goals

| Goal | Why it matters at this phase |
|---|---|
| Prove the synthesis hypothesis | Establish that cross-source synthesis produces priorities the founder would not have arrived at alone. If it does not, the entire product thesis needs revisiting before more is built. |
| Earn Trust Level 1 credibility | Every later phase depends on the founder believing the system's judgment. That belief is built or destroyed in Phase 1 and it is the real deliverable. |
| Build the memory substrate | Organizational memory is the compounding asset (`MEMORY_ARCHITECTURE.md`). Phase 1 starts its accumulation, and the value of that accumulation is realized in later phases. |
| Establish the trust and audit machinery | The gating and logging architecture from `ADR-0003` is built and exercised in Phase 1 while the stakes are zero, so that Phase 2's first real action executes through a path that has been running for weeks. |
| De-risk the integrations | Four adapters across three source families, exercised against live APIs with real pagination, rate limits, and auth failures, before any of them is load-bearing for an action. |

## 5. Success metrics

Measurement discipline matters here more than usual, because the primary outcome — "did this reduce cognitive load" — is not directly observable and the temptation is to substitute something easier to count.

### Primary

| Metric | Target | How measured |
|---|---|---|
| **Briefing open rate** | ≥ 90% of briefings opened within 3 hours of delivery | Email open tracking |
| **Sustained daily use** | 14 consecutive weekdays of opens, no gap > 1 day | Open log |
| **Misleading-recommendation count** | **Zero** over the final 14-day window | Founder flags any item that was wrong or misleading; per `ROADMAP.md` Phase 1 exit criterion |
| **Novel-priority rate** | ≥ 1 item per briefing, on average, that the founder would not have surfaced unaided | Founder marks items as "I would have missed this" |
| **Self-reported time saved** | ≥ 20 min/day | Weekly one-question survey |

### Secondary

| Metric | Purpose |
|---|---|
| Items per briefing | Watch for firehose drift; `UX_PRINCIPLES.md` names volume-as-value an anti-pattern. A briefing growing past ~12 items is regressing. |
| Evidence-link click rate | Low click-through suggests either high trust or unread items — disambiguated against open duration |
| Per-source attribution of flagged errors | Which adapter causes misleading items, per `ADR-0006` |
| Ingestion lag | Time from event occurring to record in episodic layer |
| Briefing generation cost and latency | Cost per briefing, for the cost dimension of the §19 self-review |

### Explicitly rejected as metrics

**Engagement, session count, and time-in-product.** `UX_PRINCIPLES.md` optimizes for *less* interaction. A rising time-in-product number would be evidence of failure, and adopting it as a metric would create pressure in exactly the wrong direction.

**Volume of recommendations generated.** Rewards the firehose.

**Anything the system can improve without improving the founder's day.** The only metrics that count are ones where the system cannot win without the user winning.

## 6. User personas

### Primary — the Founder-CEO

Aaron. Runs a company where his own attention is the binding constraint on execution. Technical enough to read a stack trace, but not available to babysit tooling. Days are fragmented across customer calls, internal decisions, and inbound requests, with the highest-value work being the work that gets displaced first.

- **Reads the briefing:** on a phone, before a laptop is open, in under two minutes.
- **Needs from Phase 1:** a correct answer to "what are the two things that actually matter today, and what am I forgetting."
- **Trust posture:** will extend trust readily on the first correct surprise, and withdraw it completely after two confidently-stated errors. Asymmetric, and the asymmetry drives the zero-tolerance error metric above.
- **Fails to adopt if:** the briefing is long, hedged, generic, or arrives after the day has started.

### Secondary (Phase 2, designed for but not served) — the Leadership Team member

A functional leader whose needs overlap but diverge in one important way: they need shared organizational memory without shared *visibility* into everything the founder sees. Phase 1 does not serve them, but the tenant-scoped schema and role-carrying user records (`ADR-0005`) exist so that Phase 2 can without a migration.

### Anti-persona — the power user who wants to configure everything

Explicitly not served. A configuration surface is how this product becomes a tool the founder maintains rather than a chief of staff who works. Phase 1 has a delivery time and a source list. That is the configuration.

## 7. User stories and acceptance criteria

### Epic A — Ingestion and memory

**A1.** *As the system, I ingest Gmail messages and calendar events so that the briefing can reason over the founder's commitments and correspondence.*

- Given valid OAuth credentials, when ingestion runs, then new messages and events since the last watermark are written to the episodic layer within 5 minutes of that run beginning. Combined with the 15-minute ingestion cycle in `ARCHITECTURE.md` §8, worst-case end-to-end lag from an event occurring to it being visible in memory is 20 minutes. That is the number to hold the system to; the 5-minute figure bounds the run, not the lag.
- Every episodic record carries provenance: source system, source identifier, ingestion timestamp, and the agent or process that wrote it (`MEMORY_ARCHITECTURE.md`).
- Given the source API returns a rate-limit or 5xx error, when ingestion runs, then it backs off and retries, and a partial failure never advances the watermark past unprocessed data.
- Given ingestion runs twice over an overlapping window, then no duplicate episodic records are created — source identifier plus tenant is unique.
- Given a message body contains text resembling instructions ("ignore your previous instructions and…"), when it is ingested, then it is stored and later processed as *data*, and the agent's behavior is unchanged (`SECURITY_STANDARDS.md`, prompt injection).

**A2.** *As the system, I distill episodic events into semantic records — commitments, decisions, open questions, people, projects — so that memory compounds rather than accumulating raw text.*

- Given a set of episodic records, when distillation runs, then extracted facts are written to the semantic layer, each linked to the episodic records it derives from.
- Given a fact that duplicates an existing semantic record, when distillation runs, then the existing record is updated or linked rather than duplicated (`MEMORY_ARCHITECTURE.md`: never create duplicate knowledge).
- Given a fact that contradicts an existing semantic record, when distillation runs, then the prior record is marked superseded with a forward link, and is not deleted.
- No semantic record exists without at least one link to its source. Orphans fail validation.

**A3.** *As the system, I ingest voice call transcripts so that commitments and outcomes from calls are not lost.*

- Structured intelligence per `MASTER_CONSTITUTION.md` §13 is extracted per call: intent, outcome, objections, sentiment, missed opportunities, and commitments made.
- Given a transcript with low ASR confidence or ambiguous speaker attribution, when it is processed, then extracted facts carry a confidence marker, and low-confidence facts are excluded from the briefing rather than presented with false certainty.

**A4.** *As the system, I ingest Slack messages so that decisions and requests made in channels are visible.*

- Thread boundaries are respected; a thread is summarized as a unit rather than message by message.
- Channels are configurable as in-scope or out-of-scope, defaulting to out-of-scope. The founder opts channels in.

### Epic B — The briefing

**B1.** *As the founder, I receive one email each weekday morning telling me what matters today.*

- Delivered at the configured local time, on weekdays, before the founder's first meeting.
- Contains, when the underlying data exists: highest-priority work, items awaiting my response, commitments I made that are not yet done, today's and tomorrow's calendar commitments, and anything notable from yesterday's calls.
- Given a section has no items, then the section is omitted entirely rather than rendered empty. A briefing that says "no customer issues today" three hundred times teaches the reader to skim.
- Renders correctly on a phone. Readable in under two minutes.
- Given generation fails, then the founder receives a short failure notice rather than silence, and the failure alerts per `OBSERVABILITY.md`. Silence is indistinguishable from "nothing mattered today," which is the worst possible failure mode for a trust-building product.

**B2.** *As the founder, every item shows me its trust level and links to its evidence.*

- Every item is tagged with its trust level; in Phase 1 all items are "Recommendation" (`ADR-0004`).
- Every item links to its source: the Gmail thread, the calendar event, the transcript, the Slack thread.
- Given an item derives from multiple sources, then all contributing sources are linked (`OBSERVABILITY.md` explainability requirement).
- No item appears without at least one evidence link. An unsourced assertion is not shippable at any trust level.

**B3.** *As the founder, I can tell the system an item was wrong.*

- Each item carries a lightweight "this was wrong" affordance that records the flag against the item, its source, and the reasoning that produced it.
- Flags are stored as procedural-layer input for the Phase 3 learning loop (`CONTINUOUS_IMPROVEMENT.md`), and drive the primary error metric above.
- The flag affordance is the *only* interactive element in the briefing, and it changes no state outside LEAP OS. It is a deliberate, single carve-out from the no-action-links rule in `ADR-0004`, with its security properties specified in `ADR-0007`: item-scoped, single-use, expiring, rate-limited, and incapable of any effect beyond writing one row.

### Epic C — Trust, audit, and safety

**C1.** *As the operator, no agent can act above its declared trust level.*

- The Chief of Staff agent is declared at Trust Level 1 and has no execution tools available to it at construction (`ADR-0003`).
- Given an agent proposes an action above its trust level, when the proposal reaches the gate, then it is refused and logged as a gate refusal, and the refusal alerts.
- Test coverage includes an agent deliberately configured to attempt a Level 3 action, proving the gate refuses it rather than proving that a well-behaved agent never asks.

**C2.** *As the operator, every agent action is auditable.*

- Every proposal — accepted, refused, or surfaced — produces an audit record with actor, trust level, inputs, outputs, rationale, and timestamp (`OBSERVABILITY.md`).
- Audit records are append-only with no update path (`ADR-0002`).
- Given any briefing item, then the audit trail can reconstruct which agent produced it, from which records, under which trust level.

**C3.** *As the operator, tenant isolation is enforced and proven.*

- Every table carries `org_id` with RLS enforcement (`ADR-0005`).
- An adversarial test suite attempts cross-tenant reads against a synthetic second org and fails to retrieve data.

## 8. Scope by increment

Per `ADR-0006`, delivery is sequential. Each increment ships a working briefing.

- **1a — Google Workspace.** Ingestion, memory, distillation, briefing composition, email delivery, trust gate, audit, RLS. This is the phase's architectural spine; 1b and 1c add adapters to it.
- **1b — Voice transcripts.** Transcript adapter plus §13 structured call intelligence. Blocked on a provider decision (`ADR-0006` open question).
- **1c — Slack.** Messaging adapter with thread-aware summarization and channel opt-in.

## 9. Exit criteria

Phase 1 is complete when, with all three increments live:

1. Fourteen consecutive weekdays of briefings delivered and opened, no gap greater than one day.
2. Zero misleading recommendations flagged in that window.
3. Novel-priority rate at or above one item per briefing.
4. Self-reported time saved at or above 20 minutes per day.
5. The full `DEFINITION_OF_DONE.md` checklist satisfied, including the milestone self-review from `MASTER_CONSTITUTION.md` §19.
6. No unresolved critical items in the risk register.

Failing (2) resets the 14-day window. That is intentional and it is the point of the metric.

Note that 14 consecutive *weekdays* is close to three calendar weeks, which deliberately tightens `ROADMAP.md`'s "two consecutive weeks." Weekdays are the right unit because the briefing is a weekday artifact, and counting calendar weeks would let a quiet holiday week pad the record.

## 10. Open questions

| # | Question | Owner | Blocks |
|---|---|---|---|
| 1 | Should increment 1b (voice) precede 1a (Google Workspace)? | Founder | Increment ordering, not architecture (`ADR-0006`) |
| 2 | Which voice transcript provider? | Founder | 1b adapter beyond a sketch |
| 3 | Briefing delivery time and timezone | Founder | 1a scheduling |
| 4 | Transactional email provider for delivery | Me, unless founder has a preference | 1a delivery |
| 5 | Which Slack channels are in scope | Founder | 1c |
| 6 | Is there an existing CRM to consider for Phase 3 sequencing | Founder | Nothing in Phase 1 |
