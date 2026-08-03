# Phase 1 — API Contracts

**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

`ENGINEERING_STANDARDS.md` requires every component to expose a documented interface and be independently replaceable, with no reaching into another module's internals. This document is those interfaces. They are the contract; the implementations behind them are details.

Written as TypeScript per `ADR-0001`. Types shown are illustrative but intended to be precise enough to implement against directly.

---

## 1. Shared primitives

```ts
/** Tenant context. Required by every repository call — a function that
 *  cannot be invoked without a tenant cannot forget one (ADR-0005). */
export interface TenantContext {
  readonly orgId: OrgId;
  readonly actor: Actor;
}

export type Actor =
  | { readonly kind: 'human'; readonly userId: UserId }
  | { readonly kind: 'agent'; readonly agentId: AgentId }
  | { readonly kind: 'system'; readonly process: string };

/** Branded identifiers. Prevents passing an EpisodicId where a
 *  SemanticId is expected — a class of bug that is otherwise invisible
 *  because both are strings. */
export type OrgId       = string & { readonly __brand: 'OrgId' };
export type UserId      = string & { readonly __brand: 'UserId' };
export type AgentId     = string & { readonly __brand: 'AgentId' };
export type EpisodicId  = string & { readonly __brand: 'EpisodicId' };
export type SemanticId  = string & { readonly __brand: 'SemanticId' };
export type ProposalId  = string & { readonly __brand: 'ProposalId' };

/** Explicit results at fallible boundaries. Thrown exceptions are for
 *  programmer error; expected failures are values (CODING_STANDARDS.md,
 *  explicit over implicit). */
export type Result<T, E = AppError> =
  | { readonly ok: true;  readonly value: T }
  | { readonly ok: false; readonly error: E };

export interface AppError {
  readonly code: string;
  readonly message: string;
  readonly retryable: boolean;
  readonly cause?: unknown;
}
```

Branded identifiers are worth the small ceremony. Every identifier in this system is a UUID string, which means the type system cannot distinguish an episodic record from a semantic one without branding — and confusing those two is exactly the mistake that would produce a briefing item citing the wrong evidence.

## 2. Source adapters

The interface that makes `ADR-0006`'s sequential increments additive. Adding a source means implementing this and nothing else.

```ts
export interface SourceAdapter {
  readonly system: SourceSystem;

  /** Fetch events since the opaque cursor. The pipeline never
   *  interprets the cursor; only the adapter does. */
  fetchSince(
    connection: SourceConnection,
    cursor: string | null,
    limit: number,
  ): Promise<Result<FetchPage, FetchError>>;

  /** Runtime schema for this adapter's payloads. The normalizer
   *  validates against it at the trust boundary — TypeScript types are
   *  gone at runtime and every payload here is untrusted. */
  readonly payloadSchema: RuntimeSchema<unknown>;
}

export interface FetchPage {
  readonly events: readonly RawEvent[];
  /** Cursor to persist *only if* every event in this page is
   *  successfully written. Partial failure must not advance it
   *  (ARCHITECTURE.md §4). */
  readonly nextCursor: string | null;
  readonly hasMore: boolean;
}

export interface RawEvent {
  readonly kind: EpisodicKind;
  readonly sourceId: string;        // idempotency key within the connection
  readonly occurredAt: Date;
  readonly payload: unknown;        // validated by the normalizer, not here
  readonly participants: readonly string[];
  /** ASR or extraction confidence where the source reports it.
   *  Absent means "source does not report confidence", which is
   *  different from low confidence and must not be conflated. */
  readonly sourceConfidence?: number;
}

export interface FetchError extends AppError {
  readonly kind: 'rate_limited' | 'auth_failed' | 'unavailable'
               | 'malformed' | 'unknown';
  readonly retryAfterMs?: number;
}
```

Three notes on the shape.

`retryable` and `retryAfterMs` are on the error rather than inferred by the caller, because only the adapter knows whether a given upstream failure is transient. A caller guessing produces either hammered APIs or abandoned data.

`sourceConfidence` being optional-and-meaningful is a small but real distinction. Gmail does not report confidence; a transcript provider does. Treating "not reported" as "zero confidence" would silently exclude all email from the briefing, and treating it as "full confidence" would silently promote bad ASR. The absence has to be representable.

The adapter does not validate its own payloads. Validation belongs to the normalizer, on the far side of the trust boundary, so that a compromised or buggy adapter cannot self-certify.

## 3. Ingestion

```ts
export interface Normalizer {
  /** Validate, stamp provenance, and write idempotently. Returns the
   *  count written and any events quarantined for failing validation. */
  ingest(
    ctx: TenantContext,
    connection: SourceConnection,
    events: readonly RawEvent[],
  ): Promise<Result<IngestOutcome>>;
}

export interface IngestOutcome {
  readonly written: number;
  readonly duplicatesSkipped: number;
  readonly quarantined: readonly QuarantinedEvent[];
  /** True only if every event was written or was a known duplicate.
   *  The watermark advances on this and nothing else. */
  readonly safeToAdvanceCursor: boolean;
}

export interface QuarantinedEvent {
  readonly sourceId: string;
  readonly reason: string;
  readonly rawPayload: unknown;
}
```

`safeToAdvanceCursor` is a single boolean carrying the whole correctness argument of the ingestion pipeline. Making it an explicit field rather than something the caller derives means the rule lives in one place and can be tested directly.

## 4. Memory repositories

All data access. No SQL exists outside these modules (`ADR-0002`).

```ts
export interface EpisodicRepository {
  /** Conflict semantics, specified rather than left to the
   *  implementation: on conflict against
   *  (org_id, source_connection_id, source_id), compare `content_hash`.
   *  Unchanged hash means skip and count as a duplicate. Changed hash
   *  means UPDATE the payload.
   *
   *  This is not a detail. `ROLLBACK_STRATEGY.md` answers most failures
   *  with "fix forward and re-run", and that answer is only true if
   *  re-running can *repair* a bad payload. Plain `on conflict do
   *  nothing` would make every re-run a no-op and quietly invalidate
   *  the rollback story for its most-invoked case. */
  upsertMany(
    ctx: TenantContext,
    records: readonly NewEpisodicRecord[],
  ): Promise<Result<UpsertOutcome>>;

  findByWindow(
    ctx: TenantContext,
    from: Date,
    to: Date,
    kinds?: readonly EpisodicKind[],
  ): Promise<Result<readonly EpisodicRecord[]>>;

  findById(
    ctx: TenantContext,
    id: EpisodicId,
  ): Promise<Result<EpisodicRecord | null>>;
}

export interface SemanticRepository {
  /** Write a record together with its source links in one
   *  transaction. There is deliberately no method to create a
   *  semantic record without links — the no-orphans rule from
   *  MEMORY_ARCHITECTURE.md is expressed in the interface, so
   *  violating it is not something a caller can express. */
  create(
    ctx: TenantContext,
    record: NewSemanticRecord,
    derivedFrom: readonly EpisodicId[],   // must be non-empty
  ): Promise<Result<SemanticRecord>>;

  findByDedupeKey(
    ctx: TenantContext,
    dedupeKey: string,
  ): Promise<Result<SemanticRecord | null>>;

  /** Mark superseded and link forward atomically. There is no
   *  delete method on this repository at all. */
  supersede(
    ctx: TenantContext,
    oldId: SemanticId,
    newRecord: NewSemanticRecord,
    derivedFrom: readonly EpisodicId[],
  ): Promise<Result<SemanticRecord>>;

  /** Similarity search returning records *with* their provenance,
   *  because every retrieval must be explainable
   *  (MEMORY_ARCHITECTURE.md, OBSERVABILITY.md). A search that
   *  returned bare text would make explainability optional. */
  searchSimilar(
    ctx: TenantContext,
    embedding: readonly number[],
    opts: { limit: number; kinds?: readonly SemanticKind[]; minConfidence?: number },
  ): Promise<Result<readonly RetrievedRecord[]>>;

  findActive(
    ctx: TenantContext,
    kind: SemanticKind,
    opts?: { limit?: number },
  ): Promise<Result<readonly SemanticRecord[]>>;
}

export interface RetrievedRecord {
  readonly record: SemanticRecord;
  readonly similarity: number;
  readonly sources: readonly EpisodicId[];   // never empty
}
```

The two absences here are the design. `SemanticRepository` has no `create`-without-links and no `delete` at all. Constitutional rules that can be expressed as *missing methods* are stronger than rules expressed as documentation, because a caller cannot write the violating code.

```ts
export interface KnowledgeManager {
  /** Deduplicate, link, and supersede. The only sanctioned path into
   *  the semantic layer — the extractor proposes facts, this decides
   *  what happens to them. */
  reconcile(
    ctx: TenantContext,
    candidates: readonly CandidateFact[],
  ): Promise<Result<ReconcileOutcome>>;
}

export interface CandidateFact {
  readonly kind: SemanticKind;
  readonly statement: string;
  readonly attributes: Readonly<Record<string, unknown>>;
  readonly confidence: number;
  readonly derivedFrom: readonly EpisodicId[];
}

export interface ReconcileOutcome {
  readonly created: readonly SemanticId[];
  readonly linkedToExisting: readonly SemanticId[];
  readonly superseded: readonly { old: SemanticId; new: SemanticId }[];
  readonly rejected: readonly { candidate: CandidateFact; reason: string }[];
}
```

## 5. Agent runtime and contracts

The substrate boundary from `ADR-0003`. Deliberately narrow: *given a contract and an input, return proposals.* Anything the SDK offers that does not fit through this interface should be treated with suspicion, because using it would leak the substrate into the architecture.

```ts
export interface AgentContract {
  readonly agentId: AgentId;
  /** One sentence, single purpose. If it needs "and", it is two
   *  agents (AI_AGENT_STANDARDS.md). */
  readonly responsibility: string;
  /** The level this agent is *designed* for, in source. Declaring it
   *  here documents intent and drives tool scoping.
   *
   *  It is deliberately NOT the level the gate enforces. The effective
   *  level is resolved from persisted configuration at gate time, so
   *  that revoking trust is a configuration write taking effect on the
   *  next proposal. A compile-time literal would make "instant
   *  revocation" require a build, a CI run, and a deploy — which is
   *  not instant, and the constitution's revocation guarantee
   *  (AI_AGENT_STANDARDS.md) would be false. */
  readonly designedTrustLevel: 0 | 1 | 2 | 3 | 4 | 5;
  /** Permitted tools, resolved at construction. An agent does not
   *  hold a tool it is instructed not to use — it does not hold the
   *  tool. Instruction is not a security control. */
  readonly permittedTools: readonly ToolName[];
  readonly promptVersionId: string;
  /** What to do when uncertain. Defaults to proposing at a lower
   *  impact class rather than guessing (AI_AGENT_STANDARDS.md). */
  readonly escalation: 'propose_lower_impact' | 'surface_to_human';
}

export interface AgentSubstrate {
  run(
    ctx: TenantContext,
    contract: AgentContract,
    input: AgentInput,
  ): Promise<Result<readonly Proposal[]>>;
}

export interface AgentInput {
  readonly task: string;
  /** Retrieved memory, passed as clearly delimited data. Never
   *  concatenated into instructions — ingested content is untrusted
   *  (SECURITY_STANDARDS.md). */
  readonly context: readonly RetrievedRecord[];
  readonly asOf: Date;
}
```

```ts
export interface Proposal {
  readonly agentId: AgentId;
  /** Declared by the agent. The gate refuses an absent or malformed
   *  value rather than inferring one — fail closed. */
  readonly impactClass: ImpactClass;
  /** Orthogonal to impactClass, not a member of it. An action can be
   *  both irreversible and high-impact, and an enum would force a
   *  false choice between saying so. High-impact proposals never reach
   *  `executed` at any trust level (PERMISSION_MODEL.md). */
  readonly isHighImpact: boolean;
  readonly payload: ProposalPayload;
  readonly rationale: string;
  readonly confidence: number;
  /** Evidence. Non-empty is enforced by the gate: a proposal that
   *  cannot cite its sources cannot be surfaced (PRD.md B2). */
  readonly evidence: readonly EvidenceRef[];
}

export type ImpactClass =
  | 'observation' | 'recommendation' | 'draft'
  | 'reversible_action' | 'irreversible_action';

export interface EvidenceRef {
  readonly semanticId?: SemanticId;
  readonly episodicId?: EpisodicId;
  readonly sourceUrl?: string;
}
```

## 6. The authority layer

The most important interface in the system.

```ts
export interface ToolScoper {
  /** Resolve a contract's declared tools into concrete implementations.
   *  Called before the agent loop starts. A tool absent from the
   *  contract is absent from the agent's runtime. */
  scope(contract: AgentContract): readonly Tool[];
}

/** The gate is two functions, not one, because purity and durability
 *  cannot live in the same signature. `decide` is the authority rule;
 *  `evaluate` is the only sanctioned way to invoke it. */
export interface TrustGate {
  /** PURE and SYNCHRONOUS. No I/O, no clock, no randomness. Same
   *  inputs, same disposition, every time, regardless of how the model
   *  phrased the proposal — it does not read proposal prose, only the
   *  declared impact class and high-impact flag.
   *
   *  Being pure is what makes the truth table exhaustively testable
   *  (TESTING_STRATEGY.md): 36 cells, no mocks, no database. */
  decide(input: GateInput): GateVerdict;

  /** The only path from proposal to effect. Resolves the agent's
   *  effective trust level from persisted configuration, calls
   *  `decide`, writes the audit record, and returns the outcome.
   *
   *  Authorizing and logging happen here together, which is what makes
   *  an unlogged effect inexpressible rather than merely discouraged. */
  evaluate(
    ctx: TenantContext,
    contract: AgentContract,
    proposal: Proposal,
  ): Promise<Result<GateDecision>>;
}

export interface GateInput {
  readonly impactClass: ImpactClass | 'malformed';
  readonly isHighImpact: boolean;
  readonly effectiveTrustLevel: number;
  readonly hasEvidence: boolean;
  readonly hasRationale: boolean;
  readonly usesOnlyPermittedTools: boolean;
}

export interface GateVerdict {
  readonly disposition: GateDisposition;
  readonly refusalReason?: string;
}

export interface GateDecision {
  readonly proposalId: ProposalId;
  readonly disposition: GateDisposition;
  readonly refusalReason?: string;
  /** Trust level as applied *at this moment*, recorded on the
   *  decision. Raising an agent's trust level later must not
   *  retroactively rewrite what authorized a past action. */
  readonly appliedTrustLevel: number;
}

export type GateDisposition =
  | 'logged' | 'surfaced' | 'drafted'
  | 'queued_for_approval' | 'executed' | 'discarded' | 'refused';
```

The gate refuses, rather than accepts, in each of these cases:

- Impact class absent or not a recognized value.
- Impact class exceeding the contract's trust level per the table in `ARCHITECTURE.md` §5.
- `evidence` empty for anything to be surfaced.
- `rationale` empty.
- Proposal referencing a tool not in `permittedTools`.

Every refusal is logged *and alerted*, because a refusal means either a bug or an injection attempt and both warrant a human look (`OBSERVABILITY.md`).

```ts
export interface AuditWriter {
  /** Append-only. There is no update or delete method, mirroring the
   *  revoked privileges at the database level (DATA_MODEL.md §9). */
  append(ctx: TenantContext, record: NewAuditRecord): Promise<Result<void>>;
}
```

## 7. Briefing composition and rendering

The separation `ADR-0004` requires, so that adding a surface is a new renderer rather than a rewrite.

```ts
export interface BriefingComposer {
  compose(
    ctx: TenantContext,
    recipient: UserId,
    date: Date,
  ): Promise<Result<BriefingDocument>>;
}

/** Surface-agnostic. Knows nothing about email, HTML, or Slack. */
export interface BriefingDocument {
  readonly briefingDate: Date;
  readonly recipient: UserId;
  readonly sections: readonly BriefingSection[];
  readonly generatedAt: Date;
  readonly meta: { readonly generationMs: number; readonly tokenCost: number };
}

export interface BriefingSection {
  readonly kind: BriefingSectionKind;
  readonly title: string;
  /** Non-empty by construction. An empty section is omitted from
   *  `sections` entirely rather than rendered empty — a briefing that
   *  says "no customer issues today" three hundred times teaches the
   *  reader to skim (UX_PRINCIPLES.md). */
  readonly items: readonly [BriefingItem, ...BriefingItem[]];
}

export interface BriefingItem {
  readonly proposalId: ProposalId;
  readonly headline: string;
  readonly detail?: string;
  /** Required, so no renderer can omit it. UX_PRINCIPLES.md §1 becomes
   *  a type-level guarantee rather than a review checklist item. */
  readonly trustLevel: number;
  readonly trustLabel: string;      // "Recommendation" throughout Phase 1
  /** Non-empty tuple: an item without evidence is not
   *  representable (PRD.md B2). */
  readonly evidence: readonly [EvidenceLink, ...EvidenceLink[]];
  /** The only interactive element in the briefing. It is a
   *  state-changing URL sitting in a mailbox, so it is typed with its
   *  security properties rather than as a bare string — see ADR-0007. */
  readonly flag: FlagAffordance;
}

export interface FlagAffordance {
  readonly url: string;
  /** Single-use, item-scoped, expiring. Bound to one briefing item so
   *  a leaked token cannot flag anything else, and carrying no
   *  ambient authority beyond writing one error_flag row. */
  readonly token: string;
  readonly expiresAt: Date;
}

export interface EvidenceLink {
  readonly label: string;
  readonly url: string;             // deep link into the source system
  readonly sourceSystem: SourceSystem;
}
```

Two non-empty tuple types — `[BriefingItem, ...BriefingItem[]]` and `[EvidenceLink, ...EvidenceLink[]]` — do real work. They make "no empty sections" and "no unsourced items" compile-time facts rather than runtime checks someone might forget. This is the clearest available example of the general principle: prefer constraints the compiler enforces over rules a reviewer must remember.

```ts
export interface BriefingRenderer<TOutput> {
  readonly surface: string;
  render(doc: BriefingDocument): Result<TOutput>;
}

export interface EmailPayload {
  readonly subject: string;
  readonly html: string;
  readonly text: string;            // plain-text alternative, required
}

export interface BriefingDelivery {
  /** Sending is the one non-idempotent operation in the system. Every
   *  other step is protected by a database constraint; this one leaves
   *  the building and cannot be recalled (ROLLBACK_STRATEGY.md).
   *
   *  The guard is therefore explicit and at the application layer:
   *  send() must refuse if `briefing.delivered_at` is already set for
   *  (org, recipient, date). Without it, a safe regeneration — which
   *  the rollback strategy actively encourages — produces a second
   *  email, and two briefings in one morning reads as a malfunction to
   *  the one person whose trust the phase exists to earn. */
  send(
    ctx: TenantContext,
    recipient: UserId,
    payload: EmailPayload,
  ): Promise<Result<DeliveryReceipt, AlreadyDeliveredError | AppError>>;

  /** Sent when generation fails. Silence is indistinguishable from
   *  "nothing mattered today", which is the worst failure mode
   *  available to a trust-building product (PRD.md B1). */
  sendFailureNotice(
    ctx: TenantContext,
    recipient: UserId,
    reason: string,
  ): Promise<Result<DeliveryReceipt>>;
}
```

## 8. Scheduler

```ts
export interface Scheduler {
  registerJob(job: ScheduledJob): void;
  start(): Promise<void>;
  stop(): Promise<void>;
}

export interface ScheduledJob {
  readonly name: string;
  readonly cron: string;
  /** Every job must be safe to run twice. Ingestion is idempotent by
   *  database constraint; briefing generation is idempotent per
   *  (org, recipient, date). This is what makes the rollback strategy
   *  for most failures "re-run it" (ROLLBACK_STRATEGY.md). */
  readonly idempotent: true;
  run(): Promise<Result<void>>;
}
```

`idempotent: true` as a literal type rather than a boolean is intentional: it is not a property a job declares about itself, it is a precondition for being schedulable at all.

## 9. Observability

```ts
export interface Logger {
  /** Structured only. No string interpolation of values into
   *  messages, so logs stay queryable (OBSERVABILITY.md). */
  info(event: string, fields: Readonly<Record<string, unknown>>): void;
  warn(event: string, fields: Readonly<Record<string, unknown>>): void;
  error(event: string, fields: Readonly<Record<string, unknown>>): void;
}

export interface Metrics {
  counter(name: string, tags?: Readonly<Record<string, string>>): void;
  gauge(name: string, value: number, tags?: Readonly<Record<string, string>>): void;
  histogram(name: string, value: number, tags?: Readonly<Record<string, string>>): void;
}

export interface Tracer {
  /** A single briefing must be traceable back through every agent and
   *  record that contributed to it (OBSERVABILITY.md). */
  span<T>(name: string, fn: (span: Span) => Promise<T>): Promise<T>;
}
```

A redaction obligation applies across all three: no logger, metric tag, or span attribute may carry message bodies, transcript text, or credentials. Enforced by a lint rule plus a test asserting that known-sensitive field names never appear in emitted log output — see `PRIVACY_MODEL.md`.

## 10. Contract stability

These interfaces are the reviewed artifact. Changing one after implementation begins requires updating this document in the same change, per `MASTER_CONSTITUTION.md` §17 and `DEFINITION_OF_DONE.md`.

Two interfaces are load-bearing for the constitution's guarantees and should be treated as the hardest to change: `TrustGate` and `AgentContract`. A change to either alters what the system is permitted to do, which makes it a security change under `MASTER_CONSTITUTION.md` §11 and therefore subject to approval rather than ordinary review.
