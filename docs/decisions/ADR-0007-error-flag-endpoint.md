# ADR-0007 — The error-flag endpoint as the sole carve-out from the no-action-links rule

**Date:** 2026-08-03

## Status

Accepted. Refines `ADR-0004` without superseding it.

## Context

`ADR-0004` states the Phase 1 briefing contains "**no action links of any kind.** No approve buttons, no one-click execution, no state-changing URLs," and argues that this is a security decision rather than a UX one, because a click-to-approve URL in a mailbox is a credential: forwardable, logged by intermediate mail servers, and replayable.

`PRD.md` B3 nonetheless requires that each briefing item carry a lightweight "this was wrong" affordance, because the error signal is the primary success metric of the phase (`PRD.md` §5) and the seed corpus for the Phase 3 learning loop (`CONTINUOUS_IMPROVEMENT.md`).

Those two requirements are in literal tension, and the tension went unacknowledged in both documents. `API_CONTRACTS.md` typed the affordance as a bare `flagUrl: string`, which is an unauthenticated state-changing URL — precisely the shape `ADR-0004` prohibits. Review surfaced this, and it is worth resolving in a record rather than in prose buried in a data model, because the next person to add "just one more link" needs a rule to check themselves against.

## Decision

**The error-flag endpoint is the single permitted exception, and the rule is narrowed rather than broken.**

The prohibition in `ADR-0004` is restated precisely: *no link in the briefing may cause an effect outside LEAP OS, and no link may carry ambient authority.* The flag endpoint satisfies both while still changing state, which is why it is permissible where an approve link is not.

Its required properties:

| Property | Requirement | Why |
|---|---|---|
| Scope | Bound to exactly one `briefing_item_id` | A leaked token can flag that item and nothing else |
| Capability | Inserts one `error_flag` row. Nothing more. | No ambient authority; the token is not a session |
| Single use | Consumed on first use | Removes replay value |
| Expiry | Short, on the order of the briefing's useful life | A token found in a mail archive a year later is inert |
| External effect | **None** | Nothing leaves LEAP OS; no email sent, no calendar changed, no third party contacted |
| Unauthenticated | Accepted deliberately | See tradeoffs |
| Rate limited | Per token and per org | Bounds abuse of a public endpoint |
| Audited | Every use written to `audit_record` | A flag is a signal that feeds learning, so its provenance matters |

Typed in `API_CONTRACTS.md` §7 as `FlagAffordance` with `token` and `expiresAt` rather than as a bare string, so the security properties are visible at every call site instead of living in a comment.

## Alternatives considered

**Require authentication to flag.** The obvious secure answer, and rejected on product grounds that are genuinely stronger than they first appear. The flag exists to be used in the two seconds after the founder notices something wrong, on a phone, before the next meeting. A login wall converts a two-second action into a thirty-second one, and the predictable result is that flags stop being sent. That does not merely lose a convenience: it silently corrupts the phase's primary metric, because "zero misleading recommendations" becomes indistinguishable from "nobody bothered to report any." A security control that destroys the measurement it was protecting is a bad trade at this blast radius.

**No flag affordance at all; collect errors verbally.** Rejected. `PRD.md` §5 requires the error count as a gating metric and `DEFINITION_OF_DONE.md` makes it the criterion that resets its own window. A metric gathered by memory in a weekly conversation is not a metric.

**Reply-to-flag over email.** Genuinely appealing: it uses the founder's existing reply habit, needs no URL, and authenticates weakly by sender address. Rejected for Phase 1 because parsing intent out of free-text replies is an NLP task with its own failure modes, and attributing a reply to a specific *item* within a briefing is ambiguous in exactly the cases that matter. Worth revisiting at Phase 2 alongside the dashboard, when there is a second surface to compare against.

**Defer the flag to the Phase 2 dashboard.** Rejected because it defers the metric, and the metric is what Phase 1 is for.

## Tradeoffs

We are shipping an unauthenticated, state-changing, publicly reachable endpoint. That is a real cost and should not be softened. What bounds it is that the worst outcome of full compromise is a false error flag on one briefing item, which pollutes a metric and a training signal. That is bad. It is not data exfiltration, not an action taken in the founder's name, and not anything visible outside LEAP OS.

The residual risk that actually deserves attention is subtler than abuse: **a polluted error signal degrades the Phase 3 learning loop**, and does so quietly. `CONTINUOUS_IMPROVEMENT.md` treats human corrections as ground truth, so an adversary who could flag freely could steer future prompt changes. Rate limiting and single-use tokens bound this to noise at Phase 1 volume, but the exposure grows with the loop's authority, and it should be re-evaluated before the learning loop is allowed to act on flags without review.

We also accept that this ADR creates a precedent, which is the thing most likely to cause harm later. Mitigation is the narrowed rule stated above: the test is not "is this link small" but "does it cause an effect outside LEAP OS, and does it carry ambient authority." An approve link fails both. Any future link must be checked against those two questions in a new ADR, not by analogy to this one.

## Future implications

Easier: the error metric is collected from day one at near-zero friction, which is what makes `PRD.md` §5 measurable rather than aspirational.

Harder: nothing structural, but the Phase 2 approval-link problem is unchanged and remains genuinely hard. This decision must not be cited as evidence that unauthenticated links in email are acceptable for approvals. They are not, for the specific reason that an approval *does* cause an effect outside LEAP OS and *does* carry authority — the two properties this carve-out exists to exclude. Recorded as D1 in `RISK_REGISTER.md`.

## Migration path

If the flag endpoint proves abusable in practice, it moves behind authentication and the friction cost is absorbed. That is a one-endpoint change with no schema impact, since `error_flag` does not care how the row arrived.

## Technical debt

None incurred intentionally. One obligation: the abuse-resistance properties above must be *tested*, not merely specified. Single-use enforcement, expiry, item scoping, and rate limiting each need a test that attempts the violation, because an unauthenticated endpoint whose protections were only ever exercised on the happy path is an unauthenticated endpoint with unverified protections.
