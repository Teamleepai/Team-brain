# Feeding the Prospect List into Meta — Implementation Note

**Date:** 2026-08-07
**Context:** doc `04` §4.3 recommended retargeting the outbound list rather than pure cold lead-gen.
This is how that's actually built.
**Ad account:** `1819763081734046`

---

## 0. A correction on the number

Doc `04` said "the 2,000 companies you're already dialing." **That 2,000 came from doc `03`'s planned
Phase 1 universe (2,000–5,000 raw scraped entities) — it is not a count of prospects you have actually
contacted.** I don't know that number. Size everything below off your real list.

---

## 1. The B2B problem you have to solve first

**Meta matches people, not businesses.** There is no way to target "Acme HVAC" as an entity. You target
*Josh, who owns Acme HVAC*, as an individual — and Meta only finds him if the identifiers you upload
match the ones attached to his personal Facebook or Instagram account.

That is why B2B custom audiences underperform:

| List type | Match rate | Source |
|---|---|---|
| Well-maintained B2C list | **60–80%** | [sayprimer.com](https://www.sayprimer.com/blog/customer-list-audiences-for-b2b-marketers) |
| **B2B work-email list** | **25–45%** | [sayprimer.com](https://www.sayprimer.com/blog/customer-list-audiences-for-b2b-marketers) |
| Email alone | 40–60% | [xyzlab.com](https://xyzlab.com/meta-ads/customer-list/) |
| **Email + phone + name** | **60–75%+** | [xyzlab.com](https://xyzlab.com/meta-ads/customer-list/) |

The cause is simple: *"B2B lists often contain work emails that users did not use for their Facebook
accounts."* [[sayprimer.com](https://www.sayprimer.com/blog/customer-list-audiences-for-b2b-marketers)]

`info@acmehvac.com` matches nobody. It isn't a person.

### And here is the advantage you may not have noticed

**Your top pain signal is "main line rings to a mobile number."** Doc `01` scored it `●●●` and doc `03`
called it the signal that pays for the plan, because verified mobile direct-dial connects at 18–22%
instead of 8–12%.

**Those are personal cell numbers — and a personal mobile is one of the strongest match keys Meta has**,
because it's usually the number tied to the account.

So the same filter that makes these owners reachable by phone also makes them **matchable on Meta.**
Your ICP selection has accidentally produced a high-match-rate list. Most B2B advertisers upload work
emails and get 25%; you should be uploading owner name + personal mobile + email and landing near the
top of the 60–75% band.

---

## 2. Minimums and what to expect

- **Meta needs at least 100 matched people** for an audience to deliver; a few hundred is the practical
  floor for meaningful targeting [[benly.ai](https://benly.ai/learn/meta-ads/custom-audiences-guide)]
- **Lists decay 2–4% per month.** Refresh every 60–90 days
  [[sayprimer.com](https://www.sayprimer.com/blog/customer-list-audiences-for-b2b-marketers)]

| Your list size | Work email only (25–45%) | Multi-key with mobile (60–75%) |
|---|---|---|
| 500 | 125–225 | 300–375 |
| 1,000 | 250–450 | 600–750 |
| 2,000 | 500–900 | **1,200–1,500** |

All of those clear the 100 minimum. The multi-key column is the difference between an audience that
delivers and one that delivers *efficiently* — at 300 people you'll exhaust frequency in days.

---

## 3. The file to build

One row per **person**, not per company. Include every column you have — each additional key raises the
match rate.

| Column | Meta schema key | Priority | Notes |
|---|---|---|---|
| Owner mobile | `PHONE` | **Highest** | Your strongest key. E.164 preferred (`+15551234567`) |
| Owner personal email | `EMAIL` | **Highest** | A gmail/yahoo address beats a work address every time |
| Owner work email | `EMAIL` | Medium | Include as a second row if you have both |
| First name | `FN` | High | Cheap to add, meaningful lift |
| Last name | `LN` | High | |
| City | `CT` | Medium | |
| State | `ST` | Medium | Two-letter |
| Zip | `ZIP` | Medium | |
| Country | `COUNTRY` | Medium | `US` |
| Your internal ID | `EXTERN_ID` | Optional | Not hashed. Lets you suppress and re-sync cleanly |

**Do not upload:** `info@`, `office@`, `service@`, or any main business line that is not a mobile. They
cost you nothing but they don't match, and they drag your reported match rate down so you can't tell
what's working.

### Hashing

Meta requires PII to be SHA-256 hashed. **You don't have to do this yourself** — both paths handle it:

- **Ads Manager UI** hashes in your browser before anything is transmitted
- **The MCP tool** (`ads_update_custom_audience_users`) accepts raw values, normalises them (lowercases
  and trims email, strips non-digits from phone) and SHA-256 hashes them server-side before they reach
  Meta. Already-hashed 64-char hex values pass through unchanged

Normalisation matters more than people expect — `Josh@Acme.com ` and `josh@acme.com` hash to completely
different values, so a normalisation step that isn't identical to Meta's produces silent zero matches.
Let the tool do it.

---

## 4. Two ways to load it

### Option A — Ads Manager UI

Audiences → Create Audience → Custom Audience → Customer list → upload CSV → map columns → name it.
Fine for a one-off.

### Option B — via the MCP tools (better for a repeatable process)

```
  1. ads_create_custom_audience
        subtype: CUSTOM
        customer_file_source: USER_PROVIDED_ONLY
        retention_days: 180 (max)
        → returns an audience_id, empty

  2. ads_update_custom_audience_users
        audience_id: <from step 1>
        schema: ["EMAIL","PHONE","FN","LN","CT","ST","COUNTRY"]
        data: [[...], [...], ...]     raw values are fine
        operation: ADD
        customer_consent: true|false   ← see §6

  3. ads_get_custom_audience
        → check size and delivery_status before spending anything
```

Batch in chunks of a few thousand rows. `operation: REMOVE` takes people out — use it to suppress
closed-won customers so you stop paying to advertise at people who already bought.

---

## 5. Don't rely on the uploaded list alone — layer four audiences

The customer list is one layer and it's the one with a match-rate ceiling. Build all four:

| Layer | Audience type | Why |
|---|---|---|
| **1. Prospect list** | `CUSTOM` (DFCA) | Your scored, researched targets. Match-rate limited |
| **2. Website visitors** | `WEBSITE` (pixel) | **No matching problem at all.** Anyone who visits after your call is captured regardless of what email they use |
| **3. Engagement** | `ENGAGEMENT` | Video viewers, lead-form openers, IG/FB engagers. Free, no PII, no match rate |
| **4. Lookalike** | `LOOKALIKE` off layer 1 or 2 | Prospecting beyond the list |

**Layer 2 is the one that solves the B2B match problem, and it's the one people skip.** If your cold
call or email mentions the site — "I put the three things I found on a page for you" — the pixel catches
them with no identity matching involved. That turns a phone conversation into a retargetable audience.

**On lookalikes:** a lookalike modelled on a few hundred owner-operators will find people who *resemble*
them demographically, which is not the same as finding business owners. Treat layer 4 as an experiment,
not a core channel, and judge it on booked meetings rather than CPL.

---

## 6. Before you upload anything — two things to settle

**1. Rights to use the data.** Meta's Custom Audience terms require you to attest you have the right to
use the data you upload. The MCP tool exposes a `customer_consent` flag described as *"required in some
regions."* For a list built from scraped public business data, that attestation deserves a moment's
thought rather than a reflexive `true`.

**2. CCPA.** Uploading personal information to Meta for advertising can constitute *"sharing"* for
cross-context behavioural advertising, which California residents have the right to opt out of. You are
already building a TCPA compliance posture for the SMS leg — put this question in the same Gate 1
review rather than treating it as a separate problem. **Same lawyer, same conversation, marginal extra
cost.**

I'm not a lawyer and this is not legal advice. But it belongs on the list.

---

## 7. How to actually use it

Retargeting the outbound list is not a standalone campaign — it's air cover for the calls.

- **Run the ads *before and during* the call cadence, not after.** A prospect who has seen you three
  times before the phone rings is a warmer connect. Multi-channel sequences outperform single-channel by
  **3–4x**, and coordinated email + phone lifts engagement **287%** over email alone
  [[syncgtm.com](https://syncgtm.com/blog/how-many-touch-points-before-a-sale), [prospeo.io](https://prospeo.io/s/b2b-outreach-strategy)]
- **Budget it as a fraction, not a channel.** Doc `04` allocated ~15% of ad spend to retargeting — on a
  $3–4K/month budget that's $450–600, against an audience of a few hundred to ~1,500 people. That is
  plenty of frequency
- **Suppress closed-won** with `operation: REMOVE` so you stop paying to reach customers
- **Segment by industry** if volume allows — an HVAC creative citing the $350-per-missed-call figure
  should not be shown to med spa owners
- **Measure booked meetings, not CPL.** These people are already in your outbound sequence; the ad's job
  is to make the call land, and CPL will not show you that

---

## 8. Sources

[sayprimer.com — customer list audiences for B2B](https://www.sayprimer.com/blog/customer-list-audiences-for-b2b-marketers) ·
[xyzlab.com — uploading CRM lists to Meta](https://xyzlab.com/meta-ads/customer-list/) ·
[benly.ai — custom audiences guide](https://benly.ai/learn/meta-ads/custom-audiences-guide) ·
[growwithsakib.com](https://growwithsakib.com/meta-custom-audiences/) ·
[adlibrary.com](https://adlibrary.com/posts/custom-audience) ·
[syncgtm.com — touchpoints](https://syncgtm.com/blog/how-many-touch-points-before-a-sale) ·
[prospeo.io](https://prospeo.io/s/b2b-outreach-strategy)

Tool behaviour (hashing, normalisation, schema keys, ADD/REMOVE) is from the Meta Ads MCP tool
definitions available in this session, not from secondary sources.

**Not verified:** your actual contacted-prospect count, and what identifiers you currently hold for
them. Both determine whether this is worth doing at all.
