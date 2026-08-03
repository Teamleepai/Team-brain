# Testing Standards

Governs validation before anything ships. Subordinate to `MASTER_CONSTITUTION.md`.

## No feature is complete without

- **Unit tests** — cover core logic, edge cases, and error paths, not just the happy path.
- **Integration tests** — verify the module behaves correctly against its real (or realistically faked) dependencies.
- **End-to-end tests** — verify the user- or agent-facing workflow works as a whole.
- **Performance tests** — for anything on a hot path or with scale implications, establish a baseline and a regression threshold.
- **Failure tests** — deliberately inject failures (timeouts, malformed input, dependency outage) and confirm graceful degradation, not silent corruption.
- **Security review** — see `SECURITY_STANDARDS.md`; required for anything touching data, credentials, or external communication.
- **Documentation** — updated in the same change, not deferred.
- **Monitoring** — new failure modes get an alert or dashboard signal, not just a log line nobody watches (`OBSERVABILITY.md`).
- **Rollback plan** — a documented, ideally automated, path back to the previous known-good state.

## Agent-specific testing

- **Prompt regression tests**: every prompt change runs against a held-out evaluation set before promotion; a regression on any previously-passing case blocks promotion.
- **Simulation before autonomy**: before an agent advances a trust level (see `AI_AGENT_STANDARDS.md`), its proposed autonomous actions are simulated against historical scenarios and reviewed for unintended consequences.
- **Adversarial testing**: agents that ingest external content are tested against prompt-injection and malicious-input scenarios, not just well-formed ones.

## Definition of "tested"

A change is tested when its test suite (a) exercises the new behavior, (b) would fail if the change were reverted, and (c) runs in CI on every subsequent change — not just once locally at authoring time.
