# ADR-0004 — Email as the Phase 1 briefing delivery surface

**Date:** 2026-08-03

## Status

Accepted.

## Context

`MASTER_CONSTITUTION.md` §14 requires one daily executive briefing covering priorities, revenue opportunities, customer issues, pipeline, follow-ups, unanswered email and messages, engineering risks, prompt recommendations, system health, reminders, tomorrow's priorities, and weekly and monthly trends. Phase 1 delivers a subset of these, per `ROADMAP.md`.

`UX_PRINCIPLES.md` sets the constraints that decide this question:

- The system should optimize for *less* interaction, not more engagement. Every surface must be justified by cognitive load removed rather than attention captured.
- One daily surface, not a firehose.
- Every recommendation is visibly tagged with its trust level.
- Every recommendation links to its supporting evidence, one click away.
- Notification volume as a proxy for value is named explicitly as an anti-pattern.

The critical scoping fact: Phase 1 operates at Trust Levels 0 and 1 — observe and recommend only. There is no execution and there are no drafts. That means Phase 1 has **nothing to approve**, which removes what would otherwise be the dominant design constraint on the surface.

## Decision

**Email**, as the sole Phase 1 delivery surface for the daily executive briefing.

- One message per day, on a schedule the founder sets, rendered as HTML with a plain-text alternative.
- Every item carries a visible trust-level tag, per `UX_PRINCIPLES.md` §1. In Phase 1 that tag reads "Recommendation" throughout, which is not redundant — it establishes the vocabulary before higher trust levels exist and makes the eventual appearance of "Executed" meaningful rather than novel.
- Every item links directly to its evidence in the source system: the Gmail thread, the calendar event, the call transcript. Until a dashboard exists (Phase 2), the source system *is* the drill-down surface. This is a genuine advantage of starting with email rather than a limitation to apologize for.
- **No action links of any kind.** No approve buttons, no one-click execution, no state-changing URLs. This follows from Trust Level 0–1 having no actions to take, and it is worth stating as an explicit prohibition rather than an omission, because "just add a quick approve link" is the natural next step and it is a security decision, not a UX one (see Tradeoffs).

## Alternatives considered

**A Slack bot delivering the briefing as a DM.** Interactive, natively supports buttons for future approvals, and makes follow-up questions conversational. Rejected for Phase 1 on the constitution's own terms: it risks becoming another notification stream in the place the founder already receives too many, and its principal advantage — interactivity — is worth close to nothing at Trust Level 1, where there is nothing to interact with. Slack becomes genuinely attractive at Phase 2 when drafts need approving, and this decision should be revisited then rather than treated as settled.

**A web dashboard as the primary surface.** The richest option, the best eventual home for evidence drill-down and the multi-user enterprise story, and the thing one would demo to an investor. Deferred to Phase 2 for a specific reason: it is by far the largest build, and Phase 1's job is to find out whether the briefing's *content* is valuable. Spending Phase 1 building a surface is the classic way to arrive at a beautiful frame around a briefing nobody reads. A dashboard also requires the founder to *visit* it, which fails the less-interaction test in a phase where the habit does not yet exist.

**Email plus a web dashboard together.** The correct end state — email as the daily push, dashboard as the drill-down target the email links into. Rejected as a Phase 1 scope roughly double what is needed to answer Phase 1's question.

**A CLI or a file committed to this repository.** Cheapest possible, and briefly tempting given the founder is technical. Rejected because it optimizes for the builder rather than the user. The exit criterion in `ROADMAP.md` is a real executive using this daily for two weeks; a surface that requires opening a terminal will not survive a busy Tuesday.

## Tradeoffs

Email cannot do rich interaction, follow-up questions, or progressive disclosure beyond a hyperlink. Phase 1 accepts this fully, because at Trust Level 1 the product is a well-prioritized read, not a control panel.

Email is also unforgiving about quality in a way that is worth naming as a *benefit* here. A dashboard tolerates mediocre content because the user chose to visit. A daily email that is not worth reading gets filtered within a week. That makes email a sharper instrument for testing Phase 1's actual hypothesis than a dashboard would be.

The deferred risk is real and belongs on the record: **the moment Phase 2 introduces approvals, action links become a security surface.** A naive click-to-approve URL is a credential in a mailbox — forwardable, loggable in intermediate mail servers, and replayable. When Phase 2 arrives, approval links must be single-use, short-expiry, bound to an authenticated identity, and non-idempotent-safe by design, or approvals must move to an authenticated surface instead. Phase 1 avoids this entirely by having nothing to approve, which is the right way to defer a hard problem — by not having it yet, rather than by solving it badly. Logged in the risk register against Phase 2.

## Future implications

Easier: Phase 1 ships without building a frontend, and the daily-habit hypothesis gets tested in the founder's existing workflow rather than a new one.

Harder: nothing structural. Because the briefing is generated as structured data and *rendered* to email as a final step, adding a dashboard, a Slack surface, or a mobile push later is a new renderer over the same briefing object, not a rewrite. The architecture requirement this implies — that briefing composition and briefing rendering are separate modules with a documented interface between them — is specified in `ARCHITECTURE.md` and is the single most important consequence of this ADR for implementation.

## Migration path

Adding or replacing a surface means writing a renderer against the existing briefing data structure. The composition layer, the agents, and the memory system are unaffected. If email proves wrong, replacing it is days of work, not a phase.

## Technical debt

None incurred intentionally.

One temptation to guard against explicitly: rendering the briefing directly from agent output into HTML, skipping the intermediate structured briefing object because Phase 1 has only one surface and the indirection looks unnecessary. That shortcut would couple every future surface to email's assumptions and is exactly the kind of debt `PRODUCT_PHILOSOPHY.md` §2 forbids taking on knowingly.
