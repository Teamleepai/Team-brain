# Deployment Plan — Reverse-Engineered from $50K MRR

**Date:** 2026-08-06
**Horizon:** 4 months to 31 December 2026, with a 3-year arc behind it
**Depends on:** `00-readback`, `01-pain-signal-matrix-and-icp`, `02-aisdr-brief-jameson`

**On skills:** you asked me to use every skill you've downloaded. I checked — this environment has only
the standard set (`docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`, `morning`, `session-start-hook`). No
custom GitHub skills are installed. I'm not going to pretend otherwise. I used `xlsx` to build you a
funnel model you can actually manipulate, since every number below is an assumption you should be able
to change.

---

## 0. The one thing I need from you before this plan is real

**I don't know your current MRR.** It's not in the repo and it changes everything — the gap could be
$50K or $15K. Every scenario below models the *incremental* requirement. Tell me the starting number and
I'll collapse this to one path.

**One clarification that makes the goal much more achievable than it sounds.** "$50K MRR by end of year"
is an **exit run-rate**, not cumulative collected revenue. A contract signed 28 December counts fully
toward 31 December MRR. That means the target is *signatures by year end*, not *cash collected during
the year* — a materially easier problem. I'll assume run-rate throughout. If you meant collected
revenue, the plan changes fundamentally and you need to tell me.

---

## 1. The math, worked backwards

### 1.1 Customers required, by average contract value

| Blended ACV/mo | Customers for $50K MRR | New closes per month (4 mo) |
|---|---|---|
| $1,000 | **50** | 12.5 |
| $1,500 | 34 | 8.5 |
| $2,000 | 25 | 6.3 |
| **$2,500** | **20** | **5.0** |
| $4,000 | 13 | 3.2 |
| $5,000 | 10 | 2.5 |

### 1.2 The most important conclusion in this document

**Price is a bigger lever than activity, by a wide margin.**

Moving blended ACV from $1,000 to $2,500 drops required customers from 50 to 20 — **a 60% reduction in
required funnel volume.** Achieving that same reduction through activity would mean tripling dial
capacity, which you cannot do while also delivering.

**So: optimize price first, activity second.** Every hour spent on packaging and price architecture is
worth roughly three spent on prospecting volume. This is the single highest-leverage decision in the
four months.

### 1.3 The full funnel, backwards, with benchmarks

Modeling $2,500 blended ACV → 20 customers → 5 closes/month.

| Stage | Conversion | Source of the benchmark | Monthly volume needed |
|---|---|---|---|
| Closed customers | — | — | **5** |
| Qualified opportunities | **30%** close | $10–50K ACV band benchmarks 20–28%; 30% is top-quartile [[optif.ai](https://optif.ai/learn/questions/b2b-saas-win-rate-by-deal-size/), [zenitdata.com](https://zenitdata.com/blog/b2b-saas-win-rate-benchmarks-by-deal-size-stage-and-segment-2026/)] | **17** |
| Meetings booked | **60%** become real opps | Assumption — signal-qualified should beat generic | **28** |
| Live connects | **15%** set rate | Gong 300M+ calls: avg **4.6%**, top quartile **16.7%** [[prospeo.io](https://prospeo.io/s/cold-calling-conversion-rate)] | **187** |
| Dials | **20%** connect | Generic data 8–12%; **verified mobile direct-dial 18–22%** [[skipcall.io](https://skipcall.io/en/blog/cold-call-connect-rate-benchmarks)] | **935** |

**≈ 935 dials/month ≈ 47 dials/day ≈ 24/day each for two callers.** That is comfortably achievable.

### 1.4 But that model assumes top-quartile performance twice over

Honest version. At Gong's **average** 4.6% set rate instead of 15%:

| | Optimistic (15% set) | Benchmark average (4.6% set) |
|---|---|---|
| Dials/month | 935 | **3,050** |
| Dials/day | 47 | **153** |
| Per caller (2 callers) | 24 | **76** |

**76 dials/day/person is a full-time dialing job.** Aaron and Alec cannot be the researchers, the
dialers, the closers and the delivery team simultaneously. That is the real bottleneck in this plan, and
it resolves three ways:

1. **Earn the top-quartile set rate.** Defensible — a call opening with a verified, specific, refuted-and-survived pain signal is categorically different from a generic pitch. This is the entire thesis of the signal matrix. But it is a hypothesis until Phase 3 measures it.
2. **Raise ACV** so fewer customers are needed. See §1.2.
3. **Add a dedicated dialer.** Cheapest incremental capacity, and it protects the closers' time for closing.

**My recommendation: all three, weighted toward #2.** Do not bet the quarter on hitting top-quartile
conversion — bet it on needing fewer customers.

### 1.5 The deadline is not 31 December. It's roughly 1 October

Sales cycle benchmarks: SMB under $15K ACV closes in **14–30 days**; mid-market $15K–$100K in **30–90
days** [[optif.ai](https://optif.ai/learn/questions/sales-cycle-length-benchmark/)]. At $2,500/mo you're
at $30K ACV — squarely mid-market, so **30–90 days.**

Working back from 31 December: pipeline must be *created* between 1 October (90-day deals) and 1 December
(30-day deals). **The outbound engine has to be running at full volume by early October.**

That leaves **roughly eight weeks to build.** That, not year end, is the date the plan is engineered
against.

---

## 2. Price architecture — grounded in market data

### 2.1 What the market actually pays

| Offer | Market price | Source |
|---|---|---|
| AI receptionist, agency-resold, per location | **$295–$595/mo** | [trillet.ai](https://www.trillet.ai/blogs/ai-receptionist-white-label-pricing) |
| Multi-location practices / high-value verticals | **$750+/mo** | [trillet.ai](https://www.trillet.ai/blogs/ai-receptionist-white-label-pricing) |
| Standard SMB AI receptionist | $197–$597/mo | [ringlyn.com](https://www.ringlyn.com/blog/white-label-voice-ai-marketing-agencies/) |
| **Managed outbound, high-ticket verticals** | **$797–$1,497/mo** | [ringlyn.com](https://www.ringlyn.com/blog/white-label-voice-ai-marketing-agencies/) |
| Self-serve SMB tools (the floor) | $25–$95/mo | doc `01` §4 |

Platform costs to you: Trillet $299/mo agency + $0.12/min; Synthflow $0.08+/min with a $2,000/mo
white-label add-on; **Thinkrr $499/mo and GoHighLevel-focused** — worth a look given your stack.
Realistic gross margins **50–80%**, netting **65–80%** at steady state.
[[trillet.ai](https://trillet.ai/blogs/top-10-white-label-ai-receptionist-for-agencies-2026), [ringlyn.com](https://www.ringlyn.com/blog/white-label-ai-voice-agent-reseller-program-2026/)]

### 2.2 The hard finding on your $1,000/mo target

**$1,000/mo is not a single-product price.** The market pays $295–$595 for a standalone AI receptionist.
$1,000+ is only reachable three ways:

1. **Multi-location** — $750+ is documented for multi-location practices
2. **Bundling** — receptionist + reactivation + chat + hygiene on one account
3. **Managed/high-ticket positioning** — $797–$1,497 for managed outbound

**All three point at the same ICP: the 3–8 location med spa group from doc `01`.** The price target and
the ICP recommendation independently converge, which is the strongest signal in this analysis that the
spearhead choice is right.

### 2.3 The package ladder

Built so that the bundle, not the product, carries the price.

| Tier | Composition | Target /mo | Fits |
|---|---|---|---|
| **Entry** | One product, single location | $500–750 | Referral/inbound only. Do not prospect for this |
| **Core** | Reactivation + voice AI, single or 2 locations | $1,200–1,800 | High-revenue single-location med spa |
| **Group** | Reactivation + voice + chat + hygiene retainer, 3–8 locations | **$2,500–4,000** | **The spearhead** |
| **Value-event** | Group tier + diligence-grade data cleanup, owner grooming for exit | $4,000–6,000 + setup | doc `01` §5 — the EBITDA frame |

Setup/implementation fees are separate and do not count toward MRR. Charge them anyway — they fund the
delivery capacity that the recurring revenue depends on.

### 2.4 Close rate as a price thermometer — your instinct, quantified

You said you don't want too high a close rate because it means you're underpriced. **The benchmark data
proves you right, and it lets us calibrate precisely.**

Win rates fall as deal size rises: sub-$10K ACV closes at **28–35%** (and 30–45% on qualified pipeline
with short cycles), $10–50K at **20–28%**, $50–100K at 15–22%
[[zenitdata.com](https://zenitdata.com/blog/b2b-saas-win-rate-benchmarks-by-deal-size-stage-and-segment-2026/), [optif.ai](https://optif.ai/learn/questions/b2b-saas-win-rate-by-deal-size/)].

So at $30K ACV, the instrument reads:

| Observed close rate | Diagnosis | Action |
|---|---|---|
| **> 40%** | Far above the $10–50K benchmark. You are underpriced | **Raise price 25–40% on the next 10 deals** |
| **30–40%** | Top quartile for the band. Healthy, price is near optimal | Hold. Optimize elsewhere |
| **20–30%** | At benchmark | Hold price, improve qualification |
| **< 20%** | Diagnose the loss reason before touching price | See below |

**Below 20%, read the loss reason, not the rate.** Deals dying on *price objection* means price is
ahead of the value you've proven. Deals dying on *no decision* means targeting is wrong — the pain
wasn't urgent. Those are opposite fixes and conflating them is how companies discount their way into a
worse business.

**Note what this means for your stated 30–50% target: the top of your range is the warning line, not the
goal.** Sustained 50% at $30K ACV is evidence you left money on the table. Aim at 30–35%.

---

## 3. Data source map — signal by signal

This is the operational core. The answer to "Apollo or Indeed?" is usually **neither**.

### 3.1 The finding that dictates the architecture

**Apollo and ZoomInfo do not cover your market.** ZoomInfo has approximately **20% coverage of local
service providers**, and Apollo has *less*. Coverage of micro-niches — appliance repair, pool cleaning,
junk removal — is inconsistent. In a March 2026 test of 1,000 leads, ZoomInfo returned mobile numbers
for **67%** of records vs Apollo's **41%**; direct dial **71%** vs **52%**. ZoomInfo claims 95%+
accuracy vs Apollo's 80–85%. Apollo's 275M+ contacts cover more home services purely by scale, at
$49/mo. [[zoominfo.com](https://www.zoominfo.com/compare/apollo-vs-zoominfo), [cleanlist.ai](https://www.cleanlist.ai/blog/2026-03-07-apollo-vs-zoominfo), [origami.chat](https://origami.chat/blog/best-zoominfo-alternatives-home-service)]

**This retroactively explains Aaron's Apollo med spa result.** ~500 records nationwide wasn't market
size — it was coverage. There are 10,000+ med spa locations
[[americanmedspa.org](https://www.americanmedspa.org/news/med-spa-ma-and-private-sales-a-look-back-at-2025-and-what-lies-ahead/)]. Apollo saw 5% of them.

**Therefore: Google Maps is the universe, not Apollo.** Maps has near-complete coverage of local
businesses. Contact databases are an *enrichment* layer over it, never the discovery layer. Building
top-of-funnel on Apollo would silently discard ~80% of your addressable market.

### 3.2 The stack

```
  LAYER 1 · UNIVERSE          Google Maps scrape — the only near-complete local business source
       ↓
  LAYER 2 · SIGNALS           One specialized source per pain signal, merged on entity
       ↓
  LAYER 3 · SOLVENCY          Ability-to-pay proxies, deliberately non-Google
       ↓
  LAYER 4 · CONTACT           Apollo for what it has; manual research for the ~80% it doesn't
       ↓
  LAYER 5 · VERIFY            Manual confirmation on the shortlist only. Sniper, not scrape
```

### 3.3 Source per signal

| Signal | Best source | Cost | Confidence | Notes |
|---|---|---|---|---|
| **Business universe, by industry + geo** | Google Maps via **Outscraper** ($3/1K records, 500 free) or **Apify** ($1.50/1K base) | Low | **High** | Outscraper is the simpler pay-as-you-go with enrichment; Apify wins on custom extraction. Under 2K leads Outscraper is cheapest; at 10K+ costs climb fast [[gmapsscraper.io](https://gmapsscraper.io/blog/outscraper-vs-apify-google-maps-scraper), [outscraper.com](https://outscraper.com/best-google-maps-scrapers/)] |
| **Receptionist job open 30+ days** | **Coresignal** — 399M+ postings from LinkedIn, Indeed, Glassdoor, Wellfound; 65+ fields; API from **$49/mo** | Low | **High** | **Not Apollo, and not scraping Indeed directly.** Coresignal is licensed and aggregates Indeed. JobsPikr ($79–480/mo) is the alternative [[coresignal.com](https://coresignal.com/blog/best-job-posting-data-providers-comparison-and-use-cases/), [brightdata.com](https://brightdata.com/blog/web-data/best-job-posting-data-providers)] |
| **Review complaints re: missed calls** | Google Maps review scrape (same Layer 1 pass) | Low | **High** | Free rider on the universe scrape. Highest ROI signal in the stack |
| **Review velocity vs. rating trend** | Google Maps review timestamps | Low | **High** | Same pass. Computed, not scraped |
| **Google Business Profile thin/unclaimed** | Google Maps / Places | Low | **High** | Same pass |
| **Main line rings to a mobile** | Phone line-type lookup API (Twilio Lookup or equivalent) | Low | **High** | **Highest-value signal — see §3.5** |
| **Yelp response time > 1 hr** | ⚠️ **See §3.4. Not reliably scrapable** | — | **Low** | Hard finding. Read that section |
| **Website tech / no chat widget / DIY builder** | Direct HTTP fetch + DOM parse, self-built | Very low | **High** | Build it yourself. No vendor needed |
| **Incumbent software (Boulevard, Zenoti, Jobber)** | Tech-detection via booking widget and script tags | Low | **Medium** | **Open research item.** I did not verify a specific vendor's coverage of these booking platforms — do not assume BuiltWith or Wappalyzer covers them. Jameson validates before committing |
| **SEO rank #4–10** | Rank-tracking API by geo + keyword | Medium | **Medium** | Cost scales with keyword × location count. Budget carefully |
| **Paid ads running** | Meta Ad Library (free) + a paid-search tool | Low–Med | **High** | Meta Ad Library is free and a strong solvency proxy |
| **Permits, licenses, fleet/DOT** | State and county public records | Low, high labor | **Medium** | The non-Google solvency layer. Labor-intensive, so reserve for shortlist |
| **PE / M&A activity, grooming for exit** | PE roll-up trackers, banker listings, news | Medium | **Medium** | Strongest signal in the matrix per doc `01`. Partly manual |
| **Owner name, contact** | **Apollo** ($49/mo) then manual | Low | **Low–Medium** | ~20% coverage. Plan for manual on the rest |

### 3.4 Hard finding: the Yelp response-time signal may not be buildable

Alec named "Yelp response time over an hour" as a stated trigger. **I could not confirm it's obtainable
at scale, and the evidence points the wrong way:**

- The official **Fusion API doesn't expose it**, and carries hard limits (3 reviews per business, strict terms) [[scrapfly.io](https://scrapfly.io/blog/posts/guide-to-yelp-api)]
- **Scraping Yelp is explicitly prohibited** by their terms and technically difficult [[scrapfly.io](https://scrapfly.io/blog/posts/how-to-scrape-yelpcom)]
- Third-party Yelp scrapers surface business details, reviews and **owner responses** — but I found no confirmation of the response-time metric specifically [[apify.com](https://apify.com/thirdwatch/yelp-business-scraper)]
- Two Fusion-API-based Apify actors are marked **DEPRECATED** [[apify.com](https://apify.com/renzomacar/yelp-fusion-search)]

**What this means practically:** the metric is visible to a human on a Yelp page but is not a legally
clean, reliable, at-scale top-of-funnel filter. **Do not build the Yelp agent's prospecting on it.**

**Workable substitutes, same product:**
- **Unanswered reviews** — owner-response presence *is* obtainable via scrapers, and "hasn't responded
  to the last N reviews" is a defensible proxy for slow response
- **"Request a Quote" enabled** — visible on the profile
- Verify response time **manually on the shortlist only.** At 20–50 prospects/day that's minutes of work,
  and it fits sniper doctrine exactly

This is a real reduction in scope versus what was assumed on the call. Flagging it now is cheaper than
Jameson discovering it in week three.

### 3.5 The signal that pays for the whole plan

**"Main line rings to a mobile number"** is worth calling out separately because it's worth money twice:

1. It's the **reachability** signal — owner-operator, single-threaded, decides alone
2. It **doubles-to-quadruples your connect rate.** Generic data connects at 8–12%; **verified mobile
   direct-dial connects at 18–22%** [[skipcall.io](https://skipcall.io/en/blog/cold-call-connect-rate-benchmarks)]

Every other prospecting shop dials generic business lines at 8–12%. Selecting for mobile-reachable
owners is a **structural 2x advantage on the single most expensive step in the funnel**, and it's cheap
to detect with a line-type lookup.

**Make this a mandatory filter, not a bonus.** If the main line isn't a mobile, deprioritize — no
matter how many other boxes are checked.

### 3.6 An architectural warning worth heeding

**Proxycurl shut down permanently on 4 July 2025 after LinkedIn's federal lawsuit**
[[coldiq.com](https://coldiq.com/blog/best-linkedin-jobs-apis)].

If your pipeline depends on a scraper that gets litigated out of existence, your pipeline dies overnight.
**For anything load-bearing, use licensed providers.** Bright Data, for instance, carries GDPR/CCPA
compliance and ISO 27001, which shifts legal risk to the vendor
[[brightdata.com](https://brightdata.com/blog/web-data/best-job-posting-data-providers)]. Pay the premium
on the sources you can't afford to lose; use cheap scrapers only where a substitute exists.

---

## 4. The phases

Reverse-engineered from 31 December, with the real build deadline at 1 October.

```
  NOW ──── Aug ──────── Sep ──────── Oct ──────── Nov ──────── Dec 31
   │        │            │            │            │             │
   P0       P1  P2       P3           P4           P5            $50K
  decide  found build   pilot &     full volume   close only    exit MRR
          -ations       calibrate   BUILD FROZEN
```

### Phase 0 — Decide and unblock · **this week**

Nothing else starts cleanly until these land.

| Item | Owner | Blocks |
|---|---|---|
| State current MRR | Aaron | The entire model (§0) |
| Confirm run-rate vs. collected revenue interpretation | Aaron/Alec | Whether this plan is right at all |
| Josh Astone + JJ Jardina accounts into the repo | Alec | Scorer calibration — currently calibrated against nothing |
| Aaron's SEO research, Armand + Aisha, blueprint/kit | Both | Signal definitions, differentiation claims |
| Confirm domain spelling, buy it, start warmup **now** | Aaron | Warmup takes weeks. Every day of delay is a day off the calendar |
| Start recording every cold call | Both | Training data is unrecoverable once a call happens (doc `02` A.5) |
| Sandbox + Jameson access | Aaron | Doc `02` A.8 |

**Exit criteria:** current MRR known, both reference accounts in the repo, domain purchased and warming.

> **Warmup is the hidden critical path.** A cold domain can't carry real volume immediately. Buy it in
> Phase 0 or you will be waiting on it in October.

### Phase 1 — Foundations · **weeks 1–2 of August**

Build nothing yet. Remove the things that can invalidate the build.

| Workstream | Deliverable | Exit criteria |
|---|---|---|
| **Compliance** | Jameson's Gate 1 one-pager; consent mechanic chosen; attorney opinion on the PEWC language | Signed off. Nothing sends before this |
| **Price architecture** | The §2.3 ladder priced, with margin math against real platform costs | Four tiers with defended prices and floors |
| **Data source contracts** | Outscraper/Apify trialled; Coresignal at $49/mo live; tech-detection vendor **verified, not assumed** | Cost-per-1,000-qualified-prospects known |
| **Target list v1** | Layer 1 universe scrape: 3–8 location med spa, plus HVAC/plumbing as the second front | 2,000–5,000 raw entities, deduped |
| **Baseline** | Current close rate, cycle length, ACV from whatever history exists | A real baseline, or an explicit admission there isn't one |

**Kill criterion:** if cost-per-qualified-prospect exceeds ~$50, the unit economics don't support
sniper at $2,500 ACV and the plan needs rework before proceeding.

### Phase 2 — Build the engine · **weeks 3–4 of August into early September**

| Workstream | Deliverable |
|---|---|
| Signal scrapers | The `High` confidence signals from §3.3 only. Do not build `Medium` or `Low` yet |
| Merge + score | Entity resolution, then **multiplicative** Pain × Pay × Reach (doc `01` §2) |
| Refutation pass | The adversarial check from doc `02`. Non-optional |
| Dossier + call sheet | The durable artifact. Design first — it's the product, messages are a by-product |
| Consent gate | Stage 5 from doc `02`, enforced in code |
| Config-as-code | YAML/markdown in git; GitHub web editor as the day-one command center |
| Cadence in GHL | Official MCP server; sandbox sub-account only |

**Exit criteria:** 50 scored dossiers, of which 20 hand-verified, with a **measured** false-positive rate
per signal. Not estimated. Measured.

### Phase 3 — Pilot and calibrate · **September**

The most important phase, and the one most likely to be skipped under time pressure. **Don't.**

Run at deliberately low volume — roughly 100–150 dials/week — and measure the four numbers the whole
model rests on:

| Metric | Model assumption | What you're testing |
|---|---|---|
| Dial → connect | 20% | Does the mobile-direct-dial advantage hold? (§3.5) |
| Connect → meeting | 15% | **The riskiest assumption in the plan.** Gong average is 4.6% |
| Meeting → qualified opp | 60% | Is the scoring model actually predictive? |
| Opp → close | 30% | And read it as a price thermometer (§2.4) |

**Exit criteria:** real numbers for all four, and the model in `50k-mrr-funnel-model.xlsx` re-run with
them.

**If the measured set rate lands near 4.6% rather than 15%,** you have three moves and must pick one
before Phase 4: raise ACV, add a dedicated dialer, or extend the timeline. **Do not simply try harder —
the arithmetic won't bend.**

### Phase 4 — Full volume · **October, into November**

**BUILD FREEZES ON 1 OCTOBER.** No new signals, no new products, no new tooling. Every engineering hour
after this date is stolen from the close window.

| | |
|---|---|
| Volume | Whatever Phase 3 proved is required. From the model, 900–3,000 dials/month |
| Cadence | Research → human call → written consent → autonomous SMS/email → book |
| Weekly review | The four funnel metrics, close rate as thermometer, loss reasons categorized |
| Price adjustment | Per §2.4, on rolling batches of 10 deals. Actively use the instrument |
| Only permitted "build" | Copy iteration and claim-registry additions from real objections |

**Exit criteria:** pipeline sufficient that arithmetic — not hope — produces $50K exit MRR.

### Phase 5 — Close · **November–December**

Pure execution. Aaron and Alec do nothing but close and deliver.

- No prospecting engine changes
- Delivery capacity is the constraint now: every close consumes implementation hours. **The delivery
  ceiling from doc `01` §3 becomes the binding limit, not lead flow**
- Contract structure matters for the goal: **month-to-month counts toward exit MRR the same as annual,
  and closes faster.** Optimize for signature date, not term length, in Q4 specifically

**Exit criteria:** $50K exit MRR at 31 December.

---

## 5. The three-year arc

You asked me to think years out. The four-month sprint is not the business — it's the data-collection
phase of the business.

### Year 1 (now → Dec 2026) — prove the motion

$50K exit MRR. Services revenue. The output that matters isn't the revenue — it's **a labeled dataset
connecting pain signals to outcomes.** Every dial, connect, meeting and close labels a signal as
predictive or noise.

### Year 2 (2027) — the dataset becomes the moat

**The durable asset is not the agency revenue. It's knowing which signals actually predict a close.**

Nobody else in this niche is building that. Competitors buy the same Apollo lists and guess. By mid-2027
you'd be able to say "an owner-operated 4-location med spa on Boulevard with unanswered reviews and a
receptionist posting open 40 days closes at 38%" — and that is proprietary, compounding, and impossible
to shortcut.

Three ways to monetize it:
1. **Vertical concentration** — dominate med spa, then port the playbook one vertical at a time
2. **Sell the scored list** — other agencies would pay for signal-scored prospects. Doc `00` already
   noted the med spa owner-email list as saleable on its own
3. **Price on prediction** — when you know close probability before dialing, you can quote confidently
   and skip the discount reflex

### Year 3 (2028) — the fork

Two paths, both requiring Y1–Y2 data:

- **Channel / implementation partner** (doc `00` §8). The blueprint plus a proven delivery record makes
  you a credible enterprise implementation partner for the voice AI platforms. Different buyer, far
  bigger deals. Every load-bearing fact there is still unverified — validate with one conversation
  before investing.
- **Productize the signal engine.** The Y2 dataset becomes a product rather than an internal tool.

**Decision point, not now.** Y3 optionality is *created* by executing Y1 with instrumentation. Skip the
instrumentation and both forks close.

---

## 6. The council

You asked for a council grounded in Salesloft, Outreach, Gong and Salesforce. Each challenges a specific
number with a specific number.

### 🎯 Gong — "your set rate assumption is the whole plan, and it's 3x the average"

*From 300M+ analyzed cold calls: average connect 5.4%, top quartile 13.3%. Average set rate 4.6%, top
quartile 16.7%.* [[prospeo.io](https://prospeo.io/s/cold-calling-conversion-rate)]

> You modeled 15% — essentially top quartile — on a team that has never run this motion at volume. Top
> quartile is where teams land after months of iteration on recorded calls, not where they start. If
> your real set rate is 6%, your dial requirement is 2.5x and the plan breaks in October, not in
> December, when it's too late to fix.
>
> **Verdict: the Phase 3 pilot is not optional. Measure before you commit. And record every call from
> day one — top quartile comes from call review, and you cannot review what you didn't capture.**

### 📈 Outreach — "you're planning cadence volume you're not allowed to send"

> A standard sequence is 8–12 touches across channels. You have a domain-protection rule, a hard PEWC
> gate, and no volume email. So your cadence depth is legally capped in a way most outbound playbooks
> aren't. Have you actually counted how many compliant touches you get per prospect? If it's four, your
> effective conversion is lower than any benchmark you're citing — because those benchmarks assume
> unconstrained sequences.
>
> **Verdict: count your permitted touches per prospect before trusting any conversion assumption. And
> note the upside — the human cold call as touch one is worth more than the six emails you're not
> sending.**

### ⚡ Salesloft — "two people cannot own four functions"

> Research, dial, close, deliver. Mature orgs separate SDR from AE precisely because the skills and the
> time profiles conflict. You're proposing that two closers whose value is $200K–$1.9M complex deals
> spend their days doing 76 dials. That's the most expensive dialing in the industry.
>
> **Verdict: a dedicated dialer is the cheapest lever in this entire plan and it's missing from the
> phases. Add it in Phase 1, not Phase 4 when you're behind.**

### ☁️ Salesforce — "your win rate target is above benchmark for your deal size"

*Average B2B win rate ~21%; SMB 31%; $10–50K ACV 20–28%.* [[landbase.com](https://www.landbase.com/blog/win-rate-benchmarks-industry-deal-size-2026), [salesmotion.io](https://salesmotion.io/blog/sales-win-rate-benchmarks-2026)]

> You want 30–50% at $30K ACV. The benchmark band is 20–28%. So your *floor* is above the market
> *average* and your ceiling is roughly double it. That's not impossible for elite closers on
> signal-qualified pipeline — but the model has no downside case. What's the plan at 22%?
>
> **Verdict: model the benchmark case, not just the optimistic one. Then note the corollary you already
> intuited — if you do hit 50%, that's a pricing finding, not a victory.**

### 🔍 The Data Skeptic — "one of your named signals may not exist"

> Yelp response time was a stated trigger on the call. §3.4 says it isn't reliably obtainable. How many
> other signals in the matrix are like that? You have `Medium` and `Low` confidence entries that have
> never been tested against a real source.
>
> **Verdict: Phase 1 must validate source availability for every signal before Phase 2 builds anything.
> Build only what you've confirmed you can feed.**

### 💰 The CFO — "the plan has no cost line"

> Outscraper, Coresignal, rank tracking, Apollo, voice platform per-minute fees, a dialer's salary, an
> attorney's opinion letter. Plus delivery cost per new customer. **Nowhere in this plan is $50K MRR
> converted into $X of gross margin.** Reseller margins run 50–80% gross — so $50K MRR is $25–40K of
> gross profit before your own time and before the tool stack.
>
> **Verdict: add a cost model in Phase 1. A revenue target without a margin target is how agencies grow
> into insolvency.**

---

## 7. What actually kills this

Ranked by probability × damage.

| # | Risk | Mitigation | Phase |
|---|---|---|---|
| 1 | **Set rate lands at benchmark, not top quartile** → 2.5x dial requirement | Pilot before committing; raise ACV; add a dialer | 3 |
| 2 | **Aaron and Alec become the bottleneck** doing all four functions | Dedicated dialer in Phase 1 | 1 |
| 3 | **Building past 1 October** eats the close window | Hard build freeze. Treat as a real date | 4 |
| 4 | **Delivery capacity binds before lead flow does** | Doc `01` §3 ceiling; charge setup fees to fund capacity | 5 |
| 5 | **Signals turn out not to be scrapable** (Yelp is the known case) | Validate every source in Phase 1 | 1 |
| 6 | **Compliance stops the SMS leg** after the cadence is built around it | Gate 1 first, before any build | 1 |
| 7 | **Domain warmup not started early enough** | Buy and warm in Phase 0 | 0 |
| 8 | **~80% contact-coverage gap** forces manual research at unsustainable cost | Google Maps as universe; budget manual time explicitly | 1 |
| 9 | **Underpricing at $1,000** when the ICP supports $2,500+ | Package ladder; close rate as thermometer | 1 |
| 10 | **Scoring model never calibrated** because reference accounts never arrive | Phase 0 blocker. Say so plainly if it slips | 0 |

---

## 8. Sources

**Cold call and funnel benchmarks:** [prospeo.io — conversion rate, 300M+ calls](https://prospeo.io/s/cold-calling-conversion-rate) ·
[skipcall.io — connect rate benchmarks](https://skipcall.io/en/blog/cold-call-connect-rate-benchmarks) ·
[skipcall.io — calls per meeting](https://skipcall.io/en/blog/how-many-cold-calls-to-book-a-meeting) ·
[saleshive.com](https://saleshive.com/blog/b2b-sales-cold-calling-benchmarks-teams-2025) ·
[cleverly.co](https://www.cleverly.co/blog/cold-calling-statistics)

**Win rates and cycle length:** [optif.ai — win rate by deal size, 939 companies](https://optif.ai/learn/questions/b2b-saas-win-rate-by-deal-size/) ·
[optif.ai — cycle length](https://optif.ai/learn/questions/sales-cycle-length-benchmark/) ·
[zenitdata.com](https://zenitdata.com/blog/b2b-saas-win-rate-benchmarks-by-deal-size-stage-and-segment-2026/) ·
[landbase.com](https://www.landbase.com/blog/win-rate-benchmarks-industry-deal-size-2026) ·
[salesmotion.io](https://salesmotion.io/blog/sales-win-rate-benchmarks-2026)

**Scraping and data sources:** [outscraper.com](https://outscraper.com/best-google-maps-scrapers/) ·
[gmapsscraper.io — Outscraper vs Apify](https://gmapsscraper.io/blog/outscraper-vs-apify-google-maps-scraper) ·
[gmapsscraper.io — Apify pricing](https://gmapsscraper.io/blog/apify-google-maps-scraper-pricing-review) ·
[blog.apify.com](https://blog.apify.com/best-google-maps-scrapers/)

**Job posting data:** [coresignal.com](https://coresignal.com/blog/best-job-posting-data-providers-comparison-and-use-cases/) ·
[brightdata.com](https://brightdata.com/blog/web-data/best-job-posting-data-providers) ·
[coldiq.com — Proxycurl shutdown](https://coldiq.com/blog/best-linkedin-jobs-apis) ·
[theirstack.com](https://theirstack.com/en/blog/best-job-posting-apis)

**Yelp data access:** [scrapfly.io — Yelp API guide](https://scrapfly.io/blog/posts/guide-to-yelp-api) ·
[scrapfly.io — scraping Yelp](https://scrapfly.io/blog/posts/how-to-scrape-yelpcom) ·
[apify.com — Yelp scraper](https://apify.com/thirdwatch/yelp-business-scraper)

**Contact data coverage:** [zoominfo.com](https://www.zoominfo.com/compare/apollo-vs-zoominfo) ·
[cleanlist.ai — 1,000 lead test](https://www.cleanlist.ai/blog/2026-03-07-apollo-vs-zoominfo) ·
[origami.chat — home services alternatives](https://origami.chat/blog/best-zoominfo-alternatives-home-service)

**Pricing benchmarks:** [trillet.ai — white label pricing](https://www.trillet.ai/blogs/ai-receptionist-white-label-pricing) ·
[trillet.ai — platform comparison](https://trillet.ai/blogs/top-10-white-label-voice-ai-platforms-for-agencies-2026) ·
[ringlyn.com — agency margins](https://www.ringlyn.com/blog/white-label-voice-ai-marketing-agencies/) ·
[ringlyn.com — reseller playbook](https://www.ringlyn.com/blog/white-label-ai-voice-agent-reseller-program-2026/)

**Not verified:** current MRR, delivery hours per implementation, tech-detection vendor coverage for
Boulevard/Zenoti/Jobber, and every figure sourced to the transcript rather than a citation (tagged in
doc `00`). Benchmark figures are cited secondary sources, not audited data — treat them as priors to
test in Phase 3, not as facts about your business.
