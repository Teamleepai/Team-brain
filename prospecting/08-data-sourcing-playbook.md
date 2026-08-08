# Data Sourcing Playbook — Tools and Scrapers, Per Industry

**Date:** 2026-08-07 · **Rev 2** — dental and veterinary removed per scope decision
**Builds on:** `03` §3 (source map), `05`, `07`, `09-audit-2026-08-07.md`
**Answers:** what to scrape, from where, to find (a) the owner-operator small-market fit and
(b) multi-location groups below PE scale — per industry

> **Rev 1 ranked dental first**, on the strength of the free NPPES federal provider file. Dental and
> veterinary were withdrawn from scope on 2026-08-07. **The NPPES file was dental-specific and is gone
> with it** — that was the cheapest high-quality data source in this playbook, and its loss is the main
> cost of the scope change. See `09-audit-2026-08-07.md` §1.

---

## 1. The two tracks need different mechanics

These are not the same search with a different filter. They are structurally different problems.

| | **Track A — owner-operator** | **Track B — multi-location under PE scale** |
|---|---|---|
| Target | 1–2 locations, owner decides | 3–8 locations, owner or single exec decides |
| Discovery | Google Maps universe, filtered down | **Cluster Maps results into groups, then filter** |
| Hard part | Proving they can pay | **Proving they're *not* PE-owned** |
| Key signal | Owner-operator markers (doc `01` §2.2) | Location count in the 3–8 band |
| Failure mode | Targeting businesses too small to pay | Wasting cycles on a PE platform's procurement |

**Track B's real work is exclusion, not discovery.** Finding a 6-location med spa group is easy. Knowing
whether it's independently owned or a PE platform's roll-up determines whether you have a 30-day sale or
no sale at all.

### 1.1 The multi-location clustering method

There is no database of "independent 3–8 location groups." You build it:

```
  1. Scrape the Maps universe for one industry across a geography
  2. CLUSTER on: identical brand name + shared root domain + shared main phone
  3. COUNT distinct street addresses per cluster
  4. KEEP clusters of 3-8
  5. EXCLUDE any cluster whose brand appears on the consolidator lists in §4
  6. VERIFY ownership on the remaining clusters — state SOS filing or the site's About page
```

Steps 2–4 are cheap and mechanical. **Step 5 is where the value is**, and it requires the brand lists
in §4 maintained as a file in the repo, not held in someone's head.

---

## 2. The universal stack — applies to every industry

| Layer | Tool | Cost | Purpose |
|---|---|---|---|
| **Universe** | Google Maps via **Outscraper** ($3/1K) or **Apify** ($1.50/1K base) | Low | The only near-complete local business source. Doc `03` §3.1 |
| **Reviews** | Same pass | Included | Complaint mining, velocity vs rating trend — the highest-ROI signal in the stack |
| **Phone line type** | Twilio Lookup or equivalent | ~pennies | **Mandatory filter.** Mobile direct-dial doubles connect rate to 18–22% |
| **Job postings** | **Coresignal** (from $49/mo, 399M+ postings, licensed, aggregates Indeed) | Low | The "hiring for 30+ days" signal across every vertical |
| **Website tech** | Self-built HTTP fetch + DOM parse | ~free | Chat widget, booking widget, CMS, SSL, forms. **Build it — no vendor needed** |
| **Software installs** | **6sense** or **Orbital** (withorbital.com) | Medium | Both publish software-customer mapping. Orbital advertises 14,000 auto shops mapped against Tekmetric alone |
| **Paid ads** | Meta Ad Library (free) + a paid-search tool | Low | Best single ability-to-pay proxy |
| **Licenses** | State boards — see §3 | Free–low | Existence + credential + often the owner's own name |

**This closes the doc `03` §3.3 open item on tech detection.** The answer is split: build website-surface
detection yourself (cheap, reliable, fully under your control), and buy software-install data from
6sense or Orbital where the install isn't visible in the DOM.

---

## 3. Per-industry source map

### 3.1 HVAC and Plumbing

| Need | Source | Notes |
|---|---|---|
| Universe | Google Maps | |
| **Existence + credential + owner name** | **State contractor license boards** | Coverage varies wildly by state. **Texas State Board of Plumbing Examiners publishes a free CSV licensee list, updated daily** — the gold standard [[tsbpe.texas.gov](https://tsbpe.texas.gov/free-licensee-list/)] |
| Multi-state license data | **Apify US Professional License Data** actor — name, license number, type, status, city, state; JSON/CSV/Excel; 32 boards across NJ and Indiana | Coverage is partial. Check your target states before committing [[apify.com](https://apify.com/wallman_3rd/us-professional-licenses)] |
| Other state lookups | Ohio eLicense, WV Division of Labor, NC Licensing Board | Individual lookups, not bulk |
| Ability to pay | Permit volume (county records), fleet/DOT, license class and bond amount, Meta Ad Library | **Mandatory for plumbing** — median operators run 2–8% net and cannot pay (doc `05` §2.2) |
| Software | ServiceTitan / Housecall Pro / Jobber via 6sense or booking-widget DOM detection | |
| **PE exclusion** | Apex Service Partners, Wrench Group, Sila Services, ARS/Rescue Rooter, TurnPoint, Comfort Systems USA | ~800 companies acquired since 2022 (doc `03` §5) |

**Start with Texas.** A free daily CSV of every licensed plumber in the state, cross-joined against a
Maps scrape, is the cheapest high-quality list available in any vertical here.

### 3.2 Independent mechanical auto repair — **now the top vertical**

| Need | Source | Notes |
|---|---|---|
| Universe | Google Maps | **~230,000 US auto repair shops** — a large TAM [[sacra.com](https://sacra.com/c/shopmonkey/)] |
| **Bay and technician count** — the affordability proxy | Maps photos, site copy, review text, Street View | Doc `07` §2.1 flagged a revenue conflict ($450K vs $500K–1.2M). **Bays and techs are the honest qualifier, not the industry average — and this is now load-bearing, because auto repair is the top-ranked vertical** |
| Software install | **Orbital or 6sense** — Mitchell 1 (largest installed base), ShopMonkey (~6,000 shops), Tekmetric (~3,000), Shop-Ware (multi-location focus), AutoLeap | Shop-Ware skewing multi-location makes it a **Track B tell** [[withorbital.com](https://www.withorbital.com/data/software/tekmetric/), [6sense.com](https://6sense.com/tech/automobile-repair-and-maintenance-software/shopmonkey-market-share)] |
| Credential | ASE certification, NAPA AutoCare, TechNet affiliations | Site-badge detectable |
| Franchise exclusion | Midas, Meineke, Precision Tune, quick-lube brands | Doc `07` §2.3 — avoid quick lube entirely |

**A Shop-Ware install is a signal, not just a data point.** Shop-Ware positions for multi-location, so
its presence suggests a Track B candidate before you've counted a single address.

### 3.3 Collision / body repair

| Need | Source | Notes |
|---|---|---|
| Universe | Google Maps | 105,000 businesses per IBISWorld; another source cites 8,000+ facilities. **Flagged conflict — likely all-body-shops vs larger facilities** |
| **Quality pre-filter** | **I-CAR Gold Class directory at `goldclass.i-car.com`** | A searchable directory of shops that invested in full-staff training. **This is a pre-qualified list of serious operators** [[goldclass.i-car.com](https://goldclass.i-car.com/)] |
| Additional credential | OEM certification directories; third-party aggregators verify against I-CAR and OEM databases | [[getlocalverified.com](https://getlocalverified.com/icar-gold-class-collision-repair/)] |
| **The killer signal** | **Reduced or exited DRP participation** — no database exists. Detect from site copy changes, trade press, forums, or simply ask on the call | Highest-intent signal in the vertical (doc `07` §2.4). **Manual, and worth it** |
| SEO gap | Rank tracking for "collision repair + city" | Their new and unmet need |
| **Consolidator exclusion** | Caliber (1,800+), Boyd/Gerber (900+), Crash Champions (700+), CARSTAR and Classic Collision (Driven Brands) | ~30% of industry revenue |

**I-CAR Gold Class is the highest-signal free directory in this playbook.** Gold Class requires *every*
production role — structural, non-structural, refinish, estimator — to complete and annually maintain
training. A shop that does that invests in itself, which means it has money and cares about quality.
**Cross-join Gold Class against "ranks below top 3 for collision repair + city" and you have a
near-perfect Track A list for the SEO offer.**

### 3.4 Med spa — **now rank 2**

| Need | Source | Notes |
|---|---|---|
| Universe | Google Maps | 10,000+ locations, 81% single-location |
| Credential | State medical boards — often registered under a physician's PC or a DBA, which is exactly why Apollo undercounts them (doc `03` §3.1) | |
| Software | **Boulevard** (documented weak attribution/LTV reporting — the wedge) vs **Zenoti** (strong reporting — deprioritise) | Booking-widget DOM detection. Doc `01` §1.6 |
| Multi-location | Maps clustering. Groups averaged 9 locations in 2024, up from 6 | 3–8 site operators draw the most acquisition interest |
| PE exclusion | 30+ active PE platforms; only 3–4% consolidated | **The smallest exclusion problem of any vertical in scope** |

### 3.5 Deprioritised

**Auto detailing** — cannot afford the ticket and Q4 is their off-season (doc `05` §2.4).
**Quick lube** — $50–120 ticket, chain-dominated (doc `07` §2.3).
Keep the products and existing accounts. Don't point the engine at either before spring.

---

## 4. The exclusion lists — maintain these as a file, not as memory

**This is the highest-leverage artefact in the playbook.** Every hour spent on a PE platform is a wasted
hour, and these brands are knowable in advance.

Dental DSO and veterinary consolidator lists were removed with those verticals. If either comes back
into scope, the maintained trackers are named in the git history of this file (rev 1).

### 4.1 Home services and automotive

**HVAC/plumbing:** Apex Service Partners (Alpine) · Wrench Group (Leonard Green) · Sila Services
(Goldman) · ARS/Rescue Rooter (GI Partners) · TurnPoint (OMERS) · Comfort Systems USA
**Collision:** Caliber · Boyd/Gerber · Crash Champions · CARSTAR · Classic Collision · Driven Brands
**Auto repair franchises:** Midas · Meineke · Precision Tune · all quick-lube brands
**Med spa:** 30+ active PE platforms, but only 3–4% of med spas are consolidated — the smallest
exclusion problem of any vertical in scope

Trackers: [dealseam.com](https://dealseam.com/hvac-pe-rollup-tracker-2026) ·
[bodyshopbusiness.com](https://www.bodyshopbusiness.com/auto-body-consolidation-forecast-2026-ready-for-takeoff/) ·
[ctacquisitions.com](https://ctacquisitions.com/guides/private-equity-platforms-by-sector-2026/)

---

## 5. Build order — sequenced for a 30 November deadline

| # | Vertical | Why this order | Effort |
|---|---|---|---|
| **1** | **Independent auto repair** | Google Maps + Orbital/6sense. **Best-documented voice AI pain available** — and voice AI is the product you have the most reps on | **Low** |
| **2** | **Med spa** | Maps + Boulevard widget detection. Best affordability of any vertical, and the reactivation lead product | Low–medium |
| **3** | **Collision** | I-CAR Gold Class pre-filters quality for free. **Least competitive vertical in scope** | Low–medium |
| 4 | HVAC | Maps + review mining. Heating season runs through the sell window | Medium |
| 5 | Plumbing | Best in states with bulk license data — start Texas. **Leaders only** | Medium |

**Build 1 and 2 this week. Auto repair and med spa cover both lead products, both buckets, and neither
is healthcare.**

### 5.1 Cost sanity check

Doc `03` set a kill criterion of **$50 per qualified prospect.** Against that:

| Item | Cost |
|---|---|
| Google Maps scrape, 5,000 records | ~$15 |
| I-CAR Gold Class directory | **$0** |
| Coresignal job postings | $49/mo |
| Phone line-type lookups, 5,000 | ~$25–50 |
| Software-install data | Medium — quote before committing |
| **Raw data, ~5,000 entities** | **well under $200** |

Raw data is not the cost. **Manual verification labour is**, and it's the line item nobody has priced.
That's the number to watch against the $50 threshold — particularly for the collision DRP signal, which
is manual by nature and has no database behind it.

---

## 6. What I'd challenge

1. **You now have six verticals, two tracks, and one sales team.** Doc `01` §6.4 and doc `07` §6 both
   argued reference density in one vertical beats breadth. **This playbook makes breadth *possible*,
   which is not the same as making it wise.** Build auto repair and med spa. Leave the rest documented
   and unbuilt.
2. **Track B may not fit the deadline at all.** Multi-location groups mean 30–90 day cycles (doc `05`
   §6.1). Started in September, a Track B deal lands in November — with no room for slippage. **Track B
   is a Q1 2027 motion that you seed now**, not a Q4 revenue source.
3. **Nobody has priced the manual verification labour.** Every source above is cheap; the humans reading
   the results are not. **The $50-per-qualified-prospect kill criterion will be breached by labour, not
   by data fees** — and it'll be breached quietly.
4. **The exclusion lists decay.** PE roll-ups move fast — ~800 home services companies acquired since
   2022. A brand list built today is stale in a quarter. **Assign an owner and a refresh cadence, or it
   becomes actively misleading** — worse than not having it, because you'll trust it.
5. **Losing dental cost you the cheapest data source in this playbook.** The free NPPES federal CSV had
   no equivalent in any remaining vertical. Auto repair and med spa both require paid scraping plus
   manual verification. **The cost-per-qualified-prospect assumption should be re-tested, not inherited.**
6. **The auto repair revenue conflict is unresolved and it matters more now.** $450K vs $500K–1.2M decides
   whether a shop can pay $2,000/mo. Qualify on bays and techs. Do not let the scraper decide on
   revenue estimates it can't actually see.

---

## 7. Sources

**Licensing and credentials:** [tsbpe.texas.gov — free CSV licensee list](https://tsbpe.texas.gov/free-licensee-list/) ·
[apify.com — US professional licenses](https://apify.com/wallman_3rd/us-professional-licenses) ·
[elicense4.com.ohio.gov](https://elicense4.com.ohio.gov/lookup/licenselookup.aspx) ·
[labor.wv.gov](https://labor.wv.gov/database-search)

**Collision credentials:** [goldclass.i-car.com](https://goldclass.i-car.com/) ·
[info.i-car.com](https://info.i-car.com/gold-class) ·
[getlocalverified.com](https://getlocalverified.com/icar-gold-class-collision-repair/)

**Software install data:** [withorbital.com — Tekmetric](https://www.withorbital.com/data/software/tekmetric/) ·
[6sense.com — ShopMonkey share](https://6sense.com/tech/automobile-repair-and-maintenance-software/shopmonkey-market-share) ·
[enlyft.com — Dentrix share](https://enlyft.com/tech/products/dentrix) ·
[sacra.com — Shopmonkey](https://sacra.com/c/shopmonkey/)

**PE and consolidator trackers:** [dealseam.com — HVAC](https://dealseam.com/hvac-pe-rollup-tracker-2026) ·
[bodyshopbusiness.com](https://www.bodyshopbusiness.com/auto-body-consolidation-forecast-2026-ready-for-takeoff/)

**Not verified:** whether 6sense or Orbital cover **Boulevard and Zenoti** — I confirmed auto repair
coverage only, so **quote and test before committing budget.** Also unverified: state-by-state bulk
license availability beyond Texas, New Jersey and Indiana; and the manual-labour cost per qualified
prospect, which is the number most likely to break the unit economics — **and which just got worse,
because the one free bulk source left with the scope change.**
