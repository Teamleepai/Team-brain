# Go-to-Market — Week by Week, Two Divisions in Parallel

**Date:** 2026-08-07 · Today is **Friday 7 August**
**Signature deadline:** Monday **30 November** · billing live **1 December** · collect in December
**Supersedes:** the capacity assumptions in `03` §1.4 and the barbell counts in `05` §6.2

---

## 1. The finding that inverts the plan

Every previous document assumed **two callers at 40 dials/day = 1,600 dials/month**, and treated dial
capacity as the binding constraint. Doc `03`'s council (Salesloft) said the missing lever was a dedicated
dialer.

**You already have two.** With the real roster:

| Person | Dials/day | Dials/mo | Set rate* | Meetings/mo | Role |
|---|---|---|---|---|---|
| **Grace** | 90 | 1,800 | 9% | **32.4** | Dedicated setter |
| **Javid** | 45 | 900 | 8% | **14.4** | Setter, partial — has other work |
| **Aaron** | 20 | 400 | 20% | **16.0** | Closer + Division B dials |
| **Alec** | 20 | 400 | 20% | **16.0** | Closer + Division B dials |
| **Total** | **175** | **3,500** | | **78.8** | |

\* *Set rate = connect → meeting booked. These are my estimates from your descriptions, not measured.
Gong's benchmark across 300M+ calls is **4.6% average, 16.7% top quartile**. Grace and Javid are placed
just above average as specialists; you and Alec above top quartile per your own read. **Week 3 replaces
all four numbers with measured ones.*** Connect rate 20% throughout — that's a data-quality function of
the mobile-direct-dial filter, not a skill function.

### The result

| | |
|---|---|
| Meetings/month capacity | **~79** |
| Qualified opportunities/month (at 60%) | **~47** |
| Closes/month at 35% (your stated close rate) | **~16.5** |
| Closes/month at 22% (benchmark average) | **~10.4** |
| **Customers needed** | **14** |

**At benchmark close rates you'd produce ~36 customers over the selling window. You need 14.**

**Grace alone, at 90 dials/day, covers 1.5× the entire requirement.**

### What this means, plainly

**Lead flow is no longer the constraint. Delivery capacity and closer calendar are.** That reverses the
central assumption of docs `03`–`05`, and it changes the right move:

> **Surplus dial capacity is permission to raise price.**
>
> When you can afford to lose more deals, you can quote higher. The same delivery load produces more
> revenue. You are not short of conversations — you are short of hours to implement what you sell.

So: **do not run at max capacity.** Run at roughly a third, aim it at higher-value prospects, and spend
the surplus on research depth per account and on delivery throughput.

---

## 2. The revised target — fewer customers, higher ticket

| | Old barbell (doc `05`) | **Recommended** |
|---|---|---|
| Group tier | 5 × $4,500 = $22,500 | **6 × $5,000 = $30,000** |
| Fast tier | 12 × $2,000 = $24,000 | **8 × $2,100 = $16,800** |
| **Customers** | 17 | **14** |
| **Blended ACV** | $2,735 | **$3,343** |
| Total new MRR | $46,500 | **$46,800** |
| December collected | $50,000 | **$50,300** |
| Meeting capacity used | 37% | **31%** |

**14 instead of 17 is 18% less delivery load for the same revenue.** That is the entire win from the
capacity surplus, and delivery is the thing most likely to break.

$5,000 for the Group tier sits exactly at the **mid-market agency floor** ($5,000–15,000, doc `04` §2.1)
while delivering more scope than an agency does. It is still the value option.

**Cadence: 1 close per week for 14 weeks.** That's the whole plan in one line.

---

## 3. Two divisions, running in parallel

```
  DIVISION A — SMALL MARKET                DIVISION B — MULTI-LOCATION
  ─────────────────────────                ───────────────────────────
  Independent auto repair                  Med spa groups, 3–8 locations
  1–3 locations · 4+ bays · 3+ techs       Owner or single exec decides
  $2,100/mo · Fast tier                    $5,000/mo · Group tier
  14–45 day cycle                          30–90 day cycle
  LEAD: Voice AI receptionist              LEAD: SMS reactivation
  ─────────────────────────                ───────────────────────────
  DIAL: Grace (primary) + Javid            DIAL: Aaron + Alec (peer voice)
  CLOSE: Aaron / Alec                      CLOSE: Aaron / Alec
  TARGET: 8 customers                      TARGET: 6 customers
  ~2,700 dials/mo                          ~800 dials/mo
```

**Why the split works this way:** a 6-location med spa owner screens a setter and takes a peer. A
single-location auto shop owner will talk to anyone who opens with something true about his phone. So the
senior voice goes where it changes the outcome, and volume goes where volume works.

**Division B is also the deadline risk.** 30–90 day cycles mean a Group deal started after ~1 October
may not sign by 30 November. Front-load it.

### Role assignments

| Person | Owns | Does not own |
|---|---|---|
| **Grace** | Division A dialing, ~90/day. Books meetings, does not close | Never runs a sales call |
| **Javid** | Division A overflow + Division B research and pre-qualification. 30–75/day as his other work allows | Never runs a sales call |
| **Aaron** | Division B dials (20/day). All Division B sales calls. Price decisions | Should not be doing Division A dialing |
| **Alec** | Division B dials (20/day). All Division A sales calls. Objection library | Should not be doing Division A dialing |
| **Jameson** | Data, scoring, dossiers, call sheets, the SMS/email cadence build | Never contacts a prospect |

**The one rule that protects the plan: Aaron and Alec's hours go to closing, not dialing.** Every hour
of theirs spent on Division A dials is an hour Grace could have covered at a third the cost.

---

## 4. Weeks 1–2 — the data sprint

**No dialing this fortnight.** Two weeks to build the lists you'll live on for fourteen.

> **One unblock worth knowing now: cold *calling* does not need Gate 1.** Human-dialed B2B calls are
> legal without prior consent. **Only the SMS and email legs need the consent gate.** So dialing starts
> Week 3 regardless of where the attorney review sits — the legal review gates *channels*, not the whole
> plan. That was ambiguous in earlier docs and it matters for the timeline.

### Week 1 · Mon 10 – Fri 14 August

| Day | Owner | Deliverable |
|---|---|---|
| Mon | **Aaron** | **Buy the domain** (confirm `itsleepai` vs `itsleapai` first) and start warmup. It needs 4–8 weeks and it's already the critical path |
| Mon | **Jameson** | Gate 1 compliance one-pager started. Sandbox confirmed |
| Mon–Tue | **Jameson** | **Division A universe scrape** — auto repair, target geos. Google Maps via Outscraper/Apify |
| Tue–Wed | **Jameson** | **Division B universe scrape** — med spa, then cluster into 3–8 location groups per `08` §1.1 and filter against PE brands |
| Wed | **Jameson** | Phone line-type lookups across both lists. **Drop anything that isn't a mobile** — this is the mandatory filter, it doubles connect rate |
| Wed–Thu | **Jameson** | Review mining: complaint keywords, review velocity vs rating trend. Job-posting pull via Coresignal |
| Thu | **Jameson** | Boulevard/Zenoti booking-widget detection on Division B. Bay-count estimation on Division A |
| Fri | **Jameson** | Merge, score multiplicatively (Pain × Pay × Reach), rank. **Report the measured false-positive rate per signal** |
| Fri | **Aaron/Alec** | Review the top 50 of each list. Kill what looks wrong. This is the calibration the scorer never had |

**Week 1 exit:** two scored lists, mobile-verified, with a measured false-positive rate. Domain warming.

### Week 2 · Mon 17 – Fri 21 August

| Day | Owner | Deliverable |
|---|---|---|
| Mon | **Jameson** | Manual verification of the top 200 Division A and top 100 Division B. Build call sheets — one page per prospect: the signal, the evidence, the opener |
| Mon | **Alec** | **Write both openers.** Division A leads on the missed-call arithmetic; Division B leads on the dormant patient database |
| Tue | **Aaron/Alec** | Train Grace and Javid on the signal-based opener. **The script is not a pitch — it's reading one true thing back to them and asking a question** |
| Tue | **Aaron** | Gate 1 attorney session booked. Confirm Group tier price at $5,000 |
| Wed | **Grace + Javid** | **Pilot: 50 dials each.** Purpose is not booking — it's finding out which openers land and which signals are wrong |
| Thu | **All** | Pilot debrief. Rewrite the opener. **Record every call from here on** |
| Thu | **Jameson** | Fix the signals the pilot proved wrong. Re-score |
| Fri | **Grace + Javid** | Second pilot: 75 dials each with the revised opener |
| Fri | **Aaron** | Assign the referral list to a name and send the first five. $8,000/mo at zero CAC is still unassigned |

**Week 2 exit:** openers tested against ~250 real dials, revised. Grace and Javid trained. Referral
outreach started. **First meetings likely booked in the pilots — take them.**

---

## 5. Weeks 3–16 — execution

### Weeks 3–4 · 24 Aug – 4 Sep · RAMP

- **Grace** to full volume, 90/day, Division A
- **Javid** starts at 30/day, builds toward 45–75 as his other work allows
- **Aaron + Alec** begin Division B dials, 20/day each. **Front-load Division B — its cycle is the long one**
- **Measure the four rates.** Replace every estimate in §1 with a real number and re-run the model
- Expect **2–4 meetings/week** in week 3, **6–8/week** by week 4
- **First closes land here** on Division A's short cycle

**Gate:** by end of week 4 you have measured connect, set, meeting→opp and close rates. If the set rate
comes in near Gong's 4.6% average rather than 8–9%, **you still clear the target** — that's the point of
the surplus. But you'll know, rather than assume.

### Weeks 5–8 · 7 Sep – 2 Oct · FULL VOLUME

- All four dialing. ~175/day, ~875/week
- **Target: 1 close/week.** 4 by end of week 8
- **SMS + email cadence goes live** once Gate 1 clears and the domain is warm
- **Price calibration starts.** Doc `03` §2.4 thermometer: above 40% close at $5,000 → raise; below 20% → read the loss reason before touching price
- **Weekly scorecard, every Friday** (§6)

**Hard gate at 1 October:** build freezes. No new signals, no new products, no new tooling. Every
engineering hour after this is stolen from the close window.

### Weeks 9–12 · 5 Oct – 30 Oct · PEAK

- **This is where the number is made.** 8 cumulative closes by end of week 12
- **Last Division B start date is ~1 October** — a 90-day Group cycle from here just makes 30 November.
  After this, new Division B prospects are Q1 pipeline, not Q4 revenue
- Division A keeps producing: 14–45 day cycles mean a deal started in week 12 still signs
- Aaron/Alec dialing drops as their calendar fills with sales calls. **That's correct — let it happen**

### Weeks 13–16 · 2 Nov – 27 Nov · CLOSE

- **Pure execution. No prospecting changes**
- Division A only for new starts — it's the only cycle short enough
- **Week 15–16: every deal signs by Monday 30 November.** Configure billing for 1 December as each closes
- **Contract structure: month-to-month counts the same as annual for December collection, and closes
  faster.** Optimise for signature date, not term length
- **Delivery is now the constraint.** 14 implementations landing across Q4 against a ceiling nobody has
  measured

---

## 6. The weekly scorecard — every Friday, 15 minutes

| Metric | Target | Read |
|---|---|---|
| Dials — Grace / Javid / Aaron / Alec | 450 / 225 / 100 / 100 | Per-person, not team total. Hides nothing |
| Connect rate | 20% | Below 15% = the mobile filter is leaking |
| Set rate, per caller | Grace 9% · Javid 8% · A/A 20% | **The number the whole plan rests on** |
| Meetings booked | 6/week | Above 10 and you're over-filling the closers |
| Qualified opps | 3.3/week | |
| **Closes** | **1/week** | The only number that matters |
| Close rate | 30–40% | **Above 40% = underpriced, raise it** |
| Loss reasons, categorised | — | Price objection vs no-decision are opposite fixes |
| Division B starts | Front-loaded | Zero new starts after ~1 Oct |
| Delivery hours consumed | — | **The real ceiling. Track from close #1** |

**One rule: if closes lag but meetings hit target, the problem is the closers' calendar or the
qualification bar — not the dialers.** Don't add dials to fix a closing problem.

---

## 7. What breaks this

Ranked by probability × damage, revised for the real roster.

| # | Risk | Why it's different now | Mitigation |
|---|---|---|---|
| **1** | **Delivery capacity, not lead flow** | 14 implementations in Q4 against an unmeasured ceiling. **This is now the #1 risk, promoted from #4** | Measure hours on implementation #1. Charge setup fees to fund capacity |
| **2** | **Aaron and Alec's calendar saturates** | 47 opps/month capacity vs the hours to run them. Their dialing competes with their closing | Cap their dials at 20/day and let it fall as the calendar fills |
| **3** | Division B cycles overrun 30 November | 30–90 days means ~1 Oct is the last viable start | Front-load Division B in weeks 3–8 |
| **4** | Javid's capacity is unreliable | "Has a lot of work" — 30–75/day is a wide band | Plan on 30. Treat 75 as upside, never as the base case |
| **5** | Set rates come in at benchmark, not above | Grace/Javid at 4.6% instead of 8–9% | **Already survivable** — that's what the surplus buys. Measure in week 4 |
| **6** | Building past 1 October | Steals the close window | Hard freeze. Treat it as a real date |
| **7** | Gate 1 slips | Blocks SMS and email — **not dialing** | Dial from week 3 regardless. Channels unlock as they clear |
| **8** | Domain warmup started late | 4–8 weeks, needed by ~1 Sept | **Buy it Monday** |

---

## 8. What I'd challenge in this plan

1. **The four set rates are my estimates from your qualitative descriptions, not measurements.** They are
   the load-bearing assumption in §1, and the entire "you have 3× the capacity you need" conclusion rests
   on them. **Week 4 replaces them.** If Grace comes in at 4% rather than 9%, the surplus halves — still
   enough, but the headroom I'm describing is smaller than it looks.
2. **"Close rate very high above industry average" is your own assessment.** Benchmark at $40–60K ACV is
   20–28%. I modelled 35%. If it's actually 25%, you need 47 opps/month rather than 40 — still inside
   capacity, but the margin narrows. **The model has no downside case unless you build one.**
3. **Raising the Group tier to $5,000 is a recommendation, not a validated price.** It's the mid-market
   agency floor, and you deliver more scope — but you haven't sold at that number yet. **The first three
   Group deals are the test, and close rate is the instrument.**
4. **Two divisions with one closing pair is real context-switching cost.** Division A opens on missed-call
   arithmetic; Division B on a dormant database. Different products, buyers, objections. **Consider
   Alec owning Division A calls and Aaron owning Division B** rather than both doing both — it halves
   the mental switching and lets each build a deeper objection library.
5. **Nobody has priced Jameson's two-week sprint against the $50-per-qualified-prospect criterion.** Raw
   data is under $200. His hours are not, and the free NPPES source left with dental. **Track it from
   week 1.**
6. **Grace covering 1.5× the requirement alone is a fragility, not just a comfort.** If she leaves or is
   out for two weeks, Division A halves. **Javid's ramp is the insurance policy** — treat his development
   as a deliverable, not a nice-to-have.

---

## 9. The whole thing on one page

```
  WEEK  1─2      3─4        5─8         9─12        13─16
        DATA     RAMP       FULL VOL    PEAK        CLOSE
        ────     ────       ────────    ────        ─────
  Aug 10        Aug 24     Sep 7       Oct 5       Nov 2      Nov 30
        │        │          │           │           │            │
  no dialing    measure    1 close/wk  the number  signatures   BILLING
  build lists   the rates  build FREEZE  is made   only         LIVE Dec 1
                           ↑ Oct 1                 Div A only
                                        ↑ last Div B start ~Oct 1

  DIVISION A  auto repair · $2,100 · 8 customers · Grace + Javid dial
  DIVISION B  med spa 3-8 loc · $5,000 · 6 customers · Aaron + Alec dial
              14 customers × $3,343 blended = $46,800 + $3,500 = $50,300 collected
              Capacity used: 31% of meetings. Constraint: delivery, not dials.
```

---

**Unverified in this document:** all four set rates (estimates from description); the 35% close rate
(your assessment, above the 20–28% benchmark band for this ACV); the $5,000 Group price (recommended, not
tested); Javid's sustainable daily volume; and delivery hours per implementation — which is now the
number most likely to break the plan.
