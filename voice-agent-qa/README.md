# Voice Agent QA — Mia / Ace Detailing

Tooling to audit a Retell agent's recent calls and score it against a
$2,000/mo retention standard.

## Why this exists as tooling instead of an answer

The analysis of Damian's last 40 calls could not be run from the Claude Code
web sandbox. Two independent blockers:

1. **No credential.** No `RETELL_API_KEY` exists anywhere in the session
   environment, and Retell is not one of the connected MCP connectors
   (connected: Docusign, Gmail, Google Drive, Leep AI Meta Ads, Slack).
2. **Network policy.** `api.retellai.com:443` is denied at the egress proxy —
   `CONNECT tunnel failed, response 403`. Confirmed against the proxy's own
   status endpoint, which logged the rejection.

Neither is fixable from inside the sandbox. So: the deterministic half of the
audit is committed here as a script, and the judgment half as a rubric.

## Run it

```bash
export RETELL_API_KEY=key_xxxxx        # Retell dashboard -> API Keys
python3 pull_retell_calls.py --agent "Mia" --limit 40
```

If several agents match "Mia", the matched names and IDs print to stderr — rerun
with the exact one:

```bash
python3 pull_retell_calls.py --agent-id agent_abc123 --limit 40
```

No dependencies beyond the Python 3 standard library.

## What you get

| File | Contents |
|---|---|
| `out/stats.json` | Every metric derivable from Retell's own fields |
| `out/transcripts.md` | 40 transcripts formatted for scoring |
| `out/calls_raw.json` | Full payloads, kept for audit |

Then score `out/transcripts.md` against `SCORECARD.md`.

## What the script will and won't tell you

**Deterministic** (straight off the API): durations, sub-15s dropoff,
disconnection-reason breakdown, infra error rate, transfer rate, voicemail
rate, e2e latency p50/p95, cost, and Retell's own sentiment labels.

**Not deterministic — requires reading transcripts and listening to
recordings:** booking conversion, hallucinated prices, objection handling,
barge-in behavior, data-capture completeness. The script lists these under
`requires_transcript_read` rather than inventing a number for them. Booking
conversion in particular cannot be inferred from `call_successful` — that
field is Retell's LLM grading its own call, and it is optimistic.

## One caveat on the API surface

Field and enum names (`filter_criteria`, `disconnection_reason` values,
`latency.e2e.p50`, `call_cost.combined_cost`) are written against Retell's v2
API as documented. The script is defensive about it — unknown disconnection
reasons are bucketed rather than dropped, and `error_*` is matched by prefix —
but if Retell has renamed a field, `stats.json` will show nulls in that
section rather than crashing. Check `calls_raw.json` against the current API
reference if a section comes back empty.
