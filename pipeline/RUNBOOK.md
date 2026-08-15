# Runbook — LA (Redondo) + Atlanta pull

**Configured 2026-08-07 from Aaron's answers.** Jameson runs stages 1–3 on a machine with network;
hand the output back and stages 4–5 (scoring + call sheets) get run against it.

## What was decided

| Question | Answer |
|---|---|
| Location bands | **Split** — auto repair + collision **1–3** (owner-operator); med spa **3–8**, plumbing + HVAC **2–8** |
| Volume | **25 per vertical TOTAL** across both metros = **125 records** |
| Split of work | **Jameson runs 1–3**, hands back JSONL, scoring runs here |
| Geo anchoring | **HQ / primary location only** — a group is kept only if its *primary* site is in radius |

**Primary location** = the site with the most reviews in the cluster. One row per group goes downstream,
carrying `location_count` and `branch_addresses`, so stage 2 fetches one website per group rather than
one per branch.

## Radius — read this before running

A straight-line radius from Redondo Beach reaches further than it feels:

| From Redondo Beach | Distance |
|---|---|
| Manhattan Beach, Torrance | ~3 mi |
| El Segundo, LAX | 5–7 mi |
| Long Beach, Santa Monica | 12–13 mi |
| **Downtown LA** | **16.3 mi** |
| **Pasadena** | **24.9 mi** |
| Santa Clarita | 38.5 mi |

**Currently set to 25 miles**, which reaches Pasadena. If "as close as possible to Redondo" means tight
South Bay, **change `radius_miles` to 15** in `config.yaml` — that holds it to Manhattan Beach through
Long Beach and Santa Monica.

Output is sorted nearest-first regardless, so you can cut the list wherever you like after seeing it.
Note these are crow-flies miles; 25 miles in LA can be a 60–90 minute drive. Irrelevant for phone
sales, relevant if anyone plans site visits.

Atlanta is set to 30 miles, which covers the perimeter and inner suburbs.

## Run it

```bash
cd pipeline
pip install -r requirements.txt

# 0. free, no keys — prove the logic before spending anything
python 02_signals.py --selftest
python 04_score.py   --selftest

export OUTSCRAPER_API_KEY=...

# 1. universe — one file per vertical. Both metros are queried inside each run.
for v in auto_repair collision med_spa plumbing hvac; do
  python 01_universe.py --vertical $v --out out/universe_$v.jsonl
done
cat out/universe_*.jsonl > out/universe.jsonl
wc -l out/universe.jsonl

# 2. website signals — no key needed, run this widest
python 02_signals.py --in out/universe.jsonl --out out/signals.jsonl

# 3. line type — THE mandatory filter
export TWILIO_ACCOUNT_SID=...  TWILIO_AUTH_TOKEN=...
python 03_linetype.py --in out/signals.jsonl --out out/lines.jsonl
#    ^ this prints the MEASURED mobile rate. Report that number — it replaces
#      every vendor estimate in prospecting/11 §2.
```

**Then hand back `out/lines.jsonl`** (commit it to a branch, or attach it). Stages 4–5 run against it
and produce the ranked 25-per-vertical list with call sheets.

If you'd rather finish it yourself:

```bash
python 04_score.py      --in out/lines.jsonl  --out out/scored.jsonl     --top 25
python 05_callsheets.py --in out/scored.jsonl --out out/callsheets.md    --top 25
```

## Expected shape of the funnel

Rough, and worth recording against actuals:

```
  raw Maps results        several thousand across 5 verticals x 2 metros
    -> dedupe             place_id then phone
    -> cluster            brand + domain + phone -> location_count
    -> HQ anchoring       ONE row per group, primary must be in radius
    -> brand exclusions   Caliber, Gerber, Midas, Roto-Rooter, LaserAway, etc.
    -> review floor       25-40 depending on vertical
    -> location band      1-3 or 2-8 or 3-8 per vertical
    -> website required
  = the universe that reaches stage 2
    -> mobile-line gate   expect heavy attrition here. THIS IS THE POINT
  = scored, ranked, top 25 per vertical
```

**Expect the multi-location bands to be thin.** Independent 3–8 location med spa groups are genuinely
uncommon — 81% of med spas are single-location. If med spa comes back with fewer than 25 groups,
that's the market, not a bug. Report the count rather than loosening the band to fill a quota.

## Before any of it reaches a dialler

- [ ] **DNC scrub — national + state.** Not built into the pipeline; I had no DNC access. The mobile
      filter deliberately finds sole-proprietor personal cells, which are the highest-converting *and*
      highest-exposure numbers. See `prospecting/11-contact-data-stack.md` §1.
- [ ] **Manual dial only.** TCPA applies to mobiles even in B2B.
- [ ] **No SMS until a written opt-in is captured.** A verbal "sure, text me" is not consent.

## Things to report back

1. **Measured mobile rate** from stage 3
2. **Row counts at each funnel stage** — where the attrition actually happens
3. **Any vertical that returns under 25** after filtering, and at what band
4. **Whether Outscraper's field names matched** `01_universe.py` — I wrote it from their published
   client but could not reach their docs from the build environment
5. **Your hours.** Tooling is under $200; labour is what breaches the $50-per-qualified-prospect line
