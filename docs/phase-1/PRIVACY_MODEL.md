# Phase 1 — Privacy Model

**Date:** 2026-08-03
**Status:** Draft for critical review, per `MASTER_CONSTITUTION.md` §6

Required by `MASTER_CONSTITUTION.md` §6 and §15, and by `SECURITY_STANDARDS.md`, which requires data handling for retention, deletion, and export to be designed into the first schema rather than retrofitted. Companion to `DATA_MODEL.md` (which defers two decisions here) and `THREAT_MODEL.md`.

---

## 1. The framing that matters

Phase 1 has one user. It does not have one data subject.

That sentence is the whole privacy problem. The founder consented to LEAP OS; the founder connected the accounts; the founder reads the briefing. Nobody else did any of those things. But the corpus LEAP OS ingests is overwhelmingly *other people's* personal data: the people who emailed the founder, the people on the founder's calendar, the people who spoke on recorded customer calls, the colleagues in a Slack channel. None of them know LEAP OS exists. None of them agreed to have their words distilled into durable semantic records, embedded as vectors, and transmitted to a model API.

A privacy model written from the user's perspective would be almost empty and would be wrong. This one is written from the third party's perspective, because that is where the actual obligations sit.

The second framing point follows from `ADR-0005`. The single active tenant is the founder's own organization, so LEAP OS is currently an *internal* tool: the organization is processing data it already lawfully held for its own purposes. That posture makes Phase 1 defensible. It also does not survive Phase 4, when external customers arrive and LEAP OS becomes a processor acting on *their* data subjects. Everything below should be read as: correct now, and structured so that the Phase 4 version is an extension rather than a rewrite.

## 2. Data inventory

What Phase 1 actually processes, by source, with the sensitivity that matters rather than the sensitivity that is easy to write down.

| Source | Personal data ingested | Whose | Sensitivity notes |
|---|---|---|---|
| **Gmail** | Full message bodies, subjects, sender and recipient addresses, display names, thread structure, timestamps. Attachments are **not** ingested in Phase 1. | Every correspondent, and every person merely *mentioned* in a message | Bodies are unbounded free text. They routinely contain health, financial, employment, and family information that nobody classified as such. Assume special-category data is present. |
| **Google Calendar** | Event titles, descriptions, times, locations, **full attendee lists with email addresses**, and response status | Every attendee, including external ones | Attendee lists are an under-appreciated disclosure. They reveal an organization's relationship graph — who is talking to which customer, which candidate is interviewing, which lawyer is involved — with far less noise than email bodies. Response status additionally reveals behaviour. |
| **Voice call transcripts** | Verbatim speech of all parties, speaker attribution, timing, plus derived intent, sentiment, objections, and outcomes per `MASTER_CONSTITUTION.md` §13 | Customers, prospects, and anyone else on the call | **The sharpest issue in this document. See §3.** Derived sentiment and coaching signals are new personal data about the speaker that did not exist before we created it. |
| **Slack** | Message text within opted-in channels, thread structure, author identity, timestamps | Colleagues, and external members of shared channels | Channels default to out-of-scope with explicit opt-in (`PRD.md` A4), which is a genuine minimization control and not merely a configuration convenience. Internal Slack is a candid register; people write things there they would not write in email. |
| **Derived — semantic layer** | Commitments, decisions, open questions, and person/project entities attributed to named individuals | Everyone above | This is a *profile*. "Person X owes Y, has previously decided Z, sounded frustrated on the last two calls" is a materially different artifact from the messages it came from, and it is the artifact that persists indefinitely. |
| **Derived — embeddings** | `vector(1536)` per semantic record | Everyone above | Not human-readable, and not anonymous. Embeddings of short specific statements are substantially invertible and must be treated as personal data, not as a hash. Deleting a `statement` while retaining its embedding does not accomplish deletion. |
| **Operational** | The founder's identity, briefing open times, error flags | The founder | Behavioural data about the user. Low sensitivity, but it is the user's data and belongs in an export. |

**Not ingested, deliberately:** email attachments and their contents, Google Drive, contact lists as a standalone import, call *audio* (only transcripts), Slack DMs, and any channel not explicitly opted in. Each of these is a plausible next increment and each would materially widen exposure. They are excluded because Phase 1 does not need them, which is the only good reason to exclude anything.

## 3. Third parties who never consented

This is the issue that deserves the most weight and receives the least attention in comparable systems, so it gets its own section.

### 3.1 The specific problem

When a customer calls the company and the call is recorded and transcribed, that customer has, at best, consented to *the company* recording the call for *the company's* stated purposes. They have not agreed to:

- verbatim retention of their speech in a third-party database for 400 days;
- extraction of durable claims about their commitments and intentions into a store with indefinite retention;
- generation of sentiment, objection, and "missed opportunity" assessments about them, which are inferred personal data they never disclosed and cannot see;
- transmission of their words to Anthropic's API for processing by a model.

The company may nonetheless be lawfully entitled to do most of this. But entitlement is not the same as having thought about it, and a system that quietly industrialises the step from "we recorded the call" to "we maintain an evolving behavioural profile of the caller" has changed the nature of the processing even where it has not changed its legality.

### 3.2 Call-recording consent varies by jurisdiction, and the variation is not academic

LEAP OS does not perform the recording. It consumes transcripts, which means the consent obligation sits upstream, with whatever system captures the call. That is a real limitation on our responsibility and it is not a defence, because ingesting an unlawfully obtained recording extends the problem rather than isolating it.

| Regime | Requirement | Consequence for LEAP OS |
|---|---|---|
| US federal and majority of states | One-party consent | The company's own participation suffices. Transcripts are lawful to obtain. |
| California, Florida, Illinois, Massachusetts, Pennsylvania, Washington and others (**two-party / all-party consent**) | Every party must consent | A recording made without notifying the caller may be unlawful *and criminal*, in some states independently of any privacy statute. A transcript derived from it is fruit of that. |
| EU / UK (GDPR) | Lawful basis plus transparency plus purpose limitation. Consent, where relied upon, must be specific and informed. | Notice must cover the actual purposes, which now include AI analysis and durable profiling. A notice saying "calls may be recorded for quality and training purposes" does not obviously cover generating and retaining behavioural assessments. |
| Canada (PIPEDA) | Knowledge and consent, and the purpose must be one a reasonable person would consider appropriate | The appropriateness test bites here in a way a pure consent test does not. |

Two operational rules follow, and they are the concrete output of this section:

**PR-1. The transcript provider decision is a privacy decision, not only a technical one.** `ADR-0006`'s open question on provider selection must be answered with reference to whether the provider captures and records consent, whether it applies all-party notice, and whether it can tell us the jurisdiction of the remote party. A provider that hands us transcripts with no consent metadata leaves us unable to answer the only question that matters, and we should treat that as disqualifying rather than as a gap to paper over.

**PR-2. Absent reliable consent metadata, transcripts are ingested only from calls where the company controls the notice.** Concretely: calls placed or received through the company's own telephony with an all-party recording announcement. Inbound calls from unknown jurisdictions without announcement are out of scope for increment 1b until PR-1 is resolved. This narrows increment 1b and that is the correct trade, because the alternative is a compliance exposure that a briefing feature does not justify.

### 3.3 Notice to third parties

Honest position: **Phase 1 provides no notice to third parties that LEAP OS exists.** An email correspondent is not told their message was distilled into a semantic record. This is defensible while LEAP OS is an internal tool processing data the organization already lawfully held, under the same lawful basis as the underlying inbox, and covered by whatever privacy notice the company already publishes. It is not defensible indefinitely, and two obligations follow:

1. The company's existing privacy notice should name AI-assisted analysis of correspondence and calls as a purpose. That is a document edit, not engineering work, and it should happen before increment 1b ships.
2. Phase 4 changes this materially. Processing another organization's data subjects makes LEAP OS a processor, requires a data processing agreement, and makes the customer responsible for notice while making us responsible for having the controls to support it. The schema is built for that; the paperwork is not, and it is not Phase 1 work.

## 4. Lawful basis and purpose limitation

| Processing | Basis (GDPR framing, applied by analogy where GDPR does not directly apply) | Note |
|---|---|---|
| Ingesting the founder's own mail, calendar, and Slack | Legitimate interests of the organization in operating and improving its own work, and the founder's own instruction as user and data owner | The founder is both user and, for their own data, the subject. Simple. |
| Ingesting third-party content within those sources | Legitimate interests, with the balancing test resting on the fact that the organization already lawfully held this data for the same purpose (running its business) and LEAP OS narrows rather than widens who sees it | The balancing test is not automatically satisfied. It is satisfied by purpose continuity: LEAP OS helps the founder respond to correspondence they were already going to read. It would **not** be satisfied by using the same corpus to build a model, to score individuals for unrelated purposes, or to enrich against external data. |
| Ingesting call transcripts | Legitimate interests, **conditional on lawful recording upstream** (§3.2) | The weakest link. PR-2 exists because of it. |
| Deriving semantic records and profiles | Same basis, same purpose | The derivation is the product. It is also the step that most changes the character of the processing, so it is the step where purpose limitation is doing the most work. |
| Transmitting content to Anthropic for processing | Processor relationship under the same basis (§9) | Requires disclosure, not a separate basis. |
| Retaining audit records | **Legal obligation and legitimate interests in accountability**, deliberately a *different* basis from the operational processing | This distinction is the mechanism that resolves the deletion tension in §6. Audit retention does not depend on the operational basis, so withdrawing or exhausting the operational basis does not require deleting audit records. |

### Purpose limitation, stated as prohibitions

Purpose limitation is only meaningful as a list of things the data will not be used for. For Phase 1:

- **Not** for training or fine-tuning any model, ours or a vendor's. This is also asserted contractually against Anthropic (§9).
- **Not** for evaluating or scoring employees. `MASTER_CONSTITUTION.md` §13's call intelligence assesses *calls and prompts*, and the Sales Coach agent in `AI_AGENT_STANDARDS.md` will produce coaching signals about people. Phase 1 does not build it, and when it arrives the distinction between "coaching a rep" and "surveilling a rep" needs a written line rather than an assumption. Flagged now because the data being accumulated in Phase 1 is exactly the data that would enable it.
- **Not** for enrichment against external data sources.
- **Not** for any purpose outside the daily briefing and the memory that supports it, without a documented purpose extension reviewed under this document.

## 5. Data minimization

Minimization at ingestion is worth more than minimization anywhere else, because data not collected cannot leak, cannot be subpoenaed, cannot be exfiltrated by T4 or T7 in `THREAT_MODEL.md`, and does not need deleting.

Controls actually in place in Phase 1:

| Control | Mechanism | Effect |
|---|---|---|
| Read-only OAuth scopes | Narrowest available Gmail and Calendar read scopes | A compromised token cannot send or delete. Also bounds what we *could* collect. |
| No attachment ingestion | Adapter does not fetch attachment content | Removes the highest-density-per-byte category of sensitive content. |
| Slack channels opt-in, default out | `source_connection.config` (`DATA_MODEL.md` §5) | The founder must positively add each channel. The default is the minimizing one. |
| No Slack DMs | Adapter scope | DMs are the most private register in the tool. |
| Transcripts only, never audio | Adapter scope | Removes voiceprint biometrics entirely, which in some jurisdictions is a special category of its own. |
| Structured extraction over retention-by-default | Semantic layer holds claims; episodic layer expires at 400 days | The compounding asset is the distilled claim, not the raw body. Retention differs accordingly. |
| Confidence thresholds | `source_confidence`, `semantic_record.confidence`; low-confidence facts excluded (`PRD.md` A3) | A quality control that is also a minimization control: uncertain inferences about people are not retained as facts. |

Two minimizations Phase 1 **does not** do, named honestly:

- **No field-level pruning of email payloads.** `episodic_record.payload` stores the validated message essentially whole, including headers and quoted history. Quoted history in particular means a single thread reply can carry months of prior correspondence, including participants who are otherwise nowhere in the system. Pruning quoted history at the normalizer is a real minimization win and is not currently specified. Open question §10.1.
- **No pseudonymization of participants.** `episodic_record.participants` holds plain email addresses, indexed with GIN for querying. Pseudonymizing would break the deep-link and dedupe paths and is probably the wrong trade at this scale, but it is a trade being made rather than a constraint.

## 6. Retention and deletion

### 6.1 The retention table

Reproduced from `DATA_MODEL.md` §12, which is authoritative for the schema, with the privacy rationale that the schema document deliberately deferred here. Where a row's stated handling has an implementation problem, it is flagged and resolved in §6.3.

| Table | Retention | Deletion on data-subject request | Privacy rationale |
|---|---|---|---|
| `episodic_record` | 400 days rolling | Hard delete by participant identifier | Raw bodies are the largest exposure and the least compounding value. 400 days covers a full annual cycle plus a quarter of comparison, which is the longest period the briefing plausibly reasons over. |
| `semantic_record` | Indefinite | **Redact** `statement` and `attributes`; preserve structure and links | Indefinite retention of distilled claims is the product thesis (`MEMORY_ARCHITECTURE.md`). Redaction rather than deletion preserves the supersession chain, whose integrity other records depend on. |
| `semantic_link`, `semantic_edge` | Indefinite | Preserved | Pure structure, no content. Deleting them would orphan records and violate the no-orphans rule. |
| `audit_record` | 7 years | **Never deleted.** Redact personal data within `inputs` / `outputs` | Accountability under a separate lawful basis (§4). See §6.2. |
| `agent_proposal` | **Not specified in `DATA_MODEL.md` §12 — gap.** Proposed: 7 years, matching `audit_record` | Redact `payload` and `rationale`; retain `impact_class`, `trust_level`, `disposition`, `refusal_reason` | `agent_proposal` holds proposed content and model reasoning, which is personal data, and it is `briefing_item`'s foreign-key parent. It is part of the accountability record and must follow `audit_record`, not `briefing`. Its omission from the retention table is a real defect. |
| `prompt_version` | Indefinite | Not applicable | Should contain no personal data. If a prompt body ever embeds an example drawn from real correspondence, this row becomes wrong, so: prompts must not contain real personal data, stated as a rule. |
| `briefing`, `briefing_item`, `briefing_item_evidence` | 2 years | Hard delete | The briefing is a derived, re-generable view. Deleting it loses nothing that `agent_proposal` and the audit trail do not retain. |
| `error_flag` | Indefinite | Anonymize `flagged_by` | Learning signal for Phase 3. Retains value once detached from who flagged it. See §6.3 for the constraint problem. |
| **Logs, metrics, traces** | **Not specified anywhere — gap.** Proposed: 30 days for application logs, 90 days for metrics and traces | Not individually addressable | `OBSERVABILITY.md` requires a clear deletion policy for anything containing PII, and T8 in `THREAT_MODEL.md` establishes that despite the redaction rule some personal data will reach logs. Short retention is the control that bounds a leak we cannot fully prevent. |
| **Embeddings** (`semantic_record.embedding`) | Follows `semantic_record` | **Must be nulled whenever `statement` is redacted** | Embeddings are substantially invertible (§2). Redacting a statement while retaining its vector is redaction theatre. Stated explicitly because it is easy to miss. |

### 6.2 Data subject rights

| Right | Phase 1 mechanism | Honest status |
|---|---|---|
| **Access / portability** | A `dataSubjectExport(orgId, identifier)` operation returning every `episodic_record` where the identifier appears in `participants` or the payload, every `semantic_record` linked to those, and every `briefing_item` evidenced by them, as structured JSON | Buildable directly on existing indexes: the GIN index on `participants` and the `semantic_link` join. Manual-trigger operator tooling in Phase 1, not a self-service surface. Adequate at one tenant, inadequate at Phase 4 volume. |
| **Rectification** | Supersession. A corrected fact supersedes the incorrect one with a forward link (`MEMORY_ARCHITECTURE.md`) | Genuinely good. The architecture makes correction natural and non-destructive, and preserves the record that the system once believed otherwise, which is itself a fair thing for a subject to be able to see. |
| **Erasure** | §6.3 | The hard one. |
| **Objection / restriction** | Add the identifier to a suppression list checked at the normalizer, so future content involving that person is not ingested | **Not specified in `DATA_MODEL.md`. A real gap.** A suppression list is the only mechanism that makes objection meaningful, since deletion without it means re-ingestion tomorrow. Open question §10.3. |
| **Automated decision-making** | Not applicable in Phase 1 | Phase 1 makes no decisions about anyone. It recommends to one human. Worth recording as the baseline, because Phase 3's autonomous actions may cross into territory where this right engages. |

### 6.3 Erasure while audit records survive

The tension `DATA_MODEL.md` §12 names and defers here: audit records must survive for accountability, and data subjects have deletion rights. Both are real; neither yields entirely.

**The resolution is redaction within audit records rather than removal of them.** An audit record has two separable components: the *fact of an action and its authorization*, and the *personal content the action concerned*. Accountability requires only the first. Erasure concerns only the second. So the second is destroyed and the first is preserved.

Concretely, after an erasure request affecting a given data subject:

**What is destroyed**

- `episodic_record` rows where the subject is the sole or a named participant: hard deleted, payload and all.
- `semantic_record.statement` and `.attributes`: overwritten with a redaction tombstone recording that redaction occurred, when, and under what request identifier. Never a plain `NULL`, because the distinction between "never had a value" and "was redacted" is itself audit-relevant.
- `semantic_record.embedding`: set to `NULL`.
- Personal content inside `audit_record.inputs` and `.outputs`: replaced field-wise with redaction markers.
- `agent_proposal.payload` and `.rationale`: same treatment.
- `briefing_item.headline` and `.detail`: hard deleted along with the parent briefing rows.

**What remains provable, and this is the point of the design**

- That an action occurred, at a precise time.
- Which agent produced it, under which `prompt_version_id`, at which `trust_level` as applied at that moment (`DATA_MODEL.md` §9 is explicit that trust level is stored on the proposal rather than joined, so history is not rewritten by later configuration).
- What `impact_class` was declared and what `disposition` the gate reached, including `refusal_reason` for refusals.
- The `approval_chain`, empty throughout Phase 1 and load-bearing from Phase 2.
- The full graph of `semantic_link` and `semantic_edge` relationships, so supersession chains stay intact and no record is orphaned.
- That a redaction occurred, when, and under which request.

The claim being preserved is therefore: *"On this date, this agent, running this prompt version at this trust level, proposed something of this impact class, and the gate disposed of it thus."* That is the complete accountability claim `OBSERVABILITY.md` and `SECURITY_STANDARDS.md` require. It survives erasure entirely, because none of it is personal data about the subject.

**Three implementation problems, stated because they are the kind that get discovered during a live erasure request rather than during design.**

1. **`audit_record` has `UPDATE` revoked (`DATA_MODEL.md` §9) and redaction requires `UPDATE`.** This is a direct contradiction between §9 and §12 of the data model and it must be resolved before the first migration, not at first request. Three options: (a) a `SECURITY DEFINER` function owned by a privileged role, the sole permitted mutation path, which itself writes an audit record of the redaction — recommended, because it keeps append-only as the default and makes each exception self-documenting; (b) store personal content in a separate `audit_payload` table that permits deletion, leaving `audit_record` immutable and content-free — architecturally cleaner and a schema change; (c) accept that redaction runs as the service role outside the privilege model, which is how this usually happens and is the wrong answer, because it means the append-only property was never real.
2. **`episodic_record` hard deletion collides with `semantic_link`'s foreign key and with the no-orphans rule.** `DATA_MODEL.md` §12 says hard delete; §7 requires every `semantic_record` to retain at least one `semantic_link` to an `episodic_record`, enforced by a commit-time trigger. Deleting the last episodic source of a semantic record therefore either fails on the constraint or orphans the record, and both `ARCHITECTURE.md` §6 and `DATA_MODEL.md` §1 forbid the second. Resolution: erasure replaces the episodic row with a **tombstone** retaining `id`, `org_id`, `source_connection_id`, `kind`, `occurred_at`, and a redaction marker, with `payload`, `participants`, and `content_hash` cleared. Links stay valid, no orphan is created, and no content survives. This changes "hard delete" to "hard delete of content" and `DATA_MODEL.md` §12 should be amended to say so.
3. **`error_flag.flagged_by` is a non-null foreign key to `app_user`, so it cannot be anonymized by nulling.** Either the column becomes nullable, or anonymization repoints it to a permanent tombstone user row. The tombstone is better: it keeps the constraint meaningful and makes the anonymization visible in the data rather than inferable from an absence.

**What erasure cannot reach.** Content already transmitted to Anthropic, Google, Slack, or the transactional email provider is outside our deletion. We rely on their retention commitments (§9). Content already in log or trace storage is bounded by log retention, not by request, which is the second reason §6.1 proposes short log retention. Both limits should be disclosed in any erasure response rather than implied to be complete.

## 7. Redaction obligations for logs, metrics, and traces

`API_CONTRACTS.md` §9 states the rule and points here for the specifics.

**The rule.** No logger call, metric tag, or span attribute may carry message bodies, transcript text, subject lines, calendar event titles or descriptions, semantic record statements, prompt bodies, or any credential. Observability data carries record *identifiers* and *counts*. If an investigation needs content, it queries the database through the repository layer, where access is subject to RLS and produces its own trail.

**Why identifiers rather than content is the right line.** It is enforceable. "Log only what is necessary" is a judgment call made at 11pm by a developer chasing a bug; "log UUIDs and integers, never strings from a payload" is a rule that can be checked mechanically and that a reviewer can apply without thinking about the content.

**Specific prohibitions worth naming because they are the ones that actually happen:**

- Metric tags must never carry an email address or a participant identifier. High-cardinality tags are a cost problem and a permanent-retention personal-data problem at the same time.
- Error objects must not be logged whole. `logger.error('ingest_failed', { err })` where the error wraps the offending payload is the single most common leak path and it is invisible in review, which is why T8's residual risk is medium rather than low.
- Quarantined events (`QuarantinedEvent.rawPayload`, `API_CONTRACTS.md` §3) contain the full unvalidated payload by design, and quarantine is exactly when someone wants to look at it. Quarantine storage is therefore in the database under the same retention as `episodic_record`, never in a log stream.
- Model requests and responses must not be logged verbatim. The prompt contains retrieved context by construction, so logging the prompt logs the corpus.

**Enforcement.** A lint rule for the named field names, plus a test asserting that known-sensitive field names never appear in emitted output (`API_CONTRACTS.md` §9). Both are partial, as T8 records. Short retention is the control that bounds what they miss.

## 8. Column-level encryption of `payload` — the open question from `DATA_MODEL.md` §13

`DATA_MODEL.md` §13 item 4 defers this decision here. Answering it rather than restating it:

**The question.** `episodic_record.payload` and `call_transcript` content currently rely on Supabase's at-rest encryption, which is full-disk encryption with a key the platform manages. Column-level encryption with an application-held key would additionally protect the content from anyone holding database access but not the application key.

**What it would actually defend against.** Precisely one class of adversary: someone who obtains database access without obtaining application secrets. That is a narrow set — a leaked read-replica connection string, a stolen backup, an insider at the hosting provider, a subpoena served on Supabase rather than on us. It is not empty, and the backup and subpoena cases are the realistic members.

**What it does not defend against.** T4 (source credential compromise, which needs no database at all), T5 (service-role compromise, which in practice arrives with application secrets), T7 (supply chain, which takes the key), and T8 (log leakage, which bypasses the column entirely). In other words it does not defend against any of the highest-severity threats in `THREAT_MODEL.md`.

**What it costs.** Search over payload becomes impossible in SQL, which today matters less than it appears because retrieval runs through pgvector over `semantic_record.embedding` rather than over payload text. The real costs are elsewhere: key management becomes a system we own, including rotation and re-encryption; a lost key is unrecoverable data loss; and the retention sweep and the erasure tooling both become more complex, which per §6.3 is already the fragile part.

**Decision for Phase 1: do not implement column-level encryption of `payload`. Instead:**

1. Rely on at-rest encryption plus TLS in transit for `payload`.
2. **Encrypt backups under a key we hold**, separately from the platform's. This captures most of the realistic benefit — the stolen-backup case — at a fraction of the cost, and it is the concrete substitute rather than a promise to revisit.
3. Keep credentials out of the database entirely, which `DATA_MODEL.md` §5 already does by storing only `secret_ref`. The most valuable thing an attacker could find in `payload` is a credential a correspondent emailed, and the second most valuable is nothing we can encrypt our way out of.
4. Revisit at Phase 4, where the calculus genuinely changes: multi-tenant hosting of other organizations' data makes per-tenant key separation a customer requirement rather than a defence-in-depth nicety, and a subpoena served on the platform concerns data we do not own.

Recorded as a decision with a stated basis, so that Phase 4 revisits a conclusion rather than reopening a question.

## 9. Third-party processors

Every processor is a place our data exists that we do not control, and each one widens the surface in §2 of `THREAT_MODEL.md`. Enumerated so the list is a fact rather than a memory.

| Processor | What flows to it | Direction | Notes |
|---|---|---|---|
| **Anthropic** (Claude API, via the Agent SDK) | Prompts containing retrieved semantic records and episodic content: email text, transcript excerpts, Slack messages, calendar detail. Model outputs return. | Outbound content, inbound proposals | **See §9.1.** The most consequential entry. |
| **Supabase** | Everything. The entire database: all payloads, all semantic records, all embeddings, all audit records. | At rest | Named as a platform dependency in `ADR-0002`. Practically our data custodian. Sub-processor relationships (its own cloud host) inherit. |
| **Google** (Gmail, Calendar APIs) | Nothing new outbound beyond OAuth requests. Inbound: the founder's mail and calendar. | Inbound | Google already holds this data. LEAP OS is a reader, so the marginal privacy delta is zero at Google and entirely on our side. |
| **Slack** | Nothing new outbound. Inbound: opted-in channel content. | Inbound | Same posture as Google. |
| **Voice transcript provider** (undetermined, `ADR-0006`) | Nothing outbound from us. Inbound: verbatim customer speech. | Inbound | **The provider is a processor of customer speech before we ever see it**, and the consent question in §3.2 is largely theirs. This is why PR-1 makes provider selection a privacy decision. |
| **Transactional email provider** (undetermined, `PRD.md` §10 item 4) | The rendered briefing: a synthesized digest of the most sensitive material in the system, in plain text and HTML, in an external system's logs and delivery records. | Outbound | Under-weighted in most designs. The briefing is more concentrated than any single source. Selection criteria must include log retention, whether bodies are stored, region, and a data processing agreement. Not merely deliverability. |
| **Log / metrics backend** (if external) | Whatever survives §7's redaction rule. | Outbound | If observability is hosted externally it is a processor and belongs in this table with a retention commitment. If it is self-hosted in the same Postgres, it inherits Supabase's row. Undecided; belongs in `OBSERVABILITY.md`. |

### 9.1 Sending customer call transcripts to a model API is a processor relationship requiring disclosure

Stating this plainly because the temptation to treat model API calls as somehow not data transfers is strong and it is wrong.

When the Chief of Staff agent reasons over yesterday's calls, the verbatim words of a customer who called the company are transmitted over the network to Anthropic and processed on Anthropic's infrastructure. That is a disclosure of third-party personal data to a third-party processor. It is not different in kind from uploading the transcript to a SaaS vendor. It is the same act, and it is a *sub-processing* relationship if the company processes that data on behalf of anyone else.

What follows concretely:

1. **Disclosure.** The company's privacy notice must state that correspondence and call content is processed by third-party AI providers. Naming Anthropic specifically is stronger than a generic reference and is what a data subject exercising an access right is entitled to learn.
2. **Contractual footing.** Commercial API terms with zero-retention or bounded-retention handling and no training on inputs, plus a data processing agreement. `AI_AGENT_STANDARDS.md` and this document both prohibit training on customer content; that prohibition must be contractual with the provider, not merely a rule we follow ourselves, because it is their systems that would do the training.
3. **Region and transfer.** For EU or UK data subjects, cross-border transfer mechanics apply. Region selection where the provider offers it, transfer safeguards where it does not.
4. **Minimization at the prompt boundary.** This is the engineering obligation and the one most within our control. `AgentInput.context` carries `RetrievedRecord[]`, not whole payloads. Retrieval limits, `minConfidence`, and kind filters (`API_CONTRACTS.md` §4) are privacy controls as much as cost controls: every record not retrieved is a record not transmitted. Sending the top ten relevant semantic statements rather than fifty raw email bodies is both a better prompt and a smaller disclosure, which is a rare case where the privacy-optimal choice is also the quality-optimal one and should be exploited rather than merely noted.
5. **Do not let the episodic layer become the prompt.** The single largest privacy regression available to this codebase is a change from "retrieve distilled facts" to "stuff recent raw messages into context because recall improved." It would be defensible on quality grounds, it would pass every test, and it would multiply what leaves our infrastructure by an order of magnitude. **A change to what the agent receives as context is a privacy change and requires review under this document.**

## 10. Open questions

1. **Quoted-history pruning at the normalizer (§5).** A single reply can carry months of prior correspondence and participants who appear nowhere else. Pruning is a real minimization win, is bounded engineering work, and slightly risks losing context the briefing uses. Unowned.
2. **Special-category data is present and unclassified.** Email bodies contain health, financial, and employment information that nothing in Phase 1 identifies as such, so nothing handles it differently. Detection is genuinely hard and probably not Phase 1 work. Recorded so it is a known gap rather than an oversight.
3. **Suppression list for objection (§6.2).** Without one, erasure is undone by the next ingestion run. This is the most important missing piece of data-subject-rights machinery and it is not in `DATA_MODEL.md`.
4. **`DATA_MODEL.md` amendments this document requires.** Four, and each is a real defect rather than a stylistic preference: `agent_proposal` missing from the retention table; the `audit_record` `REVOKE UPDATE` versus redaction contradiction (§6.3 item 1); episodic "hard delete" versus `semantic_link`'s foreign key and the no-orphans trigger (§6.3 item 2); `error_flag.flagged_by` non-null versus anonymization (§6.3 item 3). All should be resolved before the first migration.
5. **Log and trace retention is unspecified anywhere.** §6.1 proposes 30 and 90 days. Needs a decision and a home, probably `OBSERVABILITY.md`.
6. **Erasure tooling is unbuilt and untested.** Phase 1 has a design for erasure and no code. The first real request will therefore be handled by hand-written SQL under time pressure against the two constraint conflicts in §6.3, which is exactly the wrong conditions. A minimal tested erasure path is worth more than it looks, because it also proves the retention design is coherent.
7. **Whose privacy notice, and does it exist?** §3.3 and §9.1 both depend on the company having a published privacy notice that covers AI-assisted analysis of correspondence and calls. Whether one exists is a founder question, and if it does not, that is a smaller task than any engineering item in this document and a larger exposure than most.
