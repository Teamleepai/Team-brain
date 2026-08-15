#!/usr/bin/env python3
"""
Stage 3 — line type. Twilio Lookup v2.

THE MANDATORY FILTER. Generic business data connects at 8-12%; verified mobile
direct-dial connects at 18-22% (doc 03 §3.5). Selecting for mobile-reachable
owners is a structural 2x on the most expensive step in the funnel.

    export TWILIO_ACCOUNT_SID=... TWILIO_AUTH_TOKEN=...
    python 03_linetype.py --in out/signals.jsonl --out out/lines.jsonl

Endpoint: GET https://lookups.twilio.com/v2/PhoneNumbers/{e164}?Fields=line_type_intelligence
Returns lineTypeIntelligence.type in {mobile, landline, fixedVoip, nonFixedVoip, tollFree, ...}
Docs: https://www.twilio.com/docs/lookup/v2-api/line-type-intelligence

*** COMPLIANCE — doc 11 §1 ***
A mobile that a sole proprietor uses for business is treated as a RESIDENTIAL line
and IS on the DNC registry if they registered it. This stage finds the numbers that
convert best AND the numbers with the most exposure. DNC scrub is not optional, and
dialing must be manual — TCPA applies to mobiles even in B2B.
"""
from __future__ import annotations
import argparse, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth

BASE = "https://lookups.twilio.com/v2/PhoneNumbers/"


def e164(raw: str) -> str | None:
    d = re.sub(r"\D", "", raw or "")
    if len(d) == 10:
        return "+1" + d
    if len(d) == 11 and d.startswith("1"):
        return "+" + d
    return None


def lookup(rec: dict, auth) -> dict:
    rec = dict(rec)
    num = e164(rec.get("phone", ""))
    if not num:
        rec["line_type"] = None; rec["line_error"] = "unparseable_phone"; return rec
    try:
        r = requests.get(BASE + num, params={"Fields": "line_type_intelligence"},
                         auth=auth, timeout=20)
        if r.status_code == 404:
            rec["line_type"] = None; rec["line_error"] = "not_found"; return rec
        r.raise_for_status()
        lti = (r.json() or {}).get("lineTypeIntelligence") or {}
        rec["line_type"] = lti.get("type")
        rec["carrier"] = lti.get("carrier_name")
        rec["phone_e164"] = num
    except Exception as e:                                  # noqa: BLE001
        rec["line_type"] = None; rec["line_error"] = f"{type(e).__name__}: {str(e)[:120]}"
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    sid, tok = os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN")
    if not (sid and tok):
        print("ERROR: set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN", file=sys.stderr); return 2
    auth = HTTPBasicAuth(sid, tok)

    recs = [json.loads(l) for l in Path(a.inp).read_text().splitlines() if l.strip()]
    print(f"{len(recs)} lookups")

    counts: dict[str, int] = {}
    with Path(a.out).open("w") as fh, ThreadPoolExecutor(max_workers=a.workers) as ex:
        for fut in as_completed([ex.submit(lookup, r, auth) for r in recs]):
            r = fut.result()
            counts[str(r.get("line_type"))] = counts.get(str(r.get("line_type")), 0) + 1
            fh.write(json.dumps(r) + "\n")

    print(f"wrote {a.out}")
    for k, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {n:5}  {k}")
    mob = counts.get("mobile", 0)
    if recs:
        print(f"\nmobile rate: {mob/len(recs):.1%}  <-- these are the high-connect targets")
    return 0


if __name__ == "__main__":
    sys.exit(main())
