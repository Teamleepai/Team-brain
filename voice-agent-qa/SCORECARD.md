# Voice Agent Scorecard — $2,000/mo Retention Standard

Scoring rubric for Mia (Ace Detailing) and any other client-facing Retell agent.
Calibrated to one question: **would a client paying $2,000/month renew?**

At $2k/mo the client is not buying "an AI that answers the phone." They are
buying booked jobs they would otherwise have lost, at a cost below a
part-time receptionist (~$2,200/mo loaded for 20hrs/wk). That framing sets
every threshold below. An agent that answers politely and books nothing is
worth $0 to them, not $2,000.

## Hard-fail gates (any one hit = ceiling of 45/100, regardless of everything else)

These are the things that get a contract cancelled on a single incident. They
are gates, not point deductions, because a client does not average them.

| Gate | Threshold | Why it's a gate |
|---|---|---|
| **Price hallucination** | >0 calls inventing a price, package, or discount not in the prompt | Creates a quote the shop must honor or refuse an angry customer. Direct revenue and reputation loss. |
| **Booking black hole** | Any call where caller says yes and no appointment is captured | The one job the agent exists to do. |
| **Wrong hours / wrong location** | >0 calls stating incorrect operating info | Sends customers to a closed shop. |
| **Dead air >5s mid-call** | >2% of calls | Callers hang up; reads as broken, not slow. |
| **Infra error rate** | >5% of calls ending `error_*` | Platform fault, not prompt — but the client experiences it as your product failing. Fix before touching prompts. |

## Weighted score (100 pts) — only scored if no gate is hit

| # | Dimension | Wt | What earns full marks | Source |
|---|---|---:|---|---|
| 1 | **Booking conversion** | 30 | ≥60% of qualified callers with intent leave with a booked slot | transcripts |
| 2 | **Task completion / containment** | 15 | ≥85% resolved without human transfer, and every genuine edge case *does* transfer cleanly | transcripts + `disconnection_reason` |
| 3 | **Data capture completeness** | 12 | ≥95% of bookings carry name + callback number + vehicle + service + time | transcripts / `custom_analysis_data` |
| 4 | **Conversational latency** | 12 | e2e p50 <1000ms; p95 <2000ms | `latency.e2e` |
| 5 | **Objection & edge handling** | 12 | Handles "how much", "can you do today", "do you come to me", pricing pushback without looping or deflecting | transcripts |
| 6 | **Barge-in / interruption** | 8 | Yields immediately when interrupted; no talk-over, no restart-from-top | recordings |
| 7 | **Brand voice & naturalness** | 6 | Sounds like Ace's front desk; no robotic re-greeting, no "as an AI" | recordings |
| 8 | **Sentiment / caller effort** | 5 | ≤10% negative sentiment, no repeat-yourself loops | `user_sentiment` + transcripts |

### Grade bands

| Score | Verdict at $2,000/mo |
|---|---|
| 90–100 | Best-in-class. Renews, expands, gives you the case study. |
| 80–89 | Healthy. Renews. This is the floor you should be shipping at. |
| 70–79 | **At risk.** Renews once, churns in 60–90 days unless fixed. Client is already comparing you. |
| 55–69 | **Churning.** They have started pricing replacements. |
| <55 | Refund conversation. |

**A 75 is not a pass.** At this price point 75 means the client is tolerating
the agent, and tolerance does not survive one bad month.

## Benchmark: what top-tier implementation teams hold themselves to

This is the comparison set — the shops charging $3k–$10k/mo per deployment,
where the agent is the product and churn is existential.

| Metric | Top-tier target | Acceptable | Churn zone |
|---|---|---|---|
| e2e latency p50 | <800ms | <1200ms | >1500ms |
| e2e latency p95 | <1500ms | <2500ms | >3000ms |
| Booking conversion (intent-qualified) | 65–75% | 50–65% | <45% |
| Containment (no transfer needed) | >90% | 80–90% | <75% |
| Hallucination rate | 0% | 0% | any recurrence |
| Infra `error_*` rate | <1% | <3% | >5% |
| Calls dying <15s | <8% | <15% | >20% |
| Post-call human review | 100% of calls, week 1–2; then 20% sampled weekly forever | 10% sampled | none |
| Prompt iteration cadence | weekly, driven by tagged failure transcripts | biweekly | "set and forget" |

**The single biggest differentiator is not the prompt — it is the review
loop.** Top teams tag every failed call into a category, fix the top category
that week, and re-measure. Teams that churn ship a good prompt on day one and
never look at a transcript again. That gap shows up in month 3, not month 1.

Two caveats, stated honestly: the latency and error-rate figures reflect broad
industry consensus for real-time voice and are well-established. The booking
conversion and containment targets are directional benchmarks from how these
deployments are typically sold and evaluated — they vary by vertical and by
lead quality, so treat them as the bar to argue against with your own data,
not as published constants.

## Scoring procedure

1. Run `pull_retell_calls.py` → gives dimensions 2, 4, 8 and all gate data
   except hallucination, deterministically from Retell's fields.
2. Read all 40 transcripts in `out/transcripts.md`. For each, tag:
   `booked` / `intent-no-book` / `no-intent` / `voicemail` / `infra-fail`,
   plus any gate hit. Booking conversion = `booked ÷ (booked + intent-no-book)`.
   Excluding no-intent and voicemail from the denominator is what makes the
   number honest — do not inflate it by counting wrong numbers as successes.
3. Spot-listen ≥10 recordings for dimensions 6 and 7. These cannot be scored
   from text; a transcript hides talk-over completely.
4. Score, apply gates, then write the churn verdict in one sentence.

## Failure-tag taxonomy for the weekly loop

Tag every non-booking. This is the artifact that drives training.

- `no-ask` — agent never asked for the booking
- `price-dodge` — deflected a price question instead of answering or bridging
- `loop` — asked for the same field twice
- `slot-blind` — no live calendar availability, offered "someone will call back"
- `hours-wrong` / `service-wrong` — factual error
- `barge-fail` — talked over the caller
- `greeting-drop` — caller hung up in first 15s
- `handoff-fail` — should have transferred, didn't (or transferred badly)
- `capture-partial` — booked without a callback number

Top-tier practice: whichever tag is most frequent this week is the *only*
prompt change you make this week. One variable at a time, or you cannot
attribute the improvement.
