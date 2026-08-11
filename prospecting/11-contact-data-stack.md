# Finding the Owners + Getting Accurate Cell Phones and Emails

**Date:** 2026-08-07
**Covers:** Division A (independent auto body / auto repair) and Division B (multi-location med spa)
**Builds on:** `08-data-sourcing-playbook.md`, `10-gtm-week-by-week.md`

---

## 0. Scope flag before anything else — "body shop" changes the lead product

You said **auto body shop.** Body = **collision.** In the current plan Division A is independent
**mechanical** repair, and the two are different businesses with opposite problems (doc `07` §2):

| | Independent **mechanical** repair | Independent **body / collision** |
|---|---|---|
| Bucket | **B1 — drowning** | **B2 — starving, newly** |
| The wound | 25–45 calls/day, 20–30% missed, 85% of voicemail callers never return | Losing DRP referral work, no direct-acquisition capability |
| **Lead product** | **Voice AI receptionist** | **SEO + lead gen** |
| Your proof | Strongest — most reps on voice AI | **Weakest — Aaron's SEO research still isn't in the repo** |
| Ranked | **1** | 3 |

**Discovery tooling is ~80% identical for both, so everything below serves either.** But you need to pick,
because the opener and the product differ. **My recommendation stays mechanical repair for Division A** —
it leads with your strongest product and its pain is the best-documented of any vertical. Collision is
the 2027 vertical to own.

I've built the tooling for both. Tell me which and I'll collapse it.

---

## 1. The finding that changes how you dial

**Your single best targeting signal creates your single largest DNC exposure.** This is new and it
matters more than any tool choice below.

The signal is "main line rings to a mobile number" — scored `●●●` throughout these docs because it
doubles connect rate to 18–22%. **What that signal actually selects for is a sole proprietor using a
personal cell for business.** And:

| Finding | Source |
|---|---|
| Most B2B calls are exempt from the national DNC registry when selling the business a product or service — but **"the TSR's B2B exemption is real but narrow"** | [leadcompliant.com](https://leadcompliant.com/articles/cold-calling-rules/ftc-telemarketing-sales-rule-business-to-business-exemption) |
| **"If a sole proprietor or small business owner uses a personal cell phone or a home line for business, that number IS a residential line and IS on the DNC registry if they registered it"** | [leadcompliant.com](https://leadcompliant.com/articles/cold-calling-rules/business-to-business-telemarketing-rules) |
| **"The FTC's enforcement pattern suggests sole proprietors acting in a personal capacity, and micro-businesses that blur the consumer/commercial line, get treated as consumers"** | [leadcompliant.com](https://leadcompliant.com/articles/cold-calling-rules/business-to-business-telemarketing-rules) |
| **"The TCPA applies to mobile numbers, even in B2B."** With a power dialer or auto-dialer you need express consent before calling business cell phones | [smarte.pro](https://www.smarte.pro/blog/state-do-not-call-laws) |
| Many states don't exempt B2B at all — those lists must be scrubbed against **state** registries too | [smarte.pro](https://www.smarte.pro/blog/state-do-not-call-laws) |

### Three operating consequences

1. **Scrub against the national DNC registry — and the state registries in your target states.** Not
   optional. The B2B exemption is not reliable when the number is a sole proprietor's personal cell,
   which is *exactly* what you're selecting for.
2. **Manual dial only. No power dialer, no auto-dialer, on cell numbers.** Grace at 90 dials/day by hand
   is achievable. **If anyone was planning a power dialer to hit those volumes, that's a TCPA question
   before it's an efficiency question.** Worth knowing now rather than in week 5.
3. **This joins Gate 1.** It's a fifth question for the same attorney session, and it's cheaper to ask
   alongside the other four than to discover later. HIPAA left when dental did — this takes its slot.

**None of this stops the plan.** It constrains *how* you dial, not *whether*. But it was not in any prior
document and it should have been.

---

## 2. Contact data — the honest hierarchy

The question "how do we get the most accurate cell phones" has a counterintuitive answer: **the tools
built for B2B sales are the *worst* at this, and the tools built for real-estate marketers are the best.**

Because B2B databases index *corporate contacts* — people with work emails at companies with org charts.
A guy who owns three bays and answers his own phone isn't in that index. **He's in consumer/property
records, under his own name.**

### Tier 1 · Published in public — free, zero risk, highest accuracy

For owner-operators, the cell is frequently just *there*:

- The website footer or contact page — often the owner's cell, especially on smaller sites
- **Google Business Profile** — sometimes a mobile as the primary number
- **Owner responses to reviews** — often signed with a name, sometimes a direct number
- Facebook business page, Instagram bio
- Vehicle wraps and signage visible in Street View and Maps photos
- The "About" or "Meet the team" page — the owner's name, which is what Tier 3 needs

**Do this first, on the top 100 of each list.** It costs nothing, it's more accurate than any database,
and it produces the owner's *name* — which is the key input everything else depends on.

### Tier 2 · B2B waterfall enrichment — compliant, purpose-built, modest mobile yield

Waterfall tools query many providers in sequence and charge only for verified hits:

| | |
|---|---|
| **BetterContact** — 20+ providers | **87–95% email**, **70–85% phone** overall match; **mobile hits 20–35% on typical B2B contact lists** [[bettercontact.rocks](https://bettercontact.rocks/blog/waterfall-enrichment/), [syncgtm.com](https://syncgtm.com/blog/bettercontact-review)] |
| Also in this class | Findymail, FullEnrich, Kaspr, Clay — all query multiple providers and charge per verified result [[formanorden.com](https://formanorden.com/blog/b2b-data-enrichment-tools/)] |
| 2026 tool ratings (data & lead gen, out of 30) | Amplemarket 29 · ZoomInfo 24 · Cognism 23 · Apollo 21 · Clay 20 [[amplemarket.com](https://www.amplemarket.com/blog/best-b2b-data-enrichment-tools)] |
| Amplemarket | Under 3% email bounce, 70M+ records refreshed weekly [[amplemarket.com](https://www.amplemarket.com/blog/best-b2b-data-enrichment-tools)] |

**Read the mobile number carefully: 20–35%.** That's the ceiling for B2B waterfall on this population.
And recall from doc `03` §3.1 that **ZoomInfo covers ~20% of local service providers and Apollo less** —
so you're taking 20–35% of an already-thin base.

**Use waterfall for email, which it's genuinely good at (87–95%).** Don't rely on it for cells.

### Tier 3 · Skip-trace providers — 2–3× the mobile yield, with real conditions

This is where the cells actually are, and it's the tier nobody in B2B thinks to use:

| Provider | Mobile / accuracy | Note |
|---|---|---|
| **SmartSkip** | **Mobile numbers for 65–75% of records**; 92% average match confidence | [smartskip.io](https://smartskip.io/resources/blog/how-accurate-is-skip-tracing) |
| **DataZapp** | 75–85% phone accuracy, **~3¢ per record** | [datazapp.com](https://www.datazapp.com/skip-tracing-real-estate-marketing/) |
| PropertyRadar | 80%+ accuracy reported by customers | [propertyradar.com](https://www.propertyradar.com/blog/the-complete-guide-to-skip-tracing) |
| BatchSkipTracing / BatchData | Up to 10 phone numbers per lead; **"no licensing required"** | [batchdata.io](https://batchdata.io/blog/batchdata-skip-tracing-comparison-tlo-idi) |

**65–75% mobile versus 20–35% from B2B waterfall.** That's the gap, and it's the answer to your question.

**Calibrate your expectations honestly:** industry consensus is that **above 70% match rate is very high
quality**, a **60–70% usable-number rate is realistic on cold data**, and **"anyone promising 90%+ usable
mobile numbers on cold data is selling optimism"** [[readysms.io](https://readysms.io/blog/best-skip-tracing-services-compared-2026)].
If a vendor quotes you 95%, that's your tell.

**How it works, and why it needs the owner's name:** skip tracing matches a *person* — name plus address
— against consumer and property records. So the sequence is **owner name (Tier 1) → address → skip
trace**, not "company → phone." Get the name first or this tier does nothing for you.

### Tier 4 · TLO and IDI — do not use these

These are the accuracy gold standard and **they are off the table for prospecting:**

- **"Marketing is not listed as a permissible purpose"** under FCRA [[oncalllegal.com](https://www.oncalllegal.com/is-skip-tracing-legal/)]
- Using DMV-sourced data **for marketing is a federal violation** under DPPA [[proofserve.com](https://www.proofserve.com/learn/the-legal-limits-of-skip-tracing-for-attorneys)]
- **TLO requires credentialing including business verification and site inspections; IDI mandates a strict
  application verifying permissible purpose under FCRA** [[batchdata.io](https://batchdata.io/blog/batchdata-skip-tracing-comparison-tlo-idi)]

BatchData being licence-free **"reflect[s] different compliance frameworks"** — it works with public or
less-regulated sources, which is why it's available to marketers and TLO isn't
[[batchdata.io](https://batchdata.io/blog/batchdata-skip-tracing-comparison-tlo-idi)].

**Before buying any Tier 3 provider, read their terms and confirm marketing/sales outreach is a permitted
use under your specific licence.** That question goes to the same attorney session. I am not a lawyer and
this is the part of the stack where getting it wrong is a federal issue, not a deliverability issue.

---

## 3. Division A — finding independent auto body / repair shops

| Need | Tool | Cost | Verified? |
|---|---|---|---|
| **Universe** | Google Maps via **Outscraper** ($3/1K) or **Apify** ($1.50/1K) | Low | ✅ |
| **Quality pre-filter, collision only** | **I-CAR Gold Class directory** — `goldclass.i-car.com`. Requires *every* production role trained and annually maintained, so it self-selects serious operators | **Free** | ✅ |
| Additional credential | OEM certification directories | Free | ✅ |
| **State licensing, California** | **BAR Auto Shop Locator** + DCA License Search. **34,483 licensed automotive repair dealers in CA as of 30 Sept 2025** | Free | ✅ existence · ⚠️ **bulk download unconfirmed** |
| Other states | Varies. Apify's US Professional Licenses actor covers 32 boards across NJ and Indiana | Low | ⚠️ partial |
| **Bays and technicians** — the affordability qualifier | Maps photos, Street View, site copy, review text | Labour | ✅ method, ⚠️ accuracy unmeasured |
| Software install | **Orbital** or **6sense** — Mitchell 1 (largest installed base), ShopMonkey (~6,000 shops), Tekmetric (~3,000), Shop-Ware (multi-location skew = a Track B tell) | Medium | ✅ auto repair coverage |
| Reviews, job postings | Same Maps pass · **Coresignal** from $49/mo | Low | ✅ |
| **Exclusions** | Caliber · Boyd/Gerber · Crash Champions · CARSTAR · Classic Collision · Driven Brands · Midas · Meineke · Precision Tune · quick-lube brands | Free | ✅ |

**Best single move for collision:** cross-join the **free I-CAR Gold Class directory** against "ranks below
top 3 for collision repair + city." Certified quality that's invisible online — and SEO is the product
they need.

**Best single move for mechanical:** Maps universe → mobile line-type filter → review complaint mining.
All three come from one scrape plus one cheap lookup.

---

## 4. Division B — finding multi-location med spa groups

Harder, because **there is no directory of independent 3–8 location med spa groups.** You build it.

| Need | Tool | Cost | Verified? |
|---|---|---|---|
| **Universe** | Google Maps. 10,000+ US locations, **81% single-location** | Low | ✅ |
| **The group-finding method** | **Cluster** Maps results on identical brand name + shared root domain + shared main phone → **count distinct addresses** → keep 3–8 → exclude PE brands → verify ownership | Labour | ✅ method (doc `08` §1.1) |
| Ownership verification | State Secretary of State business filings; the site's About page | Free–low | ✅ |
| **The wedge signal** | **Boulevard** booking-widget detection — documented weak on campaign attribution and lifetime-value reporting. **Zenoti = deprioritise** (strong reporting, less gap) | Low | ✅ |
| Dormant-base signal | Review count far exceeding recent review velocity | Free with the Maps pass | ✅ |
| Owner / physician identity | State medical boards — often registered under a physician's PC or a DBA, **which is exactly why Apollo undercounts med spas** | Free | ✅ |
| PE exclusion | 30+ active platforms but only **3–4% consolidated** — the smallest exclusion problem in scope | Free | ✅ |
| ~~AmSpa member directory~~ | **Not viable.** 3,000+ members but **no publicly searchable directory** — members-only portal, built for networking. Mining it for cold outreach would likely breach their terms | — | ✅ *checked and ruled out* |

**Why Apollo failed you before:** doc `03` §3.1 — you found ~500 med spas nationwide against 10,000+
actual locations. That's ~5% coverage, and the DBA/physician-PC registration pattern is the mechanism.
**Maps is the universe; Apollo is enrichment only.**

---

## 5. The recommended stack

### Division A · owner-operator, high mobile yield needed

```
  1. Outscraper / Apify        Maps universe + reviews            ~$15 / 5,000
  2. Twilio Lookup             line type — keep mobiles only      ~$25-50 / 5,000
  3. MANUAL, top 100           owner name from site / reviews / GBP    labour
  4. BetterContact             email waterfall (87-95%)           per verified hit
  5. DataZapp or BatchData     skip trace name+address -> cell    ~3c/record
  6. DNC SCRUB                 national + state registries         MANDATORY
  7. Coresignal                job postings, 30+ days              $49/mo
```

### Division B · multi-location, fewer records, deeper research

```
  1. Outscraper / Apify        Maps universe, med spa
  2. Cluster + count           3-8 locations, exclude PE brands        code
  3. Boulevard detection       booking-widget DOM parse                code
  4. MANUAL, all of them       ~100 groups. Verify ownership,
                               find the owner or exec by name          labour
  5. BetterContact / Clay      email + phone waterfall
  6. DNC SCRUB                 before Aaron or Alec dials              MANDATORY
```

**Division B is small enough to research by hand and should be.** ~100 groups at $5,000/mo each. Manual
research per account is the correct spend, and it's what makes a peer-level opening call land.

### Cost sanity check

| | |
|---|---|
| Maps scrape, 5,000 records | ~$15 |
| Line-type lookups, 5,000 | ~$25–50 |
| Skip trace, 1,000 records at ~3¢ | ~$30 |
| Coresignal | $49/mo |
| BetterContact entry | from ~$15/mo |
| I-CAR Gold Class, BAR, state boards, SOS filings | **Free** |
| **Tooling total** | **well under $200/month** |

**Tooling is not the cost. Jameson's hours are.** The $50-per-qualified-prospect kill criterion breaks on
labour, and Tier 1 and the Division B manual pass are both labour by design. **Track hours from day one**
— that number is the one that will decide whether this motion is economic.

---

## 6. What I could not verify

Stated plainly rather than papered over:

1. **Whether California BAR publishes a bulk download.** The Auto Shop Locator and DCA License Search
   exist and 34,483 licensees is a real figure, but I found no confirmation of a downloadable file. **Call
   BAR and ask.** Same question for every other target state.
2. **Whether 6sense or Orbital cover Boulevard and Zenoti.** I confirmed auto repair software coverage
   only. **Quote and test before committing budget.**
3. **Whether marketing/sales outreach is a permitted use under any specific Tier 3 provider's licence.**
   BatchData advertises no licensing requirement; that is not the same as a legal opinion about your use
   case. **Attorney question, same session.**
4. **Bay-count estimation accuracy from Maps photos and Street View.** The method is sound; the error rate
   is unmeasured, and it's the affordability qualifier for your top vertical. **Measure it against 20
   hand-checked shops in week 1.**
5. **Actual mobile hit rate on *your* lists.** Every number here is a vendor or industry benchmark. Run
   200 records through two providers in week 1 and measure. Cheap, fast, and it replaces every estimate in
   §2 with a fact.

---

## 7. What I'd challenge

1. **The DNC finding constrains the operating model and nobody has priced it.** Scrubbing is a step, a
   cost, and a compliance obligation. **And manual-dial-only may collide with Grace's 90/day** if the
   plan quietly assumed dialer software. Resolve before week 3.
2. **"Auto body" versus "mechanical repair" is still undecided** and it changes the lead product from
   voice AI (your strongest) to SEO (your least documented, and the research still isn't in the repo).
   **Pick one before Jameson scrapes.**
3. **Tier 3 is the highest-yield and highest-risk tier.** Do not let it become the default because the
   hit rate is attractive. **Tier 1 first, always** — for an owner-operator the cell is often published,
   free, and more accurate than any database.
4. **Two providers minimum on any paid tier.** Every accuracy figure in §2 is self-reported by the vendor
   selling it. Run both against the same 200 records and compare. The consensus view that 90%+ claims are
   "selling optimism" applies to every table above.
5. **Division B's manual pass is ~100 accounts of real research.** At $5,000/mo each that's correct
   spend, but it is **not** a two-week job on top of everything else in Jameson's sprint. Either extend
   the window or narrow Division B to 50 accounts and go deeper.

---

## 8. Sources

**Waterfall enrichment:** [bettercontact.rocks](https://bettercontact.rocks/blog/waterfall-enrichment/) ·
[syncgtm.com — BetterContact review](https://syncgtm.com/blog/bettercontact-review) ·
[amplemarket.com](https://www.amplemarket.com/blog/best-b2b-data-enrichment-tools) ·
[formanorden.com](https://formanorden.com/blog/b2b-data-enrichment-tools/) ·
[clay.com — data waterfalls](https://www.clay.com/blog/data-waterfalls) ·
[moderninbound.com](https://moderninbound.com/blog/fullenrich-vs-bettercontact)

**Skip tracing accuracy:** [smartskip.io](https://smartskip.io/resources/blog/how-accurate-is-skip-tracing) ·
[datazapp.com](https://www.datazapp.com/skip-tracing-real-estate-marketing/) ·
[propertyradar.com](https://www.propertyradar.com/blog/the-complete-guide-to-skip-tracing) ·
[readysms.io](https://readysms.io/blog/best-skip-tracing-services-compared-2026) ·
[batchdata.io — vs TLO/IDI](https://batchdata.io/blog/batchdata-skip-tracing-comparison-tlo-idi)

**Skip tracing legality:** [oncalllegal.com — is it legal](https://www.oncalllegal.com/is-skip-tracing-legal/) ·
[proofserve.com — legal limits](https://www.proofserve.com/learn/the-legal-limits-of-skip-tracing-for-attorneys) ·
[oncalllegal.com — ethically](https://www.oncalllegal.com/how-to-skip-trace/)

**DNC and B2B calling:** [leadcompliant.com — TSR B2B exemption](https://leadcompliant.com/articles/cold-calling-rules/ftc-telemarketing-sales-rule-business-to-business-exemption) ·
[leadcompliant.com — B2B telemarketing rules](https://leadcompliant.com/articles/cold-calling-rules/business-to-business-telemarketing-rules) ·
[smarte.pro — state DNC laws](https://www.smarte.pro/blog/state-do-not-call-laws) ·
[covelaw.com](https://covelaw.com/b2b-calls-exemptions-the-dnc-list/) ·
[ftc.gov — DNC Q&A](https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr-0)

**Automotive directories and licensing:** [goldclass.i-car.com](https://goldclass.i-car.com/) ·
[bar.ca.gov — licensing data](https://www.bar.ca.gov/arsc/newsletters/newsletter/fall-2025/licensing-data) ·
[aftermarketmatters.com — Auto Shop Locator](https://www.aftermarketmatters.com/regions/northern-california/bureau-of-automotive-repair-launches-new-auto-shop-locator/) ·
[ca.gov — find an auto shop](https://www.ca.gov/departments/137/services/6/) ·
[apify.com — US professional licenses](https://apify.com/wallman_3rd/us-professional-licenses)

**Med spa:** [americanmedspa.org](https://www.americanmedspa.org/) ·
[americanmedspa.org — member benefits](https://americanmedspa.org/why-amspa)

**I am not a lawyer.** The DNC, TCPA, FCRA and DPPA findings are cited secondary sources. Items 3 and the
whole of §1 belong in the Gate 1 attorney session before any list is dialled or purchased.
