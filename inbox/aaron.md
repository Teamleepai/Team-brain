# Inbox — Aaron

Added by Claude session `session_01NYeVaKj98DGejrZgz9KFKL` on 2026-08-07.
Branch: `claude/prospecting-strategy-framework-nae2oh`

## NEW — the 16-week GTM plan is live

`prospecting/10-gtm-week-by-week.md`. **Read §1 first — it inverts the earlier plan.**

- [ ] **Your real roster gives you ~3× the pipeline you need.** 175 dials/day across four people, ~79
      meetings/month, against 14 customers required. **Grace alone covers 1.5× the requirement.**
      Lead flow is no longer the constraint — **delivery capacity and your calendar are.**
- [ ] **Therefore: raise price rather than add dials.** Recommended 6 Group @ $5,000 + 8 Fast @ $2,100 =
      $46,800 from **14 customers instead of 17** — 18% less delivery load for the same revenue.
- [ ] **Stop doing Division A dialing.** Every hour you or Alec spend on it is an hour Grace covers at a
      third the cost. Your 20/day goes to Division B (multi-location) where a peer voice changes the
      outcome, and to reviving stalls.
- [ ] **Cold calling does not need Gate 1.** Human-dialed B2B calls are legal without prior consent —
      only SMS and email need the consent gate. **Dialing starts week 3 regardless of the attorney
      timeline.** That was ambiguous in earlier docs.
- [ ] **Consider splitting the divisions between you and Alec** rather than both doing both. Different
      products, buyers and objections — one each halves the context-switching and deepens each objection
      library. `10` §8.4.

## Decisions only you can make

- [ ] **Confirm the prospecting domain spelling before purchase.** You wrote `itsleapai.com` but the
  brand is Leep (`@leepai.io`) — l-e-e-p. A misspelled lookalike of your own domain reads as a phishing
  pattern to filters and is expensive to undo. Then **buy it this week**: a cold domain needs a 4–8 week
  warmup to reach 50 emails/day, and the engine has to be live ~1 September. Ref `04` §A.6.
- [ ] **Decide the Group tier price.** Everything downstream keys off it. Recommendation: $4,000/mo
  blended with the Group tier listed $4,000–6,000. Mid-market agencies charge $5,000–15,000 and
  multi-location SEO alone is $3,000–6,000, so $2,500 for a five-product bundle is below the price of
  SEO by itself. Ref `04` §2, `05` §3.
- [ ] **Assign referral outreach to a named person.** Two referrals at $4,000 is $8,000/mo — a sixth of
  the target — at effectively zero CAC, and nobody owns it. Ref `04` §4.3.
- [ ] **Start recording every cold call, from call one.** It is the Straz training corpus and it is
  unrecoverable once a call happens. Check all-party consent states first — it's one sentence in the
  opener and it strengthens the TCPA consent trail. Ref `02` §A.5, §A.7.
- [ ] **Pick the SMS consent mechanic:** inbound keyword text, one-field opt-in link, or email reply. A
  verbal "sure, text me" is **not** valid consent for marketing SMS. Ref `02` §A.1.
- [ ] **Buy the domain MONDAY 10 AUGUST.** 4–8 week warmup, needed live by ~1 Sept. It is the critical
  path and it is the one item that cannot be compressed.
- [ ] **Confirm the git commit identity question** — see the note at the bottom of
  `sessions/claude/2026-08-07.md`. All commits so far are attributed to Claude, not to you.

## BLOCKING MONDAY — one field in one file

- [ ] **`pipeline/config.yaml` → `geography.markets` is empty, and stage 1 refuses to run without
      it.** Fill in the metros you actually sell into. **This is the single input I cannot guess** —
      a Denver list is worthless if you sell in Phoenix. Everything in the two-week sprint waits on
      this one line.

I tried to pull the live list you asked for and **could not — all external network egress is blocked
in this environment** (Google Maps, Yelp, I-CAR and California BAR all refused at the proxy). I did
not fabricate one, because a real business name attached to an invented pain signal is the exact
thing we've spent eleven documents warning against. **What exists instead is `pipeline/` — five
tested stages that produce the real list in a few hours once the geography is set.**

## DECIDE BEFORE JAMESON SCRAPES MONDAY

- [ ] **"Auto body" or "mechanical repair" for Division A?** You said body shop; the plan says mechanical.
      **Body = collision = SEO lead product** (your least documented, research still not in the repo).
      **Mechanical = voice AI lead product** (your strongest, best-documented pain of any vertical).
      Discovery tooling is ~80% shared, but the opener and product differ. Ref `11` §0.

## Legal — one review, FIVE questions (Gate 1)

- [ ] **Book one telecom/privacy attorney session covering all of these together.** Same lawyer, one
  conversation, marginal extra cost per item:
  1. Does our SMS consent language and logging meet TCPA prior express written consent?
  2. Can prospecting SMS and client-delivery SMS share the same A2P 10DLC brand registration? (If not,
     a violation could take down paying clients' SMS, not just prospecting.)
  3. Call recording — which states require all-party consent, and what's the exact opener sentence?
  4. Meta Custom Audience: rights-to-use attestation for scraped data, and whether uploading to Meta
     constitutes CCPA "sharing" for cross-context behavioural advertising.

  5. **DNC and the mobile-targeting problem — NEW, and it constrains how we dial.** Our top signal
     ("main line rings to a mobile") selects for **sole proprietors using personal cells for business.**
     Sources say that number **is a residential line and IS on the DNC registry if they registered it**,
     and that FTC enforcement treats micro-businesses blurring the consumer/commercial line **as
     consumers.** Also: **the TCPA applies to mobiles even in B2B — a power dialer needs express
     consent.** Questions for the attorney: (a) do we scrub national + state DNC? (b) is manual-dial-only
     mandatory on these numbers? (c) **is marketing/sales outreach a permitted use under a skip-trace
     provider's licence** — marketing is *not* a permissible purpose under FCRA, and DPPA makes
     marketing use of DMV data a federal violation. Ref `11` §1 and §2 Tier 4.

  **HIPAA dropped off this list** when dental and veterinary went out of scope — question 5 takes its
  slot, so it's still one session and four-to-five questions.

- [ ] **Check whether anyone was planning dialer software for Grace's 90/day.** If so, that's a TCPA
      question before it's an efficiency question. Manual dialing at 90/day is achievable; a power dialer
      on cell numbers may not be lawful without consent.

## Verify before use in outreach

- [ ] **The $75,000/month auto repair missed-call figure is a ceiling, not a median** — and it's now
  attached to your top-ranked vertical. Build the arithmetic live from the three well-sourced components
  (25–45 calls/day, 20–30% missed, their own average repair order) rather than asserting the headline.
  Ref `07` §2.1.
- [ ] **Med spa net margin (15–25%) in `05` §3 is my estimate, not a citation.** Med spa ranks top on
  affordability *because* of that number, and you have client P&L exposure to check it.
- [ ] **Auto repair revenue conflicts across sources** ($450K vs $500K–1.2M). Qualify on bay and
  technician count, not the industry average, or you'll pitch $2,000/mo to a shop clearing $450K.
  **Now load-bearing — auto repair is the top vertical.**

## New — from the 2026-08-07 audit

- [ ] **Read `prospecting/09-audit-2026-08-07.md` §1.1.** Backing out of dental cost you the free NPPES
  federal data source and the 31 Dec benefits timing hook. Both were real advantages. The decision is
  yours and defensible — just hold the cost consciously.
- [ ] **Cost-per-qualified-prospect should be re-tested, not inherited.** The $50 kill criterion was set
  when a free bulk source was in the mix. It isn't any more.
