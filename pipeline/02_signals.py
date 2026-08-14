#!/usr/bin/env python3
"""
Stage 2 — website signal detection.

Fetches each prospect's site and detects the pain signals that are visible in the
DOM. This is the one stage with NO third-party dependency: pure HTTP plus parsing,
so it costs nothing per record and nothing here needs an API key.

Signals detected (all mapped to the matrix in prospecting/01-pain-signal-matrix-and-icp.md):

  no_chat_widget        B1  intake form present but no chat -> form fills die in an inbox
  has_intake_form       B1  their funnel depends on someone answering
  booking_platform      B2  Boulevard = the wedge; Zenoti = deprioritise
  no_ssl                B2  browser warning is costing them traffic today
  stale_copyright       B2  nobody is maintaining the site
  diy_builder           B2  outgrew the platform
  not_mobile_ready      B2  most local search is mobile
  no_marketing_footprint B2 nobody is working the customer base
  claims_247            B1  a promise to verify against an off-hours call
  volume_claim          B2  self-reported customer count -> reactivation math input

Usage:
    python 02_signals.py --in out/universe.jsonl --out out/signals.jsonl
    python 02_signals.py --selftest        # runs offline against fixtures, no network
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

UA = "Mozilla/5.0 (compatible; LeepAI-prospect-research/1.0)"
TIMEOUT = 15

# --- detection tables -------------------------------------------------------
# Substring signatures. Kept as plain lowercase substrings rather than regex so a
# non-engineer can add a vendor without breaking the file.

CHAT_WIDGETS = [
    "tawk.to", "intercom", "drift.com", "livechatinc", "zendesk", "crisp.chat",
    "tidio", "hubspot-messages", "podium", "birdeye", "gohighlevel", "leadconnector",
    "smartsupp", "olark", "freshchat", "chatway", "elfsight-chat", "manychat",
]

BOOKING_PLATFORMS = {
    # med spa — the Boulevard/Zenoti distinction is the wedge (doc 01 §1.6)
    "boulevard": ["joinblvd", "blvd.co", "getboulevard"],
    "zenoti":    ["zenoti"],
    "mangomint": ["mangomint"],
    "vagaro":    ["vagaro"],
    "aesthetic_record": ["aestheticrecord"],
    # home services / auto — install implies a database exists
    "servicetitan": ["servicetitan"],
    "housecallpro": ["housecallpro", "housecall.pro"],
    "jobber":      ["getjobber", "jobber.com"],
    "shopmonkey":  ["shopmonkey"],
    "tekmetric":   ["tekmetric"],
    "shopware":    ["shop-ware", "shopware.com"],
    "mitchell1":   ["mitchell1", "mitchellone"],
}

DIY_BUILDERS = {
    "wix": ["wix.com", "wixstatic", "parastorage"],
    "squarespace": ["squarespace", "sqspcdn"],
    "godaddy": ["godaddy", "wsimg.com"],
    "weebly": ["weebly"],
    "duda": ["dudaone", "multiscreensite"],
}

MARKETING_FOOTPRINT = [
    "mailchimp", "klaviyo", "constantcontact", "activecampaign", "hubspot",
    "convertkit", "sendinblue", "brevo", "newsletter", "subscribe to our",
    "join our mailing list", "email list",
]

FORM_HINTS = [
    "<form", "request a quote", "request an estimate", "get a quote",
    "schedule service", "book now", "book an appointment", "contact us today",
    "free estimate", "request appointment",
]

CLAIM_247 = [
    "24/7", "24 hours", "24-hour", "around the clock", "anytime day or night",
    "emergency service available", "always open",
]

VOLUME_CLAIM_RE = re.compile(
    r"(?:over|more than|serving|trusted by|join)\s+"
    r"([0-9][0-9,]{2,})\s*\+?\s*"
    r"(?:happy\s+|satisfied\s+|local\s+)?"
    r"(?:customers|clients|patients|families|homeowners|vehicles|drivers|members)",
    re.I,
)

COPYRIGHT_RE = re.compile(r"(?:©|&copy;|copyright)[^0-9]{0,20}((?:19|20)\d{2})", re.I)
VIEWPORT_RE = re.compile(r'<meta[^>]+name=["\']viewport["\']', re.I)


def _find(haystack: str, needles) -> list[str]:
    return [n for n in needles if n in haystack]


def detect(html: str, final_url: str, *, this_year: int) -> dict:
    """Pure function: HTML in, signals out. No network. Unit-testable."""
    low = html.lower()
    out: dict = {}

    # --- chat / intake -----------------------------------------------------
    chat_hits = _find(low, CHAT_WIDGETS)
    out["chat_widget_vendors"] = chat_hits
    out["has_chat_widget"] = bool(chat_hits)

    form_hits = _find(low, FORM_HINTS)
    out["has_intake_form"] = bool(form_hits)
    out["intake_form_hints"] = form_hits[:5]

    # The signal is the PAIR: a form with no chat behind it. Doc 01 §1.3.
    out["form_without_chat"] = out["has_intake_form"] and not out["has_chat_widget"]

    # --- booking / incumbent software -------------------------------------
    platforms = [name for name, sigs in BOOKING_PLATFORMS.items() if _find(low, sigs)]
    out["booking_platforms"] = platforms
    out["on_boulevard"] = "boulevard" in platforms   # the wedge
    out["on_zenoti"] = "zenoti" in platforms         # deprioritise
    out["has_online_booking"] = bool(platforms)

    # --- website health ----------------------------------------------------
    out["no_ssl"] = urlparse(final_url).scheme != "https"

    years = [int(y) for y in COPYRIGHT_RE.findall(html)]
    out["copyright_year"] = max(years) if years else None
    out["stale_copyright"] = bool(years) and (this_year - max(years)) >= 2

    builders = [name for name, sigs in DIY_BUILDERS.items() if _find(low, sigs)]
    out["diy_builder"] = builders[0] if builders else None

    out["not_mobile_ready"] = not bool(VIEWPORT_RE.search(html))

    # --- marketing / volume ------------------------------------------------
    mk = _find(low, MARKETING_FOOTPRINT)
    out["marketing_footprint"] = mk[:5]
    out["no_marketing_footprint"] = not bool(mk)

    out["claims_247"] = bool(_find(low, CLAIM_247))

    m = VOLUME_CLAIM_RE.search(html)
    if m:
        try:
            out["claimed_customer_count"] = int(m.group(1).replace(",", ""))
            out["volume_claim_text"] = m.group(0).strip()[:120]
        except ValueError:
            out["claimed_customer_count"] = None
    else:
        out["claimed_customer_count"] = None

    return out


def fetch_and_detect(rec: dict, this_year: int) -> dict:
    import requests  # imported here so --selftest works without the dep

    url = (rec.get("site") or "").strip()
    rec = dict(rec)
    if not url:
        rec["signals"] = {"error": "no_website"}
        rec["disqualified"] = "no_website"   # doc 01 §4.1 — DQ unless revenue proof exists
        return rec
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": UA}, allow_redirects=True)
        rec["signals"] = detect(r.text, r.url, this_year=this_year)
        rec["signals"]["http_status"] = r.status_code
        rec["signals"]["final_url"] = r.url
    except Exception as e:                      # noqa: BLE001 — log and continue
        rec["signals"] = {"error": type(e).__name__, "detail": str(e)[:200]}
    return rec


# --- offline self-test ------------------------------------------------------

FIXTURES = [
    (
        "form, no chat, stale copyright, wix, http, no viewport",
        "http://x.test",
        """<html><head><title>Bob's Auto</title></head><body>
           <form action="/quote">Request a Quote</form>
           <script src="//static.parastorage.com/wix.js"></script>
           <footer>&copy; 2021 Bob's Auto Repair</footer></body></html>""",
        {"form_without_chat": True, "stale_copyright": True, "diy_builder": "wix",
         "no_ssl": True, "not_mobile_ready": True, "no_marketing_footprint": True},
    ),
    (
        "boulevard med spa, chat present, volume claim, 24/7",
        "https://y.test",
        """<html><head><meta name="viewport" content="width=device-width"></head><body>
           <script src="https://cdn.joinblvd.com/booking.js"></script>
           <script src="https://embed.tawk.to/abc"></script>
           <p>Trusted by over 4,200 happy patients</p>
           <p>Open 24/7 for emergencies</p>
           <a href="#">Join our mailing list</a>
           <footer>© 2026 Glow Med Spa</footer></body></html>""",
        {"on_boulevard": True, "has_chat_widget": True, "claimed_customer_count": 4200,
         "claims_247": True, "no_marketing_footprint": False, "stale_copyright": False,
         "no_ssl": False, "not_mobile_ready": False},
    ),
    (
        "zenoti — should be flagged for deprioritisation",
        "https://z.test",
        """<html><head><meta name="viewport" content="w"></head><body>
           <script src="https://zenoti.com/w.js"></script>
           <footer>© 2026</footer></body></html>""",
        {"on_zenoti": True, "on_boulevard": False, "has_online_booking": True},
    ),
]


def selftest() -> int:
    year = 2026
    failures = 0
    for name, url, html, expect in FIXTURES:
        got = detect(html, url, this_year=year)
        bad = {k: (v, got.get(k)) for k, v in expect.items() if got.get(k) != v}
        if bad:
            failures += 1
            print(f"FAIL  {name}")
            for k, (want, actual) in bad.items():
                print(f"        {k}: expected {want!r}, got {actual!r}")
        else:
            print(f"ok    {name}")
    print()
    print("SELFTEST PASSED" if not failures else f"{failures} FIXTURE(S) FAILED")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out", dest="out")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not a.inp or not a.out:
        ap.error("--in and --out are required unless --selftest")

    year = datetime.now(timezone.utc).year
    records = [json.loads(l) for l in Path(a.inp).read_text().splitlines() if l.strip()]
    print(f"{len(records)} records -> fetching with {a.workers} workers")

    done = 0
    with Path(a.out).open("w") as fh, ThreadPoolExecutor(max_workers=a.workers) as ex:
        futures = {ex.submit(fetch_and_detect, r, year): r for r in records}
        for fut in as_completed(futures):
            fh.write(json.dumps(fut.result()) + "\n")
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(records)}", file=sys.stderr)

    print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
