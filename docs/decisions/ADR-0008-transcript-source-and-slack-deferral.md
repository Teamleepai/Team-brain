# ADR-0008 — Zoom as the transcript source; Slack deferred to Phase 2

**Date:** 2026-08-03

## Status

Accepted. Supersedes `ADR-0006` in part: the transcript provider open question is answered, and increment 1c is removed from Phase 1. The rest of `ADR-0006` — three source families delivered sequentially with source-tagged records — stands.

## Context

`ADR-0006` left two things unresolved: which voice transcript provider feeds increment 1b, and it assumed a Slack workspace existed to validate increment 1c against. Founder input resolved both, and the second answer was not the one the original plan assumed.

**On transcripts:** the founder records meetings in Zoom and uses Otter. Both are candidates, and the stated ideal was a provider that pushes transcripts automatically rather than requiring a poll.

**On Slack:** the founder is moving to Slack *over time* and is not on it today. That invalidates increment 1c as scoped, because `DEFINITION_OF_DONE.md` §2 requires live-credential validation at every increment gate and there is no workspace to validate against.

## Decision — part 1: Zoom is the transcript source

**Zoom Cloud Recording, ingested via the `recording.transcript_completed` webhook, authenticated with a Server-to-Server OAuth app.**

The mechanism: Zoom fires `recording.transcript_completed` when a cloud recording's transcript is ready. The event payload carries a download URL and a download token for the VTT file, which the adapter fetches and hands to the normalizer as a `call_transcript` episodic record.

This is a genuine departure from the polling model in `ARCHITECTURE.md` §4, and it matters architecturally. Every other Phase 1 source is pull-based on a 15-minute cycle against a watermark. Zoom is push-based. The `SourceAdapter` interface in `API_CONTRACTS.md` §2 assumes `fetchSince(cursor)`, so it needs a webhook-shaped sibling — see Consequences.

Requirements the founder must confirm: cloud recording enabled, audio transcript enabled, on a plan that includes cloud recording. Recording already happens in Zoom, so this is likely already satisfied.

### Why Zoom over Otter

**Otter's public API is gated to Enterprise workspaces.** Key creation lives under Integrations → Developer, and access is an Enterprise entitlement. If the founder is on Pro, this is a hard blocker rather than a preference, and that alone would decide it.

Three reasons Zoom wins even if Otter were available:

1. **Zoom is the system of record.** Otter is a layer over the same meetings. Ingesting from Zoom removes a dependency rather than adding one, and removes a second party from the data path — which `PRIVACY_MODEL.md` §9 has to enumerate as a processor either way.
2. **Otter's differentiated value is the layer we are replacing.** Otter's summaries, action items, and insights are exactly what the distillation pipeline and the Chief of Staff agent produce. Paying Otter to summarize so that we can re-summarize its summary is redundant at best, and at worst it launders provenance: a commitment extracted from Otter's summary of a meeting has weaker evidence than one extracted from the transcript, and `MEMORY_ARCHITECTURE.md` requires we be able to point at the source.
3. **Server-to-Server OAuth suits an unattended backend.** No user-consent flow to maintain or re-authorize, which matters for something that must run every morning without intervention. This also reduces the R6 exposure in `RISK_REGISTER.md` (a source silently stopping on token expiry), since a machine credential has fewer ways to lapse than a delegated user token.

### Alternatives considered

**Otter as primary.** Rejected on the Enterprise gate and the redundancy argument above. Worth noting the honest counter-argument: Otter's transcription quality and speaker attribution are generally better than Zoom's native output, and speaker misattribution is exactly the failure mode `PRD.md` A3 and `FAILURE_MODES.md` treat as high-severity, because it produces confidently wrong commitments attributed to the wrong person. If Zoom's diarization proves inadequate in increment 1b's quality gate, Otter becomes the fallback and this ADR should be superseded rather than worked around.

**Both, with Zoom as primary and Otter enriching it.** Rejected as premature. Two transcript sources for the same meeting means deduplicating the *same* call across providers, which is a harder instance of the `dedupe_key` problem already flagged as R7 — the highest-risk unresolved detail in the schema. Not the place to add difficulty.

**A meeting-bot provider** (Recall.ai or similar) that joins calls and transcribes independently. Rejected for Phase 1: it adds a vendor, a processor relationship, and a bot visibly joining meetings, in exchange for platform independence we do not yet need. Revisit if the founder moves off Zoom or needs to cover Meet and Teams calls too.

## Decision — part 2: Slack moves to Phase 2

**Increment 1c is removed from Phase 1.** Phase 1 is now Google Workspace (1a) plus Zoom transcripts (1b).

The founder is not on Slack yet. Building the adapter now would mean shipping it against fixtures with no live workspace to validate against, which fails the live-credential exit gate by construction and would book exactly the debt R5 already warns about — except knowingly, which `PRODUCT_PHILOSOPHY.md` §2 forbids.

This is a scope *reduction* and therefore worth being explicit that it is the founder's call to reverse. The recommendation stands on two grounds. A two-source Phase 1 reaches a working briefing sooner, and `ADR-0006` already identified 1c as the correct thing to cut if Phase 1 ran long. And the messaging adapter is better built once the founder is actually on the platform, because channel structure and volume — which drive the thread-boundary and noise problems — cannot be designed against a workspace that does not exist.

**Open question:** what is the founder on for messaging *today*? If Teams, that adapter is substantially the same work as Slack and could take 1c's place in Phase 1 with a live workspace to validate against. If nothing, then email is already carrying that traffic and 1a covers it.

## Consequences

**The `SourceAdapter` interface needs a push-shaped variant.** `API_CONTRACTS.md` §2 assumes `fetchSince(connection, cursor, limit)`. Zoom delivers events by webhook. The clean resolution is a second interface — `WebhookSourceAdapter`, with `verifySignature(request)` and `toRawEvents(payload)` — feeding the same normalizer, so the trust boundary, provenance stamping, and idempotent upsert are unchanged. Both interfaces produce `RawEvent[]`; only acquisition differs.

Two properties must not be lost in the switch. The normalizer's idempotency still holds, because a replayed webhook carries the same `source_id` and hits the same unique constraint. But **watermarks no longer protect against missed data** for this source: if a webhook delivery fails and Zoom exhausts its retries, there is no cursor that will notice the gap. That is a new failure mode not present in the pull-based sources, and it needs a reconciliation sweep — a periodic `GET /users/me/recordings` over the last N days to catch anything the webhook never delivered. Without it, increment 1b acquires a silent-incompleteness failure mode of exactly the kind R6 exists to prevent.

**Webhook endpoint security.** Zoom webhooks require signature verification. This is now the second unauthenticated inbound endpoint in the system after the error-flag endpoint (`ADR-0007`), and unlike that one it accepts a payload. `THREAT_MODEL.md` needs a row for it: unverified webhook payloads would let anyone inject arbitrary transcript content into episodic memory, which is a direct path to the prompt-injection surface T11 already covers, with the added twist that the attacker controls the whole record rather than a message body inside one.

**Privacy scope narrows slightly and sharpens.** Dropping Slack removes a processor. Zoom transcripts do not reduce the R9 exposure at all: recordings of customers and counterparties who never consented to LEAP OS remain the sharpest privacy issue in the project, and `PRIVACY_MODEL.md` §3 still gates increment 1b on settling the consent position.

## Migration path

If Zoom's diarization quality fails increment 1b's gate, Otter becomes primary and this ADR is superseded. Because both would implement the same adapter interface and produce `call_transcript` episodic records, the change is one adapter plus a credential, not a redesign.

If the founder later moves off Zoom or needs Meet and Teams coverage, a meeting-bot provider becomes the platform-independent answer, and the `WebhookSourceAdapter` interface built here is the attachment point.

## Technical debt

1. **The reconciliation sweep is not optional.** A webhook-only ingestion path has no way to detect what it never received. Shipping 1b without the sweep means shipping a source that can be silently incomplete, and silent incompleteness is the failure mode `FAILURE_MODES.md` grades most dangerous because the briefing still looks healthy.
2. **Zoom's native diarization is unvalidated.** Speaker misattribution produces commitments assigned to the wrong person, which is a confidently-wrong-recommendation failure (R3). Increment 1b's quality gate must specifically check attribution accuracy, not just that transcripts arrive.
