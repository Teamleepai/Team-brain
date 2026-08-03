# UX Principles

Governs the human-facing surface of LEAP OS. Subordinate to `MASTER_CONSTITUTION.md`.

## The core UX bet

The executive user should feel like they have a Chief of Staff, not a chatbot. That means the interface optimizes for **less interaction**, not more engagement — every screen or notification should be justified by cognitive load it removes, not attention it captures.

## Principles

1. **Show the trust level.** Every recommendation, draft, or executed action is visibly tagged with its trust level so the user always knows whether they're looking at a suggestion or a fait accompli.
2. **One daily surface, not a firehose.** The executive briefing (master §14) is the default interface; ad hoc notifications are reserved for things that genuinely can't wait until the next briefing.
3. **Approval friction matches impact.** A Level 3 action needing approval should take one glance and one tap — not a form. A high-impact action (§11 of the master doc) can and should take longer to review.
4. **Never hide the "why."** Every surfaced recommendation links to its supporting evidence (the meeting, the email thread, the metric) — one click away, not buried.
5. **Reversibility is visible.** If an action can be undone, the undo path is as visible as the action itself. If it can't be undone, that is stated before, not after.
6. **Consistency of agent voice.** Regardless of which specialized agent produced content, the user-facing tone and format are consistent — the user should never have to relearn a UI pattern because a different agent under the hood produced this particular card.

## Anti-patterns

- Notification volume as a proxy for value delivered.
- Confirmation dialogs so frequent that users learn to click through them without reading (alert fatigue directly undermines the Trust Framework).
- Surfacing raw agent reasoning/chain-of-thought as the primary UI — the user wants the conclusion and an optional "why," not a transcript of the reasoning process.
