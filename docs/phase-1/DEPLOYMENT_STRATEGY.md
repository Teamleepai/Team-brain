# Phase 1 — Deployment Strategy

**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

The Phase 1 instantiation of `DEPLOYMENT.md`. That document sets the principles — incremental, reversible, approval-gated for anything customer-facing, with a rollback path defined before rollout. This document says what those principles mean for a TypeScript service, a Supabase Postgres, one prompt, one agent, and one user. Rollback itself is specified separately in `ROLLBACK_STRATEGY.md`.

---

## 1. The shape of the problem at Phase 1

Phase 1 production has one user. That fact changes the deployment strategy in two opposite directions at once, and getting both right is the whole content of this document.

It makes some standard practice pointless. There is no population to canary into. A 5% rollout of one user is either 0% or 100%. Blue/green cutover protects against a bad deploy affecting many users mid-flight, and there are no many users and no mid-flight requests — the system is a scheduler and a batch job. Autoscaling protects against load that does not exist. Building any of it now would be complexity for its own sake, which `PRODUCT_PHILOSOPHY.md` forbids as firmly as it forbids technical debt.

It also makes some standard practice *more* important, not less. With one user, a bad deploy has 100% blast radius by definition, and there is no gradual-rollout mechanism to catch it. The compensating controls therefore have to sit earlier — in CI, in pre-send validation, and in the fact that every job can simply be re-run (`ROLLBACK_STRATEGY.md` §1). And the single user is the person whose trust is the actual Phase 1 deliverable (`PRD.md` §4), which means a deploy that produces one misleading briefing costs more than a deploy that produces an hour of downtime. `PRD.md` §6 records that this founder withdraws trust completely after two confidently-stated errors. Uptime is not the risk here. Correctness is.

The governing asymmetry, then: **be relaxed about availability and unyielding about correctness.** A missed briefing is recoverable by re-running a job. A wrong briefing is not recoverable at all (`ROLLBACK_STRATEGY.md` §4).

## 2. Environments

| Environment | Data | Credentials | Purpose | Who deploys |
|---|---|---|---|---|
| **Local / dev** | Synthetic fixtures only. Never production data, anonymized or otherwise. | None real | Fast iteration, unit and integration tests, adapter development | Anyone, continuously |
| **Staging** | Seeded synthetic org plus a second synthetic org for RLS adversarial tests | Live credentials with read-only scopes against a dedicated test Google/Slack account | E2E, migration rehearsal, prompt regression, live-credential validation, briefings sent to a test mailbox | CI on merge to `main` |
| **Production** | The founder's real data, one org | Live credentials, least scope required | One user, one briefing per weekday | CI on tag, after staging is green |

Three notes.

**Dev has no live credentials by design and by accident.** `ADR-0006` records that none exist yet, so all adapters are built against fixtures. That is a stated technical debt, not a strategy, and it is why every increment's exit gate requires live-credential validation (§7). The strategy part is that dev will *continue* to have no live credentials even after they exist: adapter development happens against fixtures, and live validation happens in staging against a dedicated test account, so that a developer's laptop is never a place where the founder's inbox can be reached.

**Staging must be production-like in the dimensions that actually bite.** Same Postgres major version, same extensions (`vector`, `pgcrypto`), RLS enabled with the same policies, same model IDs, same email provider in sandbox mode. Not the same instance size — that would be theatre at this volume, and nothing in Phase 1 is performance-sensitive enough for instance parity to buy information.

**"Anonymized data only" in dev needs to be read strictly.** `DEPLOYMENT.md` permits synthetic or anonymized data. At Phase 1 the honest position is synthetic only, because anonymizing an email corpus well is a project in itself and anonymizing it badly is a data leak that looks like compliance. The fixtures are hand-authored, including adversarial ones: the prompt-injection fixture required by `PRD.md` A1 and the low-ASR-confidence fixture required by A3 are fixtures, not production samples.

## 3. CI: what must pass before merge

Every gate below runs on every pull request and blocks merge. `TESTING_STANDARDS.md` §"Definition of tested" requires that a test run in CI on every subsequent change, not once locally, and this table is that requirement made concrete.

| Gate | What it proves | Why it blocks |
|---|---|---|
| `tsc --noEmit` strict | Types hold | The branded identifiers and non-empty tuples in `API_CONTRACTS.md` do real safety work; unchecked, they are decoration |
| Lint | `CODING_STANDARDS.md` conformance | |
| **Redaction lint rule** | No sensitive field name reaches `Logger` / `Metrics` / span attributes | `OBSERVABILITY_STRATEGY.md` §7 |
| **Layering lint rule** | No SQL outside `memory/repositories`; no import from `agents/*` into `authority/*`; no cycles | `ADR-0002` and `ARCHITECTURE.md` §3. A circular dependency is a build failure, not a warning |
| Unit tests | Core logic, edge cases, error paths | `TESTING_STANDARDS.md` |
| Integration tests | Repositories against a real Postgres, adapters against fixtures, gate against the substrate | |
| **RLS adversarial suite** | Cross-tenant reads from a synthetic second org fail | The single most dangerous surface in the schema (`ADR-0002`, `DATA_MODEL.md` §11). A policy exercised by one tenant has never been tested |
| **Migration policy check** | Every table with `org_id` has RLS enabled and at least one policy | §4 below |
| **Gate refusal suite** | An agent deliberately configured to attempt a Level 3 action is refused | `PRD.md` C1. Proving the gate refuses, not that a well-behaved agent never asks |
| **Two-permission-system test** | The gate holds on a path where the SDK *would* have permitted the action | `ADR-0003` technical debt item 1 |
| **Redaction emission test** | No sentinel from a fixture appears in any emitted log, tag, or span | `OBSERVABILITY_STRATEGY.md` §7 |
| E2E | Fixtures → ingestion → distillation → agent → gate → briefing → rendered email, with evidence links present on every item | `PRD.md` B2: an unsourced assertion is not shippable |
| Failure-injection tests | Timeouts, 429s, malformed payloads, model API errors degrade gracefully | `TESTING_STANDARDS.md`. Includes the watermark-held path, which is a correctness invariant |
| **Prompt regression suite** | Every previously-passing evaluation case still passes | Runs on any change to `prompt_version` content or agent contract; see §5 |
| **Secret scanning** | No credential in the diff or in history | `SECURITY_STANDARDS.md`. Includes prompt bodies — see §6 |
| Docs check | `API_CONTRACTS.md` updated in the same change when an interface changed | `MASTER_CONSTITUTION.md` §17, `DEFINITION_OF_DONE.md` |

Performance tests are required by `TESTING_STANDARDS.md` for anything on a hot path with scale implications. Phase 1 has no hot path, so the obligation is discharged as a *baseline* rather than a threshold: the E2E run records briefing generation duration and token cost, and CI fails if either exceeds 2× the recorded baseline. That catches the realistic Phase 1 performance regression, which is not latency but a prompt or retrieval change that silently triples context size and cost.

## 4. Migration discipline

**Migrations are forward-only.** There are no down migrations, and this is a considered position rather than a shortcut.

A down migration is a claim that the prior state can be restored, and for this schema that claim is false in the cases where it would matter. `audit_record` has `UPDATE` and `DELETE` revoked (`DATA_MODEL.md` §9) and `MASTER_CONSTITUTION.md` §11 classes deleting information as a high-impact action requiring approval; a down migration that dropped an audit column would be an unapproved deletion executed by automation. The semantic layer has no delete path at all by design. A migration framework that offers `down()` invites its use in exactly the emergency where it is least safe, and having the escape hatch present but forbidden by policy is weaker than not having it.

The cost of forward-only is that safety has to be designed in at authoring time. Every migration is therefore **expand-then-contract**, with the contract step in a later release:

| Change | Authored as |
|---|---|
| Add a column | Nullable or with a default, in one migration. Never `not null` without a default on a populated table |
| Rename a column | Add new, backfill, dual-write, switch reads, drop old in a *later* release |
| Change a type | Same as rename. Never in place |
| Drop a column or table | Only after a release in which nothing reads it, and only with explicit approval |
| Add a constraint | `not valid` first, validate separately, so a long validation does not hold a lock |

The practical rule: no single migration is both destructive and irreversible in the same deploy. If step one is destructive, the deploy is wrong, not brave.

### RLS deployment and verification

RLS policies are deployed in the same migration as the table they protect, in the same transaction. Not a follow-up migration, not a manual step, not a separate policy file applied afterward.

The reason is a specific asymmetry in how Postgres fails here. A table with RLS enabled and no policy denies everything to non-owner roles — loud, obvious, caught by the first test. A table with **RLS never enabled** returns every row to every caller, which looks exactly like a working system. `ADR-0002` and `DATA_MODEL.md` §11 both make this point: RLS fails permissively when it is wrong. The dangerous mistake is not writing a bad policy. It is forgetting to enable RLS at all.

So the build enforces it, twice:

1. **A static check** parses migration files and fails if any `create table` containing an `org_id` column is not accompanied, in the same migration, by `alter table … enable row level security` and at least one `create policy`.
2. **A runtime assertion** runs against staging and production after every migration, querying `pg_class.relrowsecurity` and `pg_policies` for every table possessing an `org_id` column, and fails the deploy if any table lacks either. This catches what the static check cannot: a table created by a tool, a hand-run statement, or a Supabase dashboard action.

Then the adversarial suite from §3 attempts actual cross-tenant reads against a synthetic second org. The three layers answer three different questions — did we write the policy, is the policy live, does the policy work — and none substitutes for the others.

A migration adding a tenant-scoped table without an RLS policy must fail the build because the alternative is a silent, indefinite cross-tenant read path in a system whose entire multi-tenant story rests on RLS being the backstop beneath application scoping. There will be exactly one tenant when the mistake is made and no test will notice, and it will be discovered by the second customer.

### Migration deployment order

Because expand-then-contract makes every migration backward-compatible with the currently-running code, migrations run **before** the application deploy. The old code continues to work against the new schema, so the ordering is safe and there is no window in which the app expects a column that does not yet exist.

## 5. Prompt and agent deployments

`DEPLOYMENT.md` requires that prompt changes and trust-level advancements get the same rigor as code. At Phase 1 they get *more*, because they are the only components whose behavior cannot be verified by reading them.

### A prompt deployment is a database write, and it is still a deployment

Prompts live in `prompt_version` (`DATA_MODEL.md` §8), with `rationale` non-null and at most one active version per agent enforced by the `one_active_prompt_per_agent` partial unique index. The full path:

| Step | Requirement |
|---|---|
| 1. Author | New row in `prompt_version`, `version` incremented, `activated_at` null. `rationale` states the failure pattern it targets, per `CONTINUOUS_IMPROVEMENT.md` |
| 2. Review | Prompt diff reviewed like code, in a pull request, because the prompt body is checked into the repository and seeded into the database by migration — not typed into a SQL console |
| 3. Regression | Full evaluation set. A regression on any previously-passing case blocks promotion (`TESTING_STANDARDS.md`) |
| 4. Shadow | Generate the next briefing under both versions and diff (below) |
| 5. Approve | Founder approval. This is a §11 high-impact change (below) |
| 6. Activate | One transaction: set `deactivated_at` on the current active row, set `activated_at` on the new one. The partial index makes a two-active-version state unrepresentable |
| 7. Record | Change record per `DEPLOYMENT.md`, linked to the `prompt_version` row |
| 8. Watch | Compare item count, flag count, and token cost against the prior version's trailing average for five briefings |

**Step 4 is the Phase 1 substitute for a canary, and it is a better one.** `DEPLOYMENT.md` asks for incremental rollout, which normally means splitting a population. One user cannot be split. What *can* be split is time and output: run the new prompt version against the same retrieved context as the live version, compose both `BriefingDocument`s, render neither, and diff them. Because composition is separated from rendering and delivery (`ADR-0004`, `ARCHITECTURE.md` §7), producing a briefing without sending it is a natural operation rather than a special mode. The diff shows exactly what the founder's next briefing would gain and lose. This is genuinely more information than a 5% canary provides, and it is available only because the architecture kept composition pure.

Shadow generation costs one extra model call per prompt change. That is the entire cost, and it should be run for every prompt change without exception.

### A prompt change affecting the founder's briefing is a §11 high-impact change

`MASTER_CONSTITUTION.md` §11 lists "prompt changes affecting customers" among the actions always requiring approval. Phase 1 has one customer and every prompt affects him, so **every** prompt change to the Chief of Staff agent requires founder approval before activation. There is no low-impact prompt change in Phase 1.

The awkwardness is worth naming: the approver and the affected customer are the same person, which makes the approval feel ceremonial. It is not. The approval artifact is a record of what changed, why, and what the shadow diff showed, and its value is that a later trust-level decision can be argued from it. A prompt that changed for reasons nobody wrote down cannot be evaluated against its intent later, which is exactly why `rationale` is a non-null column and not a commit message.

The same clause makes changes to `TrustGate` or `AgentContract` approval-gated, per `API_CONTRACTS.md` §10, on the grounds that they alter what the system is permitted to do and are therefore security changes.

### Trust-level advancement is a deployment event

Advancing the Chief of Staff agent from Trust Level 1 requires its own approval and its own evidence, and it is a deployment even though it may not involve a code change:

| Requirement | Source |
|---|---|
| Simulation of proposed actions against historical scenarios, reviewed for unintended consequences | `TESTING_STANDARDS.md` |
| An evidence pack from observability: refusal history, flag history, acceptance rate, explainability audit results | `OBSERVABILITY.md`, `OBSERVABILITY_STRATEGY.md` §4 |
| `explain()` answering all five questions for a sample of items | `OBSERVABILITY_STRATEGY.md` §4 |
| Explicit founder approval, recorded | `MASTER_CONSTITUTION.md` §11 |
| A change record naming the prior level, the new level, and the evidence | `DEPLOYMENT.md` |
| A revocation path that does not require a code deploy | `ROLLBACK_STRATEGY.md` §4 |

Phase 1 will not advance a trust level — the phase is defined as Levels 0–1 and `ROADMAP.md` puts Level 2 in Phase 2. The machinery is specified here anyway, for the reason `PRD.md` §4 gives for the gate itself: build and exercise it while the stakes are zero, so that the first real advancement runs a path that already works.

The last row is a Phase 1 obligation with teeth. If an agent's trust level is a constant in TypeScript, revoking it requires a build, a test run, and a deploy. It should be a value read at gate time from the agent contract's persisted configuration, so that revocation is a single write. See `ROLLBACK_STRATEGY.md` §4.

## 6. Secrets

`SECURITY_STANDARDS.md` is unambiguous: secrets live in a secrets manager, and agents reference them by name, never by value. The schema already encodes this — `source_connection.secret_ref` is a name, and `DATA_MODEL.md` §5 states the reasoning plainly: a column that *can* hold a credential eventually will, and then it is in every backup, so the column that would have held it does not exist.

| Concern | Phase 1 handling |
|---|---|
| Where secrets live | The platform secrets manager (Supabase secrets for database-adjacent config; the host platform's secret store for runtime env). One store, not two conventions |
| How code gets them | A `SecretResolver` interface taking a `secret_ref` name and returning a value, with no caching to disk. Resolution failure emits `security.secret_resolution_failed` and fails closed |
| What is in the repository | Reference names, never values. `.env.example` lists names only |
| CI secrets | Provided by the CI platform's secret store, scoped per environment; staging credentials cannot reach production |
| Rotation | Rotate by updating the value behind the existing `secret_ref`. No schema change, no code change, no deploy. This is the practical payoff of reference-by-name |
| Detection | Secret scanning in CI on the diff and on history; a hit blocks merge |
| OAuth scopes | Least privilege per `SECURITY_STANDARDS.md`. Phase 1 is read-only across every source, because Phase 1 executes nothing. A write scope requested at Phase 1 is a design error, and the scope list is reviewed at each increment gate |

One Phase-1-specific trap. `prompt_version.body` is a text column in Postgres, read by the agent at runtime, and included in every database backup. A credential pasted into a prompt is therefore a credential in every backup and in every audit export, and secret scanning of the *repository* will not catch it if the prompt was edited in the database. Two mitigations: prompt bodies are authored in the repository and seeded by migration so they pass through secret scanning like any other file, and the redaction emission test from §3 treats prompt bodies as sensitive content that must not be logged.

## 7. Release cadence and increment gating

Two different rhythms operate at once, and conflating them is how a phase gate quietly becomes a calendar date.

**Code releases are continuous and small.** Merge to `main` deploys to staging automatically. A tagged release deploys to production. Deploys happen after the day's briefing has been delivered, never in the hour before it, because the briefing is the only production workload with a deadline and there is no reason to overlap the two. A deploy that must happen before tomorrow's briefing has a full day of staging exposure available to it; use it.

**Increments are gated milestones.** Per `ADR-0006` and `PRD.md` §8, 1a (Google Workspace), 1b (voice), 1c (Slack) ship in sequence, each with its own exit gate, each shipping a working briefing.

Each increment's exit gate:

| # | Gate | Notes |
|---|---|---|
| 1 | Full CI suite green, including the adversarial and regression suites | §3 |
| 2 | **Live-credential validation** against a real account for that increment's source | Not fixture-passing tests. See below |
| 3 | Briefing quality attributable to that source, judged over a minimum observation window | `ADR-0006`: the gate is quality attributable to the source, not "the adapter runs" |
| 4 | Zero unresolved critical risk register items for that increment | `DEFINITION_OF_DONE.md` |
| 5 | Threat model and privacy model updated for the new source | `SECURITY_STANDARDS.md`: every new capability touching customer data gets a threat model |
| 6 | Retention policy confirmed for the new episodic kind | `DATA_MODEL.md` §12 |
| 7 | Observability complete: source appears in the per-source freshness tile, error attribution tags flow, consecutive-failure alert configured | `OBSERVABILITY_STRATEGY.md` §9 |

Gate 2 is the one that carries the real risk and it deserves its own statement. `ADR-0006` records that no live credentials exist and that all adapters are built against fixtures, and it names precisely where fixtures lie: real-world pagination, rate limits, malformed payloads, and authentication edge cases. Those are the four things that will break, and none of them can be discovered by a test suite that passes. Live-credential validation for an increment specifically requires:

- A multi-page fetch that actually paginates, verified against a corpus larger than one page.
- An observed rate-limit response, provoked deliberately if necessary, with the backoff path exercised and `retryAfterMs` honored.
- A token expiry and refresh cycle completed.
- A revoked-credential path producing `security.source_auth_failed` and the consecutive-failure alert rather than a silent stall.
- Cursor semantics verified across a restart: stop mid-run, resume, and confirm no gap and no duplicate. Gmail `historyId` and Calendar `syncToken` have genuinely different expiry and invalidation behavior, and both can become invalid in ways a fixture will never reproduce.

Phase 1 as a whole exits on the composite criteria in `PRD.md` §9, measured after 1c lands. Increment gates are necessary and not sufficient.

## 8. Deliberately not built

Naming these matters as much as naming what is built, because each is a defensible engineering practice whose absence could be mistaken for carelessness.

| Not built | Why that is correct at Phase 1 | What would change the answer |
|---|---|---|
| Blue/green or rolling deploys | The production workload is a cron-triggered batch job with no in-flight user requests. There is nothing to drain and no session to preserve. A restart between briefings is invisible | A synchronous user-facing surface — the Phase 2 dashboard or an approval endpoint |
| Canary by population | One user cannot be a percentage. Shadow generation (§5) provides strictly more information than a 100%-or-nothing canary would | The second user |
| Autoscaling | One briefing a day and a fifteen-minute ingestion cycle. Provisioning for load that does not exist is the premature optimization `PRODUCT_PHILOSOPHY.md` forbids | Sustained resource pressure, measured, not anticipated |
| Multi-region | One user in one timezone. Multi-region doubles the operational surface and introduces data-residency questions the privacy model has not yet answered | An enterprise customer with a residency requirement, in Phase 4 |
| A feature-flag service | Flags at Phase 1 are configuration rows and environment variables. A flag service is infrastructure for coordinating flags across teams, and there are no teams | More than one deployable service, or flags that must change without a deploy |
| Kubernetes or a custom orchestrator | A managed container runtime plus managed Postgres. The interesting complexity in this system is the authority layer, and every hour spent on cluster configuration is an hour not spent there | Multiple services with distinct scaling profiles |
| A read replica | `ADR-0002` names it as the conventional answer to analytical load, and explicitly defers it as premature | Measured contention between briefing generation and ingestion |

The distinction to hold onto: everything above is deferred because it addresses **scale**, and Phase 1 has none. Nothing is deferred that addresses **correctness**. RLS policies, the adversarial suite, forward-only migration discipline, append-only audit, the gate refusal suite, prompt regression testing, and secret management are all built now at full strength, at one user, because they are the things that are impossible to retrofit honestly and dangerous to discover missing. `ENGINEERING_STANDARDS.md` asks us to design as if the system will grow to millions of users; that obligation lands on interfaces, schema, and enforcement boundaries, not on provisioning capacity nobody needs.

## 9. Change records

Every production deployment writes a change record, per `DEPLOYMENT.md`: what changed, why, who approved it, and its observed impact. At Phase 1 this is the git tag plus release notes for code, and the `prompt_version` row plus its `rationale` for prompts, joined by a deployment log entry carrying `commit_sha`, timestamp, migrations applied, prompt versions activated, approver, and a link to the shadow diff where one exists.

`MEMORY_ARCHITECTURE.md` names commits and prompt versions among the categories organizational memory must hold, and `CONTINUOUS_IMPROVEMENT.md` requires that every deployed improvement be tracked against its original hypothesis's success criteria. Phase 1 does not close the learning loop (`PRD.md` §3), but the change record is the input the loop will need, and it is cheap now and unreconstructable later.

## 10. Residual risks and open questions

**Fixture-validated adapters are the largest deployment risk in Phase 1.** Carried from `ADR-0006` and `ARCHITECTURE.md` §11. Gate 2 in §7 is the mitigation and it is not a complete one, because live validation against a test account still is not live validation against the founder's actual mailbox volume and history. Expect at least one adapter defect to surface only in production, and expect it to be a cursor or pagination defect.

**The approver is the affected party.** Every §11 approval in Phase 1 is the founder approving a change to his own briefing. This is structurally weak review and there is no fix available at one person. The compensating control is that the *artifact* is mandatory even when the conversation is trivial, so a later reviewer has something to read.

**No production database restore has been rehearsed.** A backup that has never been restored is a hypothesis. `ROLLBACK_STRATEGY.md` §6 specifies the procedure and the audit-preservation problem it must solve; rehearsing it against staging belongs in increment 1a, not later.

**Open: hosting platform for the Node service.** Supabase settles persistence (`ADR-0002`) but not compute. The choice interacts with §6 (secret store), §7 (deploy trigger), and the scheduler's reliability, which the P1 delivery alert depends on. A platform whose scheduler can silently skip an invocation is disqualified, and that property is worth checking specifically rather than assuming.

**Open: transactional email provider.** `PRD.md` open question 4. It gates increment 1a delivery and determines what open tracking is even possible, which `OBSERVABILITY_STRATEGY.md` §10 already flags as the weakest measurement in Phase 1.

**Open: how prompt bodies are seeded.** §5 asserts prompts are authored in the repository and seeded by migration, which keeps them under review and secret scanning. That conflicts slightly with prompts being live-editable data in the procedural layer, and the tension resolves toward the repository for Phase 1 only because no automated process writes prompts yet. When the Phase 3 learning loop proposes prompt changes, the source of truth must be the database and the review path has to move with it. Worth deciding before the loop exists rather than during.
