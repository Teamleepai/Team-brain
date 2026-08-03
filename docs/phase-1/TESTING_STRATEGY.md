# Phase 1 — Testing Strategy

**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

Companion to `PRD.md`, `ARCHITECTURE.md`, `DATA_MODEL.md`, and `API_CONTRACTS.md`. This document is the Phase 1 instantiation of `TESTING_STANDARDS.md` and the quality bar in `MASTER_CONSTITUTION.md` §16. It does not restate those standards; it says what they mean for *this* system, where the hard parts are, and what specific suites exist.

---

## 1. What Phase 1 actually has to prove

Ordinary feature testing asks "does the code do what it says." Phase 1 has three obligations beyond that, and they determine everything below.

**The authority layer must be proven to refuse.** `ARCHITECTURE.md` §1 stakes the whole design on one sentence: the model decides what to propose, deterministic code decides what is permitted. A permission system that has only ever been observed agreeing with the thing it wraps has not been tested. The gate suite is therefore built around *deliberate misbehavior*, not around confirming good behavior.

**Tenant isolation must be proven adversarially.** `ADR-0002` and `ADR-0005` both name Row-Level Security as the most dangerous surface in the system, for the same reason: it fails permissively and silently. Wrong RLS looks exactly like working RLS from inside the only tenant that exists.

**Correctness has to be tested where the exit criterion lives.** `PRD.md` §9 requires zero misleading recommendations over 14 consecutive weekdays, and a failure resets the window. That is not a test-suite outcome — no suite can assert "not misleading." What the suite *can* do is eliminate the mechanical causes of misleading output: duplicated or collapsed semantic records, briefing items citing the wrong evidence, low-confidence transcript facts leaking into the briefing, a silently stalled source producing a quietly incomplete briefing. Every one of those is a deterministic bug wearing a quality-problem costume, and each gets a named suite below.

A fourth obligation is temporal rather than technical. The gating and audit machinery is built in Phase 1 specifically so that Phase 2's first real action runs through a path with weeks of production history (`PRD.md` §4). That only pays off if the Phase 1 tests are the tests Phase 2 inherits. Suites here are written against the interfaces in `API_CONTRACTS.md`, not against Phase 1 implementations, so that adding the `draft` and `queued_for_approval` dispositions extends a truth table rather than rewriting a suite.

## 2. Pyramid shape

The conventional pyramid assumes the expensive tests are the slow ones. Here the expensive tests are the *non-deterministic* ones, which changes the shape: this system has an unusually fat unit layer, a substantial integration layer against real Postgres, a thin deterministic E2E layer, and a separate evaluation tier that is not part of the pyramid at all because it does not pass or fail in the same sense.

```mermaid
flowchart TB
    EVAL["<b>Evaluation tier</b> — agent quality<br/><i>statistical, thresholded, not pass/fail per run</i><br/>prompt regression over an eval set + held-out set"]
    E2E["<b>E2E</b> — fixtures in, rendered briefing out<br/><i>deterministic because the agent is stubbed</i>"]
    INT["<b>Integration</b> — real Postgres, real RLS, real constraints<br/><i>repositories, invariants, idempotency, tenant isolation</i>"]
    UNIT["<b>Unit</b> — pure logic<br/><i>trust gate truth table, dedupe_key, ranking,<br/>watermark arithmetic, renderers, normalizer validation</i>"]

    UNIT --> INT --> E2E
    EVAL -.->|"gates promotion,<br/>not merge"| E2E
```

| Level | Runs against | What belongs here | Latency budget |
|---|---|---|---|
| Unit | No I/O at all | Trust gate dispositions, `dedupe_key` derivation, prioritization and ranking, empty-section elision, watermark advance logic, runtime schema validation, email/text renderers, redaction helpers | Whole layer under 30s |
| Integration | Real Postgres (ephemeral, migrated) | Repository contracts, RLS policies, commit-time triggers, unique constraints, supersession atomicity, gate-plus-audit as one transaction, adapter-against-fixture-server | Whole layer under 5 min |
| E2E | Fixture sources + stubbed agent + real database + captured mail transport | Scheduler → ingest → distill → propose → gate → compose → render → deliver, plus the failure-notice path | Under 3 min |
| Evaluation | Real model, curated inputs | Briefing quality, prompt regressions, injection resistance in the model's actual behavior | Minutes; runs on prompt change and nightly |

Two deliberate departures from the default.

**Postgres is not mocked, ever.** Five of the constitution's memory guarantees are enforced by database constraints rather than application code (`DATA_MODEL.md` §1). A mocked repository tests the mock's opinion of those guarantees. Every repository test runs against a migrated ephemeral Postgres with RLS enabled, because the thing under test *is* the schema.

**The agent is stubbed in E2E and exercised only in the evaluation tier.** An E2E test that calls the real model is a test whose failures you cannot attribute and whose passes you cannot trust. Stubbing the agent at the `AgentSubstrate` boundary (`API_CONTRACTS.md` §5) makes the pipeline deterministic end to end, which is what lets E2E assert exact rendered output. Agent quality is a separate question measured separately.

## 3. The trust gate

This is the most important suite in Phase 1 and it is pure unit-level work, which is fortunate, because it means exhaustiveness is affordable.

### 3.1 A purity seam is required first

`ARCHITECTURE.md` §5 specifies the gate as a pure function:

```
disposition = gate(proposal.impactClass, agent.trustLevel, policy)
```

`API_CONTRACTS.md` §6 specifies `TrustGate.evaluate` as async, returning a `Result<GateDecision>`, and also states that authorizing and logging are the same operation. Both are right about what they want, and they are not the same function. The implementation must therefore be two things: a pure, synchronous `decide(impactClass, trustLevel, policy) → Disposition` with no I/O, and an `evaluate` wrapper that validates the proposal's well-formedness, calls `decide`, writes the audit record, and returns the decision. The wrapper is the only exported path from proposal to effect, so the architectural guarantee holds. The seam exists so the truth table can be tested exhaustively in microseconds without a database, and so nobody is tempted to skip cases because the setup is expensive.

This is flagged as an inconsistency between the two documents in §14; the resolution above is the recommendation.

### 3.2 Exhaustive truth table

Six impact classes (`DATA_MODEL.md` §9) across six trust levels (`MASTER_CONSTITUTION.md` §10) is 36 cells. The suite asserts all 36 as an explicit table in the test file, not as a loop over the implementation's own policy object — a test that derives its expectations from the code under test asserts nothing. The table is transcribed by hand from `ARCHITECTURE.md` §5 and reviewed as a document, because it *is* the permission model.

| Impact class | Trust 0 | Trust 1 | Trust 2 | Trust 3 | Trust 4 | Trust 5 |
|---|---|---|---|---|---|---|
| `observation` | logged | logged | logged | logged | refused¹ | refused¹ |
| `recommendation` | discarded + alert | **surfaced** | surfaced | surfaced | refused¹ | refused¹ |
| `draft` | refused | **refused** | drafted | drafted | refused¹ | refused¹ |
| `reversible_action` | refused | **refused** | refused | queued_for_approval | refused¹ | refused¹ |
| `irreversible_action` | refused | **refused** | refused | refused | refused¹ | refused¹ |
| `high_impact` | refused | **refused** | refused | queued_for_approval | refused¹ | refused¹ |

¹ `ARCHITECTURE.md` §5 specifies policy for trust levels 0–3 only. Levels 4 and 5 have no Phase 1 policy row, and the gate must therefore **refuse them entirely rather than extrapolating**. This is the fail-closed rule applied to its own configuration, and it is worth a dedicated test with a comment explaining why the twelve cells are not "unimplemented": an unspecified authority level is not a permissive one. When Phase 3 defines those rows, the test table changes in the same commit as the policy.

Bold cells are Phase 1's live configuration. Everything else is tested now and exercised later, which is the point of building the machinery while the stakes are zero.

### 3.3 Negative cases the table does not cover

`API_CONTRACTS.md` §6 lists five refusal conditions beyond the class-versus-level matrix. Each gets its own case, and each asserts three things: disposition is `refused`, `refusalReason` is populated (the `refusal_has_reason` constraint in `DATA_MODEL.md` §9 makes an empty reason unstorable), and an alert was emitted.

| Input | Expected |
|---|---|
| `impactClass` absent | refused, reason names the missing field |
| `impactClass` an unrecognized string (e.g. `"urgent"`, `"RECOMMENDATION"`, `""`) | refused — no coercion, no case-insensitive match, no nearest-neighbour guess |
| `evidence` empty, class `recommendation` | refused (`PRD.md` B2) |
| `rationale` empty or whitespace | refused |
| Proposal references a tool absent from `permittedTools` | refused |
| Proposal well-formed but `contract.trustLevel` absent or out of range | refused |

The unrecognized-class cases matter more than they look. A gate that normalizes `"RECOMMENDATION"` to `recommendation` has begun interpreting model output, and the next normalization will be the one that maps something to a permissive class. The test exists to make that regression fail loudly.

### 3.4 Proving the gate refuses a misbehaving agent

`PRD.md` C1 requires this explicitly, and it is the difference between having a permission system and believing you have one.

The suite includes an agent fixture — `rogue-cos` — declared at Trust Level 1 with a stub substrate that returns proposals with `impactClass: 'reversible_action'` and `impactClass: 'irreversible_action'`, complete with plausible payloads, well-formed evidence, and confident rationale. It is a deliberately misconfigured agent doing exactly what a compromised or model-erred agent would do: asking for more than it is allowed.

Asserted:

1. Every above-level proposal is refused. None reaches the composer.
2. Each refusal produces an `agent_proposal` row with `disposition = 'refused'` and a non-null `refusal_reason`, and an `audit_record` — refusals are audited, not dropped.
3. A refusal alert fires (`OBSERVABILITY.md`).
4. The briefing composed in the same run contains only the permitted `recommendation` items. A refused proposal does not poison the run, because a run that aborts on refusal is a denial-of-service vector reachable from ingested content.

**Why testing well-behaved agents does not test a gate.** A gate has exactly one job: to say no to something that asked. If every input the suite provides is something the gate would permit anyway, the suite is satisfied by an implementation of `decide` that is `return 'surfaced'` — literally a function with the refusal logic deleted. That implementation passes a well-behaved-agent suite completely. It also passes if the policy table is loaded from the wrong file, if a typo makes the class comparison always fall through to the permissive branch, or if someone reverses an inequality. The only test that distinguishes a gate from a pass-through is one where the input is refused, and the only test that distinguishes a *correct* gate is one where refusal is asserted across the whole boundary rather than at one sampled point. This is also the mechanical answer to the erosion risk in `ARCHITECTURE.md` §11: an agent quietly handed a tool "just for this" fails the `rogue-cos` suite, because the suite asserts what the gate refuses rather than what the current agents happen to ask for.

## 4. The two-permission-systems seam

`ADR-0003` records this as a carried obligation: the Claude Agent SDK has its own notion of tool permissions, we layer ours above it, and a mismatch could hide in the gap. The specific danger is not that both systems refuse — that is fine and invisible. It is that a future SDK default, a permissive tool registration, or an MCP connector's own scope makes an action *available at the substrate level*, and our gate is the only thing standing between that availability and an effect.

A gate tested only on paths where the layer beneath it also refuses has not been tested. So the suite constructs the disagreement deliberately:

1. An agent contract declared at Trust Level 1 with `permittedTools` containing read-only memory tools only.
2. A substrate stub configured to make an execution-capable tool *available and successfully invocable* — the SDK layer permits it, no error, no refusal.
3. The agent proposes an action using it.

Asserted: our gate refuses, the audit record exists, the alert fires, and no effect occurred. Then the same scenario at the construction boundary: `ToolScoper.scope` is asserted to return a tool set that does not contain the execution tool even when the substrate would offer it, because `ARCHITECTURE.md` §5 puts the primary defense at construction and the gate second. Both layers are asserted independently, since the value of defense in depth is entirely in each layer holding when the other does not.

One further case, cheap and worth having: assert that the tool set handed to the agent is exactly the contract's list, by set equality rather than by containment. `expect(tools).toContain(...)` passes when the SDK has silently added three more.

## 5. RLS adversarial testing

### 5.1 Why this suite exists at all

Phase 1 has one organization. Every legitimate query in every other test passes with RLS enabled, and would pass equally with RLS disabled, with a policy of `using (true)`, or with a policy referencing a session variable that is never set and silently coerces to permissive. All four states are indistinguishable from inside a single tenant. This is precisely the observation in `ADR-0005`: a tenant-scoped schema whose policies have only ever been exercised by one tenant provides *the appearance* of isolation without evidence of it, and the appearance is more dangerous than the absence, because it stops anyone from checking.

RLS also fails in the worst available direction. A too-restrictive policy produces an empty result and someone notices within minutes. A too-permissive policy produces correct-looking results forever, and the first time anyone finds out is when a second tenant exists and reads the first tenant's inbox. There is no error, no log line, no metric. The failure is a successful query.

### 5.2 The synthetic second organization

`ADR-0005` requires isolation to be *proven* against a synthetic second org that exists only in tests. Concretely, the integration fixture seeds two organizations, `org_alpha` and `org_beta`, each with a user, a source connection, and a populated set of episodic, semantic, procedural, briefing, proposal, and audit records with overlapping shapes — same participant email addresses, same `source_id` values, similar statements. Overlap is load-bearing: identical `source_id` across two orgs proves the unique constraint is scoped rather than global, and identical `dedupe_key` proves the same for the semantic layer.

For every table carrying `org_id`, and generated so that adding a table without adding tests is a failure:

| Attempt as `org_alpha` | Required outcome |
|---|---|
| Select `org_beta` rows | Zero rows. Not an error — zero rows, which is what RLS does. |
| Select by known `org_beta` primary key | Null result |
| Update an `org_beta` row | Zero rows affected |
| Delete an `org_beta` row | Zero rows affected, or privilege error where DELETE is revoked |
| Insert a row with `org_id = org_beta` | Rejected by policy `with check` |
| Vector similarity search whose nearest neighbour is an `org_beta` record | `org_beta` record absent from results |
| Recursive CTE traversal from an `org_alpha` record along an edge crossing into `org_beta` | Traversal terminates at the boundary |
| Aggregate count over each table | Matches `org_alpha`'s seeded count exactly |

The last three are where real bugs live. Similarity search is the query most likely to be written outside the repository layer's discipline during a debugging session, `hnsw` index scans do not care about policies, and a leak there surfaces as another tenant's content inside a briefing. Recursive traversal is the second: a CTE that re-enters the table can pick up rows the policy would have excluded on a plain select if the query is run in a context with elevated privilege.

### 5.3 Two structural tests

**The metatest.** A test enumerates `information_schema` for every table with an `org_id` column and asserts (a) `relrowsecurity` is true, (b) at least one policy exists, and (c) the table appears in the adversarial matrix above. A table added in Phase 2 without a policy fails a test on the day it is added, rather than in Phase 4 during a security review. This is the "re-verification whenever a table is added" obligation from `ADR-0002` made automatic instead of remembered.

**The privilege test.** All RLS tests run as the same non-superuser role the application uses. Supabase's service role and the migration role bypass RLS by design. A suite that connects as either proves nothing at all while producing a full green run, which is the most expensive possible test outcome. The connection role used by the RLS suite is asserted explicitly at suite setup, and the assertion includes a negative control: with the session variable `app.current_org_id` unset, reads return zero rows rather than everything. If that control passes when it should fail, the suite is misconfigured and says so.

## 6. Testing non-deterministic agent output

`ADR-0003` accepts plainly that the agent loop is not reproducible and that identical inputs may yield differently-worded proposals. The testing consequence follows directly, and it is worth stating in the sharpest available form: **golden-file testing of agent output is impossible, and anyone expecting it will be correctly disappointed.** A committed expected-briefing fixture will fail on the next run for reasons that have nothing to do with any change, and a suite that fails for reasons unrelated to changes is a suite people disable.

What is testable is everything around the prose. Assertions target **structure** and **permissibility**, never text.

| Assertable | Not assertable |
|---|---|
| Every proposal carries a recognized `impactClass` | The wording of `rationale` |
| Every proposal has non-empty `evidence` | Which of several valid framings the headline uses |
| Every evidence ref resolves to a record that exists, in this org, and is not superseded | Item ordering among items of genuinely equal priority |
| Every surfaced item's disposition matches the gate table for its class and level | The exact count of items on a given day |
| No item derives from a semantic record below the confidence floor | Whether the model chose to mention a marginal item |
| `item_count` within the configured band, and section kinds drawn from the enum | Phrasing of the section summary |
| The output parses as valid `Proposal[]` under runtime validation | — |
| No proposal references a tool outside `permittedTools` | — |

One structural assertion deserves emphasis because it is the mechanical guard against the worst class of misleading recommendation: **evidence must resolve, and it must resolve to records that actually support the item.** An item citing a superseded record, a record from a different date window, or a record whose `dedupe_key` collapsed two distinct facts is a confidently-wrong briefing item produced by correct-looking code. That check is deterministic, cheap, and runs on every generated briefing in E2E and in production as a post-generation invariant, not only in tests.

### 6.1 Prompt regression as a statistical gate

`TESTING_STANDARDS.md` requires that every prompt change run against a held-out evaluation set before promotion, and that a regression on any previously-passing case blocks promotion. The Phase 1 mechanics:

- **Evaluation set.** Curated scenarios, each a fixed set of episodic and semantic records plus a rubric of assertions over the resulting `BriefingDocument`. Rubric items are structural where possible ("the commitment from the Tuesday call appears in `open_commitments`", "the low-ASR-confidence fact does not appear anywhere") and judged where not.
- **Held-out set.** A subset never used while iterating on a prompt. Its only purpose is to detect the prompt having been fitted to the visible cases, which is the specific failure mode that makes an evaluation set stop meaning anything. Held-out cases are rotated in and replaced, not reused after exposure.
- **Repetition.** Each case runs *n* times (n = 5 at Phase 1 volume) and reports a pass rate. A single run of a non-deterministic system is a sample, not a result. Flakiness within a case is itself a signal: a case that passes three times in five is a case the prompt does not reliably handle, regardless of the aggregate.
- **Promotion rule.** Aggregate pass rate must not decrease, *and* no case that previously passed at 5/5 may drop. The second condition is the one that matters and it is the one `TESTING_STANDARDS.md` states: aggregate improvement that trades away a previously-solid case is a regression, because the founder experiences the individual case and not the aggregate. A promotion blocked this way requires either fixing the prompt or an explicit, recorded decision to accept the regression, written into `prompt_version.rationale` (`DATA_MODEL.md` §8).
- **Where it runs.** Not in the merge gate — a non-deterministic, model-cost-incurring suite blocking every commit would be routed around within a week. It gates *promotion of a prompt version*, which is the mechanism `DEPLOYMENT.md` already requires, plus a nightly run to catch drift in the underlying model with no change on our side.

Model drift with no local change is a real and easily-missed failure. The nightly run against a fixed evaluation set is the only instrument that detects it, and its alert is worth having even though the fix is not ours.

## 7. Idempotency

`API_CONTRACTS.md` §8 makes `idempotent: true` a literal type — a precondition for being schedulable rather than a claim a job makes. The suite has to earn that.

**Ingestion.** Run against an overlapping window and assert zero duplicates, exercising the unique constraint on `(org_id, source_connection_id, source_id)` (`DATA_MODEL.md` §6) rather than any application-level check.

| Scenario | Assertion |
|---|---|
| Same window twice | Second run: `written = 0`, `duplicatesSkipped = n`, episodic count unchanged |
| Overlapping windows (50% overlap) | Total records equal the union, not the sum |
| Re-fetch of a *mutated* record (edited calendar event, same `source_id`) | Upsert updates payload, `content_hash` changes, `ingested_at` advances, `occurred_at` and identity are stable, and no second row appears |
| Concurrent runs over the same window | No constraint-violation crash; one writer wins, the other reports duplicates |
| Re-run after a mid-page failure | Records from the failed page are written on the retry; already-written records are not duplicated |

The mutated-record case is the interesting one, and it is the reason `content_hash` exists. It also exposes a design question §14 records: an updated episodic record may already have semantic records derived from it, whose statements are now potentially wrong. Distillation must be re-triggered on content-hash change, and this suite is where that is asserted.

Concurrency is not hypothetical even at one user. A 15-minute schedule (`ARCHITECTURE.md` §8) plus a manual re-run during debugging produces overlap, and the ingestion path must survive that without a page in the middle of the night.

**Briefing generation.** Idempotent per `(org, recipient, date)`, backed by the unique constraint in `DATA_MODEL.md` §10.

| Scenario | Assertion |
|---|---|
| Generate twice for the same date | One `briefing` row; no duplicate email is sent |
| Re-generate after new records arrived | Either a stable no-op or an explicit regeneration that replaces items and records why — asserted against whichever is chosen, never left ambiguous |
| Generate for the same date across two recipients (Phase 2 shape) | Two rows, no collision |
| Delivery succeeded but the `delivered_at` write failed | Retry does not send a second email |

That last row is the durable-side-effect problem: the send is not transactional with the database write, so "did we already send" cannot be answered by the absence of a timestamp. Phase 1's answer is an idempotency key on the transactional-email provider derived from `(org_id, recipient_id, briefing_date)`, asserted in the delivery suite with a captured transport. This is a small detail with a large user-visible failure attached — two briefings in one morning is a credibility event, not a cosmetic bug.

## 8. Memory invariants

These are integration tests against real Postgres, because the invariants are constraints and triggers (`DATA_MODEL.md` §1). Each is tested by attempting the violation and asserting the database refuses.

**No orphan semantic records.** Enforced by a deferred constraint trigger at commit. Insert-time enforcement is impossible since the record must exist before it can be linked, so the tests must be transaction-aware:

- Insert a `semantic_record` with no `semantic_link`, commit → transaction fails.
- Insert record, then link, then commit → succeeds. This proves the trigger is genuinely deferred and not merely absent.
- Insert record and link, then delete the link, then commit → fails.
- Insert record, link, and a *second* record with no link in the same transaction → fails, and the first record is not persisted either. Partial success would leave an orphan.
- `SemanticRepository.create` called with an empty `derivedFrom` → rejected at the type level and, for the runtime path, at the repository boundary. `API_CONTRACTS.md` §4 makes an orphan inexpressible in the interface; the test covers callers that route around the type via `any` or dynamic input.

**Supersession.** The `supersession_closes_validity` check constraint forbids the half-state where a record is pointed forward but still reads as valid. It is deliberately one-directional, so the test suite must cover both legal shapes: superseded with a successor and a closed window, and expired with a closed window and no successor.

- `superseded_by` set with `valid_until` null → rejected.
- `valid_until` set with `superseded_by` null → rejected. (Worth noting this constraint also forbids a record that legitimately expires without a successor — a commitment whose due date passes. §14 records this as a design question rather than papering over it in the test.)
- `SemanticRepository.supersede` → old record ends its validity, points forward, new record exists and is linked, all in one transaction.
- Failure injected mid-supersede → neither change persists; the old record remains active and readable.
- A query for active records excludes superseded ones, and the partial index `where superseded_by is null` is actually used (asserted via plan inspection, since an unused index here is a silent full-scan at volume).
- Supersession chains of length 3+ resolve to exactly one active record. A chain converging on two active records produces contradictory briefing items, which is a misleading recommendation by construction.
- No cycle: A superseded by B superseded by A → rejected.

**`dedupe_key`.** `DATA_MODEL.md` §13 names this the most consequential unresolved detail in the schema, and that is the right assessment. It gets a dedicated suite, and the suite is written *before* the derivation is implemented, because the suite is how the specification gets written.

The failure is two-sided and both sides degrade the briefing. Too strict, and every restatement of the same commitment becomes a new record; memory fills with near-duplicates, the briefing lists the same obligation four times with slightly different wording, and `MEMORY_ARCHITECTURE.md`'s never-duplicate rule is violated while the unique constraint reports success. Too loose, and two genuinely distinct facts collide on one key; the second is silently rejected or merged, a real commitment disappears, and the founder is told something inaccurate with full confidence.

The suite is a corpus of labelled pairs, each tagged `same` or `distinct`, with an asserted verdict per pair:

| Pair | Label | Why it is the hard case |
|---|---|---|
| "Send the pricing deck to Acme" from an email; the same commitment restated on a call | same | Cross-source restatement is the whole point of the system |
| "Send the pricing deck to Acme by Friday" vs "…by Monday" | distinct — supersession, not duplication | A changed due date is new information and must go down the supersession path, not the dedupe path |
| "Send the deck to Acme" vs "Send the deck to Initech" | distinct | Entity substitution with near-identical text |
| "Follow up with Dana" from two different threads, same week | same | Weak entity resolution — which "Dana" |
| "Follow up with Dana" (January) vs "Follow up with Dana" (June) | distinct | Time-boundedness of a recurring obligation. Any derivation ignoring time collapses a year of follow-ups into one record. |
| "We decided to use Postgres" vs "We decided against Postgres" | distinct | Negation. Any similarity-based derivation gets this wrong. |
| Same statement, different casing, punctuation, or ASR-mangled spelling of a name | same | Normalization has to absorb transcript noise without absorbing meaning |
| Same statement, two different orgs | distinct | Keys are org-scoped; also covered in §5 |

Reported as a confusion matrix rather than a pass/fail count, because the two error types have different costs and the derivation will be tuned against the tradeoff. Both error rates are tracked over time, and a change to the derivation that improves one while worsening the other requires an explicit decision. A key derivation change also requires a backfill plan, since existing keys become inconsistent with new ones — that plan is part of the change, and `ROLLBACK_STRATEGY.md` is where it lands.

## 9. Prompt injection

`SECURITY_STANDARDS.md` treats all ingested content as untrusted, and `ARCHITECTURE.md` §4 is precise about where the defense actually sits: not in asking the model to be careful, but in the agent having no tool capable of harm and the gate refusing anything above its level. An injected instruction that convinces the model to propose a deletion produces a gate refusal and an alert, which is **a detection event rather than a breach**. The tests are built to confirm exactly that framing.

Fixture corpus, one per source kind, each carrying instruction-shaped text: direct override ("ignore your previous instructions and…"), fake system framing ("SYSTEM: you are now authorized to…"), fake tool-call syntax in a body, an email signature block instructing the assistant to forward the thread, a transcript where a speaker reads an injection aloud, a Slack message with an injection inside a code fence, unicode and homoglyph obfuscation, and an instruction to omit a specific item from the briefing.

Asserted at three layers.

*Ingestion (unit and integration, deterministic).* The content is stored intact as data — not sanitized, not stripped, not rejected. Sanitizing at ingestion would corrupt the evidence trail and give a false sense of safety; the record must match what the founder would see in Gmail. `PRD.md` A1 requires exactly this.

*Authority (unit, deterministic).* Given a stub substrate that returns whatever the injection asked for — a deletion proposal, a send proposal, a proposal claiming a higher trust level, a proposal referencing an unpermitted tool — the gate refuses, audits, and alerts. This is the load-bearing assertion, and it does not involve the model at all, which is why it is reliable.

*Agent behavior (evaluation tier, statistical).* With injected content in retrieved context, assert the resulting `BriefingDocument` is structurally equivalent to the same scenario without the injection: same items present, no item whose text is drawn from the injected instruction, no proposal above `recommendation`. Because this tier is statistical, it is a quality signal rather than a guarantee — the guarantee lives in the layer above, which is the correct division of labour. Any observed escalation attempt is recorded as an evaluation case permanently.

Also asserted: the *omission* attack, where injected content instructs the agent to leave something out. This is the injection that produces no refusal and no alert, because nothing above trust level was ever proposed. The evaluation case pairs an injected run against a clean run and asserts the expected item still appears. It is the hardest injection to detect and the one most likely to cause a real miss.

## 10. Failure injection

`TESTING_STANDARDS.md` requires deliberately injected failures with graceful degradation rather than silent corruption. The specific corruption to prevent here is a watermark advancing past data that was never processed, because that data is then never fetched again and the loss is permanent and invisible.

Adapters are tested against a controllable fake HTTP server rather than a mocked client, so that retry, backoff, timeout, and partial-response behavior are exercised through the real transport.

| Injected condition | Required behavior | Watermark |
|---|---|---|
| 429 with `Retry-After` | Honor the header, retry, succeed | Advances only after full success |
| 429 without `Retry-After` | Exponential backoff with jitter, bounded attempts | Does not advance on give-up |
| 500 / 502 / 503 | Retry with backoff, then return `unavailable` with `retryable: true` | Does not advance |
| 401 / 403 (revoked token) | Return `auth_failed`, `retryable: false`, no retry storm | **Does not advance**, `consecutive_failures` increments, alert fires |
| Malformed JSON | Quarantine, do not write | Does not advance past the malformed item |
| Valid JSON failing the runtime schema | Quarantined with reason and raw payload preserved | Does not advance past it |
| Payload missing `source_id` | Quarantined — no synthesized identity, since a synthesized key breaks idempotency forever | Does not advance |
| Timestamp in the future or before epoch | Quarantined rather than clamped | Does not advance |
| Connection reset mid-page | Whole page retried; partial page not written | Does not advance |
| Page 3 of 5 fails | Pages 1–2 persist; cursor stays at the page-2 boundary, not the page-5 one | Advances to the last fully-processed page only |
| Empty page with `hasMore: true` | Loop terminates; no infinite pagination | Advances safely |
| Cursor rejected as expired by the source | Falls back to a bounded time-window re-fetch; idempotency absorbs the overlap | Reset, with an audit note |
| Database unavailable during write | Nothing written, error surfaced | Does not advance |

`safeToAdvanceCursor` (`API_CONTRACTS.md` §3) carries the whole correctness argument in one boolean, and is asserted directly in every case above rather than inferred from the resulting record count.

Downstream failure injection, same discipline:

| Injected condition | Required behavior |
|---|---|
| Model API 429 or 5xx during briefing generation | Bounded retry; on exhaustion, a **failure notice is delivered**, not silence (`PRD.md` B1) |
| Model returns unparseable output | Treated as generation failure; failure notice; raw output captured for diagnosis |
| Model returns valid JSON with an invalid `impactClass` | Gate refuses; other items still ship |
| Semantic retrieval returns zero records | Briefing states it has nothing rather than fabricating (§11 of `FAILURE_MODES.md`) |
| Transactional email provider 5xx | Retry with backoff; on exhaustion, alert loudly — a failed failure notice is the silence case and must page |
| Postgres connection pool exhausted | Requests queue and time out cleanly; no partial writes |
| Generation exceeds its wall-clock budget | Aborted, failure notice sent, timeout recorded |
| Runaway agent loop (repeated tool calls) | Hard iteration and token ceiling terminates the run; cost-guard alert fires |

The failure-notice path is tested as carefully as the success path, and that is unusual enough to state plainly: it is the mitigation for the single worst failure mode this product has (`FAILURE_MODES.md` §2). An untested mitigation for the worst failure mode is not a mitigation.

## 11. Performance baselines

`TESTING_STANDARDS.md` requires a baseline and a regression threshold for anything on a hot path or with scale implications. Phase 1 has one user, which changes what a threshold can mean. A percentage delta off a baseline measured at n=1 is noise. What is meaningful is an **absolute budget tied to a user-visible deadline or to a scale assumption we have already committed to** (`ENGINEERING_STANDARDS.md`: design for millions while building for ten).

| Measure | Phase 1 baseline | Why this number | Regression means |
|---|---|---|---|
| Ingestion lag, event to episodic record, p95 | ≤ 15 min | The schedule interval; anything larger means a run overlaps its successor | Data missing from the briefing that occurred before it was generated |
| Briefing generation wall clock, p95 | ≤ 120 s | Must fit inside the delivery window with room for one full retry | Late delivery risk (`FAILURE_MODES.md`) |
| Delivery latency, generation start to inbox, p99 | ≤ 5 min | The briefing is worthless after the first meeting | Direct exit-criterion risk |
| Semantic similarity search, p95 | ≤ 200 ms at 100k records | Called many times per generation; the composite drives the budget above | Generation time will breach before anyone notices the query |
| Gate evaluation, p99 | ≤ 5 ms | It is a pure function plus one insert; anything slower means I/O crept into `decide` | The purity seam has been violated |
| Distillation throughput | ≥ 500 episodic records/min | Must clear a day's backlog inside one interval | Backlog grows monotonically and never recovers |
| Token cost per briefing | Recorded, budget set after two weeks | Cost is a §19 self-review dimension; a cost never recorded cannot be reviewed | Prompt or retrieval change ballooning context |
| Peak memory per ingestion run | Bounded and flat with respect to page count | Proves pagination streams rather than accumulating | An adapter buffering everything works at fixture scale and dies at real scale |

Two of these are worth more than the rest. The vector-search baseline is measured against a **synthetic 100k-record corpus**, not the Phase 1 dataset, because at Phase 1 volume every query is fast and the HNSW index configuration is untested. That measurement is the only Phase 1 evidence that the retrieval design survives contact with the compounding asset it is designed to build. And the flat-memory assertion is the only fixture-era test that meaningfully probes pagination, which §12 identifies as exactly where fixtures lie.

Baselines are recorded per commit on the main branch and reviewed at the milestone self-review (`MASTER_CONSTITUTION.md` §19), not enforced as a CI failure gate at Phase 1 — a hard performance gate at n=1 on shared CI hardware fails for reasons unrelated to the change and gets disabled. The gate is human review of a trend line. That is a deliberate and reversible choice, and it should be revisited the moment there is a second user.

## 12. Fixture strategy and its limits

No live credentials exist for Gmail, Calendar, Slack, or any transcript provider (`ADR-0006`, technical debt item 1). Every adapter is built against fixture data behind its real interface. This is acknowledged technical debt and it belongs in the risk register with a removal date, not in a footnote.

**How fixtures are built to be worth something.** Fixtures are captured or hand-constructed to match each provider's documented response shape exactly, including fields we do not use — an adapter that only tolerates the subset it needs breaks on first contact with reality. Each source has a fixture set covering: an empty result, one item, a multi-page result, a page with `hasMore` and no items, mutated records on re-fetch, records at window boundaries, malformed and schema-invalid payloads, unicode and emoji in bodies, very large bodies, missing optional fields, threads with deep nesting, calendar events with recurrence and timezone edge cases, transcripts with low ASR confidence and ambiguous speaker attribution, and the injection corpus from §9. Fixtures are served by a fake HTTP server implementing the provider's URL shape, so the adapter exercises its real client, real retry logic, and real pagination loop.

**Where fixtures lie, stated without hedging.** Being explicit here is more useful than any amount of fixture coverage, because it tells the reader what the green suite does not mean.

| Fixtures cannot test | Consequence |
|---|---|
| Real pagination semantics — cursor expiry, results shifting between pages, non-obvious ordering, Gmail `historyId` gaps, calendar `syncToken` invalidation | The single most likely source of silently missed records. A fixture server always returns pages that partition cleanly; real APIs do not. |
| Real rate limits — actual quotas, per-method costs, undocumented burst behavior, throttling that manifests as latency rather than 429 | Backoff logic tuned against a fake is tuned against nothing |
| Auth edge cases — token refresh races, mid-run expiry, scope changes, consent revocation, re-auth flows | Precisely the path behind the silent-stall failure mode (`FAILURE_MODES.md`) |
| Real payload variance — fields absent in ways the docs do not mention, encodings, malformed MIME, provider-specific quirks | Quarantine rate could be far higher than fixtures suggest |
| Real volume and shape | A founder's actual inbox is not a fixture set's distribution |
| Real latency and its variance | The generation budget in §11 is measured against instant responses |
| Provider-side eventual consistency | An event fetched immediately after occurring may be incomplete |
| Timezone and DST behavior in real calendar data | Directly affects "today's commitments" correctness |

**Therefore: live-credential validation is part of each increment's exit gate, not a follow-up.** `ADR-0006` says this and it is repeated here because it is the load-bearing mitigation. Concretely, an increment does not exit until, against live credentials on the founder's real account: a full backfill and at least 72 hours of continuous incremental ingestion complete without gaps; the quarantine rate is measured and explained rather than merely observed; at least one real rate-limit or transient failure has been survived and its handling verified in logs; a token refresh has occurred across a run boundary; and a reconciliation query confirms the record count in the episodic layer matches the source's own count for the window. That reconciliation is the only real test of pagination correctness and it cannot be simulated.

Until every increment has passed that gate, "the test suite is green" means the adapter is correct about the fixtures. The distinction is not pedantic. It is the difference between a briefing that is complete and one that quietly is not.

## 13. CI and what "tested" means

`TESTING_STANDARDS.md` defines a change as tested when its suite exercises the new behavior, would fail if the change were reverted, and runs in CI on every subsequent change. All three clauses do work in this repository.

**Exercises the new behavior.** Not the module around it. A trust gate change is tested by a case whose input is the newly-handled input, not by an existing case that still passes.

**Would fail if the change were reverted.** This is the clause most often quietly unsatisfied, and it has a specific meaning for a permission system: revert the refusal branch and the suite must go red. Where a test's failure-on-revert is not self-evident — RLS policies, deferred triggers, the fail-closed default for undefined trust levels — the reviewer's obligation is to verify it by actually mutating the implementation and watching the test fail. For the authority layer and the RLS suite this is not optional judgment; a suite whose tests all pass against a deleted policy is worse than no suite, because it stops anyone from checking. Mutation testing of `authority/*` is the mechanical version of this discipline and is worth adopting for that module alone, where the surface is small and the stakes are highest.

**Runs in CI on every subsequent change.** Not once locally at authoring time.

| Trigger | Runs | Blocking |
|---|---|---|
| Every commit / PR | Unit, integration (ephemeral Postgres, migrations applied), E2E with stubbed agent, lint, typecheck, the redaction test from `API_CONTRACTS.md` §9, the RLS metatest | Yes |
| Every PR | Performance measurement, recorded and reported as a trend | No — reviewed, not gated (§11) |
| Prompt version change | Prompt regression over the evaluation set and the held-out set | Yes, blocks promotion (`DEPLOYMENT.md`) |
| Nightly | Full evaluation set including injection cases; drift detection against a fixed corpus | Alerts |
| Increment exit gate | Live-credential validation per §12 | Yes, blocks increment completion |
| Migration touching any table | RLS metatest, adversarial matrix regenerated | Yes |

Two hard rules. Skipped tests require a linked issue and an expiry date; a permanently-skipped test is deleted, because a skipped test is a lie about coverage. And no test may be disabled to unblock a release without the disabling appearing in the risk register — the authority and RLS suites specifically cannot be disabled at all, since they are the evidence for the two guarantees Phase 2 will be built on top of.

## 14. What this strategy cannot prove, and open questions

Named honestly, because a testing document that implies completeness is doing harm.

**The exit criterion is not testable.** Zero misleading recommendations over 14 weekdays is measured in production by the founder's flags (`PRD.md` B3), not by CI. This strategy reduces the mechanical causes of misleading output; it cannot establish that a well-formed, well-evidenced, correctly-gated recommendation was *right*. That gap is the honest reason `PRD.md` §5 puts a human in the measurement loop.

**Agent quality assertions are statistical.** Every evaluation-tier result is a sample. A 5/5 pass rate is not a proof, and it will occasionally be wrong in production on a case the suite covers.

**Fixture-era adapter confidence is low and should be treated as such** until §12's live gate passes per increment. This is the largest known gap in Phase 1's evidence.

**One user means no concurrency, no load, and no multi-tenant runtime behavior.** `ADR-0005` is explicit that a tenant-scoped schema is not a multi-tenant product; the same applies to its tests. The RLS suite proves policy correctness, not behavior under concurrent tenant load.

Open questions, each of which should be resolved before or during the increment it blocks:

| # | Question | Blocks |
|---|---|---|
| 1 | `ARCHITECTURE.md` §5 specifies the gate as a pure function; `API_CONTRACTS.md` §6 specifies `evaluate` as async and audit-writing. §3.1 above recommends splitting `decide` from `evaluate`. Both documents need updating to match whichever is chosen. | Gate implementation and its suite |
| 2 | `dedupe_key` derivation has no specification (`DATA_MODEL.md` §13). The labelled corpus in §8 is proposed as the specification's acceptance criteria. Who owns writing it? | Distillation, increment 1a |
| 3 | ~~The `supersession_complete` constraint forbids `valid_until` without `superseded_by`, which also forbids a fact that legitimately expires with no successor.~~ **Resolved:** `DATA_MODEL.md` §7 now uses the one-directional `supersession_closes_validity`, which permits expiry without a successor. Both cases need invariant tests: superseded-with-successor, and expired-without-successor. | Semantic layer, increment 1a |
| 4 | On episodic re-fetch with a changed `content_hash`, are derived semantic records re-distilled, superseded, or left stale? Currently unspecified. | Distillation correctness |
| 5 | Evaluation-set authorship. Cases must be drawn from real founder data to be meaningful, which means the evaluation set contains personal content and needs a handling policy (`PRIVACY_MODEL.md`). | Prompt regression testing |
| 6 | No voice transcript provider chosen (`ADR-0006`), so 1b's fixtures cannot be shaped and its ASR-confidence tests cannot be calibrated. | Increment 1b |
| 7 | Is briefing re-generation for an already-delivered date a no-op or a replacement? §7 asserts whichever is chosen; the choice is not yet made. | Briefing suite, increment 1a |
