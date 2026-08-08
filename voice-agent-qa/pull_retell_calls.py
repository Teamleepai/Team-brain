#!/usr/bin/env python3
"""
Pull the last N calls for a Retell agent and compute the hard, non-negotiable metrics.

Usage:
    export RETELL_API_KEY=key_xxxxx
    python3 pull_retell_calls.py --agent "Mia" --limit 40
    python3 pull_retell_calls.py --agent-id agent_abc123 --limit 40

Outputs into ./out/:
    calls_raw.json     full API payloads (keep for audit)
    transcripts.md     human/LLM-readable transcripts, one per call
    stats.json         computed metrics
    stats.md           the same metrics as a readable table

Only computes metrics that come straight off Retell's own fields. Conversation
QUALITY (objection handling, booking discipline, hallucination) is not guessable
from these fields -- that is scored by reading transcripts.md against
SCORECARD.md. This script deliberately does not fake those numbers.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from statistics import median

BASE = "https://api.retellai.com"


def api(path, key, method="GET", body=None):
    req = urllib.request.Request(
        f"{BASE}{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:600]
        sys.exit(f"HTTP {e.code} on {method} {path}\n{detail}")
    except urllib.error.URLError as e:
        sys.exit(
            f"Could not reach {BASE} ({e.reason}).\n"
            "If you are inside a sandboxed/proxied environment, api.retellai.com "
            "is probably not on the network allowlist. Run this from a machine "
            "that can reach it."
        )


def resolve_agent(name, key):
    """Find agent_id(s) by case-insensitive name substring."""
    agents = api("/list-agents", key)
    if isinstance(agents, dict):
        agents = agents.get("agents") or agents.get("data") or []
    hits = [
        a for a in agents
        if name.lower() in str(a.get("agent_name") or "").lower()
    ]
    if not hits:
        names = sorted(str(a.get("agent_name")) for a in agents)
        sys.exit(f"No agent matching {name!r}. Available:\n  " + "\n  ".join(names))
    for a in hits:
        print(f"  matched agent: {a.get('agent_name')} -> {a.get('agent_id')}",
              file=sys.stderr)
    return [a["agent_id"] for a in hits]


def fetch_calls(agent_ids, limit, key):
    """Page /v2/list-calls newest-first until we have `limit` calls."""
    out, cursor = [], None
    while len(out) < limit:
        body = {
            "filter_criteria": {"agent_id": agent_ids},
            "limit": min(100, limit - len(out)),
            "sort_order": "descending",
        }
        if cursor:
            body["pagination_key"] = cursor
        page = api("/v2/list-calls", key, "POST", body)
        if isinstance(page, dict):
            page = page.get("calls") or page.get("data") or []
        if not page:
            break
        out.extend(page)
        cursor = page[-1].get("call_id")
    return out[:limit]


def ts(ms):
    if not ms:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


def pct(n, d):
    return round(100.0 * n / d, 1) if d else 0.0


def get_latency(call, track, stat):
    node = (call.get("latency") or {}).get(track) or {}
    return node.get(stat)


def compute(calls):
    n = len(calls)
    if not n:
        sys.exit("No calls returned for that agent.")

    durs = [c["duration_ms"] / 1000 for c in calls if c.get("duration_ms")]
    reasons = Counter(str(c.get("disconnection_reason") or "unknown") for c in calls)

    # Retell only populates call_analysis when post-call analysis is enabled.
    analyzed = [c for c in calls if c.get("call_analysis")]
    successful = [
        c for c in analyzed
        if (c["call_analysis"] or {}).get("call_successful") is True
    ]
    sentiment = Counter(
        str((c.get("call_analysis") or {}).get("user_sentiment") or "unscored")
        for c in calls
    )

    # Failure buckets. `error_*` = platform/infra fault, not the prompt's fault.
    infra = sum(v for k, v in reasons.items() if k.startswith("error_"))
    voicemail = sum(v for k, v in reasons.items() if "voicemail" in k or "machine" in k)
    transfers = sum(v for k, v in reasons.items() if "transfer" in k)
    inactivity = sum(v for k, v in reasons.items() if "inactivity" in k)
    user_hangup = reasons.get("user_hangup", 0)

    # A call under ~15s almost never contains a real conversation. High counts
    # here usually mean hangups on the greeting -- a prompt/voice problem.
    sub15 = sum(1 for d in durs if d < 15)
    sub30 = sum(1 for d in durs if d < 30)

    e2e_p50 = [v for v in (get_latency(c, "e2e", "p50") for c in calls) if v]
    e2e_p95 = [v for v in (get_latency(c, "e2e", "p95") for c in calls) if v]

    costs = [
        (c.get("call_cost") or {}).get("combined_cost")
        for c in calls
    ]
    costs = [c for c in costs if isinstance(c, (int, float))]

    return {
        "calls_analyzed": n,
        "window_start_utc": ts(min((c.get("start_timestamp") or 0) for c in calls)),
        "window_end_utc": ts(max((c.get("start_timestamp") or 0) for c in calls)),
        "duration": {
            "median_sec": round(median(durs), 1) if durs else None,
            "mean_sec": round(sum(durs) / len(durs), 1) if durs else None,
            "max_sec": round(max(durs), 1) if durs else None,
            "under_15s_count": sub15,
            "under_15s_pct": pct(sub15, n),
            "under_30s_count": sub30,
            "under_30s_pct": pct(sub30, n),
        },
        "outcomes": {
            "disconnection_reasons": dict(reasons.most_common()),
            "infra_error_count": infra,
            "infra_error_pct": pct(infra, n),
            "voicemail_pct": pct(voicemail, n),
            "transfer_pct": pct(transfers, n),
            "inactivity_pct": pct(inactivity, n),
            "user_hangup_pct": pct(user_hangup, n),
        },
        "retell_self_report": {
            "calls_with_analysis": len(analyzed),
            "call_successful_pct_of_analyzed": pct(len(successful), len(analyzed)),
            "user_sentiment": dict(sentiment.most_common()),
            "note": "call_successful is Retell's own LLM judging its own call. "
                    "Treat as a signal, never as the KPI.",
        },
        "latency_ms": {
            "e2e_p50_median_across_calls": round(median(e2e_p50)) if e2e_p50 else None,
            "e2e_p95_worst_call": round(max(e2e_p95)) if e2e_p95 else None,
            "calls_reporting_latency": len(e2e_p50),
        },
        "cost": {
            "total_usd": round(sum(costs) / 100, 2) if costs else None,
            "median_per_call_usd": round(median(costs) / 100, 3) if costs else None,
            "note": "Retell reports cost in cents; divided by 100 here.",
        },
        "requires_transcript_read": [
            "booking_conversion_rate",
            "hallucination_rate (invented prices / hours / services)",
            "objection_handling",
            "interruption_and_barge_in_quality",
            "data_capture_completeness",
        ],
    }


def write_transcripts(calls, path):
    with open(path, "w") as f:
        f.write("# Transcripts — newest first\n\n")
        f.write("Score these against SCORECARD.md. Do not score from stats alone.\n\n")
        for i, c in enumerate(calls, 1):
            an = c.get("call_analysis") or {}
            dur = c.get("duration_ms")
            f.write(f"\n---\n\n## Call {i} — `{c.get('call_id')}`\n\n")
            f.write(f"- start: {ts(c.get('start_timestamp'))}\n")
            f.write(f"- duration: {round(dur/1000,1) if dur else 'n/a'}s\n")
            f.write(f"- status: {c.get('call_status')}\n")
            f.write(f"- disconnection_reason: {c.get('disconnection_reason')}\n")
            f.write(f"- retell_call_successful: {an.get('call_successful')}\n")
            f.write(f"- retell_user_sentiment: {an.get('user_sentiment')}\n")
            if an.get("call_summary"):
                f.write(f"- retell_summary: {an['call_summary']}\n")
            if c.get("recording_url"):
                f.write(f"- recording: {c['recording_url']}\n")
            f.write("\n```\n")
            f.write((c.get("transcript") or "(no transcript)").strip() + "\n")
            f.write("```\n")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--agent", help="agent name substring, e.g. Mia")
    g.add_argument("--agent-id", action="append", help="explicit agent_id (repeatable)")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()

    key = os.environ.get("RETELL_API_KEY")
    if not key:
        sys.exit("Set RETELL_API_KEY first (Retell dashboard -> API Keys).")

    ids = args.agent_id or resolve_agent(args.agent, key)
    calls = fetch_calls(ids, args.limit, key)
    print(f"  fetched {len(calls)} calls", file=sys.stderr)

    os.makedirs(args.out, exist_ok=True)
    with open(f"{args.out}/calls_raw.json", "w") as f:
        json.dump(calls, f, indent=2)
    write_transcripts(calls, f"{args.out}/transcripts.md")

    stats = compute(calls)
    with open(f"{args.out}/stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
