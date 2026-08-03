# Product Philosophy

Governs how LEAP OS decisions get made. Subordinate to `MASTER_CONSTITUTION.md`.

## Guiding tension

Every product decision balances two forces: **leverage** (does this reduce executive cognitive load or increase organizational intelligence?) and **trust** (does this action deserve the autonomy it's being given?). When in doubt, resolve toward trust — an under-powered but trusted assistant compounds; an over-eager one gets disabled.

## Principles

1. **Long-term architecture over short-term speed.** A feature shipped in a day that requires a rewrite in a month is a net loss. Estimate the cost of the rewrite before shipping the shortcut.
2. **No intentional technical debt.** If a shortcut is taken under real time pressure, it is logged in the Risk Register (`DEFINITION_OF_DONE.md`) with an owner and a removal date — not left implicit.
3. **No premature optimization.** Build for correctness and clarity first; optimize only against a measured bottleneck.
4. **No complexity for its own sake.** "This is technically interesting" is not a justification. "This is the simplest thing that satisfies the requirement" is the bar.
5. **Elegant over clever.** Clever code impresses the author and confuses everyone else six months later.
6. **Modularity over monoliths.** Every capability should be replaceable without a rewrite of its neighbors.
7. **Deterministic behavior over hidden magic.** If a user or developer cannot predict what the system will do from its documented behavior, the design has failed, regardless of how impressive the demo looks.
8. **Transparency over unexplainable automation.** Any automated action must be traceable to the reasoning, data, and permission level that produced it.
9. **Written justification for every architectural decision.** A decision without a documented alternative considered is a decision that will be re-litigated for free later.

## What "increasing leverage" means in practice

- A feature that saves an executive 5 minutes but requires 10 minutes of trust-building/verification is not leverage yet — it belongs at Trust Level 1 (Recommend), not Level 3+.
- A feature that removes a decision entirely (fully deterministic, fully reversible, fully logged) is a leverage candidate for higher trust levels.
- Cognitive load is not just time — it's context switching, uncertainty, and the need to double-check. Reducing the *need to verify* is often higher leverage than reducing the *time to do*.

## Anti-patterns to actively reject

- Building a feature because a competitor has it, without a leverage case.
- Adding a new agent when an existing agent's responsibility could reasonably absorb the task (see `AI_AGENT_STANDARDS.md` on single-responsibility agents).
- Automating an action before the trust level for that action class has been earned.
- Optimizing for engagement/usage metrics rather than executive time saved and decision quality improved.
