# Phase 1 — Rollback Strategy

**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

`DEPLOYMENT.md` requires that every deployment's rollback path be defined before rollout rather than improvised after an incident: what triggers a rollback, who or what executes it, and how fast. This document is that definition for Phase 1. Companion to `DEPLOYMENT_STRATEGY.md`.

---

## 1. The general principle, and its precise limit

For most Phase 1 failures, the rollback is **fix forward and re-run the job**. That is not a shortcut. It follows from a specific property the architecture paid for deliberately, and it is worth stating exactly what the property is and exactly where it stops.

Every scheduled job is idempotent, and idempotency is enforced by the database rather than by application logic:

| Job | Idempotency key | Enforcement |
|---|---|---|
| Ingestion | `(org_id, source_connection_id, source_id)` | Unique constraint on `episodic_record` (`DATA_MODEL.md` §6) |
| Briefing generation | `(org_id, recipient_id, briefing_date)` | Unique constraint on `briefing` (`DATA_MODEL.md` §10) |
| Distillation | `(org_id, dedupe_key)` | Unique constraint on `semantic_record` (`DATA_MODEL.md` §7) — with an important caveat in §4 |

`API_CONTRACTS.md` §8 makes `idempotent: true` a literal type on `ScheduledJob` rather than a boolean, on the grounds that it is a precondition for being schedulable at all rather than a property a job asserts about itself.

Why this buys a rollback, mechanically: a classical rollback restores prior state, because the system's state is a history of mutations and undoing the last one is the only way back. Here, the desired state of the episodic layer is a **pure function of the source data**, and the desired state of a briefing is a pure function of memory plus code plus prompt at a given date. So there is nothing to undo. Fixing the function and evaluating it again produces the correct state directly. The unique constraints are what make re-evaluation *convergent* instead of *cumulative* — without them, a second run would append a second copy and recovery would require deletion, which the schema deliberately does not offer.

Now the limit, because overstating this is the way it becomes false.

**Idempotency buys re-runnability, not reversibility.** A re-run converges on the same key. It does not remove rows the bad version wrote under *different* keys. Ingestion is genuinely self-correcting because the key is derived from the source and cannot change. Distillation is not, because its key is derived from a model's interpretation of content, so a bad distillation run writes rows under keys a corrected run will never touch. That asymmetry is the entire reason §4's distillation case is hard and §4's ingestion case is trivial.

**One further requirement follows, and it is a real gap in the current contracts.** For ingestion re-runs to actually repair bad data, the upsert must *update* on conflict when `content_hash` differs, not skip. `EpisodicRepository.upsertMany` in `API_CONTRACTS.md` §4 does not specify conflict behavior, and `IngestOutcome.duplicatesSkipped` reads as though the answer is `on conflict do nothing`. If it is, then a run that wrote correct rows with a broken normalizer can never be repaired by re-running, and the central claim of this document fails for the exact case it is most often invoked for. The required semantics: on conflict, compare `content_hash`; if it differs, update `payload`, `participants`, `source_confidence`, and `content_hash`, and leave `ingested_at` and provenance intact. `content_hash` exists in the schema for change detection on re-fetch and this is what it is for. Recorded as an open question in §8.

**Also: re-running is not free where the model is involved.** An ingestion re-run costs API calls. A distillation or briefing re-run costs model tokens. At Phase 1 volumes that is rounding error, and the cost anomaly alert (`OBSERVABILITY_STRATEGY.md` §6) exists partly so a re-run loop is noticed rather than billed.

## 2. Rollback by subsystem

| Subsystem | Mechanism | Speed | Who |
|---|---|---|---|
| Code deploy | Re-deploy the prior tagged image | < 5 min | Automated on trigger, or founder |
| Schema migration | Forward-fix migration. Never a reversal | Minutes to hours | Founder, with approval if destructive |
| Prompt version | Activate the prior body in one transaction | < 1 min | Automated or founder |
| Agent trust level | Write the contract's trust level down | < 1 min, no deploy | Automated or founder |
| Bad ingestion run | Re-run the job | Minutes | Automated |
| Bad distillation run | Supersede the affected records | Hours, and semi-manual | Founder |
| Delivered briefing | **Not possible** | — | — |
| Database corruption | Point-in-time recovery, with audit preservation | Hours | Founder |

### Code deploy

Ordinary and boring, which is the goal. Redeploy the previous tag. Safe without coordination because migrations are expand-then-contract (`DEPLOYMENT_STRATEGY.md` §4), which means the schema in front of the old code is always one it can run against. That backward compatibility is the whole reason code rollback is a non-event, and it is a property that must be preserved deliberately: the first migration that is not backward-compatible with the prior release converts code rollback from a one-command operation into an incident.

There is no in-flight request to drain. The production workload is cron-triggered batch work, so the worst case for a mid-run restart is a job that dies partway, which is the case idempotency already covers.

### Schema migration

Forward-only, per `DEPLOYMENT_STRATEGY.md` §4. Recovery from a bad migration is a new migration, and the recovery path depends on how bad:

| Situation | Remedy |
|---|---|
| Additive migration, wrong shape, nothing written yet | Forward migration correcting it. Effectively free |
| Additive migration, wrong shape, **already written to by the live system** | The hard case. Below |
| Destructive migration that dropped data | Not recoverable by migration. Point-in-time recovery (§6). This is why destructive steps require approval and never ship in the same release as their expand step |

**The hard case, properly.** A column was added, the application has been writing to it for two days, and the type or semantics are wrong — say a timestamp stored as local time instead of UTC, or an enum missing a value that has been silently coerced. The prior state is not recoverable and is not what anyone wants: the two days of data are real and must be kept, just corrected. The procedure:

1. **Stop writing wrong data first.** Disable the affected job or ship a code fix that stops writing the bad column. Fixing the data underneath a process still corrupting it is a race that never converges.
2. **Add a new, correctly-shaped column.** Never alter the old one in place. The old column is now evidence of what happened and it is needed for step 3.
3. **Backfill with an explicit, reviewed transformation.** If the transformation is not deterministic from what was stored, the data is genuinely lost and §6 is the only path. Determining which of those two situations obtains is the first diagnostic question, not the last.
4. **Dual-read** — prefer new, fall back to old — for one release, so a backfill defect surfaces as a discrepancy rather than a gap.
5. **Switch writes and reads to the new column.**
6. **Drop the old column in a later release,** with approval, once nothing reads it.

Two Phase 1 tables constrain this. `audit_record` has `UPDATE` and `DELETE` revoked, so an audit column with wrong data cannot be corrected in place at all — the remedy is a new column and a forward-looking correction, with the old values left standing as the record of what was written. And `semantic_record` has no delete path, so a backfill error there produces records that must be superseded rather than fixed (§4).

### Prompt version

The fastest and cleanest rollback in the system, and it is fast because `DATA_MODEL.md` §8 made the invariant a database constraint rather than a deployment convention.

The `one_active_prompt_per_agent` partial unique index guarantees at most one active version per agent, where active means `deactivated_at is null and activated_at is not null`. A revert is therefore one transaction:

```sql
begin;
  -- Deactivate the bad version.
  update prompt_version set deactivated_at = now()
   where org_id = :org and agent_id = :agent
     and deactivated_at is null and activated_at is not null;

  -- Activate a new row carrying the prior body.
  insert into prompt_version
    (org_id, agent_id, version, body, rationale, activated_at,
     created_by_kind, created_by_id)
  select org_id, agent_id, :next_version, body,
         'Revert of v' || :bad_version || ': ' || :reason,
         now(), 'human', :user_id
    from prompt_version
   where org_id = :org and agent_id = :agent and version = :good_version;
commit;
```

Two details are deliberate.

**A revert inserts a new version rather than reactivating the old row.** Clearing `deactivated_at` on a historical row would rewrite the record of what was active when — the same reason `agent_proposal.trust_level` is stored on the proposal rather than joined from current config (`DATA_MODEL.md` §9). The version history stays append-only and the revert appears in it as an event with a stated reason, which is what `CONTINUOUS_IMPROVEMENT.md` needs when it later asks why a hypothesis was withdrawn.

**Ordering inside the transaction is forced by the index and that is a feature.** Deactivate must precede activate, or the partial unique index rejects the insert. There is no sequence of statements that leaves two versions active, and no sequence that leaves zero active without the transaction being visibly incomplete. The dangerous states are unrepresentable rather than merely avoided.

Post-revert, `agent_proposal.prompt_version_id` on every existing proposal still points at the version that produced it, so a revert does not obscure which prompt produced a bad recommendation. That is the property that makes the founder's error flags still analyzable after a revert.

### Agent trust level

Revocation must be instant, and instant means no build and no deploy.

`AgentContract.trustLevel` in `API_CONTRACTS.md` §5 is typed as a literal union, which reads as a compile-time constant. If it is one, revocation requires editing TypeScript, running CI, and deploying — minutes at best, and dependent on CI being green, which is not a dependency an emergency control should have. **The Phase 1 requirement is that the effective trust level is resolved at gate time from persisted agent-contract configuration,** so revocation is a single write and takes effect on the next gate evaluation.

The gate table in `ARCHITECTURE.md` §5 then does the rest without any special-case code. Writing the Chief of Staff agent from Level 1 to Level 0 changes `recommendation` from `surface` to `discard + alert`, so the agent keeps running, keeps proposing, keeps producing audit records, and nothing reaches the founder. That is a considerably better revocation than switching the agent off: the system stays observable while it is untrusted, which is exactly the state in which observation is most valuable.

Revocation does not rewrite history. `agent_proposal.trust_level` and `GateDecision.appliedTrustLevel` record the authority in force at the time, so past recommendations remain explainable under the authority that actually authorized them.

Revocation is a security control and needs no approval to *lower*. Raising is a §11 change requiring approval and evidence (`DEPLOYMENT_STRATEGY.md` §5). Asymmetry is correct: reducing autonomy is always safe, and a control that is hard to apply will not be applied in time.

### A bad ingestion run

The easy case, and the one the architecture was designed to make easy.

Re-run the job with the watermark reset to before the affected window. The unique constraint means the re-run converges rather than duplicating, and `ARCHITECTURE.md` §4 already states that re-fetching is free for exactly this reason. Watermarks advance only past fully-processed data, so a partial failure has already left the cursor behind and the next scheduled run will re-fetch without intervention at all.

The residual risks are narrow and worth naming. Resetting a cursor for a provider whose cursor is not a timestamp — Gmail `historyId`, Calendar `syncToken` — may mean a full resync rather than a windowed one, because those cursors cannot be arithmetically rewound. A full resync is slow and rate-limit-sensitive but not dangerous. And the correctness of the whole approach depends on the upsert-updates-on-content-change requirement in §1.

### A bad distillation run

The genuinely hard subsystem, and it is hard for a structural reason: **there is no delete path for semantic records**, by design (`MEMORY_ARCHITECTURE.md`, `ADR-0002`, `API_CONTRACTS.md` §4, which omits a delete method deliberately). A distillation run that extracted wrong facts has written rows that cannot be removed, and unlike ingestion, a corrected run will not overwrite them, because the corrected fact has a different `dedupe_key` and lands as a new row beside the bad one.

The remedy is supersession, using the mechanism the memory model already provides:

1. **Freeze distillation** for the affected window. As with a bad migration, correcting output while the producer still runs does not converge.
2. **Identify the affected set** precisely. This is why `distillation.run.completed` and `distillation.record.superseded` carry run identity and why every semantic record stores the `trace_id` of the run that wrote it (`OBSERVABILITY_STRATEGY.md` §5). Without run attribution, the affected set has to be guessed, and guessing means either superseding good facts or leaving bad ones live.
3. **Re-derive correctly** from the episodic records, which are intact — episodic data is the source of truth and distillation is a derived view, which is what makes this recoverable at all.
4. **Supersede** each bad record with its corrected successor via `SemanticRepository.supersede`, atomically setting `superseded_by` and `valid_until`. Superseded records fall out of the partial index `on semantic_record (org_id, kind) where superseded_by is null`, so they stop appearing in retrieval and stop reaching briefings, while remaining in place for audit.
5. **Re-run affected briefings** if any already-generated briefing cited the bad records. Briefing generation is idempotent per `(org, recipient, date)`, so regeneration is safe — but if the briefing was already *delivered*, see §4, because regeneration fixes the record and not the founder's memory.
6. **Unfreeze.**

Two problems with step 4 as the schema currently stands, and both need resolving before distillation ships.

**A bad fact with no corrected successor could not be marked invalid — now fixed.** The original `supersession_complete` check required `superseded_by` and `valid_until` to be both null or both non-null. That was correct for its intended purpose, preventing the half-state where a record reads as currently valid while pointing forward, but it also made it impossible to express "this record is garbage and there is no replacement" — the common case when a model hallucinated a commitment that was never made.

`DATA_MODEL.md` §7 now uses the one-directional `supersession_closes_validity`: a superseded record must have a closed validity window, but a closed window does not require a successor. That admits both invalidation and natural expiry, such as a commitment whose deadline simply passes.

The alternative considered was a tombstone successor row of a `retraction` kind, preserving the stricter constraint and keeping every invalid record pointing at an explanation. It was rejected as heavier: it creates rows whose only purpose is to say something is not the case, and it conflates "retracted as never true" with "expired as no longer true," which are different facts about a claim. If an explanation for an invalidation proves necessary in practice, an `invalidation_reason` column is the cheaper addition.

**`unique (org_id, dedupe_key)` blocked the corrected successor — now fixed.** If `dedupe_key` is a normalized identity for a claim, then a corrected version of the same claim computes the *same* key, and inserting it violated the unique constraint while the superseded row still held that key. Supersession and a global unique dedupe key were in direct conflict, and the conflict would have surfaced as a failing insert on the very first supersession. `DATA_MODEL.md` §7 now uses the partial unique index `one_open_record_per_claim`, scoped to records that are neither superseded nor expired, mirroring the pattern already used for `one_active_prompt_per_agent`. The scoping predicate covers both closing conditions deliberately, so an expired-without-successor record does not block a later revival of the same claim.

## 3. Automated versus manual triggers

`DEPLOYMENT.md` prefers automated rollback triggers wherever the trigger condition is unambiguous. The discipline is in being honest about which conditions actually are.

**Automated.** Each of these is a mechanical fact with one correct response:

| Trigger | Action |
|---|---|
| Health check fails after deploy, 3 consecutive attempts | Redeploy prior tag |
| Migration fails mid-application | Abort the transaction, abort the deploy, leave the prior schema live |
| Post-migration RLS assertion fails (`DEPLOYMENT_STRATEGY.md` §4) | Abort the deploy. A tenant-scoped table without RLS is never acceptable, so there is nothing to weigh |
| `security.audit_write_failed` | Halt the affected pipeline. The gate's guarantee that authorizing and logging are one operation has been broken; continuing means producing unlogged effects |
| Model API error rate > 90% for 10 minutes | Halt agent runs, deliver the failure notice (`PRD.md` B1), retry on the next cycle |
| Prompt regression suite fails during activation | Refuse activation, leave the prior version active |
| Ingestion job crash | No action needed. The watermark held; the next run re-fetches |

**Manual, and deliberately so.** Each of these requires a judgment that automation would get wrong:

| Trigger | Why not automated |
|---|---|
| A single flagged misleading item | The correct response depends on the cause. It might be a prompt revert, a distillation supersession, an adapter fix, or nothing at all if the item was defensible. Automating a prompt revert on one flag hands prompt selection to a single data point and makes reverting the reflex |
| Briefing quality degradation | Not machine-observable. `ADR-0006` already concedes that attributable quality requires someone to look at briefings and decide, and that this is appropriate at Phase 1 and would not scale |
| Cost anomaly | Might be a bug, might be a legitimately busy week. Alerts, does not act |
| Item count drifting past ~12 | A slow regression toward a firehose, not an incident. Belongs in the weekly review |
| Trust-level revocation | Revocation is instant and needs no approval, but *deciding* to revoke is a judgment about the founder's confidence, which no metric holds. The mechanism is automatable and the decision is not |
| Any destructive schema change | `MASTER_CONSTITUTION.md` §11 makes deleting information approval-gated. Automation cannot hold an approval |

The line between the two columns is worth naming plainly: **automate the rollback when the trigger condition and the correct response are both single-valued.** An unambiguous trigger with several plausible responses is an alert, not an automation, and automating it produces a system that reacts confidently to things it has diagnosed wrongly — the same failure the trust framework exists to prevent in the agent.

## 4. The one truly irreversible action

**A briefing delivered to the founder's inbox cannot be recalled.**

This is the only irreversible action in Phase 1, and everything about the phase's risk posture follows from it. There is no recall in SMTP. There is no unsend from a transactional email provider. The message may already be read, on a phone, before any monitoring notices anything is wrong. `PRD.md` §6 records that the founder reads it before a laptop is open. A correction email is not a rollback — it is a second message, and a second message admitting the first was wrong is itself a cost against the exact asset Phase 1 exists to build. `UX_PRINCIPLES.md` §5 requires that irreversibility be stated before rather than after, and here it is stated to ourselves: there is no undo on this path.

Two implications, and the first is the more important.

**All validation must be pre-send, because there is no post-send.** The briefing pipeline separates composition, rendering, and delivery (`ADR-0004`, `ARCHITECTURE.md` §7), and that separation is what makes a real gate possible between the last two steps. The pre-send validation is a hard gate: it either passes or the briefing does not go, and a briefing that does not go triggers the failure notice, which is a recoverable outcome. Every check below is available from the `BriefingDocument` alone and none requires a model call:

| Check | Rationale |
|---|---|
| Every item has ≥ 1 evidence link | `PRD.md` B2. Already a non-empty tuple type, so this is defense in depth against a runtime construction path |
| Every item has a trust level and label | `UX_PRINCIPLES.md` §1 |
| No section is present but empty | `PRD.md` B1 |
| Item count within bounds | Above ~12, hold and alert rather than send a firehose (`ARCHITECTURE.md` §7) |
| Every item traces to a gate disposition of `surfaced` | Nothing reaches the founder that did not pass the gate. This is the check that would catch a composer bug reaching around the authority layer |
| No item derives from a superseded semantic record | The specific failure §2's distillation case produces |
| No item derives from a record below the confidence floor | `PRD.md` A3: exclude rather than hedge |
| No secret-shaped string in rendered output | Cheap regex, catastrophic if omitted |
| Rendered HTML and plain text both non-empty | `ADR-0004` requires a plain-text alternative |
| Exactly one recipient, matching `briefing.recipient_id` | Guards the worst available failure: the founder's briefing delivered elsewhere |
| Idempotency: no `delivered_at` already set for this `(org, recipient, date)` | Prevents a re-run from sending a second briefing. The unique constraint prevents a duplicate row; only this check prevents a duplicate *send* |

That last row is the sharpest edge in the whole document. Briefing generation is idempotent at the database, which makes regeneration safe. **Delivery is not idempotent**, because sending is an external side effect that no constraint can deduplicate. So the re-run-freely principle that governs every other subsystem stops precisely at the send boundary, and the boundary needs an explicit guard: `delivered_at` is set in the same transaction that records the provider's accepted message ID, and a re-run with `delivered_at` already set regenerates and re-validates but does not send.

**Second implication: the cost of a bad briefing is measured in the exit criteria, not in an incident log.** `PRD.md` §9 resets the fourteen-day window on a single misleading recommendation, and calls that intentional. So the correct trade at the send gate is always to hold. A held briefing costs one day of the streak. A wrong briefing costs fourteen.

## 5. Who executes, and how fast

One human. That constrains the design more than any target does: any control whose execution requires a person is unavailable while that person is asleep, in a meeting, or on a plane. Everything in §3's automated column exists to be safe without him.

| Operation | Executor | Target |
|---|---|---|
| Automated triggers in §3 | The system | < 2 min from detection |
| Code rollback | Founder or automation | < 5 min |
| Prompt revert | Founder or automation | < 1 min |
| Trust-level revocation | Founder | < 1 min, given §2's no-deploy requirement |
| Hold a briefing | Automated at the send gate | Pre-send, always |
| Distillation supersession | Founder | Hours; not urgent, since superseded records stop reaching briefings immediately once superseded |
| Point-in-time recovery | Founder | Hours |

Deploy authority is the founder's alone, and there is no break-glass path that bypasses CI. At one contributor, a bypass mechanism would be used routinely and would therefore be the normal path rather than the exception.

## 6. Data recovery

| Layer | Mechanism |
|---|---|
| Postgres | Supabase automated daily backups plus point-in-time recovery. PITR is the one that matters; daily snapshots lose up to a day of ingestion and, worse, up to a day of audit records |
| Retention | PITR window of at least 7 days. Shorter means a Friday defect discovered on Monday is unrecoverable |
| Restore target | A new database, never in place. Restoring over the live database destroys the evidence needed to understand what happened |
| Verification | A restore rehearsal against staging, in increment 1a. A backup that has never been restored is a hypothesis, not a backup |
| Secrets | Not in the database by construction (`DATA_MODEL.md` §5). Recovered independently from the secrets manager, which needs its own backup story |
| Fixtures, prompts, migrations | Git |

### Restore must not silently lose audit records

This is the hardest constraint in data recovery and it needs stating precisely.

`audit_record` retention is seven years and the records are **never deleted** (`DATA_MODEL.md` §12). `SECURITY_STANDARDS.md` requires that every agent action be logged. A point-in-time recovery to `T-6h` discards every audit record written between `T-6h` and now — which is not merely data loss, it is the destruction of the record of what the system did during the window that is under investigation, performed as part of investigating it. A restore that quietly does this satisfies the letter of every backup policy and violates the constitution.

The procedure therefore preserves audit before it restores anything:

1. **Before touching anything, export from the live database:** `audit_record` and `agent_proposal` for the full window at risk, plus `briefing` and `briefing_item` and `error_flag`. Export to durable storage outside the database, verified by row count. If this step fails, the restore does not proceed.
2. Restore to a new database at the chosen point in time.
3. **Re-insert the exported audit and proposal rows** that postdate the restore point, preserving original identifiers and `occurred_at`. This requires `INSERT` privilege on a table whose `UPDATE` and `DELETE` are revoked, which is exactly the append-only design working as intended: history can be added to and never rewritten.
4. Reconcile foreign keys. An audit row may reference a proposal, and a proposal may reference a `prompt_version`, that the restore point predates. Insert the referenced parents from the export before their children. An audit row whose parent genuinely cannot be reconstructed is inserted with the reference nulled and a note, because losing the audit row is worse than losing the link.
5. Re-run ingestion from before the restore point. Idempotency makes the episodic layer self-healing, so lost episodic rows are re-fetched rather than restored — this is the payoff of §1 in the single scenario where it matters most.
6. **Accept that the semantic layer is not fully recoverable**, and re-derive it. Distillation is a model output, so re-derivation produces *equivalent* facts rather than identical ones, with different identifiers. Semantic records lost between the restore point and now are gone as records even though their content is re-derivable, which means any `briefing_item_evidence` row pointing at a lost semantic record has a dangling reference. Re-derive first, then reconcile evidence against the re-derived set, then flag any item whose evidence cannot be reconstructed as unexplainable — because `OBSERVABILITY_STRATEGY.md` §4 treats an unexplainable delivered item as a defect, and a restore is not an exemption from that.
7. **Cut over**, and record the whole operation as an incident per `SECURITY_STANDARDS.md`, with root cause, blast radius, and a permanent risk register entry, regardless of severity.

Step 3 needs a privileged role that can insert into `audit_record` outside the normal application path. That role is itself a security-relevant capability: its use must emit a `security.*` event and alert (`OBSERVABILITY_STRATEGY.md` §2), because a mechanism for writing arbitrary audit history is precisely what an attacker covering their tracks would want. It exists because the alternative — an unrecoverable audit gap — is worse, and it is watched for the same reason.

## 7. Pre-flight checklist for the riskiest operation

The riskiest operation in Phase 1 is not a migration and not a deploy. It is **sending a briefing whose generation path has changed** — a new prompt version, a new source adapter going live, a change to composition or the confidence floor. It is the riskiest because it is the only irreversible one (§4), and because the failure it produces is a confidently-stated wrong statement to the one person whose trust the phase exists to earn.

Run before the first send under any changed generation path:

- [ ] Full CI suite green on the exact commit, including RLS adversarial, gate refusal, and prompt regression suites (`DEPLOYMENT_STRATEGY.md` §3)
- [ ] Shadow generation completed and the diff against the current version reviewed item by item (`DEPLOYMENT_STRATEGY.md` §5)
- [ ] For a prompt change: §11 approval recorded, with `rationale` naming the failure pattern it targets
- [ ] For a new adapter: live-credential validation complete — pagination, rate limit, token refresh, revocation, cursor-across-restart (`DEPLOYMENT_STRATEGY.md` §7)
- [ ] Every pre-send validation check in §4 passing on the shadow document, not just on fixtures
- [ ] `explain()` run against a sample of shadow items; all five explainability questions answered (`OBSERVABILITY_STRATEGY.md` §4)
- [ ] Item count within bounds; no section present but empty
- [ ] No item derives from a superseded or below-floor record
- [ ] Recipient verified as exactly the intended address
- [ ] Rendered on a phone-width viewport and read end to end by a human. Two minutes, per `PRD.md` §6
- [ ] Prompt revert transaction (§2) prepared and its target version identified, so a revert is a paste rather than a lookup
- [ ] Trust-level revocation path confirmed executable without a deploy (§2)
- [ ] Delivery watchdog heartbeat healthy, so a silent failure would be caught (`OBSERVABILITY_STRATEGY.md` §6)
- [ ] Sent to a test mailbox first and read there before the founder's address is used

The last item is the cheapest insurance in Phase 1 and the easiest to skip once the pipeline has worked twenty times in a row.

## 8. Residual risks and open questions

**Two schema defects blocked the distillation rollback story. Both are now fixed in `DATA_MODEL.md` §7.** The table-wide `unique (org_id, dedupe_key)` on `semantic_record` conflicted with supersession and is now the partial unique index `one_open_record_per_claim`, scoped to open current records. And `supersession_complete` made it impossible to invalidate a record with no corrected successor — the common case for a hallucinated fact — and is now the one-directional `supersession_closes_validity`, which permits `valid_until` without `superseded_by`. Both were cheap to fix at design time and would have become migrations against populated tables later.

**Ingestion upsert conflict semantics are unspecified.** §1. If `upsertMany` skips on conflict rather than updating on `content_hash` change, then "re-run it" does not repair bad episodic data, and the general principle of this document is narrower than it claims. `API_CONTRACTS.md` §4 should state the semantics explicitly.

**Trust-level revocation may currently require a deploy.** §2. `AgentContract.trustLevel` reads as a compile-time literal. If the effective level is not resolved at gate time from persisted configuration, the fastest emergency control in the system is gated behind CI.

**Delivery is not idempotent and only one guard stands between a re-run and a duplicate send.** §4. The `delivered_at` check is application logic, not a constraint, which makes it the weakest link in a document that otherwise leans on database enforcement throughout. It needs its own test, including the concurrent case where two generator invocations overlap — unlikely under cron, not impossible.

**The semantic layer is not point-in-time recoverable in the strict sense.** §6 step 6. Re-derivation produces equivalent facts under new identifiers, so evidence links into the lost window are permanently broken. The mitigating fact is that the episodic layer is the source of truth and it *is* recoverable, so no information is lost — but the provenance graph has a scar, and any briefing item pointing into it becomes unexplainable, which is a defect by `OBSERVABILITY_STRATEGY.md` §4's own standard.

**No restore has been rehearsed.** Carried from `DEPLOYMENT_STRATEGY.md` §10, restated because the audit-preservation procedure in §6 is intricate, has never been executed, and would be executed for the first time under incident pressure. Rehearsal belongs in increment 1a.

**Open: PITR window length and Supabase plan.** The 7-day minimum in §6 is a requirement stated here, not a confirmed capability. It interacts with the platform dependency `ADR-0002` accepted explicitly.

**Open: where audit exports are written.** §6 step 1 requires durable storage outside the database. That destination needs its own access control, retention, and encryption posture, and it holds audit content — which means it inherits the redaction and data-subject obligations in `DATA_MODEL.md` §12. Belongs in `PRIVACY_MODEL.md`.
