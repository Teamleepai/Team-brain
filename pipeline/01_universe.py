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


def haversine_mi(lat1, lon1, lat2, lon2) -> float | None:
    """Great-circle distance in miles. None if any coordinate is missing."""
    try:
        from math import radians, sin, cos, asin, sqrt
        lat1, lon1, lat2, lon2 = map(float, (lat1, lon1, lat2, lon2))
    except (TypeError, ValueError):
        return None
    dlat, dlon = radians(lat2 - lat1), radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 3958.7613 * 2 * asin(sqrt(a))


def primary_of(members: list[dict]) -> dict:
    """The cluster's HQ / flagship = the location with the most reviews.

    Aaron chose HQ-only anchoring (2026-08-07): a group is kept only if THIS
    location falls inside the radius, not merely any of its sites.
    """
    return max(members, key=lambda m: (m.get("reviews") or 0))


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
        hq = primary_of(members)
        for m in members:
            m["group_id"] = f"g{gid:05d}"
            m["group_key"] = key
            m["location_count"] = max(len(addrs), 1)
            m["is_primary"] = (m is hq)
            m["hq_name"] = hq.get("name")
            m["hq_address"] = hq.get("full_address") or hq.get("address")
            out.append(m)
    return out


def anchor_filter(records: list[dict], anchors: list[dict]) -> tuple[list[dict], int]:
    """HQ-only anchoring: keep a group iff its PRIMARY location is inside a radius.

    Returns (kept_primaries, dropped_count). One row per group — the HQ row —
    carrying location_count, so downstream stages fetch one site per group
    rather than one per branch.
    """
    by_group: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        by_group[r["group_id"]].append(r)

    kept, dropped = [], 0
    for members in by_group.values():
        hq = next((m for m in members if m.get("is_primary")), members[0])
        best_d, best_anchor = None, None
        for a in anchors:
            d = haversine_mi(hq.get("latitude"), hq.get("longitude"), a["lat"], a["lon"])
            if d is not None and (best_d is None or d < best_d):
                best_d, best_anchor = d, a
        if best_d is None:
            dropped += 1                      # no coordinates -> cannot anchor
            continue
        if best_d > best_anchor["radius_miles"]:
            dropped += 1
            continue
        hq["anchor"] = best_anchor["name"]
        hq["distance_mi"] = round(best_d, 1)
        hq["branch_addresses"] = [
            m.get("full_address") or m.get("address") for m in members if not m.get("is_primary")
        ]
        kept.append(hq)
    return kept, dropped


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
    anchors = cfg["geography"]["anchors"]
    if not anchors:
        print("ERROR: config.yaml geography.anchors is empty.", file=sys.stderr)
        return 2

    v = cfg["verticals"][a.vertical]
    limit = cfg["geography"]["limit_per_query"]
    excl = [e.lower() for e in v.get("exclude_name_contains", [])]
    lo, hi = v.get("target_locations", [1, 99])

    raw: list[dict] = []
    for anchor in anchors:
        for q in v["queries"]:
            query = f"{q} near {anchor['query_area']}"
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

    # HQ-only anchoring — one row per group, the primary location
    anchored, out_of_radius = anchor_filter(clustered, anchors)
    print(f"{len(clustered)} locations -> {len(anchored)} groups with HQ in radius "
          f"({out_of_radius} groups dropped: outside radius or no coordinates)")

    kept, dropped = [], defaultdict(int)
    for r in anchored:
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

    kept.sort(key=lambda r: r.get("distance_mi", 9e9))   # closest to anchor first

    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with Path(a.out).open("w") as fh:
        for r in kept:
            fh.write(json.dumps(r) + "\n")

    print(f"\nkept {len(kept)} groups -> {a.out}")
    for reason, n in sorted(dropped.items(), key=lambda x: -x[1]):
        print(f"  dropped {n:5}  {reason}")
    by_anchor: dict[str, int] = defaultdict(int)
    for r in kept:
        by_anchor[r.get("anchor", "?")] += 1
    for k, n in by_anchor.items():
        print(f"  {n:5} in {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
