# ADR-0006 — Three Phase 1 data sources, delivered as three sequential increments

**Date:** 2026-08-03

## Status

Accepted, with one open question requiring founder input (see below).

## Context

`ROADMAP.md` Phase 1 specifies one agent, observing **a single data source**, at Trust Levels 0–1, with the exit criterion: *the daily briefing is used by a real executive for two consecutive weeks with measurable time saved and no false or misleading recommendations.*

The founder has directed that Phase 1 observe three source families: Google Workspace (Gmail and Calendar), voice call transcripts, and Slack or Teams messaging.

`MASTER_CONSTITUTION.md` §5 obliges me to disagree with a requested implementation where a superior approach exists, show evidence, and recommend an alternative rather than comply silently. This ADR is that disagreement, and its resolution.

The disagreement is narrow. The founder's scope is not wrong on ambition — three sources is a far more useful briefing than one, and a briefing built on email alone will feel thin to someone whose real work is spread across calls and Slack. The objection is to landing them **simultaneously**, and it comes down to attribution.

Phase 1's exit criterion is not "the briefing works." It is "no false or misleading recommendations over two consecutive weeks." That is a quality bar, and quality bars require the ability to diagnose failures. Three ingestion paths shipped together mean that when a briefing surfaces a misleading priority, the cause could be transcript speaker-attribution error, Slack thread-boundary detection, Gmail thread summarization, or the prioritization logic that consumes all three — and each of those has a different fix. Diagnosing that is materially harder than diagnosing it with one source live, and the difficulty compounds because the sources have genuinely different failure characteristics: Gmail is structured and reliable, Slack is high-volume and noisy with weak thread semantics, transcripts carry ASR errors and speaker confusion that propagate silently into confident-sounding summaries.

There is a second, quieter argument. Trust is earned per `MASTER_CONSTITUTION.md` §10, and it is earned by the *user*, not just recorded by the system. A founder who receives a briefing that is right about email and wrong about calls in week one does not form the belief "the transcript adapter needs work" — they form the belief "this thing is unreliable." That belief is expensive to reverse and it is the actual asset Phase 1 is trying to build.

## Decision

**All three sources are in Phase 1 scope, delivered as three sequential increments, each with its own exit gate.**

| Increment | Source | Contributes to the briefing |
|---|---|---|
| **1a** | Google Workspace — Gmail + Calendar | Highest-priority work, emails awaiting response, today's and tomorrow's commitments, critical follow-ups |
| **1b** | Voice call transcripts | Call outcomes, objections, missed opportunities, commitments made on calls, follow-ups owed |
| **1c** | Slack / Teams messaging | Messages awaiting response, surfaced decisions and commitments made in channels |

Governing rules:

- **One shared ingestion interface.** All three adapters implement the same contract — a source yields timestamped, provenance-carrying episodic records — so adding an increment is additive and touches no prior adapter. Specified in `ARCHITECTURE.md`. This is what makes sequencing cheap: the sequence is a delivery decision, not an architectural one.
- **Each increment carries its own exit gate**, and the gate is briefing quality attributable to that source, not merely "the adapter runs."
- **Each increment's records are tagged by source** in the episodic layer, so briefing-quality regressions can be attributed by source after the fact rather than guessed at. This is the mechanism that makes the whole argument above operational rather than rhetorical.
- **The two-week exit criterion from `ROADMAP.md` applies to the composite**, measured after 1c lands. Phase 1 is not complete when the third adapter ships; it is complete when the briefing built on all three earns two clean weeks.
- Phase 1 remains at Trust Levels 0–1 throughout. No increment introduces execution.

## Open question for the founder

**Should increment 1b (voice transcripts) be promoted ahead of 1a (Google Workspace)?**

The constitution devotes an entire section (`MASTER_CONSTITUTION.md` §13) to voice intelligence — transcript, intent, outcome, objections, sentiment, transfer quality, booking quality, missed opportunities, prompt failures — with a specificity that no other data source receives. That is a strong signal that voice is closer to the commercial core of the business than a generic executive assistant would be, and possibly that LEAP OS's differentiated wedge is call intelligence rather than inbox triage.

If that reading is right, the ordering above is wrong, and 1b should lead. Two reasons: the differentiated capability should be validated first, and the structured call intelligence in §13 is far more prescriptive than anything in the email path, which means it is more specified and therefore more buildable.

I have defaulted to Google Workspace first because it is the lowest-risk path to a briefing that stands on its own — calendar and inbox cover most of the Phase 1 briefing sections without depending on any other source — and because ASR quality problems are a poor first impression. But this is a business-strategy judgment more than an engineering one, and it is the founder's to make. **Flagging rather than deciding.** The architecture is indifferent to the ordering; only the sequence changes.

## Alternatives considered

**Strict one-source Phase 1, per the roadmap as written.** The most disciplined option, and the one the roadmap literally specifies. Rejected because it overrides an explicit founder decision on scope without sufficient cause. The concern motivating the roadmap's single-source rule is diagnosability, and sequential increments with source-tagged records address that concern directly while preserving the founder's intent. Overriding a founder on scope requires the alternative to be *unable* to meet the underlying requirement, and it can.

**All three sources landing simultaneously.** Rejected for the attribution and trust-formation reasons above. Worth noting the honest counter-argument: simultaneous delivery is faster to a genuinely useful briefing, and a thin single-source briefing risks failing the two-week usage test for lack of value rather than lack of quality. That is a real risk and it is why all three remain in Phase 1 rather than being deferred to Phase 2 — the disagreement is about ordering within the phase, not about scope.

**Deferring Slack to Phase 2.** Consistent with `ROADMAP.md`, which places messaging in Phase 2 and notes that Slack is usually more valuable once email triage has proven itself. Rejected in deference to the founder's explicit inclusion. Recorded because if Phase 1 runs long, increment 1c is the correct thing to cut, and it should be cut deliberately rather than dropped silently.

## Tradeoffs

Sequential delivery means Phase 1 takes longer to reach its full briefing than parallel delivery would, and increments 1a and 1b will each ship a briefing that is visibly incomplete relative to the eventual product. The founder will see gaps and know they are gaps.

We also accept that gating each increment on briefing quality introduces judgment into the schedule: "attributable quality" is not a number that arrives on its own, and someone has to look at briefings and decide. That is appropriate for Phase 1 and would not scale, and the scoring mechanics in `CONTINUOUS_IMPROVEMENT.md` are what eventually replace the judgment.

## Future implications

Easier: source-tagged episodic records and a shared adapter interface mean every subsequent source — CRM in Phase 3, anything in Phase 4 — is additive, and quality regressions remain attributable indefinitely. The tagging is a permanent diagnostic asset, not Phase 1 scaffolding.

Harder: nothing structural.

## Migration path

Not applicable — this is a delivery-sequencing decision. Reordering increments requires no architectural change, which is the point of the shared adapter interface.

## Technical debt

Two items for the risk register, both real:

1. **Fixture-based adapters.** No live credentials exist for Gmail, Calendar, Slack, or any transcript source at time of writing. All three adapters will be built against realistic fixture data behind their real interfaces. Adapter logic is therefore *unvalidated against live API behavior* — real-world pagination, rate limits, malformed payloads, and authentication edge cases are exactly where fixtures lie. Each increment's exit gate must include live-credential validation, not fixture-passing tests alone.

2. **Voice transcript source undetermined.** Increment 1b has no specified provider, and its adapter cannot be more than a sketch until one exists. ASR output shape, speaker attribution, diarization quality, and metadata availability vary enormously between providers, and these differences propagate into the quality of every downstream summary. Needs founder input alongside the open question above.
