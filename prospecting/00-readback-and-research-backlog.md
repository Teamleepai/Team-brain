# Prospecting Strategy — Phase 0 Read-Back & Research Backlog

**Date:** 2026-08-05
**Source:** Voice transcript, Alec + Aaron (~1 hour), prospecting/GTM strategy session
**Status:** Phase 0 of 4. Comprehension + notation + research scoping ONLY. No research executed.

---

## 0. How to read this document

Alec's closing instruction defined the sequencing explicitly:

> "First it needs to plan the plan of the plan. So first you need to take all of that, notate
> everything. But it needs to figure out, out of all of that, what needs research. That needs to
> deploy, builders can do the research. We're gonna come back to that research, then we need to
> audit that research, and then, after that passes, then we turn it into an executable plan, and
> to-dos."

That gives four phases:

| Phase | Work | Status |
|---|---|---|
| **0** | Ingest transcript, notate everything, lose nothing, identify what needs research | **This document** |
| **1** | Deploy researchers/builders against the scoped questions | Not started — blocked, see §10 |
| **2** | Audit the research adversarially — does it hold, is it sourced | Not started |
| **3** | Convert audited research into executable plan + to-dos | Not started |

**Nothing in this document is a research finding.** It is a structured restatement of what was said,
plus explicitly-labeled analysis where I was invited to challenge the logic.

### Citation convention

Per the standing rule — *"Never speak... without being able to cite your source on it"* — every claim
below carries a tag:

- **[T]** — Stated in the transcript. Directly quotable.
- **[INF]** — My inference from what was said. Not stated. Challengeable.
- **[UNVERIFIED]** — Asserted in the transcript as fact, but sourced to memory/anecdote and **not yet
  verified**. Must not enter a plan until confirmed.
- **[GAP]** — Referenced internal source that I **do not have access to**. See §10.
- **[GARBLE]** — Transcription is ambiguous. Needs human confirmation before it can be relied on.

---

## 1. The one-sentence version

> **We are inverting the prospecting motion: instead of building a list from firmographics and then
> hunting for pain, we scrape one pain signal at a time at massive scale, merge the results on the
> business entity, score each entity by how many pain signals it carries, and let the ranked output
> tell us who our ICP actually is — including which industry and which company size we should be
> targeting in the first place.** [T]

Everything else in the transcript is either (a) an elaboration of that mechanism, (b) a constraint on
it, or (c) a second, parallel business idea that emerged mid-conversation (§8).

---

## 2. The originating problem — "the Josh Problem"

This is the question Alec opened with and the one he called a blocker on:

> "What is the threshold employee count that is the sweet spot for us to have a very limited barrier
> to entry, meaning there's not a ton of receptionists, but their volume is so high, where all of our
> products are probably going to be a good fit... How do I find the Joshes of the world, but that are
> two to three times bigger than Josh?" [T]

Decomposed, this is a **three-variable optimization with a built-in tension**: [INF]

| Variable | We want | Why |
|---|---|---|
| **Volume / revenue** | HIGH — 2–3× Josh Astone [T] | More inbound = our products produce more measurable ROI; more revenue = they can pay |
| **Budget** | HIGH — "three times more money" [T] | Larger contract values, room for multi-product attach |
| **Gatekeeping** | LOW | We need to reach the decision maker directly |

The tension Alec named precisely: **the things that come with size are exactly the things that block
us.** [T] As a company grows it acquires:

- A receptionist / front-desk layer [T]
- An IVR / phone tree [T]
- A hidden owner cell phone — *"hiding his direct cell"* [T]
- Eventually: corporate procurement, IT security review, PE-owned vendor process [T]

**So the strategic question is: does a band exist where volume and budget have scaled but gatekeeping
has not yet hardened? And if it exists, can a database find it at scale?** [T]

His own proposed answer to the "how":

> "Just do a massive scrape for those one at a time and then merge... So how can we scrape? One of
> the things that we have — they have no good website? Okay, let's do a massive scrape on that. Then
> how do we scrape for the next one? Oh, they have an IVR system. Let's do a massive scrape on that.
> Theoretically, we take that data and merge it all... and give us a ranking system based on how many
> of them check off the most boxes." [T]

Aaron's refinement, which Alec confirmed as "100%":

> "We take the pain points and the trigger events and solely scrape based off of the pain and the
> trigger events. And then we score them, rank them, and then get the right contacts — whether it's
> owner or VP of ops — and then we segment it by small market, mid market." [T]

### The architecture this implies

**Signal-first, firmographic-second.** [INF] The conventional motion is: define ICP → pull a list →
enrich → look for triggers. The motion described here is the reverse:

```
  Scrape A: no good website          ─┐
  Scrape B: IVR system detected       │
  Scrape C: Yelp response time >1hr   │
  Scrape D: SEO ranked #4–10          ├──► MERGE on entity ──► SCORE ──► RANK ──► contact resolution
  Scrape E: hiring a receptionist     │      (dedupe/match)     (boxes      (owner vs.      ──► segment
  Scrape F: reviews cite missed calls │                          checked)    VP Ops)         (SMB/mid)
  Scrape G: "500+ customers" claims   │
  Scrape H: incumbent software stack ─┘
```

Alec's key structural point: each scrape is independently cheap and mechanical, and the *intelligence
lives in the merge and the score*, not in any individual scrape. [T] — *"which is super easy for
Claude to do."*

**One correction to the mental model I want to put on the record now (see §9.1):** the ranked output
of "most boxes checked" is a **product-attach surface score**, not a propensity-to-buy score. Those
are different things and conflating them will systematically surface the worst-run, least-solvent
businesses. Alec independently intuited this via the JJ Jardina caveat (§5) but it is not yet built
into the scoring model as described. [INF]

---

## 3. Artifact #1 — The Product × Trigger Matrix ("the column list")

Alec specified the exact shape of this when Aaron asked him to verbalize it:

> "Column number one: primary, voice AI receptionist. Row — each cell is filled with a piece of logic
> that in some way, shape, or form we are going to use to identify qualified prospects. For example,
> under voice AI receptionist: row one, cell one — hiring for a receptionist. No current receptionist.
> IVR system in place. Because all three of those triggers are telling me that our voice AI
> receptionist would win against all of that and would do better against all of that." [T]

> "Each one of my rows underneath my column is all of the potential pain points or potential buying
> triggers or potential research insight that could lead to having a more effective conversation that
> we want to go hunting for in order to curate the best quality prospect list." [T]

**Structure:** Columns = products. Rows under each column = individual, *scrapable*, *sourced* pieces
of qualifying logic. [T]

### 3.1 The product columns as specified

| # | Product | Triggers named in transcript | Research required |
|---|---|---|---|
| 1 | **Voice AI receptionist** (flagship) | Hiring for a receptionist; no current receptionist; IVR system in place [T]. Later added: Google reviews complaining about callbacks, missed calls, response time, service [T] | How to detect IVR at scale; how to detect "no receptionist"; review-mining methodology |
| 2 | **SMS chat agent** | None specified. Instruction: *"reference clients Armand and Aisha and figure out how that fits in the equation. I don't precisely know how or if we have sold that as a standalone product"* [T] [GAP] | Reverse-engineer triggers from Armand + Aisha accounts; establish whether it's ever been sold standalone |
| 3 | **Website chat bot / chat agent** | Websites with an intake or order form where a human follows up hours later [T]. Worked example: *"which is what happened to our client AFC last Friday, and they lost a job over it"* — 3-hour callback on a form fill [T]. Also: *"Alec will send you more info on this from JJ Jardina"* [T] [GAP] | How to detect form-present-but-slow-response at scale |
| 4 | **SEO** | Ranked #4–10 on Google — *"that is kind of there, but they just need to get into the top three"* [T]. Plus: *"utilize Aaron's research, all of the deep research he has done on SEO"* [T] [GAP] | Which SEO signals are cheaply visible at scale (DNS? backlinks?) and indicate poor SEO + high headroom **without a full per-site audit** [T] |
| 5 | **Yelp agent** | Yelp response time over one hour [T] | Which industries actually use Yelp beyond auto detailing [T]; **does the Yelp agent port to other platforms — Angi named as example, incl. API/ToS reality** [T] |
| 6 | **SMS reactivation campaign** (GoHighLevel) | Self-claimed high customer volume — *"we have over 500 customers... they market themselves as we have high customer volume, then that could be a trigger"* [T]. Plus incumbent-software capability check [T] | Detect volume claims at scale; detect incumbent software stack; map which incumbents have this built in |
| 7 | **Website hosting / maintenance / design** | *"needs website enhancements... or outdated website"* [T] | *"Use whatever triggers you would use to indicate how much maintenance the website needs, AND if the company can afford to prioritize website maintenance"* [T] |
| 8 | **CRM data hygiene + optimization retainer** — NEW, emerged in this call (§6) | Bloated systems; bad data integrity; CRM badly utilized [T] | Whole product needs definition — scope, pricing, liability |
| 9 | **Lead generation** — NEW, emerged in this call (§7) | For "Bucket 2" — not enough inbound [T] | *"Don't go crazy on this... but just bake it in"* [T] |
| 10 | **Channel / implementation delivery partner** — NEW, separate motion (§8) | N/A — different buyer entirely | Partner program research (Retell, Synthflow, Smith AI, ElevenLabs) [T] |

### 3.2 The explicit design constraint on this matrix

Every cell must be a **piece of logic we can actually go hunting for** — not a description of a good
customer. [T] The test is: *can this be scraped at volume?* If it can't, it isn't a row; it's a
talking point. [INF]

---

## 4. The disqualifier logic, and Alec's invitation to challenge it

### 4.1 "No website" as a hard DQ

Alec was explicit, and explicitly invited pushback:

> "Websites is a good box to check, but not a key buying criteria. **And challenge my logic on this if
> you need to**, but I would assume that companies with no website are not companies that we would
> want to work with — not that have a bad website and no SEO presence, but **no website at all**. That
> is probably a dead end." [T]

Aaron confirmed the intent: *"no website is a disqualifier... if they don't have this, then they're
probably not our target market fit."* [T]

So the stated rule is:

- Bad website + no SEO presence → **strong buying signal**, keep [T]
- No website at all → **disqualify** [T]

**I am accepting the invitation to challenge this. See §9.2 — it directly contradicts the JJ Jardina
insight, which is the most valuable idea in the transcript.** [INF]

### 4.2 "Incumbent software already has the feature" as a DQ — proposed, then reversed

Alec first proposed it:

> "Checking their incumbent software systems and seeing if their incumbent software systems have that
> built-in capability, yes or no. For example, I believe Boulevard has that capability. So we DQ
> people that we find using Boulevard." [T]

Aaron immediately challenged it, using precedent:

> "Hold on on that, though. Yes, you're right, 100%, but — remember when you DQ'd yourself out of, oh,
> let's not go after a Jobber or HouseCall Pro because those are the big dogs, and then you kicked
> their ass in the sales process? Remember? And then what percentage of our customers have CRMs that
> they're using super well and have it super dialed in?" [T]

**This exchange produced what I consider the second-most important reframe in the transcript:** [INF]

> **Incumbent software is not a competitor. It is a delivery surface.** [INF, from T]

Alec's articulation:

> "What's the difference in selling an SMS reactivation campaign on our end versus just going in [to
> their system]?... What about a monthly retainer, a consultancy retainer, if somebody just goes into
> your existing system and does it for you?... We could literally do it in Boulevard... **We're a CRM
> specialist in your software.**" [T]

And the reason this is strategically powerful — it kills the biggest silent objection:

> "The barrier to entry and the objections, the silent objections that come from like, oh shoot, I got
> to get all my customer contacts out of your system into my system, and go through all that pain —
> the barrier. If we make it super simple, that makes a lot of sense." [T]

Plus: *"that's way less liability"* [T] and *"those are high ticket"* [T].

**Net:** "Boulevard has it built in" is not a DQ. It is a **qualified wedge** — it tells us they have
the data and the platform, and that they're almost certainly using ~10% of it. [T]

---

## 5. The JJ Jardina Insight — "that's a money thought"

This is the passage Aaron reacted to most strongly, and I agree with his assessment.

Alec's setup:

> "Note to Claude: check... Alec is going to push to my inbox relevant details on project JJ Jardina,
> to understand what led to a high revenue company like JJ Jardina not being relevant on Google — to
> see if we can reverse engineer that into some sort of formula that could tell us how we target
> companies making decent revenue but do not appear on Google. **Because what we don't want to go
> hunting for is companies that don't appear on Google because they're bad companies and then have no
> money to afford to pay us.**" [T]

Aaron: *"Holy crap, that's a good insight right there, dude. That's a money thought right there."* [T]

Alec's compression of it: *"They're good on revenue, but they don't appear good on Google."* [T]

### 5.1 Why this is the highest-value idea in the transcript

Because it defines a segment with **zero incumbent vendor and total product whitespace**, and it is
**structurally invisible to every competitor using conventional prospecting** — everyone else finds
prospects *through* Google. [INF]

### 5.2 Why it is also the hardest technical problem in the transcript

Alec asked exactly the right question and correctly identified the paradox himself:

> "Question for Claude: is the fact that we can find them on a Google Maps [scrape] relevant to their
> SEO configuration? And if SEO is one of our products that we want to offer, and it's a trigger for
> our ICP, then — **is there even a world, or a tool, or a resource, to go about finding companies that
> do not have SEO and have no presence, as they're not going to show up in our Google Maps [scraping]
> layers?**" [T]

**This is a negative-space search problem.** [INF] You cannot find an entity in a dataset by querying
that dataset for its absence. The scrape target and the discovery mechanism are the same system.

Therefore the JJ Jardina formula requires **a non-Google source of both existence and revenue proof**,
cross-referenced against Google absence. [INF] That is a genuinely different data architecture from
every other scrape in §3, and it should be scoped as its own research workstream rather than as a row
in the matrix. [INF]

---

## 6. The Data-Trust Wedge — CRM hygiene as a Trojan horse

This thread started as a product idea and ended as a **positioning strategy**. It deserves its own
section because it changes what business we're in. [INF]

The chain of reasoning, in order:

1. **The stated pain isn't the real pain.** [T] Alec, on the mid-market Bucket-2 prospect:
   > "Their problem might be not enough leads. Or their problem also may be — we've gotten too big and
   > our systems have gotten too bloated, and the data integrity is so bad it's affecting our lead
   > volume. And it's the last project I want to touch, because I know it's going to take many months
   > to even get cleaned up, because I don't know how to use AI to leverage how to clean up my CRM to
   > actually produce quality leads." [T]

2. **But that's still not the real pain.** [T]
   > "But that's not even the real pain point. The pain point is behind that — which lets us get our
   > foot in the door. **Because once we can prove that they can trust us with their data, then they'll
   > trust us pretty much with anything. It's a high trust touch point.**" [T]

3. **Aaron's own live engagement is the proof case.** [T]
   > "You're a good example. You've helped them with their most sensitive data, which is not effing up
   > merge and duplicate data — which is literally the lifeblood of their business. Because if you take
   > that away, then they can't prospect and can't get leads. So you prove that, then they give you
   > more responsibility. Hence the Yardi, GoFind [GARBLE], other 20,000 things. 'I trust you to pull
   > this — hell yeah, let's do it right now.'" [T]

4. **Therefore: land and expand.** *"It's just another way in the door, for us to land and expand."* [T]

5. **And there's messaging in it.** *"There's content messaging behind that 100%. That's such a high
   touch at that point."* [T]

6. **Explicit scope instruction:** *"Claude, scope that for the mid market too, for the big
   multi-location chains."* [T] Worked example: not Orkin (*"way too fucking big"*), but *"a 20
   location, private equity owned [pest control company]... just cleaning up all of their crap in
   their CRM."* [T]

### 6.1 The offer-stacking motion this enables

Alec walked through the packaged version, med spa as the example: [T]

```
  ENTRY:   "We saw you're on Boulevard. The majority of our clients use Boulevard at 10% of its
            capability. Let's do a discovery call and generate X amount more revenue — or we work
            for free until we do."                                    [T, near-verbatim]
             ↓
  LAND:    SMS reactivation campaign, run inside THEIR system         [T]
             ↓
  STACK:   "+$200 [or $1,000–$2,000 setup] and we do a full hygiene cleanse of all your data —
            getting rid of all your dupes, all of your past clients that haven't talked to you
            in 10 years"                                              [T]
             ↓
  EXPAND:  campaigns on the back end, then the rest of the stack      [T]
```

Aaron's reaction to the entry line: *"my god, that'll land."* [T]

Pricing figures mentioned, all **[UNVERIFIED]** and partially **[GARBLE]**: *"$2,000 setup"* for a
standalone med spa; *"$1,000 bucks off that"* for organizing the CRM; *"$200 more"* to stack the
hygiene cleanse; *"$500,000 bucks monthly setting"* [GARBLE — almost certainly "$500/mo retainer"].
**These are conversational, not a pricing model. Do not treat as such.** [INF]

One scope boundary Aaron drew: *"that's PII... It's not like we're going to cross-check verify
personal info from another database out there... but just organizing our CRM — yes."* [T] So: internal
data organization, **not** external PII enrichment against third-party databases. [T]

---

## 7. The Two-Bucket Frame — "the epiphany"

Alec flagged this as a distinct realization from earlier the same day:

> "Note for Claude: Aaron and I had an epiphany earlier where we talked about how every single client
> or prospective client can typically fall into two buckets." [T]

| | **Bucket 1 — Too much volume** | **Bucket 2 — Not enough volume** |
|---|---|---|
| **Definition** [T] | *"so much inbound volume that they couldn't keep up and needed help"* | *"not enough inbound volume — not enough leads to even generate enough business for our AI receptionist to be effective"* |
| **Named examples** [T] | Josh Astone; AFC *"when we met them with their storm roofing situation"* | Mid-market prospects with bloated CRMs / weak lead flow |
| **Lead products** [INF] | Voice AI receptionist, SMS agent, web chat, Yelp agent — capacity products | Lead gen, SEO, SMS reactivation, CRM hygiene — demand + database products |

### 7.1 The critical mechanic: the buckets convert into each other

> "So we want to be able to accommodate for either or, **and lead one to the other**. At the end of the
> day, we find somebody that's not getting enough leads, we help them get more leads, then we plug in
> our systems on the back end. Once they get enough leads, our other systems work for them — and vice
> versa." [T]

**Strategic consequence: there is no such thing as an unqualified prospect in our ICP — only a
differently-sequenced one.** [INF] Bucket 2 is not a rejection queue; it is a pipeline that
manufactures Bucket 1 customers.

**Implementation consequence: every signal in the §3 matrix must be tagged with which bucket it
indicates.** [INF] "Slow Yelp response" is Bucket 1 (drowning). "No SEO presence" is Bucket 2
(starving). A scoring model that sums them without distinguishing them will produce incoherent
recommendations — a company scoring high on both is either a contradiction in the data or a company in
transition, and either way it needs different handling. This is a concrete gap in the model as
described. [INF]

---

## 8. Artifact #3 — The Channel Partnership Play (parallel motion)

This emerged late, from a weekend conversation, and is **a completely different business from
everything above**. [INF] Alec's framing: *"I just had a thought, bro. Hold on."* [T]

### 8.1 The reasoning chain

1. **The platforms sell enterprise voice AI deals and charge enormously for implementation.**
   > "Guess what ElevenLabs charges quarterly to their clients for voice AI retainer, their in-house
   > implementation team. 250K. 250K a quarter." [T] [**UNVERIFIED** — sourced to a single
   > conversation]

2. **But they don't want to deliver it themselves.**
   > "Nobody uses ElevenLabs['s own implementation team]... They go out to these partners **that all
   > suck**, but they do it for less than 250K a quarter obviously." [T] [UNVERIFIED]
   > "A lot of the software companies want to get out of service. They don't want to deal with
   > professional services, especially at a large scale." [T]

3. **The analogy is the HCM/ERP implementation-partner ecosystem.**
   > "You know, like Workday and Ceridian and UKG — they would have implementation delivery partners."
   > [T] Aaron: *"Oh, yeah, yeah, yeah."* [T]
   Referral source: *"Dan Rackley, who owns Calibrate HCM"* — *"bro, you need to go into this space...
   I do implementation for all my Paycom clients"* [T]. Contact at ElevenLabs: *"Noah
   [Wymanheimer?]"* [GARBLE — name uncertain], *"a top exec rep in Denver, he's at ElevenLabs now,
   closing deals"* [T].

4. **We have a differentiated, hard-to-replicate asset: the blueprint + the kit.**
   > "Claude, also look at our experience and what we've built with a blueprint on the voice AI at
   > scale, because not a lot of people are doing this through Claude MCP, nor do you even know how to
   > do it and iterate." [T] [GAP]
   > "What is the thing that you built that is super invaluable to a large scale company that wants to
   > invest in voice AI agents? **The kit, or the blueprint. The kit lives within the blueprint.**" [T]
   Depth of the asset: *"already gone through 700 objections and test calls"* [T]; *"all your blueprint
   work and all the things that we've built over this last, whatever, six months"* [T].

5. **The buyer is the individual AE, not the partner program.** This is the sharpest tactical insight
   in the section: [INF]
   > "So what is that — just buddying up with the sales rep? **Just buddying up with the sales rep.
   > That's all it is.**" [T]
   > "You're just buddying up with the sales rep, getting all the intel. And then you're just selling
   > that sales rep on using you versus their own in-house, because the in-house company sucks and
   > they don't focus any time on it... So you buddy up with a sales rep and you sell it together. The
   > sales rep, sometimes they'll use us to help close the deal — **because we just know more about the
   > product**." [T]
   Aaron: *"Oh, that's brilliant."* [T]

6. **Deal economics sketch** [T] [UNVERIFIED]: *"a 1,000 employee deal, let's just say there's 30 voice
   agents — it's a $60K deal"* + implementation services on top.

7. **Confidence in the sales motion:**
   > "We have a cheaper product... we should win every time. Every time. No reason. We just need to get
   > on the meeting." [T]

### 8.2 The research ask, verbatim

> "So, Claude, let's do a deep dive on Retell's partner program, Synthflow's partner program, Smith AI
> partner program, to see if there's low hanging fruit where we could get in with sales reps and sales
> reps will feed us deals." [T]

> "Research those partner programs on the barrier to entry on the partner program side for
> professional services implementation delivery, because that's a skill set that we've already built
> that's differentiated... Do research on partner programs and how deals would be fed to people like
> us if we were to implement for somebody at ElevenLabs if they sold a large deal. **Look at what their
> in-house capabilities are on their implementation teams versus us as a delivery partner** — because
> once we deliver for them on the voice side, we can land and expand and build through trust as a
> consultant implementation partner." [T]

Also: *"Use Alec's GTM research [committed] within the last week as a starting point, specifically
pointing towards Avoca."* [T] [GAP]

### 8.3 The Retell "Conductor" anecdote

Aaron offered this as a check on the thesis:

> "You know that new little Retell product, the... conductor. So I asked it to check the work, and this
> was like two weeks ago at this point. And it was floored. It was like, wow, no way, are you serious?
> ... That was the first and last question I asked it. I was like, all right, that answered my
> question. If that thing gave me [that reaction], I was like, you're not gonna be able to help me."
> [T]

Alec read this as confirmation: *"I'm really glad you asked that. That confirms my hypothesis on
several things. Actually makes me feel really good."* [T]

**I am marking this [UNVERIFIED] and flagging it as a hypothesis, not evidence.** [INF] It is a single
interaction with one product two weeks ago. It is suggestive and worth testing deliberately. It is not
a basis for a market-entry decision on its own. See §9.6.

---

## 9. Where I'm challenging the logic

Alec explicitly asked for this — *"challenge my logic on this if you need to"* [T], *"play devil's
advocate"* [T], *"don't lie to me"* [T]. Seven items. All **[INF]**.

### 9.1 "Count the boxes" will float the worst companies to the top

The ranking as described sums pain signals. But a company with no website, no SEO, an IVR, slow Yelp
responses, and bad reviews is not necessarily a great prospect — **it may just be a badly run business
with no money.** Pain volume and solvency are not correlated; if anything, at the extremes they're
inversely correlated.

Alec already sensed this — it's exactly the JJ Jardina caveat (*"what we don't want to go hunting for
is companies that don't appear on Google because they're bad companies and have no money to afford to
pay us"* [T]) — but the insight is currently a footnote on one scrape rather than a structural feature
of the scoring model.

**Recommendation:** the score must be **multiplicative across three orthogonal axes, not additive
across one**:

```
  PROSPECT SCORE  =  Pain Score  ×  Ability-to-Pay Score  ×  Reachability Score
                     (§3 matrix)    (revenue proxies)        (§9.3, ease of contact)
```

Any axis near zero should zero out the prospect regardless of the other two. A high-pain,
zero-ability-to-pay company is not a prospect; it's a support ticket we never get paid for.

### 9.2 The "no website" DQ contradicts the JJ Jardina thesis — and the contradiction is where the money is

This is the most important challenge in this document.

The stated rule: no website → DQ, because it implies no money / not a real business. [T]

But the JJ Jardina insight establishes precisely the opposite as possible: **a company can be
high-revenue and simultaneously invisible online.** [T] JJ Jardina *is* the counterexample to the
no-website rule. Referral-driven trades — commercial plumbing, industrial HVAC, commercial
landscaping, restoration — routinely run eight-figure revenue on relationships, repeat contracts, and
a phone number, with no meaningful web presence.

If the DQ is applied as stated, **the very segment Alec called a "money thought" gets filtered out of
the database before it's ever scored.**

**Recommended reconciliation — replace the website DQ with a revenue-proof gate:**

| Website | Independent revenue proof | Verdict |
|---|---|---|
| Has website | — | Score normally on §3 matrix |
| No website | **No** revenue proof | **DQ** — Alec's instinct is right here |
| No website | **Yes** — strong revenue proof | **Highest-value prospect in the database** — zero incumbent vendor, total whitespace, no competitor can find them |

This preserves everything Alec was protecting against while capturing the segment he identified. It
also means the JJ Jardina research (§5) isn't a side quest — **it's the thing that makes the DQ rule
safe to relax.** The two ideas were in tension; this resolves them.

The open question that decides it: **can we source revenue proof independent of Google, at scale?**
That's Q7 in §11 and it is the single highest-leverage research question in the backlog.

### 9.3 The gatekeeping threshold is probably not a headcount number

This is my direct answer to Alec's opening question, and it reframes it.

He asked for an **employee count** threshold. [T] I don't think headcount is the right key. Owner
reachability correlates far more strongly with **owner-operator status** — is the founder still
running the business day to day — than with size.

Concretely: a 40-person owner-operated HVAC company where the founder still answers his cell is far
more reachable than a 12-person shop that got rolled up into a PE platform last year and now routes
everything through a shared services desk. Headcount says nothing about which of those you're looking
at.

**So the search key is likely a bundle of owner-operator markers, not a headcount band:** [INF]

- Owner's surname is in the business name
- No parent company / holding company / PE sponsor in corporate registration
- Single brand, not a franchise or a platform rollup
- Owner personally active on the business's social accounts / review responses
- No corporate email domain conventions (firstname.lastname@) — i.e. still on generic or personal
- Owner listed personally on state licenses, permits, or registrations
- No "Careers" page with formal HR infrastructure

**Headcount then becomes the *volume* proxy (do they have enough inbound for our products to matter),
while owner-operator status becomes the *access* proxy.** [INF] Those are two independent filters that
were collapsed into one question. Separating them is, I think, the actual unlock on the Josh Problem —
and it means "Josh × 3" may well exist in a form the original framing would have missed.

I want to be clear this is a hypothesis to test in Phase 1, not a finding. But it should be tested
*before* we spend research budget looking for a headcount number that may not exist.

### 9.4 IVR cuts both ways

Alec groups IVR with "hiring a receptionist" and "no receptionist" as equivalent signals that voice AI
wins. [T] Competitively, correct — our product beats a phone tree on customer experience.

But **commercially, IVR is a different situation from the other two.** A business with an IVR has
already: made a considered buying decision about call handling, selected a vendor, possibly signed a
contract, trained staff around it, and built process on top of it. That is switching cost, incumbent
displacement, and a longer cycle.

"No receptionist, no IVR, phone rings straight to the owner's cell" is a *greenfield* sale. "Has IVR"
is a *displacement* sale. Same product, materially different motion, different messaging, different
close probability.

**Recommendation:** don't pool them. Split into two segments with separate sequences and separate
expected close rates. It also matters for scoring — greenfield should probably score higher on
velocity even if displacement scores higher on deal size.

### 9.5 Don't read TAM off Apollo coverage

Aaron's data point:

> "Med spa — I've done a search on that before. There's like 500 that exist on Apollo... everywhere in
> the country. It was full geographic... I can't remember accurately if I put a revenue threshold of
> like a million or more. But all I do remember is the amount was not as many as I thought. I did the
> whole country and I remember only getting like 500. I was like, what? This is low." [T]

Aaron's surprise is the correct instinct, but I'd draw the opposite conclusion from it. **~500 is
almost certainly an artifact of Apollo's coverage, not the size of the med spa market.** Med spas are
commonly registered under a physician's professional corporation or a DBA that doesn't match the
consumer-facing brand, which makes them systematically invisible to firmographic databases keyed on
trade name.

**Two consequences:**
1. Do not size any market off Apollo. Use it to assess *contactability*, which is what Aaron actually
   observed — and that's genuinely useful, because it feeds the Reachability axis in §9.1.
2. Aaron's related observation stands and is important: *"Med spa is the weird one that crosses the
   line, where everything else, all the other things, small scale, they're not gonna be hitting on
   Apollo, but med spa — those people may be able to be found."* [T] **Contact-data availability varies
   enormously by industry, and that variance is itself a targeting criterion.** This independently
   validates Alec's "ease of contact" tiebreaker (§7 of the matrix work / Q18).

### 9.6 The channel play is a different company, and that's a focus risk

I think §8 may be the single highest-expected-value idea in the transcript. I also think it shares
**zero components** with the SMB scraped-list motion:

| | SMB motion (§2–§7) | Channel motion (§8) |
|---|---|---|
| Buyer | Owner-operator / VP Ops | AE at a voice AI platform |
| Discovery | Massive scrape + score | Relationship, one rep at a time |
| Cycle | Short, transactional | Long, trust-built |
| Delivery | Productized, repeatable | Enterprise implementation |
| Asset used | The trigger matrix | The blueprint + kit |
| Constraint | Deliverability (§9.7) | Partner program gatekeeping |

Running both in parallel with a small team is a real risk of doing neither well. **Recommendation:**
scope §8 as a separate, explicitly-resourced track with its own owner and its own success metric —
not as a column in the prospecting matrix. It should not compete for the same research or execution
cycles.

Also worth noting: the entire §8 thesis currently rests on **one weekend conversation, one anecdote
about ElevenLabs' pricing, one referral from Dan Rackley, and one interaction with Retell's Conductor.**
Every load-bearing fact is [UNVERIFIED]. That's fine for a hypothesis — it's not fine for a plan. The
cheapest possible validation is one conversation with the ElevenLabs contact, and that should precede
any partner-program deep dive.

### 9.7 "Massive scrape" and "can't send volume" need to be reconciled explicitly

The deliverability constraint is stated in absolute terms:

> "I don't think we should ever do anything like that... they just can't spam. Even if they do the
> warning and all that stuff... if you go too crazy on the volume, then you get pushed to spam, which
> is why people tread very lightly thinking about sending anything from Alec at LeepAI to [anyone].
> **Because once you get spam, then your inbox is shut down. And then you gotta burn that domain.**
> That's our burned website. That's everything." [T]

The domain is being treated — correctly — as a **critical, non-expendable asset.** [T] [INF]

Alec then closed the loop himself:

> "This is good because this circles back to the front of the conversation. And that's exactly why
> we're gonna take whatever list we generate for that mid market... and go after these mid-market
> people." [T]

**The principle I'd state explicitly, because it's implied but never said outright:** [INF]

> **Scrape wide to select narrow.** The massive scrape exists to *select* a small number of accounts,
> not to *feed* a high-volume send. Breadth of scraping buys precision of targeting, not volume of
> outreach.

This has a hard consequence that should be decided consciously in Phase 3: **what is the target list
size?** If we can't send volume, then per-touch conversion has to be extraordinary, which means the
list is dozens to low hundreds of deeply-researched accounts — not thousands. That number determines
how much scrape breadth is even worth building. Right now it's undefined, and every downstream
estimate depends on it.

---

## 10. Blocker: I don't have the sources

Standing rule from the transcript: *"Never speak... without being able to cite your source on it"* [T]
and *"use as much [data] as we have from our current existing sources on all these things"* [T].

**The `Team-brain` repository currently contains exactly one file: `README.md`.** [Verified — `git
ls-files`] None of the following referenced sources are available to me:

| Source referenced in transcript | Needed for |
|---|---|
| Aaron's SEO deep research [T] | Q10 — cheap at-scale SEO signals; SEO column rows |
| Alec's GTM research from last week, esp. **Avoca** [T] | Q17 — ceiling analysis; §8 competitive framing |
| The **voice AI blueprint** and **the kit** [T] | §8 — the entire differentiation claim |
| **JJ Jardina** project details (*"Alec is going to push to my inbox"*) [T] | Q7 — the reverse-engineering formula; §5 |
| **AFC** account detail (storm roofing; the lost Friday job) [T] | Bucket 1 archetype; web chat triggers |
| **Josh Astone** account detail [T] | The entire ICP baseline — "Josh × 3" is undefined without it |
| **Armand** and **Aisha** accounts [T] | Q12 — SMS chat agent triggers |
| The HVAC + plumbing scrape (*"part of the thousand"*) [T] | Q3/Q4 — what scraping already works, at what yield |
| The med spa Apollo search [T] | Q23 — contactability baseline |
| The existing product **column list** [T] | §3 — confirming I have all products |
| Prior Claude output: *"73% of a med spa's revenue is repeat business"* [T] | Q23 — needs re-sourcing |

**Phase 1 cannot start properly until these are in the repo or otherwise provided.** Without them,
researchers will either work from public sources only (losing all the proprietary advantage the
transcript is built on) or silently invent grounding — which is precisely what the "cite your sources"
rule exists to prevent.

**Ask:** drop these into `Team-brain` (raw is fine — exports, notes, docs, transcripts). Josh Astone
and JJ Jardina are the two highest-priority, because "Josh × 3" is the definition of the target and JJ
Jardina is the formula behind the highest-value segment.

---

## 11. Research backlog — 24 questions scoped for Phase 1

Grouped by workstream. Priority: **P0** = blocks other work; **P1** = core; **P2** = valuable, not
blocking. "Blocked" = requires a §10 source.

### A. Feasibility of the core mechanism

| # | Question | Pri | Blocked |
|---|---|---|---|
| Q1 | Does a size band exist with high volume/budget but low gatekeeping? Is the key headcount, or owner-operator status (§9.3)? | **P0** | Josh Astone |
| Q2 | Can any commercially available database search at that granularity and scale to find "Josh × 3"? | **P0** | Josh Astone |
| Q3 | Which of these can actually be mass-scraped, at what cost/yield/legality: no-good-website · IVR present · Yelp response >1hr · SEO rank #4–10 · hiring a receptionist · reviews citing missed calls · "500+ customers" claims · incumbent software stack | **P0** | — |
| Q13 | Can incumbent software stacks be detected at scale? Which incumbents' built-in features are a wedge vs. a genuine DQ? | P1 | — |

### B. The JJ Jardina / negative-space problem

| # | Question | Pri | Blocked |
|---|---|---|---|
| Q7 | Reverse-engineer JJ Jardina: what makes a high-revenue business invisible on Google, and how do we formalize a targeting formula that finds rich-and-invisible while excluding poor-and-invisible? | **P0** | JJ Jardina |
| Q6 | Is there any tool or method to find businesses with no Google/SEO presence, given a Maps-based scrape structurally cannot see them? What non-Google sources exist (licenses, permits, DOT/fleet, contractor boards, associations, job boards)? | **P0** | — |
| Q5 | Is Google Maps presence a valid proxy for or signal about SEO configuration? | P1 | — |
| Q8 | Confirm or overturn the "no website = DQ" rule; evaluate the revenue-proof gate proposed in §9.2 | **P0** | — |

### C. Per-product trigger definition

| # | Question | Pri | Blocked |
|---|---|---|---|
| Q10 | Which SEO signals are cheaply detectable at scale and indicate poor SEO + high headroom, without a full per-site audit? | P1 | Aaron's SEO research |
| Q9 | Which website signals indicate both need for maintenance AND ability/willingness to pay for it? | P1 | — |
| Q11 | Can the Yelp agent port to Angi or other platforms? API access, ToS, response-time data availability | P1 | — |
| Q4 | Which industries meaningfully use Yelp beyond auto detailing, HVAC, plumbing? | P1 | The thousand-scrape |
| Q12 | Has the SMS chat agent been sold standalone? What trigger profile do Armand + Aisha imply? | P1 | Armand, Aisha |
| Q22 | Is there a definable lead-gen product for Bucket 2, and how do we pinpoint Bucket 2 prospects? *(Explicitly time-boxed: "don't go crazy on this... just bake it in")* | P2 | — |
| Q14 | Define the CRM hygiene/optimization retainer: scope, pricing, liability, PII boundary, scalability to multi-location | P1 | Aaron's live engagement |

### D. Industry × Size matrix (Artifact #2)

| # | Question | Pri | Blocked |
|---|---|---|---|
| Q15 | Define small/mid/large **per industry** (in thirds, per Alec), build the matrix, score every cell against the full trigger set, recommend the best cell — **with a TAM sanity check** | **P0** | — |
| Q19 | Per industry, what is the optimal lead product and full-stack sequencing? (Med spa is the worked example: lead with SMS reactivation, not voice AI) | P1 | — |
| Q23 | Verify the "73% of med spa revenue is repeat business" figure; explain the Apollo ~500 count (§9.5) | P2 | Prior Claude output |
| Q18 | Of the resulting cells, which is easiest to get a decision maker on the phone or in the inbox? *(Alec: this is the tiebreaker and the starting point)* | **P0** | — |

### E. Our ceilings

| # | Question | Pri | Blocked |
|---|---|---|---|
| Q16 | What is our **delivery** ceiling — max locations/complexity we can implement on a viable timeline? (Alec guesses ~20 locations; must be derived from actual delivery data, not asserted) | **P0** | Delivery data |
| Q17 | What is our **sales-process** ceiling — where does enterprise procurement / IT security / PE vendor process make us non-competitive? Where's the multi-location sweet spot in between? | **P0** | Alec's GTM research, Avoca |

### F. Channel partnership (Artifact #3)

| # | Question | Pri | Blocked |
|---|---|---|---|
| Q21 | Validate the $250K/quarter ElevenLabs implementation retainer figure — cheapest path is one call with the ElevenLabs contact | **P0** | Contact name |
| Q20 | Deep dive: Retell, Synthflow, Smith AI, ElevenLabs partner programs — barrier to entry, deal routing to partners, in-house vs. outsourced implementation capacity, AE-level partnering motion, economics | P1 | Blueprint/kit |
| Q24 | Is there a saleable data product in its own right (e.g. ID'd med spa owner personal emails)? Legal and ethical boundary check required | P2 | — |

---

## 12. Transcription ambiguities requiring human confirmation

The instruction was *"just make sure nothing gets lost."* [T] These items are garbled and would
corrupt downstream research if guessed at:

| Heard as | Likely | Impact if wrong |
|---|---|---|
| *"Filling blanks, Sarah, what are our other products?"* | A third participant on the call, or a mis-transcription | **May mean the product column list is incomplete** — highest impact item here |
| *"pollution"* (in the industry list) | "pool service" / "pool cleaning"? | Wrong industry enters the matrix |
| *"Noah Wymanheimer"* | Name uncertain | Can't reach the ElevenLabs contact (blocks Q21) |
| *"Josh Astone"* | Name uncertain | Can't locate the baseline ICP account |
| *"the Yardi, GoFind"* | Yardi = property mgmt software; "GoFind" unclear | Misreads the expansion case study |
| *"$500,000 bucks monthly setting"* | "$500/mo retainer" | Pricing model off by 1000× |
| *"Nescons is excellent, Mars"* / *"Mascot"* | Med spa segment discussion | Garbled around a real strategic point |
| *"largest 10 to 12"* vs *"5 to 10"* | Size tiers were spoken as illustrative guesses, not decisions | Tiers must be derived in Q15 regardless |
| *"Avoca"* | Company name — spelling unconfirmed | Blocks Q17 research |
| *"part of the thousand"* | A prior ~1,000-record scrape | Can't locate prior scrape results |

---

## 13. Standing rules extracted from the transcript

These govern all four phases:

1. **Read slowly, capture everything, lose nothing.** *"That was like an hour of dump."* [T]
2. **Cite every source. Never assert without one.** [T] → the tagging convention in §0.
3. **Use internal material first.** Aaron's SEO research, Alec's GTM research, the blueprint/kit,
   existing client accounts, prior scrapes. [T] → blocked, §10.
4. **Play devil's advocate. Don't lie. Challenge the logic.** [T] → §9.
5. **Don't rabbit-hole.** Specifically time-boxed on the lead-gen/Bucket-2 thread: *"don't go crazy on
   this, don't rabbit hole forever on this front, but just bake it in."* [T]
6. **Respect the phase gates.** Research does not become a plan until it passes an audit. [T]
7. **Protect the sending domain absolutely.** No volume email. Ever. [T] → §9.7.
8. **PII boundary:** organize the client's own data; do not cross-reference personal information
   against external databases. [T]
9. **Lead with the product that matches the industry's dominant pain, not with our flagship.** Med spa
   is the proof: *"if you tell a med spa — the majority of med spas — that's not their pain point, is
   missing calls. It's upselling and making sure they're touching their current client base."* [T]

---

## 14. What I'd want decided before Phase 1 launches

Four decisions, because each one changes what the research should even look for:

1. **Target list size.** Given no-volume-email, are we building a list of 50, 500, or 5,000? This
   determines how much scrape breadth is worth building. (§9.7)
2. **Is the channel play in or out of scope for this cycle?** If in, it needs its own owner and
   budget; if out, defer §8 entirely rather than half-running it. (§9.6)
3. **Do we accept the revenue-proof gate replacing the no-website DQ?** This determines whether the JJ
   Jardina workstream is core or optional. (§9.2)
4. **Do we test owner-operator status as the access key before spending on a headcount answer?**
   (§9.3)

And the one hard dependency: **the §10 sources.** Josh Astone and JJ Jardina first.
