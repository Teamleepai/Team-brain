# Continuous Improvement

Governs the learning loop. Subordinate to `MASTER_CONSTITUTION.md`.

## The loop

Every interaction becomes learning, on a standing cycle:

**Observe → Analyze → Score → Identify failures → Generate hypotheses → Recommend improvements → Validate → Simulate → Test → Deploy after approval → Measure impact → Repeat.**

This loop applies uniformly to prompts, agent behavior, workflows, and the product itself — it is not a special process reserved for one subsystem.

## Mechanics

- **Observe**: every agent action and outcome is captured via the observability layer (`OBSERVABILITY.md`).
- **Analyze/Score**: outcomes are scored against explicit success criteria defined per agent/workflow (acceptance rate, correction rate, time saved, error rate).
- **Identify failures**: recurring low scores or human corrections are flagged as failure patterns, not treated as one-off noise.
- **Generate hypotheses**: a proposed fix (prompt change, logic change, new guardrail) is stated explicitly, with the failure pattern it targets.
- **Validate/Simulate/Test**: per `TESTING_STANDARDS.md` — no hypothesis reaches production without regression testing against historical cases.
- **Deploy after approval**: high-impact changes (customer-facing prompts, policy changes) go through human approval regardless of how confident the automated pipeline is (master §11).
- **Measure impact**: every deployed improvement is tracked against its original hypothesis's success criteria — did it actually move the metric it targeted?

## Guardrails on the loop itself

- The system proposes improvements; it does not unilaterally decide it is right. Confidence in a hypothesis is not a substitute for the approval gate.
- A hypothesis that fails validation is logged (not discarded silently) so the same failed idea isn't re-proposed without new evidence.
- The loop's own performance (how many hypotheses led to real improvement) is itself measured and reported in the monthly strategic insights section of the executive dashboard.
