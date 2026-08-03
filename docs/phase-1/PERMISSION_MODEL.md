# Phase 1 — Permission Model

**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

Required by `MASTER_CONSTITUTION.md` §6 and §15, and by `SECURITY_STANDARDS.md`, which requires that every human and agent identity map to a role, and that roles map to permitted actions and trust levels. Companion to `ARCHITECTURE.md` §5 and §9, `API_CONTRACTS.md` §5–6, and `THREAT_MODEL.md`.

---

## 1. The organizing idea

There are two permission subjects in LEAP OS and they are governed by entirely different mechanisms. Conflating them is the most common way systems of this kind end up with authority they cannot describe.

**Humans have roles.** A role answers *what may this person see and change*. It is enforced by RBAC and, beneath it, by Row-Level Security. It is about data access.

**Agents have contracts.** A contract answers *what capabilities does this agent hold, and what class of proposal may it get past the gate*. It is enforced by tool scoping at construction and by the trust gate. It is about authority to act.

An agent does not have a role and a human does not have a trust level. An agent acting "on behalf of" a user is a fiction this system deliberately avoids: an agent's authority comes from its contract, never from the privileges of whoever triggered it. That asymmetry is what prevents privilege escalation by association, and it is the reason a Trust Level 1 agent triggered by an owner is still a Trust Level 1 agent.

Both mechanisms rest on the same sentence from `ARCHITECTURE.md` §1:

> **The model decides what to propose. Deterministic code decides what is permitted.**

Everything in this document is an expansion of the second half.

## 2. Human RBAC

### 2.1 The role enum

`DATA_MODEL.md` §3 establishes the skeleton:

```sql
create type user_role as enum ('owner', 'admin', 'member', 'viewer');
```

Phase 1 has one organization with one user in the `owner` role. Nothing branches on role. The enum exists because `SECURITY_STANDARDS.md` requires an RBAC skeleton and because having the type present means Phase 2 adds behaviour rather than a migration on a populated table.

That is a genuine and modest claim. Having the enum is not having RBAC. What has been bought is the absence of a schema change, not the presence of access control, and the same honesty `ADR-0005` applies to tenancy applies here.

### 2.2 What each role may do

| Capability | `owner` | `admin` | `member` | `viewer` | Phase 1 status |
|---|---|---|---|---|---|
| Receive a briefing | ✓ | ✓ | ✓ | ✓ | **Active** for the single owner |
| Read own briefings and their evidence | ✓ | ✓ | ✓ | ✓ | **Active** |
| Flag a briefing item as wrong | ✓ | ✓ | ✓ | ✓ | **Active** (`PRD.md` B3) |
| Read semantic memory scoped to own visibility | ✓ | ✓ | ✓ | ✓ | Phase 2 — requires the visibility model in §2.3 |
| Read others' briefings | ✓ | ✓ | ✗ | ✗ | Phase 2 |
| Connect or disconnect a data source | ✓ | ✓ | ✗ | ✗ | **Owner only in Phase 1**, operator action, no UI |
| Configure briefing schedule and Slack channel opt-in | ✓ | ✓ | ✗ | ✗ | **Owner only in Phase 1** |
| Invite or remove users, assign roles | ✓ | ✓ | ✗ | ✗ | Phase 2 (`ADR-0005`: not built) |
| Approve a queued action | ✓ | ✓ | ✗ | ✗ | Phase 3. See §5 on why role alone is insufficient. |
| Advance or revoke an agent trust level | ✓ | ✗ | ✗ | ✗ | **Owner only, permanently.** §7 |
| Activate a `prompt_version` | ✓ | ✗ | ✗ | ✗ | **Owner only, permanently.** High-impact under §11; T10 in `THREAT_MODEL.md` |
| Change `TrustGate` or `AgentContract` behaviour | ✓ | ✗ | ✗ | ✗ | Code change, and a security change requiring approval (`API_CONTRACTS.md` §10) |
| Trigger a data-subject export or erasure | ✓ | ✓ | ✗ | ✗ | Operator tooling, Phase 1 (`PRIVACY_MODEL.md` §6.2) |
| Read the audit trail | ✓ | ✓ | ✗ | ✗ | Phase 2 as a surface; queryable by the owner in Phase 1 |
| Delete anything from memory | ✗ | ✗ | ✗ | ✗ | **Nobody, at any role.** Supersession replaces deletion (`MEMORY_ARCHITECTURE.md`), and `SemanticRepository` has no delete method to call (`API_CONTRACTS.md` §4). The sole exception is the privacy erasure path, which redacts rather than deletes and writes its own audit record. |

Four notes on the shape of that table.

**`admin` and `owner` differ only on authority over the system's authority.** Both administer data and users. Only the owner may change what agents are permitted to do, what prompt is active, or what trust level applies. This is the distinction that keeps `MASTER_CONSTITUTION.md` §11's "policy changes and security changes require approval" meaningful once more than one administrator exists.

**`viewer` is deliberately not "member minus write."** In Phase 1 the two are indistinguishable because nothing is writable. The distinction becomes real in Phase 2, and it is worth stating now that `viewer` means *no ability to influence the system's future behaviour* — no flags, no approvals, no configuration. Since flagging is learning input, a viewer who can flag can steer the model. `viewer` therefore loses the flag affordance in Phase 2 even though the table above grants it in Phase 1, where the only user is the owner and the distinction is moot.

**Nobody can delete.** This is unusual enough to be worth defending. The audit and memory guarantees in `ADR-0002` and `MEMORY_ARCHITECTURE.md` are only as strong as the absence of a delete path, and a delete path that exists "for admins" is a delete path. Deletion is expressed as supersession or as redaction, both of which leave evidence.

**Role does not confer trust level.** An owner cannot cause an agent to execute an action by triggering it. §1.

### 2.3 The Phase 2 problem this document should not pretend to solve

`PRD.md` §6 identifies it precisely: leadership team members need shared organizational memory without shared *visibility* into everything the founder sees. That is a per-record access control problem inside a single tenant, and it is genuinely hard, because a semantic record distilled from a confidential email is not obviously confidential on its face.

Phase 1 does not solve it and should not. The relevant Phase 1 obligation is to avoid foreclosing it: every semantic record retains mandatory `derived_from` links to its episodic sources (`DATA_MODEL.md` §7), so a future visibility rule can be computed from provenance rather than requiring a classification pass over records whose origins were forgotten. That is the whole Phase 1 requirement, and it is already satisfied by the memory design for unrelated reasons.

## 3. Agent permissions

### 3.1 The agent contract is the unit of authority

From `API_CONTRACTS.md` §5, an `AgentContract` declares `agentId`, `responsibility`, `trustLevel`, `permittedTools`, `promptVersionId`, and `escalation`. Those six fields are the complete statement of what an agent is allowed to be. There is no other source of agent authority: no runtime elevation, no per-request override, no inheritance from the triggering user.

Phase 1's single contract:

| Field | Value | Rationale |
|---|---|---|
| `agentId` | `chief-of-staff` | — |
| `responsibility` | Synthesize and prioritize the daily executive briefing from organizational memory | One sentence, no "and" joining two responsibilities. `AI_AGENT_STANDARDS.md` treats a conjunction as evidence of two agents. |
| `trustLevel` | `1` | Recommend only (`MASTER_CONSTITUTION.md` §10, `ROADMAP.md` Phase 1) |
| `permittedTools` | `memory.searchSimilar`, `memory.findActive`, `memory.findByWindow`, `memory.findById` | Read-only, semantic and episodic. Nothing else. |
| `promptVersionId` | Current active version | Exactly one active version per agent, enforced by a partial unique index rather than by deploy discipline (`DATA_MODEL.md` §8) |
| `escalation` | `propose_lower_impact` | Uncertainty produces a weaker proposal, never a guess at a stronger one |

What is **absent** from `permittedTools` is the substance of the security posture: no send, no draft, no calendar write, no delete, no HTTP fetch, no shell, no arbitrary SQL, no write access of any kind to memory. The distillation path writes to the semantic layer, but it does so through `KnowledgeManager.reconcile`, which is not a tool the Chief of Staff holds.

### 3.2 Tool scoping happens at construction

`ToolScoper.scope(contract)` resolves declared tool names into concrete implementations *before the agent loop starts* (`API_CONTRACTS.md` §6). The set passed to the substrate is the set the contract declares.

The consequence is worth stating in the strongest available form, because it is easy to read as a stylistic preference rather than the load-bearing control it is:

> **An agent does not hold a tool it is instructed not to use. It does not hold the tool.**

There is no prompt text saying "do not delete." There is no tool named delete. A model cannot invoke a function that was never registered, and no amount of persuasion in an ingested email body registers one. Instruction is a probability; absence is a category. `THREAT_MODEL.md` §5.1 develops why this is the only defense against prompt injection that does not degrade as attackers improve.

Two corollaries follow directly and both are enforcement rules rather than observations:

- **Adding a name to `permittedTools` is an authority change**, not a configuration tweak, and falls under §11 approval alongside changes to the gate itself. The most likely real erosion of this system is a tool added "just for this increment" (T11).
- **A tool must be constructible without ambient privilege.** A read-only memory tool that internally holds the Supabase service role is not read-only, because the tool is the boundary and the credential is inside it. Tools receive `TenantContext` and a repository, never a raw connection.

### 3.3 Least privilege per agent, before there are agents to distinguish

Phase 1 has one agent, so least privilege is trivially satisfied and the discipline is unexercised. The Phase 2 roster in `AI_AGENT_STANDARDS.md` is where it starts doing work, and recording the intended shape now costs nothing:

| Agent (Phase 2+) | Reads | Holds | Never holds |
|---|---|---|---|
| Chief of Staff | Semantic memory, procedural layer | Read tools, orchestration routing | Any source-write tool. It coordinates; it does not act on external systems. |
| Email Intelligence | Email episodic records, related semantic records | Draft composition (Trust 2) | Send. Delete. Calendar. |
| Meeting Intelligence | Transcript episodic records | Extraction, semantic write via Knowledge Manager | Any communication tool |
| Knowledge Manager | Semantic layer | The only semantic write path | Any external tool at all. It is the integrity keeper for memory and holds no reach outside it. |

The rule generalizing that table: **an agent's tool set is derived from its responsibility statement, and a tool that cannot be justified by one sentence of the responsibility is not granted.** `SECURITY_STANDARDS.md` states the same principle as "an Email Intelligence agent does not have delete-database access."

## 4. The trust gate truth table

### 4.1 The function

```
disposition = gate(proposal.impactClass, contract.trustLevel, policy)
```

Five properties, each of which is a design commitment rather than an implementation detail:

1. **Pure.** No I/O in the decision, no clock, no configuration read at decision time. Auditable by reading it.
2. **Deterministic.** The same proposal from the same agent yields the same disposition every time, regardless of how the model phrased it.
3. **Prose-blind.** The gate reads `impactClass`, never `payload` or `rationale`. This is what makes it immune to persuasion: there is no argument a proposal can make to the gate, because the gate does not read arguments. A gate that inspected prose would be a second language model, with a second set of injection vulnerabilities and no determinism.
4. **Fails closed.** Absent, unrecognized, or malformed impact class refuses. It never infers a class, because inference is exactly the door an attacker or a bug walks through.
5. **Inseparable from audit.** The gate is the only path from proposal to effect and it writes the audit record. Authorizing and logging are one operation, so an unlogged effect is not expressible (`ARCHITECTURE.md` §5).

### 4.2 The full table

Extends `ARCHITECTURE.md` §5 across all six trust levels. Phase 1 operates in the Trust 0 and Trust 1 columns; the rest is specified now so that later phases enable a row rather than design one, and so that the shape of the escalation is reviewable before anything depends on it.

| Impact class | Trust 0 (observe) | **Trust 1 (Phase 1)** | Trust 2 (draft) | Trust 3 (execute on approval) | Trust 4 (guarded autonomy) | Trust 5 (self-optimizing) |
|---|---|---|---|---|---|---|
| `observation` | logged | **logged** | logged | logged | logged | logged |
| `recommendation` | discarded + alert | **surfaced** | surfaced | surfaced | surfaced | surfaced |
| `draft` | refused | **refused** | drafted | drafted | drafted | drafted |
| `reversible_action` | refused | **refused** | refused | queued for approval | executed within guardrails | executed within guardrails |
| `irreversible_action` | refused | **refused** | refused | refused | queued for approval | queued for approval |
| `high_impact` (§11) | refused | **refused** | refused | queued for approval | **queued for approval** | **queued for approval** |
| absent / malformed | refused | **refused** | refused | refused | refused | refused |

Dispositions are the `gate_disposition` enum from `DATA_MODEL.md` §9: `logged`, `surfaced`, `drafted`, `queued_for_approval`, `executed`, `discarded`, `refused`.

Reading notes, because several cells are non-obvious:

**`recommendation` at Trust 0 is discarded *and alerted*, not silently dropped.** A Level 0 agent proposing a recommendation is misconfigured or has been influenced. Silence would hide both.

**`irreversible_action` is never executed without approval at any trust level, including 5.** The diagonal does not continue to its natural conclusion, and that is deliberate. Trust Level 5 in `MASTER_CONSTITUTION.md` §10 is "continuously optimize while reporting changes," which is not the same as "may do anything." Irreversibility is a property of the action, not of the actor, and no amount of demonstrated competence makes an unrecoverable action recoverable.

**`high_impact` remains gated at Trust 4 and 5.** §11 says high-impact actions *always* require approval. The word is always. That is what §5 below makes precise.

**The malformed row is the fail-closed rule, expressed as a row rather than as prose,** so that it is visible in the same artifact a reviewer reads and cannot be omitted by someone implementing the table faithfully.

### 4.3 Refusals beyond the table

The table covers impact class against trust level. The gate additionally refuses, per `API_CONTRACTS.md` §6:

| Condition | Why refusal is right |
|---|---|
| `evidence` empty for anything to be surfaced | `PRD.md` B2: an unsourced assertion is not shippable at any trust level. Non-empty is also a type-level requirement in `BriefingItem`, so this refusal catches the case where the proposal, not the document, is malformed. |
| `rationale` empty | `OBSERVABILITY.md`'s explainability requirement cannot be met retroactively. |
| Proposal references a tool not in `permittedTools` | Redundant with construction-time scoping, and intentionally so. Defense in depth at the one boundary where a bypass of construction-time scoping would otherwise be invisible. |
| `impactClass` not a recognized enum value | Fail closed. |
| Trust level on the contract exceeds the configured maximum for the phase | A cheap phase-level ceiling: Phase 1 refuses anything above 1 regardless of what a contract claims, so a mis-edited contract cannot silently unlock a later phase's behaviour. |

**Every refusal is logged and alerted.** A refusal means a bug or an injection attempt, and both warrant a human look. Per `THREAT_MODEL.md` §5.1, `agent_proposal` rows with `disposition = 'refused'` are the primary intrusion-detection dataset of Phase 1, which is also why muting that alert is an authority change and not an operational convenience.

### 4.4 What the gate deliberately does not do

- It does not evaluate whether a proposal is *good*. Quality is the model's job and the founder's flag. The gate evaluates permissibility only, and keeping those two concerns apart is what makes it a pure function.
- It does not rank, filter for relevance, or deduplicate. That is the composer's job.
- It does not resolve conflicts between agents. `AI_AGENT_STANDARDS.md` requires conflicts be surfaced to the human, not silently resolved, so conflicting proposals both pass the gate and both reach the briefing.

## 5. High-impact actions always require approval

`MASTER_CONSTITUTION.md` §11 enumerates them. Made specific for this system:

| §11 category | Concrete LEAP OS action | Earliest phase it could exist | Approval requirement |
|---|---|---|---|
| Financial transactions | Any payment, invoice, refund, or spend commitment | Phase 3+ | Always |
| Customer communications | Any outbound message to a party outside the org: email send, Slack DM to an external member, calendar invite to an external attendee | Phase 2 (draft) / Phase 3 (send) | Always, per message. **Never batchable.** |
| Legal actions | Contract execution, notice, anything creating or waiving an obligation | Phase 3+ | Always |
| Deleting information | Any destructive operation on memory, source data, or audit records | — | Always, **and additionally not permitted to any role or agent** (§2.2). Approval is the second lock on a door that has no handle. |
| Production deployments | Any deploy | Now | Always |
| Prompt changes affecting customers | Activating a `prompt_version` | **Now, Phase 1** | Always. The only §11 category live in Phase 1, and T10 in `THREAT_MODEL.md` explains why it is more powerful than it looks. |
| Policy changes | Editing the gate table, changing an agent's trust level, changing `permittedTools`, muting a refusal alert | **Now, Phase 1** | Always |
| Security changes | Editing RLS policies, changing database roles, changing OAuth scopes, changing secret handling | **Now, Phase 1** | Always |
| Architecture rewrites | Changing `TrustGate` or `AgentContract` (`API_CONTRACTS.md` §10) | Now | Always |

Three rules make "always" mean something.

**Rule 1. High-impact status is a property of the action, not of the actor's trust level.** This is why the `high_impact` row of §4.2 never reaches `executed`. An agent at Trust Level 5 with a perfect record still queues a customer email for approval, because the reason for the gate is the consequence of being wrong, and demonstrated competence does not reduce that consequence.

**Rule 2. Classification must not be the model's unilateral decision, and this is a real weakness in the current design.** `impact_class` is declared by the agent (`DATA_MODEL.md` §9) and the gate takes the declaration at face value, having deliberately chosen not to read prose. An agent that misclassifies a customer email as `recommendation` is therefore not caught by the gate. Phase 1 is safe from this because no send tool exists in any contract, so misclassification produces a misleading recommendation rather than an action. **That safety is a property of Phase 1's tool absence, not of the gate, and it expires the moment an execution tool exists.** From Phase 2, classification needs a deterministic backstop: the impact class of an action is derived from *which tool it invokes*, and the agent's declaration is cross-checked against that derivation, with a mismatch refusing. Recording it here so Phase 2 inherits a requirement rather than discovering a gap. This is the most significant open weakness in the permission model.

**Rule 3. The approval workflow is configurable, not hardcoded** (§11, final sentence). Phase 1 builds no approval workflow, because there is nothing to approve. What Phase 1 must not do is hardcode the *absence*: the gate's `queued_for_approval` disposition exists in the enum and in the table, so Phase 3 adds a queue and a surface rather than a disposition.

`approval_chain` on `audit_record` is empty throughout Phase 1 and present because Phase 2 fills it (`DATA_MODEL.md` §9). The same reasoning applies.

## 6. Tenant isolation

Per `ADR-0005` and `ARCHITECTURE.md` §9: `org_id` on every table from migration one, RLS enforcing it, one active org.

Two defenses, deliberately redundant, because the first will eventually have a bug.

### 6.1 Defense one — required tenant argument at the repository layer

Every repository method takes `TenantContext` as its first argument (`API_CONTRACTS.md` §1). It is not read from ambient state, not from a request-local, not from a module-level singleton.

The rationale is narrow and worth stating precisely: **a function that cannot be called without a tenant context cannot forget one.** Ambient context is forgettable in exactly the situations that matter, which are background jobs, retries, cron entries, and scripts written to debug a production issue. A required parameter makes the omission a compile error, and `ADR-0005` calls this discipline structural rather than remembered — free after the first day, whereas discipline requiring memory fails on a busy Tuesday.

Two supporting rules:

- `TenantContext` also carries the `Actor` (`API_CONTRACTS.md` §1), so the provenance columns that `MEMORY_ARCHITECTURE.md` requires are populated from the same object that carries the tenant. Provenance and tenancy travel together, and neither can be supplied without the other.
- No SQL exists outside repository modules (`ADR-0002`). A single query written elsewhere is a single query outside this defense.

### 6.2 Defense two — RLS at the database

```sql
create policy tenant_isolation on episodic_record
  using (org_id = current_setting('app.current_org_id')::uuid);
```

The session variable is set by the repository layer from `TenantContext`. RLS converts an application-layer tenancy bug from a cross-tenant data leak into a query that returns nothing.

**RLS is the most dangerous control in the system**, for the reason developed in `THREAT_MODEL.md` T6 and flagged in both `ADR-0002` and `DATA_MODEL.md` §11: a too-permissive policy returns more rows, errors nothing, and passes every confirmatory test. It looks exactly like a working system, indefinitely. The specific consequences for this document:

| Requirement | Why |
|---|---|
| Adversarial test suite attempting cross-tenant reads against a synthetic second org, before any real second user exists | A policy exercised only by a single tenant has never been tested. The assertion that carries information is the negative one. |
| A schema test enumerating every `org_id`-bearing table and asserting RLS is enabled with at least one policy | Makes a new table without a policy a test failure rather than a review miss. |
| The application database role must not be `BYPASSRLS`, must not be the table owner, or `force row level security` must be set | RLS is silently inert for bypassing roles and for the owning role. A correct policy that does nothing is the worst of both worlds, because it reads as protection. |
| The Supabase service role is used only by migrations and the retention/erasure jobs, never by request-path code | The service role bypasses RLS by design (`THREAT_MODEL.md` T5). Every request-path use of it silently deletes defense two. |
| Re-verification whenever a table is added | `ADR-0002` technical debt item 1. |

### 6.3 Why two defenses rather than one good one

Because they fail independently and for different reasons. The repository argument fails to a developer mistake, which is common and caught by types. RLS fails to a policy mistake, which is rare and caught by nothing. Neither is strong enough alone: types cannot enforce a runtime predicate, and RLS cannot be relied upon as a sole control when the same codebase also holds a role that bypasses it. Together, a cross-tenant leak requires two independent errors of different kinds, which is materially less likely than one.

## 7. Advancing and revoking trust levels

`AI_AGENT_STANDARDS.md` sets the standard: advancement requires a minimum volume of successful human-verified outcomes at the current level, a documented failure-mode review with no unresolved critical failures, and explicit human sign-off recorded in the knowledge system. Revocation is instant on regression. `OBSERVABILITY.md` adds the mechanism that makes this evidence-based rather than a gut call.

Made concrete.

### 7.1 Advancement criteria

| Requirement | Level 0 → 1 | Level 1 → 2 (draft) | Level 2 → 3 (execute on approval) |
|---|---|---|---|
| Minimum volume at current level | 14 consecutive weekdays of briefings (`PRD.md` §9) | 30 days at Level 1 with a measured recommendation acceptance rate | 30 days at Level 2 with a measured draft acceptance rate |
| Quality bar | **Zero misleading recommendations** in the final 14-day window; a flag resets the window (`PRD.md` §9) | Acceptance rate stable or improving; no flagged item traced to a systematic cause that remains unfixed | Draft edit rate below an agreed threshold; zero drafts that would have caused harm if sent unedited |
| Failure-mode review | Documented, no unresolved critical items in the risk register | Same, plus a review of every flagged item with root cause and disposition | Same, plus rollback and blast-radius analysis for each action in the proposed action set |
| Gate evidence | Adversarial gate test passing: an agent deliberately configured to attempt a Level 3 action is refused (`PRD.md` C1) | Same, plus the two-permission-systems seam test (`ADR-0003` debt item 1) | Same, plus the tool-derived impact-class cross-check from §5 Rule 2 |
| Tool scope review | `permittedTools` reviewed against the responsibility statement; nothing unjustified | Same, and the new tool is justified in one sentence of the responsibility | Same |
| Sign-off | **Owner only**, recorded as a `decision` semantic record with rationale and links to the evidence | Same | Same |
| Recorded where | Semantic layer as a `decision` record, per `MEMORY_ARCHITECTURE.md`; the contract change is itself an audited high-impact policy change (§5) | Same | Same |

Three notes.

**Advancement is per agent, not per system.** Email Intelligence reaching Level 2 says nothing about Meeting Intelligence. Trust is earned by a responsibility, and the evidence supporting it is evidence about that responsibility.

**Advancement is a configuration change against a contract, not a code change** (`ADR-0003`). That is a genuine benefit of the architecture and also a hazard, because the cheapness of the change is not proportional to its consequence. Hence owner-only sign-off, an audit record, and a written decision record with the evidence attached.

**The evidence must exist before the review, not be assembled for it.** This is the whole reason `PRD.md` §3 has Phase 1 instrument for the learning loop without closing it, and why `agent_proposal` stores `trust_level` as applied at the time rather than joining to current configuration (`DATA_MODEL.md` §9). Raising an agent's trust level must not retroactively rewrite what authorized a past action, or the record supporting the next advancement is contaminated by the last one.

### 7.2 Revocation

Instant, unilateral, and cheap on purpose.

| Trigger | Response |
|---|---|
| A flagged misleading recommendation traced to a systematic cause | Investigate at current level; revoke if the cause is not understood within the review window |
| Any action taken that a human would not have approved | **Immediate revocation to Level 1**, no review period, no discussion |
| A gate refusal traced to an agent attempting an action above its level, other than in a test | Immediate revocation pending root cause. The agent asked; that is the signal. |
| Evidence that an injected instruction changed agent behaviour | Immediate revocation of the affected agent, plus a `THREAT_MODEL.md` T1/T3 incident and a review of the memory the injection may have poisoned |
| Any security-relevant incident touching the authority layer | Revoke all agents to Level 1 until the incident is closed. The blast radius of an unknown authority defect is every agent. |
| A processing or privacy incident | Revoke to Level 1; an agent that should not be trusted with data should not be trusted with actions |

Two governing rules:

**Revocation requires no sign-off, only a record.** Advancement is deliberately hard and revocation is deliberately trivial, and the asymmetry is the mechanism. Anyone who can observe a regression can revoke. `OBSERVABILITY.md` puts it directly: if a system cannot explain what it did, dial it back to Recommend until it can.

**Revocation is not a punishment and should not be treated as costly.** A system where revoking trust requires justifying oneself is a system where trust is not revoked. Every revocation produces an incident record with root cause per `SECURITY_STANDARDS.md`, regardless of severity, and that record is the input to the next advancement rather than an accusation.

## 8. Open questions and known weaknesses

1. **Impact-class classification is the model's unilateral decision (§5 Rule 2).** The gate is prose-blind by design, which means it cannot detect a misdeclared impact class. Phase 1 is safe only because no dangerous tool exists. The tool-derived cross-check is required before Phase 2 grants any tool with an external effect, and it is the single most important thing this document asks a later phase to build.
2. **Role checks are unimplemented.** §2.2 is a specification, not a description. Phase 1 enforces nothing at the role layer because there is one user in the owner role. The risk is that Phase 2 adds users before it adds enforcement, since the schema will accept a `member` row today and nothing will stop that user from doing everything. **A minimal enforcement point — one function mapping role to capability, called at every entry point, defaulting to deny — should exist before the second user, not with them.**
3. **No separation of duties.** The owner advances trust levels, activates prompts, approves security changes, and is also the sole reviewer of all of the above. Structurally unavoidable in a single-person phase, and worth naming rather than describing a control that does not exist. Phase 2's first additional `admin` is the point at which two-person review on trust advancement becomes possible and should become required.
4. **Agent identity is a string.** `agent_proposal.agent_id` and `prompt_version.agent_id` are `text` with no foreign key to a registry of contracts, because contracts live in code rather than in the database. A typo produces an orphan audit trail that looks like a real one. A contract registry table with a foreign key is cheap and would make the audit trail's actor column trustworthy.
5. **`viewer` retains the flag affordance in §2.2's Phase 1 column and must lose it in Phase 2** (§2.2, third note). Recorded so it is a scheduled change rather than a discovered inconsistency.
6. **Muting an alert is an authority change and nothing enforces that.** §3.2 and §4.3 both assert it. There is no mechanism making an alert configuration change go through the same path as a gate change, and alert fatigue after a noisy week is the concrete form T11 most often takes.
