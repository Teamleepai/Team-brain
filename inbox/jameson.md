# Inbox — Jameson

Added by Claude session `session_01NYeVaKj98DGejrZgz9KFKL` on 2026-08-07.
Branch: `claude/prospecting-strategy-framework-nae2oh`

## Read these two first, in this order

- [ ] **`prospecting/02-aisdr-brief-jameson.md`** — your brief. Part A is context written for Aaron and
  Alec; **Part B is the prompt you paste into Claude.** Read Part A anyway so you understand why the
  constraints exist rather than just following them.
- [ ] **`prospecting/08-data-sourcing-playbook.md`** — what to scrape and from where, per industry. This
  is your implementation guide for stages 1 and 2 of the cadence.

## Before you write any code

- [ ] **Gate 1 is a compliance document, not a build.** One page, sourced. It blocks everything else.
  Nothing sends before Aaron signs it off. Details in `02` Part B.
- [ ] **Confirm your sandbox is actually a sandbox.** You should have a dedicated GHL sub-account with no
  real client data, no production sending credentials, and **no A2P brand access.** If you've been given
  any of those, stop and tell Aaron — a mistake with the A2P brand can take down paying clients' SMS,
  not just prospecting. Ref `02` §A.8.
- [ ] **Design the prospect dossier schema first.** It is the actual product; the messages are a
  by-product. Everything else assumes it exists.

## Build order — start here

> **Scope changed 2026-08-07: dental and veterinary are OUT.** If you already started on the NPPES
> file, stop — it was dental-specific. See `prospecting/09-audit-2026-08-07.md`.

- [ ] **Independent auto repair first.** Google Maps universe + Orbital/6sense software-install data.
  Best-documented voice AI pain available, and voice AI is the product with the most reps behind it.
  **Qualify on bays and technicians, never on revenue** — sources conflict badly ($450K vs $500K–1.2M)
  and a scraper can't see revenue anyway. It can see bay count in Maps photos and Street View.
- [ ] **Med spa second.** Maps + Boulevard booking-widget detection. Together with auto repair this
  covers both lead products (voice AI and reactivation) and both buckets.
- [ ] **Do not build all five verticals.** The playbook documents five because the research covered five.
  Two is the plan.

## Open research items — answer these, don't assume

- [ ] **Verify 6sense / Orbital actually cover Boulevard and Zenoti.** I confirmed auto repair coverage
  only. **Get a quote and test before committing budget.**
- [ ] **Reconcile the collision facility count** (105,000 IBISWorld vs 8,000+ elsewhere) before any TAM
  sizing. Don't size off either number.
- [ ] **Check bulk license-data availability for your actual target states.** Confirmed: Texas plumbing
  (free daily CSV), and the Apify professional-licenses actor covering NJ and Indiana. Everything else
  is unverified.
- [ ] **The Yelp response-time signal may not be buildable.** Fusion API doesn't expose it, scraping is
  prohibited by Yelp's terms, and two Fusion-based Apify actors are deprecated. Use unanswered-reviews as
  the proxy and verify response time manually on the shortlist only. Ref `03` §3.4.
- [ ] **Measure the false-positive rate per signal.** Not estimate — measure, against 20 hand-checked
  prospects. If IVR detection is wrong 15% of the time, 15% of our openers are factually false to the one
  person who knows the truth.

## Things that will bite you

- [ ] **A verbal "sure, text me" is not valid SMS consent.** Marketing texts to a cell require prior
  express *written* consent. The gate must be enforced in code: no consent artifact, no channel entry.
- [ ] **Never use AI voice for outbound cold calls.** FCC Declaratory Ruling of 8 Feb 2024 puts
  AI-generated voices — explicitly including real-time conversational agents — under the TCPA's
  artificial-voice restrictions. Humans dial. Verify this yourself and tell Aaron if I've got it wrong.
- [ ] **The reply agent will invent commitments** unless the claim registry is hard-bounded. Assume it
  will try. This is the most important guardrail in the build.
- [ ] **Config-as-code, in git** — not in a database. Five non-engineers will edit agent behaviour, and
  when reply quality drops on a Thursday `git log` answers why in seconds while a database answers never.
  GitHub's web editor plus pull requests is your day-one command centre. Ref `02` §A.8.
- [ ] **Manual verification labour is the cost nobody priced.** Raw data for ~5,000 entities is under
  $200. The $50-per-qualified-prospect kill criterion will be breached by human hours, not data fees.
  Track it from day one. Ref `08` §5.1.

## Report format

Phase-gated. **Stop at each gate and wait for sign-off.** At every gate include what you verified, what
you inferred, what you couldn't determine, and **what you think is wrong in the brief** — that last one
is mandatory and "nothing" isn't an acceptable answer.
