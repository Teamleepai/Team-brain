#!/usr/bin/env python3
"""
Stage 4 — scoring.

MULTIPLICATIVE: Pain x AbilityToPay x Reachability.

Not additive. Doc 01 §2 and §9.1: summing pain signals floats badly-run, insolvent
businesses to the top, because pain volume and solvency are not correlated. A company
with no website, no SEO, an IVR and bad reviews may simply be broke. Any factor near
zero must zero the prospect.

    python 04_score.py --in out/lines.jsonl --out out/scored.jsonl --top 25
    python 04_score.py --selftest
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

# --- pain, per vertical -----------------------------------------------------
# Each entry: (signal_key, weight, human explanation used on the call sheet)

PAIN_RULES = {
    "auto_repair": [
        ("mobile_line",            0.20, "Main line is a mobile — the owner is the service writer"),
        ("form_without_chat",      0.15, "Intake form with nothing behind it"),
        ("no_online_booking",      0.15, "4+ bays of capacity, entirely phone-dependent intake"),
        ("high_review_volume",     0.20, "Review volume implies real call volume"),
        ("claims_247",             0.10, "Advertises 24/7 — verify with an off-hours call"),
        ("no_marketing_footprint", 0.10, "Nobody is working the customer base"),
        ("website_neglect",        0.10, "Site is unmaintained"),
    ],
    "collision": [
        ("no_online_booking",      0.15, "No estimate-request path"),
        ("form_without_chat",      0.20, "Estimate form with slow follow-up"),
        ("website_neglect",        0.20, "No agency footprint — no incumbent to displace"),
        ("no_marketing_footprint", 0.25, "Never had to market; DRP sent the work"),
        ("high_review_volume",     0.20, "Established shop with real throughput"),
    ],
    "med_spa": [
        ("on_boulevard",           0.30, "Boulevard: documented weak campaign attribution + LTV reporting"),
        ("dormant_base",           0.25, "Review count far exceeds recent velocity — a dormant patient base"),
        ("no_marketing_footprint", 0.25, "Nobody is working the recall list"),
        ("volume_claim",           0.10, "Self-reported patient count = the reactivation math input"),
        ("multi_location",         0.10, "3-8 locations: one integration, many locations of revenue"),
    ],
    "plumbing": [
        ("mobile_line",            0.15, "Owner-reachable"),
        ("claims_247",             0.25, "Advertises 24/7 — emergency calls carry $150-250 surcharges"),
        ("no_online_booking",      0.15, "Phone-dependent intake"),
        ("high_review_volume",     0.20, "Real call volume"),
        ("multi_location",         0.15, "2+ locations — well above the revenue floor"),
        ("no_marketing_footprint", 0.10, "Base untouched"),
    ],
    "hvac": [
        ("mobile_line",            0.15, "Owner-reachable"),
        ("high_review_volume",     0.25, "Real call volume; $350 per missed call"),
        ("no_online_booking",      0.15, "Phone-dependent intake"),
        ("claims_247",             0.15, "Advertises 24/7"),
        ("multi_location",         0.15, "2+ locations"),
        ("no_marketing_footprint", 0.15, "Base untouched"),
    ],
}

# --- ability to pay ---------------------------------------------------------
# Deliberately non-Google where possible (doc 01 §2.1). Revenue itself is NOT
# scrapeable for private SMBs — these are proxies and are labelled as such.
PAY_RULES = [
    ("high_review_volume", 0.30, "Review volume as a throughput proxy"),
    ("multi_location",     0.30, "Location count"),
    ("has_website",        0.15, "Has a real website at all"),
    ("has_online_booking", 0.15, "Pays for booking software — spends on tooling"),
    ("not_diy_builder",    0.10, "Not on a free site builder"),
]

# --- reachability -----------------------------------------------------------
REACH_RULES = [
    ("mobile_line",       0.45, "Mobile direct-dial: 18-22% connect vs 8-12% generic"),
    ("owner_named",       0.25, "Owner identified by name"),
    ("small_footprint",   0.20, "Below the ~100-employee committee threshold"),
    ("not_excluded_brand",0.10, "Not a consolidator or franchise"),
]


def derive(rec: dict) -> dict:
    """Turn raw record + signals into the boolean facts the rules reference."""
    s = rec.get("signals") or {}
    reviews = rec.get("reviews") or 0
    rating = rec.get("rating") or 0
    locs = rec.get("location_count") or 1

    # Dormant base: lots of lifetime reviews but little recent activity.
    # reviews_per_score is an Outscraper field; absent it we fall back to volume.
    recent = rec.get("reviews_last_12mo")
    dormant = bool(recent is not None and reviews >= 100 and recent < reviews * 0.12)

    return {
        "mobile_line":           rec.get("line_type") == "mobile",
        "has_website":           bool(rec.get("site")),
        "form_without_chat":     bool(s.get("form_without_chat")),
        "no_online_booking":     not bool(s.get("has_online_booking")),
        "has_online_booking":    bool(s.get("has_online_booking")),
        "on_boulevard":          bool(s.get("on_boulevard")),
        "on_zenoti":             bool(s.get("on_zenoti")),
        "claims_247":            bool(s.get("claims_247")),
        "no_marketing_footprint": bool(s.get("no_marketing_footprint")),
        "website_neglect":       bool(s.get("stale_copyright") or s.get("no_ssl")
                                      or s.get("not_mobile_ready")),
        "not_diy_builder":       not bool(s.get("diy_builder")),
        "volume_claim":          bool(s.get("claimed_customer_count")),
        "high_review_volume":    reviews >= 75,
        "multi_location":        locs >= 2,
        "dormant_base":          dormant,
        "owner_named":           bool(rec.get("owner_name")),
        "small_footprint":       locs <= 8,
        "not_excluded_brand":    True,   # excluded brands are dropped in stage 1
        "rating_slipping":       bool(rating and rating < 4.3 and reviews >= 50),
    }


def apply(rules, facts) -> tuple[float, list[str]]:
    score, why = 0.0, []
    for key, weight, explain in rules:
        if facts.get(key):
            score += weight
            why.append(explain)
    return min(score, 1.0), why


def score_one(rec: dict, cfg: dict) -> dict:
    facts = derive(rec)
    vertical = rec.get("vertical", "auto_repair")
    pain, pain_why = apply(PAIN_RULES.get(vertical, PAIN_RULES["auto_repair"]), facts)
    pay,  pay_why  = apply(PAY_RULES, facts)
    reach, reach_why = apply(REACH_RULES, facts)

    sc = cfg["scoring"]
    rec = dict(rec)
    rec["facts"] = facts
    rec["pain"], rec["pay"], rec["reach"] = round(pain, 3), round(pay, 3), round(reach, 3)
    rec["why"] = {"pain": pain_why, "pay": pay_why, "reach": reach_why}

    drop = None
    if sc.get("require_mobile_line") and not facts["mobile_line"]:
        drop = "not_a_mobile_line"
    elif pay < sc.get("drop_if_pay_below", 0):
        drop = "ability_to_pay_too_low"
    elif reach < sc.get("drop_if_reach_below", 0):
        drop = "unreachable"
    elif facts["on_zenoti"]:
        drop = "zenoti_deprioritise"

    rec["dropped"] = drop
    # MULTIPLICATIVE — this is the whole point
    rec["score"] = 0.0 if drop else round(pain * pay * reach * 1000, 1)
    return rec


# --- selftest ---------------------------------------------------------------

def selftest() -> int:
    cfg = {"scoring": {"require_mobile_line": True, "drop_if_pay_below": 0.15,
                       "drop_if_reach_below": 0.15}}
    fails = 0

    def chk(label, cond):
        nonlocal fails
        print(("ok    " if cond else "FAIL  ") + label)
        if not cond:
            fails += 1

    strong = {"vertical": "auto_repair", "line_type": "mobile", "site": "https://a.test",
              "reviews": 200, "rating": 4.1, "location_count": 1, "owner_name": "Bob",
              "signals": {"form_without_chat": True, "has_online_booking": False,
                          "claims_247": True, "no_marketing_footprint": True,
                          "stale_copyright": True}}
    weak_pay = {"vertical": "auto_repair", "line_type": "mobile", "site": "",
                "reviews": 3, "location_count": 1,
                "signals": {"diy_builder": "wix", "form_without_chat": True}}
    landline = dict(strong); landline["line_type"] = "landline"
    zen = {"vertical": "med_spa", "line_type": "mobile", "site": "https://z.test",
           "reviews": 300, "location_count": 4,
           "signals": {"on_zenoti": True, "has_online_booking": True}}

    a, b, c, d = (score_one(x, cfg) for x in (strong, weak_pay, landline, zen))

    chk("strong prospect scores > 0", a["score"] > 0)
    chk("strong prospect not dropped", a["dropped"] is None)
    chk("low ability-to-pay is dropped", b["dropped"] == "ability_to_pay_too_low")
    chk("landline is dropped (mobile filter)", c["dropped"] == "not_a_mobile_line")
    chk("zenoti is deprioritised", d["dropped"] == "zenoti_deprioritise")
    chk("dropped records score 0", all(x["score"] == 0 for x in (b, c, d)))

    # the formula itself is multiplicative, not additive
    expected = round(a["pain"] * a["pay"] * a["reach"] * 1000, 1)
    chk(f"score == pain*pay*reach*1000 ({a['score']} == {expected})", a["score"] == expected)
    chk("score is NOT the sum of axes",
        abs(a["score"] - (a["pain"] + a["pay"] + a["reach"]) * 1000) > 1)

    # a genuinely weaker ability-to-pay produces a lower score
    thin = dict(strong); thin["reviews"] = 40          # below the 75 volume threshold
    lo = score_one(thin, cfg)
    chk(f"weaker ability-to-pay scores lower ({lo['score']} < {a['score']})",
        0 < lo["score"] < a["score"])
    chk("explanations are attached", bool(a["why"]["pain"]))

    print()
    print("SELFTEST PASSED" if not fails else f"{fails} CHECK(S) FAILED")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out", dest="out")
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not a.inp or not a.out:
        ap.error("--in and --out required unless --selftest")

    cfg = yaml.safe_load(Path(a.config).read_text())
    recs = [json.loads(l) for l in Path(a.inp).read_text().splitlines() if l.strip()]
    scored = sorted((score_one(r, cfg) for r in recs), key=lambda r: -r["score"])

    with Path(a.out).open("w") as fh:
        for r in scored:
            fh.write(json.dumps(r) + "\n")

    kept = [r for r in scored if not r["dropped"]]
    print(f"{len(recs)} scored -> {len(kept)} survive the gates -> {a.out}")

    reasons: dict[str, int] = {}
    for r in scored:
        if r["dropped"]:
            reasons[r["dropped"]] = reasons.get(r["dropped"], 0) + 1
    for k, n in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"  dropped {n:5}  {k}")

    print(f"\nTOP {a.top}:")
    print(f"  {'#':>3} {'score':>6} {'pain':>5} {'pay':>5} {'reach':>6}  name")
    for i, r in enumerate(kept[: a.top], 1):
        print(f"  {i:3} {r['score']:6.1f} {r['pain']:5.2f} {r['pay']:5.2f} "
              f"{r['reach']:6.2f}  {(r.get('name') or '')[:48]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
