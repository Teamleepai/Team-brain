# Data Sourcing Playbook — Tools and Scrapers, Per Industry

**Date:** 2026-08-07
**Builds on:** `03` §3 (source map), `05`, `07`
**Answers:** what to scrape, from where, to find (a) the owner-operator small-market fit and
(b) multi-location groups below PE scale — per industry

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

**Track B's real work is exclusion, not discovery.** Finding a 6-location dental group is easy. Knowing
whether it's an independent group or a Heartland-supported one determines whether you have a 30-day
sale or no sale at all.

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

### 3.2 Dental — the best data situation of all six

| Need | Source | Notes |
|---|---|---|
| **Universe + practice address + specialty + website + email** | **NPPES NPI bulk download from CMS** | **Free. Full-replacement monthly CSV, weekly incrementals.** Includes taxonomy codes (specialty), practice and alternate addresses, website URLs, email, organisation-vs-individual flag. **Use Version 2** — V1 was retired 3 March 2026 [[cms.gov](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination), [resdac.org](https://resdac.org/articles/overview-nppesnpi-downloadable-file)] |
| Alternative if you want it pre-parsed | Apify NPPES NPI Crawler (2.5M+ provider records) | Convenience, not necessity [[apify.com](https://apify.com/jungle_synthesizer/nppes-npi-crawler)] |
| Credential + owner name | State dental board lookups; ADA lists all state boards | e.g. Texas SBDE public license search [[ada.org](https://www.ada.org/resources/careers/licensure/state-dental-boards)] |
| Cross-reference | ADA Masterfile — every US dentist, reconciled against state licensure | Not free, but the authoritative source [[ada.org](https://www.ada.org/resources/research/health-policy-institute/dental-practice-research/practice-modalities-among-us-dentists)] |
| Software | Dentrix (~25% share), Eaglesoft, Open Dental, Carestream, Planet DDS | Dentrix share via enlyft. Detect via booking widget or 6sense |
| Multi-location | **Group organisational NPIs by shared name and address cluster** | The NPI file makes this unusually clean |
| **DSO exclusion** | §4.1 | **16.1% of US dentists were DSO-affiliated in 2024** — so ~84% remain your pool [[beckersdental.com](https://www.beckersdental.com/dso-dpms/the-pe-firms-behind-15-dsos/)] |

**A free, complete, monthly federal CSV with practice addresses, specialties, websites and emails is the
single best data source in this entire playbook.** Dental is not just the top-ranked vertical on
economics (doc `07` §5) — it's also the cheapest to build a list for.

One useful nuance: DSO affiliation exceeds **25% among dentists within a decade of dental school** but is
16.1% overall — so **established owner-dentists are disproportionately independent.** Practice age is a
qualifying signal, not just a demographic.

### 3.3 Veterinary — the hardest of the six

**Be aware going in: there is no NPI equivalent and no central practice registry.** Vets aren't HIPAA
covered entities, so the NPPES file doesn't help. My search for a centralised AVMA practice database
returned nothing usable.

| Need | Source | Notes |
|---|---|---|
| Universe | **Google Maps — and it's doing most of the work here** | No better option found |
| Credential | State veterinary board lookups, one state at a time | AAVSB and NBVME are exam bodies, not practice directories |
| Multi-location | Maps clustering per §1.1 | |
| **Corporate exclusion** | §4.2 | **Consolidators own ~30% of US practices, so ~70% are independent** [[transitionselite.com](https://transitionselite.com/veterinary-consolidator-ownership-map-2026/)] |
| Software | Cornerstone / ezyVet / AVImark / Covetrus | Detect via booking widget; install data thinner than dental |

**Practical consequence: veterinary costs more per qualified prospect than dental** because more of the
work is manual. Given a 30 November deadline, that's an argument for putting dental ahead of vet in the
build order, even though vet's missed-call number is larger.

### 3.4 Independent auto repair (mechanical)

| Need | Source | Notes |
|---|---|---|
| Universe | Google Maps | **~230,000 US auto repair shops** — a large TAM [[sacra.com](https://sacra.com/c/shopmonkey/)] |
| **Bay and technician count** — the affordability proxy | Maps photos, site copy, review text, Street View | Doc `07` §2.1 flagged a revenue conflict ($450K vs $500K–1.2M). **Bays and techs are the honest qualifier, not the industry average** |
| Software install | **Orbital or 6sense** — Mitchell 1 (largest installed base), ShopMonkey (~6,000 shops), Tekmetric (~3,000), Shop-Ware (multi-location focus), AutoLeap | Shop-Ware skewing multi-location makes it a **Track B tell** [[withorbital.com](https://www.withorbital.com/data/software/tekmetric/), [6sense.com](https://6sense.com/tech/automobile-repair-and-maintenance-software/shopmonkey-market-share)] |
| Credential | ASE certification, NAPA AutoCare, TechNet affiliations | Site-badge detectable |
| Franchise exclusion | Midas, Meineke, Precision Tune, quick-lube brands | Doc `07` §2.3 — avoid quick lube entirely |

**A Shop-Ware install is a signal, not just a data point.** Shop-Ware positions for multi-location, so
its presence suggests a Track B candidate before you've counted a single address.

### 3.5 Collision / body repair

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

### 3.6 Med spa

| Need | Source | Notes |
|---|---|---|
| Universe | Google Maps | 10,000+ locations, 81% single-location |
| Credential | State medical boards — often registered under a physician's PC or a DBA, which is exactly why Apollo undercounts them (doc `03` §3.1) | |
| Software | **Boulevard** (documented weak attribution/LTV reporting — the wedge) vs **Zenoti** (strong reporting — deprioritise) | Booking-widget DOM detection. Doc `01` §1.6 |
| Multi-location | Maps clustering. Groups averaged 9 locations in 2024, up from 6 | 3–8 site operators draw the most acquisition interest |
| PE exclusion | 30+ active PE platforms; only 3–4% consolidated | Small exclusion problem relative to dental or vet |

### 3.7 Deprioritised

**Auto detailing** — cannot afford the ticket and Q4 is their off-season (doc `05` §2.4).
**Quick lube** — $50–120 ticket, chain-dominated (doc `07` §2.3).
Keep the products and existing accounts. Don't point the engine at either before spring.

---

## 4. The exclusion lists — maintain these as a file, not as memory

**This is the highest-leverage artefact in the playbook.** Every hour spent on a PE platform is a wasted
hour, and these brands are knowable in advance.

### 4.1 Dental DSOs

~**130 PE-backed DSOs** exist, and dental logged **120+ PE add-on acquisitions in 2024 — the most of any
healthcare category.**

| Platform | Backer | Scale |
|---|---|---|
| Heartland Dental | KKR + Ontario Teachers' | ~2,500 supported offices |
| Aspen Dental | Leonard Green + Ares | ~1,100 offices |
| Pacific Dental Services | Founder-owned | ~1,000 offices |
| Smile Brands | New Mountain Capital | ~700 practices |
| MB2 Dental | Charlesbank + Warburg Pincus | ~600 partnerships |
| Specialty1 Partners | — | 220+ practices, 28 states |
| Mortenson Dental Partners | Audax + Genstar | — |
| Dental Care Alliance | Quad-C | — |
| Sage Dental | Carousel Capital | — |

The top three alone support ~15% of US dentists.
Maintained trackers: [beckersdental.com](https://www.beckersdental.com/dso-dpms/the-pe-firms-behind-15-dsos/) ·
[dealseam.com](https://dealseam.com/dental-pe-rollup-tracker-2026) ·
[ctacquisitions.com](https://ctacquisitions.com/dental-dso-pe-rollup-tracker-2026/) ·
[medixdental.com](https://medixdental.com/largest-dsos-in-the-us/)

### 4.2 Veterinary consolidators

Corporate owns ~**30%** of US practices; ~**70% independent.**

Mars Veterinary Health (VCA, BluePearl) · NVA — JAB Holding, ~1,400 locations · Ethos Veterinary Health
— ~145 hospitals · VetCor (Harvest Partners) · PetVet Care Centers (Ares) · Thrive Pet Healthcare —
TSG, formerly Pathway Vet Alliance · AmeriVet (AEA + Oaktree) · Veterinary Practice Partners (Pamlico) ·
Heartland Veterinary Partners (Gryphon) · Blue River PetCare (Tailwind) · Alliance Animal Health
(L Catterton) · Rarebreed (Berkshire) · Western Veterinary Partners (Prospect Hill) · United Veterinary
Care (TA Associates) · Community Veterinary Partners (OMERS)

Maintained ownership map: [transitionselite.com](https://transitionselite.com/veterinary-consolidator-ownership-map-2026/) ·
[ctacquisitions.com](https://ctacquisitions.com/guides/private-equity-veterinary-2026/)

### 4.3 Home services and automotive

**HVAC/plumbing:** Apex Service Partners (Alpine) · Wrench Group (Leonard Green) · Sila Services
(Goldman) · ARS/Rescue Rooter (GI Partners) · TurnPoint (OMERS) · Comfort Systems USA
**Collision:** Caliber · Boyd/Gerber · Crash Champions · CARSTAR · Classic Collision · Driven Brands
**Auto repair franchises:** Midas · Meineke · Precision Tune · all quick-lube brands

Trackers: [dealseam.com](https://dealseam.com/hvac-pe-rollup-tracker-2026) ·
[bodyshopbusiness.com](https://www.bodyshopbusiness.com/auto-body-consolidation-forecast-2026-ready-for-takeoff/) ·
[ctacquisitions.com](https://ctacquisitions.com/guides/private-equity-platforms-by-sector-2026/)

---

## 5. Build order — sequenced for a 30 November deadline

| # | Vertical | Why this order | Effort |
|---|---|---|---|
| **1** | **Dental** | Free NPPES federal CSV + the strongest economics + the 31 Dec benefits deadline | **Lowest** |
| **2** | **Auto repair** | Google Maps plus Orbital/6sense software data. Best-documented voice AI pain | Low |
| **3** | **Collision** | I-CAR Gold Class pre-filters quality for free. Least competitive vertical | Low–medium |
| **4** | **Med spa** | Maps plus Boulevard detection. Already scoped in docs `01`/`05` | Medium |
| **5** | HVAC / plumbing | Best in states with bulk license data — start Texas | Medium |
| **6** | Veterinary | Maps-only, manual exclusion, no central registry | **Highest** |

**Build 1 and 2 this week. They cover both lead products, both buckets, and the cheapest data.**

### 5.1 Cost sanity check

Doc `03` set a kill criterion of **$50 per qualified prospect.** Against that:

| Item | Cost |
|---|---|
| Google Maps scrape, 5,000 records | ~$15 |
| NPPES bulk file | **$0** |
| I-CAR Gold Class directory | **$0** |
| Coresignal job postings | $49/mo |
| Phone line-type lookups, 5,000 | ~$25–50 |
| Software-install data | Medium — quote before committing |
| **Raw data, ~5,000 entities** | **well under $200** |

Raw data is not the cost. **Manual verification labour is**, and it's the line item nobody has priced.
That's the number to watch against the $50 threshold — particularly for veterinary and for the collision
DRP signal, both of which are manual by nature.

---

## 6. What I'd challenge

1. **You now have six verticals, two tracks, and one sales team.** Doc `01` §6.4 and doc `07` §6 both
   argued reference density in one vertical beats breadth. **This playbook makes breadth *possible*,
   which is not the same as making it wise.** Build dental and auto repair. Leave the rest documented
   and unbuilt.
2. **Track B may not fit the deadline at all.** Multi-location groups mean 30–90 day cycles (doc `05`
   §6.1). Started in September, a Track B deal lands in November — with no room for slippage. **Track B
   is a Q1 2027 motion that you seed now**, not a Q4 revenue source.
3. **Nobody has priced the manual verification labour.** Every source above is cheap; the humans reading
   the results are not. **The $50-per-qualified-prospect kill criterion will be breached by labour, not
   by data fees** — and it'll be breached quietly.
4. **The exclusion lists decay.** PE add-ons ran 120+ in dental in 2024 alone. A brand list built today
   is stale in a quarter. **Assign an owner and a refresh cadence, or it becomes actively misleading** —
   worse than not having it, because you'll trust it.
5. **HIPAA is still unanswered for dental and veterinary.** Doc `07` §6 flagged it. This playbook now
   proposes downloading a federal healthcare provider file and scraping practice data — which makes the
   question more pressing, not less. **Gate 1 legal review before the first dental send.**
6. **The auto repair revenue conflict is unresolved and it matters here.** $450K vs $500K–1.2M decides
   whether a shop can pay $2,000/mo. Qualify on bays and techs. Do not let the scraper decide on
   revenue estimates it can't actually see.

---

## 7. Sources

**Licensing and credentials:** [tsbpe.texas.gov — free CSV licensee list](https://tsbpe.texas.gov/free-licensee-list/) ·
[apify.com — US professional licenses](https://apify.com/wallman_3rd/us-professional-licenses) ·
[ada.org — state dental boards](https://www.ada.org/resources/careers/licensure/state-dental-boards) ·
[tsbde.texas.gov](https://tsbde.texas.gov/resources/public-license-search/) ·
[elicense4.com.ohio.gov](https://elicense4.com.ohio.gov/lookup/licenselookup.aspx) ·
[labor.wv.gov](https://labor.wv.gov/database-search)

**NPPES / NPI:** [cms.gov — data dissemination](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination) ·
[resdac.org — file overview](https://resdac.org/articles/overview-nppesnpi-downloadable-file) ·
[npipublicdata.org](https://npipublicdata.org/downloads/) ·
[apify.com — NPPES crawler](https://apify.com/jungle_synthesizer/nppes-npi-crawler)

**Collision credentials:** [goldclass.i-car.com](https://goldclass.i-car.com/) ·
[info.i-car.com](https://info.i-car.com/gold-class) ·
[getlocalverified.com](https://getlocalverified.com/icar-gold-class-collision-repair/)

**Software install data:** [withorbital.com — Tekmetric](https://www.withorbital.com/data/software/tekmetric/) ·
[6sense.com — ShopMonkey share](https://6sense.com/tech/automobile-repair-and-maintenance-software/shopmonkey-market-share) ·
[enlyft.com — Dentrix share](https://enlyft.com/tech/products/dentrix) ·
[sacra.com — Shopmonkey](https://sacra.com/c/shopmonkey/)

**PE and consolidator trackers:** [beckersdental.com](https://www.beckersdental.com/dso-dpms/the-pe-firms-behind-15-dsos/) ·
[dealseam.com — dental](https://dealseam.com/dental-pe-rollup-tracker-2026) ·
[ctacquisitions.com — dental](https://ctacquisitions.com/dental-dso-pe-rollup-tracker-2026/) ·
[medixdental.com](https://medixdental.com/largest-dsos-in-the-us/) ·
[transitionselite.com — vet ownership map](https://transitionselite.com/veterinary-consolidator-ownership-map-2026/) ·
[ctacquisitions.com — veterinary](https://ctacquisitions.com/guides/private-equity-veterinary-2026/) ·
[dealseam.com — HVAC](https://dealseam.com/hvac-pe-rollup-tracker-2026) ·
[bodyshopbusiness.com](https://www.bodyshopbusiness.com/auto-body-consolidation-forecast-2026-ready-for-takeoff/)

**Dental practice data:** [ada.org — practice modalities](https://www.ada.org/resources/research/health-policy-institute/dental-practice-research/practice-modalities-among-us-dentists) ·
[adanews.ada.org — DSO affiliation](https://adanews.ada.org/ada-news/2023/june/more-dentists-affiliating-with-dsos/)

**Not verified:** whether 6sense or Orbital actually cover Boulevard, Zenoti and the veterinary PIMS
platforms — I confirmed auto repair and dental coverage only, so **quote and test before committing.**
Also unverified: state-by-state bulk license availability beyond Texas, New Jersey and Indiana; HIPAA
implications; and the manual-labour cost per qualified prospect, which is the number most likely to
break the unit economics.
