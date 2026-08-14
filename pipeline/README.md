# Prospect pipeline

Produces a scored, ranked, call-ready prospect list for the five verticals in scope.

**Why this exists:** the session that wrote it had **all external network egress blocked** —
`example.com`, Google Maps and Yelp all returned `000`, and WebFetch on the I-CAR directory and
California BAR returned `EGRESS_BLOCKED` from the proxy. No scraping was possible. Rather than
hand over a list of real businesses with invented pain signals — the exact failure mode warned
against in `prospecting/02`, `08` and `11` — this is the machinery that produces the real list.
**Run it and you have the list in a few hours.**

---

## Before you run anything

### 1. Fill in the geography — nothing works without it

`config.yaml` → `geography.markets`. **This is the one input that cannot be guessed.** A list of
Boise auto shops is worthless if you sell in Denver. Stage 1 exits with an error if it's empty.

### 2. Understand what "$300k+ revenue" can and cannot mean

**Revenue for private SMBs is not public and cannot be scraped.** What the pipeline uses instead:

| Vertical | Industry average revenue | Is a $300K floor binding? |
|---|---|---|
| Auto repair | $450K–1.2M (sources conflict, doc `07` §2.1) | **No — excludes almost nobody** |
| Collision | ~$1.2M per facility | **No** |
| Plumbing | ~$1.28M per business | **No** — and a 2+ location plumber is far above it |
| HVAC | ~$750K–1.5M at 5 employees | **No** |

At $300K the floor is nearly non-binding in every vertical here. The filters that actually
discriminate are **review volume, location count, bay count, and paid-ads presence**.

### 3. API keys

| Stage | Needs | Notes |
|---|---|---|
| 1 · universe | `OUTSCRAPER_API_KEY` | ~$3/1K records. Apify is the alternative at ~$1.50/1K base |
| 2 · signals | **nothing** | Pure HTTP + parsing. Free, and the highest-value stage |
| 3 · line type | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN` | The mandatory mobile filter |
| 4 · score | nothing | |
| 5 · call sheets | nothing | |

```bash
pip install -r requirements.txt
export OUTSCRAPER_API_KEY=...
export TWILIO_ACCOUNT_SID=...  TWILIO_AUTH_TOKEN=...
```

---

## Run order

```bash
# 0. prove the logic works before spending any money — no network needed
python 02_signals.py --selftest
python 04_score.py   --selftest

# 1. universe, per vertical
for v in auto_repair collision med_spa plumbing hvac; do
  python 01_universe.py --vertical $v --out out/universe_$v.jsonl
done
cat out/universe_*.jsonl > out/universe.jsonl

# 2. website signals — free, no key
python 02_signals.py --in out/universe.jsonl --out out/signals.jsonl

# 3. line type — the mandatory mobile filter
python 03_linetype.py --in out/signals.jsonl --out out/lines.jsonl

# 4. score, multiplicatively
python 04_score.py --in out/lines.jsonl --out out/scored.jsonl --top 25

# 5. call sheets for Grace and Javid
python 05_callsheets.py --in out/scored.jsonl --out out/callsheets.md --top 25
```

`04` and `05` were verified end-to-end against 40 synthetic Outscraper-shaped records.
`02` and `04` carry offline self-tests that pass.

---

## The scoring model

**Multiplicative, not additive:** `score = pain × pay × reach × 1000`.

Doc `01` §9.1 — summing pain signals floats badly-run, insolvent businesses to the top, because
pain volume and solvency aren't correlated. A shop with no website, no SEO and bad reviews may
simply be broke. **Any axis near zero must zero the prospect**, and only multiplication does that.

Hard gates that drop a record regardless of score:

- **Not a mobile line** — the single biggest connect-rate lever (8–12% → 18–22%)
- Ability-to-pay below threshold
- Unreachable
- **On Zenoti** — documented strong reporting, so less gap to sell into. Boulevard is the wedge

---

## What I could not verify from the build environment

Network egress was blocked, so these are from documentation and search results rather than a live call:

1. **Outscraper's exact endpoint and response field names.** `01_universe.py` reflects their
   published Python client as of Aug 2026. **Check it against current docs before the first paid
   run** — a wrong field name wastes a batch, not a day.
2. **Whether California BAR publishes a bulk download.** 34,483 licensed repair dealers and a
   searchable Auto Shop Locator are confirmed; a downloadable file is not. **Call and ask.**
3. **Twilio Lookup per-lookup pricing.** The endpoint and response shape are documented; the rate
   card wasn't in reach. Budget before running 5,000.
4. **Real mobile hit rate on your lists.** Every figure in `prospecting/11` §2 is vendor-reported.
   Stage 3 prints the measured rate — that's your real number, and it replaces the estimate.
5. **Bay-count estimation accuracy.** Not implemented here; it needs Maps photos and Street View
   and is a manual pass. It's the affordability qualifier for the top vertical, so **measure the
   error rate against 20 hand-checked shops.**

---

## Compliance — read `prospecting/11-contact-data-stack.md` §1 first

The mobile filter finds the numbers that convert best **and** the numbers with the most exposure.
A mobile a sole proprietor uses for business is treated as a **residential line** and **is on the
DNC registry if they registered it**. FTC enforcement treats micro-businesses blurring the
consumer/commercial line **as consumers**.

- **DNC scrub — national + state — before any dialling.** Not optional
- **Manual dial only.** TCPA applies to mobiles even in B2B; a power dialer needs express consent
- **No SMS until written opt-in.** A verbal "sure, text me" is not valid consent
- Call sheets carry an unticked DNC checkbox by design

The pipeline does **not** perform the scrub — no DNC access from here. Wire it in before stage 5
output reaches a dialler.

## And one thing about the output

Every signal is **machine-detected and unverified**. The call sheets carry a "verify before you say
it" block for exactly this reason. **A false signal is worse than a generic call** — it proves you
didn't actually look.
