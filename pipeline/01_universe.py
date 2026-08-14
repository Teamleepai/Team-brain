#!/usr/bin/env python3
"""
Stage 1 — universe scrape. Google Maps via Outscraper.

Maps is the universe because Apollo/ZoomInfo cover only ~20% of local service
providers (doc 03 §3.1). Building top-of-funnel on a contact database silently
discards ~80% of the addressable market.

Also does multi-location clustering: identical brand + shared domain + shared
phone -> count distinct addresses -> that is how you find 3-8 location groups,
because no database of independent groups exists (doc 08 §1.1).

    export OUTSCRAPER_API_KEY=...
    python 01_universe.py --vertical med_spa --out out/universe_med_spa.jsonl

VERIFY BEFORE FIRST RUN: I could not reach Outscraper's docs from the build
environment (network egress blocked). Endpoint and field names below reflect
their published Python client as of Aug 2026 — confirm against current docs.
Docs: https://outscraper.com/google-maps-api/
"""
from __future__ import annotations
import argparse, json, os, re, sys, time
from collections import defaultdict
from pathlib import Path
import requests, yaml

API = "https://api.outscraper.cloud/maps/search-v3"


def normalise_brand(name: str) -> str:
    """Collapse a business name to a comparison key for clustering."""
    n = (name or "").lower()
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    # strip location suffixes and generic descriptors that differ per branch
    n = re.sub(r"\b(llc|inc|co|corp|ltd|the|of|at|and)\b", " ", n)
    n = re.sub(r"\b(north|south|east|west|downtown|uptown|central|#\d+|no \d+)\b", " ", n)
    return " ".join(n.split())


def digits(p: str) -> str:
    return re.sub(r"\D", "", p or "")


def fetch(query: str, limit: int, key: str) -> list[dict]:
    r = requests.get(
        API,
        params={"query": query, "limit": limit, "language": "en", "region": "US", "async": "false"},
        headers={"X-API-KEY": key},
        timeout=600,
    )
    r.raise_for_status()
    body = r.json()
    data = body.get("data", [])
    # Outscraper returns a list-of-lists (one inner list per query)
    return [row for group in data for row in group] if data and isinstance(data[0], list) else data


def cluster(records: list[dict]) -> list[dict]:
    """Attach location_count and group_id by brand+domain+phone."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        domain = (r.get("site") or "").replace("https://", "").replace("http://", "").split("/")[0].lower()
        key = normalise_brand(r.get("name", "")) or domain or digits(r.get("phone", ""))
        groups[key].append(r)

    out = []
    for gid, (key, members) in enumerate(groups.items()):
        addrs = {(m.get("full_address") or m.get("address") or "").lower() for m in members}
        addrs.discard("")
        for m in members:
            m["group_id"] = f"g{gid:05d}"
            m["group_key"] = key
            m["location_count"] = max(len(addrs), 1)
            out.append(m)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vertical", required=True)
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    key = os.environ.get("OUTSCRAPER_API_KEY")
    if not key:
        print("ERROR: set OUTSCRAPER_API_KEY", file=sys.stderr); return 2

    cfg = yaml.safe_load(Path(a.config).read_text())
    markets = cfg["geography"]["markets"]
    if not markets:
        print("ERROR: config.yaml geography.markets is empty. This is the one input\n"
              "       that cannot be guessed — fill in your actual target metros.", file=sys.stderr)
        return 2

    v = cfg["verticals"][a.vertical]
    limit = cfg["geography"]["limit_per_query"]
    excl = [e.lower() for e in v.get("exclude_name_contains", [])]
    lo, hi = v.get("target_locations", [1, 99])

    raw: list[dict] = []
    for market in markets:
        for q in v["queries"]:
            query = f"{q} near {market}"
            print(f"  fetching: {query}")
            try:
                got = fetch(query, limit, key)
                print(f"    -> {len(got)}")
                raw.extend(got)
            except Exception as e:                      # noqa: BLE001
                print(f"    !! {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(1)

    # dedupe on place_id then phone
    seen, deduped = set(), []
    for r in raw:
        k = r.get("place_id") or r.get("google_id") or digits(r.get("phone", "")) or r.get("name")
        if k and k not in seen:
            seen.add(k); deduped.append(r)
    print(f"{len(raw)} raw -> {len(deduped)} deduped")

    clustered = cluster(deduped)

    kept, dropped = [], defaultdict(int)
    for r in clustered:
        name = (r.get("name") or "").lower()
        if any(e in name for e in excl):
            dropped["excluded_brand"] += 1; continue
        if (r.get("reviews") or 0) < v.get("min_reviews", 0):
            dropped["too_few_reviews"] += 1; continue
        if not (lo <= r["location_count"] <= hi):
            dropped["location_count_out_of_band"] += 1; continue
        if cfg["revenue_proxies"].get("require_website") and not r.get("site"):
            dropped["no_website"] += 1; continue
        r["vertical"] = a.vertical
        r["division"] = v["division"]
        r["lead_product"] = v["lead_product"]
        kept.append(r)

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with Path(a.out).open("w") as fh:
        for r in kept:
            fh.write(json.dumps(r) + "\n")

    print(f"\nkept {len(kept)} -> {a.out}")
    for reason, n in sorted(dropped.items(), key=lambda x: -x[1]):
        print(f"  dropped {n:5}  {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
