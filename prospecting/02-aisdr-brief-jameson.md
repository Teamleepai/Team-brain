# AI SDR Build Brief — Jameson

**Date:** 2026-08-05 · **Rev 2** — retooled for the call-first cadence
**Depends on:** `00-readback-and-research-backlog.md`, `01-pain-signal-matrix-and-icp.md`
**Structure:** Part A is for Aaron and Alec. Part B is the prompt Jameson uses.

---

# PART A — Read before handing anything to Jameson

## A.0 What changed in Rev 2, and where I was analyzing the wrong thing

Rev 1 recommended dropping prospect-facing SMS. **Aaron overruled it with the actual cadence, and the
cadence changes the analysis.** I was evaluating cold SMS to strangers. What he described is SMS *after a
live human conversation* — a materially different legal posture and a much better motion.

The cadence as given:

```
  1. AI SDR researches the company against the pain signal matrix
  2. AI SDR returns the top pain signals custom to that company
  3. HUMAN cold calls into it
  4. Human states the pain signals, harvests the objections
  5. If good fit — or even a decent objection — hand off to
  6. SMS cadence + email + further calls, on repeat, AI SDR replying in seconds
```

**This is a better design than what I proposed** and it solves the collision I raised in Rev 1: the
strongest signal in the matrix, "main line rings to a mobile," is a bad cold-*text* target but a perfect
cold-*call* target. Calling it is fine. The cadence routes around the problem.

**But one link in the chain doesn't hold as described, and I have to be direct about it.**

## A.1 A verbal "sure, text me" is not valid consent for marketing SMS

This is the one thing in the plan I'd stop and fix before anything ships.

| Finding | Source |
|---|---|
| Marketing texts to a cell require **Prior Express Written Consent** — the strictest standard | [activeprospect.com](https://activeprospect.com/blog/tcpa-consent/), [termsfeed.com](https://www.termsfeed.com/blog/sms-marketing-consent/) |
| **"Verbal, audio, or recorded presentation of the terms is not sufficient for PEWC."** A verbal OK does not satisfy it | [termsfeed.com](https://www.termsfeed.com/blog/sms-marketing-consent/), [leadcompliant.com](https://leadcompliant.com/articles/consent-and-optin/tcpa-sms-marketing-requires-prior-express-written-consent-opt-in) |
| Written **includes electronic** — online forms, email, e-signature — under E-SIGN | [termsfeed.com](https://www.termsfeed.com/blog/sms-marketing-consent/) |
| You must be able to prove **what the opt-in said at the time it was collected** | [activeprospect.com](https://activeprospect.com/blog/tcpa-text-messages/) |
| $500–$1,500 per violating message, no cap | [activeprospect.com](https://activeprospect.com/blog/tcpa-text-messages/) |

So step 5→6 as described — rep hears a decent objection, pushes to SMS — **creates exposure on every
message sent**, because nothing written was ever captured.

### The fix is cheap, and it makes the funnel better

Don't ask "can I text you?" on the call. **Make the prospect perform a written action.** Any of these
produce documented electronic consent:

1. **They text you first.** "Text me the word AUDIT at this number and I'll send the three things I
   found." An inbound text from their handset is written, electronic, timestamped consent.
2. **A one-field opt-in link,** sent by email while you're still on the phone. They click, it logs the
   consent language and the timestamp.
3. **Email reply.** "Reply YES and I'll text you the breakdown." The reply is the written record.

All three take ten seconds and are natural sales moves, not compliance theater.

**And here's the part worth noticing:** a prospect who performs a ten-second written action is
measurably more engaged than one who mumbled "sure." **The consent requirement is a qualification
filter, not friction.** It gates the AI SDR to prospects who did something — which is the sniper
doctrine, enforced by law rather than by discipline.

**Log for every prospect who enters the cadence:** exact consent language shown, timestamp, channel,
IP or message ID, and the recording or notes of the call that preceded it. That record is the entire
defense. No consent artifact, no channel entry — enforced in code, not policy.

## A.2 Do not use your own voice AI for the cold calls

This one matters specifically because you sell voice AI, so the temptation is built in.

| Finding | Source |
|---|---|
| FCC Declaratory Ruling, **8 February 2024** (unanimous): TCPA rules apply to calls using AI-generated voices | [wiley.law](https://www.wiley.law/alert-FCC-Extends-Regulatory-Reach-Over-AI-Announces-TCPA-Restrictions-Cover-AI-Generated-Voices-in-Outbound-Calls) |
| Covers **"real-time conversational AI, voice cloning, and large-language-model-driven agents."** The statute "does not allow for any carve out of technologies that purport to provide the equivalent of a live agent" | [henson-legal.com](https://www.henson-legal.com/ai-voice-compliance), [celloip.com](https://celloip.com/blog/tcpa-compliance-ai-outbound-calling/) |
| Outbound AI voice for **marketing requires prior express written consent** | [klariqo.com](https://klariqo.com/blog/tcpa-compliance-ai-voice-agents/), [retellai.com](https://www.retellai.com/blog/tcpa-compliance-playbook-voice-ai-outbound) |
| $500–$1,500 per call, trebled for willful, no cap | [agxntsix.ai](https://agxntsix.ai/blog/tcpa-rules-ai-voice-calls-2026) |
| An **August 2024 NPRM** proposes mandatory in-call AI disclosure and AI-specific consent language | [wiley.law](https://www.wiley.law/alert-FCC-Extends-Regulatory-Reach-Over-AI-Announces-TCPA-Restrictions-Cover-AI-Generated-Voices-in-Outbound-Calls) |

Steps 3 and 4 of the cadence must be **a human being dialing and talking.** That's legal and needs no
prior consent for B2B manual dialing. The moment an AI voice makes that first call, you need written
consent you don't have yet — the exact thing the call was supposed to earn.

Your voice AI is a product you sell and a tool for *inbound* on consented lines. It is not a
cold-prospecting tool. Selling the thing does not exempt you from the rule governing it — and you would
be an unusually visible defendant.

## A.3 The revised gate model — your goal and the risk both get served

Rev 1 put a human gate before every send. **That was right for cold email and wrong for your cadence.**
With a call-first motion the gate moves to a better place:

| Stage | Who | Autonomy |
|---|---|---|
| 1 · Discover candidates | AI SDR | **Autonomous** |
| 2 · Research + hypothesis + refutation | AI SDR | **Autonomous** — the whole edge lives here |
| 3 · Build the call sheet | AI SDR | **Autonomous** |
| 4 · Cold call | **Human. Legally required** | Manual |
| 5 · Capture written consent | Human asks, prospect acts | **HARD GATE** |
| 6 · SMS + email cadence, replies in seconds, objection handling | AI SDR | **Autonomous** |
| 7 · Book the appointment | AI SDR, bounded | **Autonomous** |
| Escalation | Human, immediately | Trigger-based |

**The gate moved from "before every message" to "at channel entry."** That is simultaneously safer
legally and faster operationally — exactly what you asked for. Once a prospect has opted in writing and
spoken to a human, an autonomous agent replying in seconds is low-risk and high-value. Before that, it's
the whole liability.

### What the autonomous reply agent must be bounded by

Seconds-latency autonomy has one dominant failure mode: **the agent inventing commitments.** Pricing it
can't honor, integrations that don't exist, timelines nobody agreed to. Non-negotiable guardrails:

- **A versioned claim registry.** The agent may assert only facts drawn from an approved list. Anything
  outside it escalates. This is the single most important guardrail in the build.
- **Instant, absolute opt-out handling.** STOP is legally mandatory and must work on the first attempt.
- **Escalation triggers:** legal threat, opt-out, anger, competitor mention, enterprise scale, pricing
  negotiation past published terms, or any question the claim registry can't answer.
- **Bounded calendar authority.** Which slots, how many per week, and a minimum qualification bar before
  it may book. An AI that fills Aaron and Alec's calendar with bad fits is worse than one that books
  nothing.
- **Quiet hours,** per state law, enforced in code.
- **AI disclosure** — see A.4.
- **Hard volume cap and a kill switch** that any of the five of you can pull.

## A.4 Disclose that it's an AI, because your outbound *is* the demo

The FCC is already moving toward mandatory in-call AI disclosure. But the stronger argument is
commercial, not legal.

**You sell AI agents. A prospect having a fast, sharp, genuinely useful exchange with your AI SDR is
experiencing your product.** That is the highest-fidelity proof of capability you will ever generate,
and it costs nothing extra.

Disclosure converts the interaction from a deception risk into a live demo: *"You've been talking to our
AI SDR for the last four minutes. That's what we build."* Hiding it inverts the asset — getting caught
pretending to be human, with a buyer who cares about AI, damages the exact credibility you're selling.

## A.5 "Training data" — what I meant, and the good news

Fair challenge; I was unclear. **I mean examples of how you two actually sell.** A model can't imitate a
voice it has never seen. Specifically:

- Recordings or transcripts of Aaron and Alec running real discovery calls
- The messages that actually produced booked meetings
- Objections you've faced and the language that beat them
- The Jobber / HouseCall Pro win narrative
- The objection library from the ~700 voice AI test calls

Without these, "best-trained Straz" produces competent generic sales copy with your names on it — which
is *worse* than neutral, because it sounds like every other tool in the inbox.

**The good news: your own cadence generates this as a byproduct.** Steps 3–4 are humans making cold
calls and harvesting objections. Record them (with consent — see A.7) and that corpus *is* the training
data. Every call improves the SDR. The motion is self-feeding, which means the right sequence is: run
the human calls first, build the voice from the transcripts second. Don't try to write the voice before
you have the recordings.

## A.6 Domain — and a spelling flag

You said **itsleapai.com**. Your brand is Leep AI and your email is `@leepai.io` — **leep**, not
**leap**. Two possibilities: it's an intentional play, or it's how "it's Leep AI dot com" came out in
speech and you actually want `itsleepai.com`. **Confirm before buying.** A lookalike-but-misspelled
domain is hard to undo, reads as a phishing pattern to filters, and costs trust with exactly the buyers
who look closely.

Separate prospecting domain is the right call regardless. Two things to plan for:

- **A new domain has no reputation.** Budget warmup time before real sends, and stand up SPF, DKIM and
  aligned DMARC plus one-click unsubscribe from day one. In 2026 failing sender checks means outright
  rejection, not the spam folder. [[inboxkit.com](https://www.inboxkit.com/learn/google-yahoo-sender-requirements-2026)]
- **The 5,000/day Gmail bulk-sender line is permanent once crossed** and never expires even if volume
  drops. [[mailover.ai](https://mailover.ai/blog/bulk-sender-requirements.html)] At sniper volume you're
  two orders of magnitude below it — cap it in code anyway so it can't happen by accident.

## A.7 Call recording consent

If you're recording the cold calls — and you should, per A.5 — some states require **all-party** consent,
not one-party. Get the state list and build the disclosure into the opener. It's one sentence and it also
strengthens your consent trail.

## A.8 Sandbox and command center — my honest recommendation

You asked for the best answer, not the easy one. **The most important decision here isn't the sandbox —
it's where the SDR's behavior lives.**

### Config-as-code, in git. Not in a database, not in code.

Every piece of behavior you five want to edit — prompts, goals, tools, claim registry, signal
definitions, cadence timing, escalation triggers, guardrails — belongs in **YAML and markdown files in a
version-controlled repo**, read by the agent at runtime.

**Why this and not an admin panel with a database:** five non-engineers editing agent behavior will
produce a moment where reply quality drops and nobody knows what changed. Git gives you diff, blame,
rollback and review natively. A database-backed panel gives you none of that. When Shally changes a
prompt on Tuesday and bookings fall on Thursday, `git log` answers it in seconds and a database answers
it never.

### Your day-one frontend already exists: GitHub's web editor plus pull requests

Free, works in a browser and on a phone, and gives you review and audit trail for nothing. All five of
you can edit YAML in it today. **Don't build a custom command center until you've actually felt the
friction** — and when you do, build it as a thin wrapper that commits to those same files, never as a
separate store.

Being straight with you: a real custom command-center UI is a two-to-four week build for a competent
developer, and **Jameson should not own the production version of it.** Config files first. Measure
whether the friction is real. Then decide.

### Sandbox spec

| | |
|---|---|
| **GHL** | Dedicated sub-account with no real client data. The MCP server is scoped per location, so this is naturally clean isolation |
| **Sending domain** | A throwaway domain — **not** itsleepai.com. Protect the real one through development |
| **Recipients** | Team-owned numbers and inboxes only, seeded as test contacts. Never a real prospect |
| **Production access** | Read-only token if he needs to inspect real schema. Write access in sandbox only |
| **A2P brand** | No access. This is the asset that can take your clients' SMS down with it |
| **Code guards** | `SANDBOX_MODE` defaulting to true and only disableable by Aaron or Alec; hard volume cap; kill switch all five of you can pull |
| **Research targets** | Real public companies are fine to research — it's public data, read-only. Sending to them is not |

## A.9 Still open

1. **Confirm the domain spelling** before purchase (A.6).
2. **Pick the consent mechanic** from A.1 — inbound text, opt-in link, or email reply. This is the one
   thing I'd want an attorney to bless, and it's now a narrow, cheap question: *does our consent language
   and logging meet PEWC?* rather than *can we do this at all?*
3. **Confirm humans make the cold calls** (A.2).
4. **Decide on AI disclosure** — I recommend yes, loudly (A.4).
5. **Start recording calls now.** Every unrecorded call is training data you can't get back (A.5).

I am not an attorney. Everything above is cited secondary sources. The exposure is large enough that an
opinion letter on the consent mechanic is cheap insurance.

---

# PART B — The prompt for Jameson

Copy everything between the rules. Written to be pasted into Claude with this file and the two
prospecting docs attached.

---

> ## MISSION
>
> You are building the AI SDR behind a sniper outbound motion for Leep AI — a boutique AI services firm
> selling voice AI receptionists, SMS and web chat agents, SEO, Yelp agents, SMS reactivation, website
> services and CRM data consulting into home services and med spa businesses.
>
> I am Jameson, an intern. Treat me as capable but unproven: explain your reasoning, and do not let me
> ship something dangerous just because I asked for it confidently.
>
> **Doctrine: sniper, not spray.** Roughly 20–50 prospects a day, deeply researched. Every message earned
> by evidence. A message we cannot defend line by line is worse than no message, because the entire
> differentiation is that we did the work.
>
> ## THE CADENCE YOU ARE BUILDING FOR
>
> ```
>   1  RESEARCH        AI SDR researches the company against the pain signal matrix   ← autonomous
>   2  BRIEF           AI SDR returns the top custom pain signals + call sheet         ← autonomous
>   3  COLD CALL       A HUMAN dials and talks                                         ← human, required
>   4  HARVEST         Human states the signals, collects objections                   ← human
>   5  CONSENT         Prospect performs a WRITTEN opt-in action                       ← HARD GATE
>   6  CADENCE         SMS + email + further calls, AI replying in seconds,
>                      handling objections, booking appointments                       ← autonomous
>   7  ESCALATE        Handoff to a human on defined triggers                          ← trigger-based
> ```
>
> Two rules define the whole architecture:
>
> - **Nothing autonomous touches a prospect before stage 5.** Research and drafting are autonomous;
>   first contact is a human on the phone.
> - **After stage 5, speed is the product.** Replies in seconds to minutes. That is the goal, and it is
>   safe *because* consent and a human conversation precede it.
>
> ## NON-NEGOTIABLE RULES
>
> 1. **Never state anything you cannot cite.** Every claim about a tool, law, price, capability or
>    prospect carries a source — URL, API response, file path, or timestamped artifact. If you can't
>    source it, label it unsourced and treat it as a question, not a finding.
> 2. **Never fabricate.** Not a statistic, capability, integration, or prospect detail. If unsure whether
>    an endpoint exists, check it or say you didn't.
> 3. **Tag everything** `[VERIFIED]`, `[INFERRED]`, or `[UNKNOWN]`. An inference dressed as a fact is the
>    failure mode that ends this project.
> 4. **No consent artifact, no channel entry.** Enforced in code, not policy. See the consent gate.
> 5. **No AI voice on outbound cold calls, ever.** FCC Declaratory Ruling of 8 February 2024 places
>    AI-generated voices — explicitly including real-time conversational agents — under the TCPA's
>    artificial-voice restrictions, which require prior express written consent for marketing. We won't
>    have it at stage 3. Humans dial. Verify this yourself and tell me if I've got it wrong.
> 6. **You work in a sandbox.** No real client data, no production sending credentials, no A2P brand
>    access. If you've been given any of those, stop and say so.
> 7. **Surface bad news in the first paragraph.** If the architecture won't work, a tool doesn't do what
>    its marketing claims, or the plan has a hole — lead with it. You will never be penalized for
>    reporting a problem, only for burying one.
>
> ## THE CONSENT GATE — stage 5, and it is absolute
>
> A verbal "sure, text me" is **not** valid consent for marketing SMS. Marketing texts to a cell require
> Prior Express Written Consent, and verbal or recorded agreement does not satisfy it. Written includes
> electronic — forms, email replies, inbound texts — under E-SIGN. Verify this and correct me if I'm
> wrong.
>
> Build the gate so a prospect cannot enter the SMS or email cadence without a stored consent record
> containing:
>
> | Field | Why |
> |---|---|
> | Exact consent language shown at the time | You must prove what they agreed to, not what the form says today |
> | Timestamp | |
> | Channel and mechanism | inbound text / opt-in link / email reply |
> | Message ID or IP | The technical artifact |
> | Reference to the preceding call | Recording or notes |
> | Opt-out status and history | Must be instant and absolute |
>
> **Never overwrite consent language.** Version it. If it changes, old records keep the old text.
>
> Evaluate the three mechanics and recommend one, with the tradeoffs: prospect texts a keyword first;
> one-field opt-in link sent during the call; email reply confirmation. Judge each on legal strength,
> friction, and how naturally it fits a live sales conversation.
>
> ## THE EVIDENCE GATE — operationalizing "cannot be refuted"
>
> A prospect only reaches the call sheet when **every** condition holds. Enforce in code.
>
> | # | Condition | Fails if |
> |---|---|---|
> | 1 | **Fresh** — signal re-verified within 7 days | Pulled from a cache older than 7 days |
> | 2 | **Artifacted** — timestamped raw artifact exists | The claim exists only as a model assertion |
> | 3 | **Refuted and survived** — an adversarial pass tried to kill it and failed | No refutation was attempted |
> | 4 | **Specific** — names one product and one defensible claim | Generic ("could use marketing help") |
> | 5 | **Can pay** — two independent ability-to-pay proxies | Pain only, no solvency evidence |
> | 6 | **Reachable** — owner-operator markers, below committee threshold | Committee-scale or no identified DM |
> | 7 | **Error modes checked** — the detection method's known false positives ruled out | Unmeasured false-positive rate |
>
> Scoring is **multiplicative: Pain × Ability to Pay × Reachability.** Any factor near zero zeroes the
> prospect. Counting boxes floats badly-run insolvent businesses to the top — read
> `01-pain-signal-matrix-and-icp.md` §2 before writing the scorer.
>
> **The refutation pass is the heart of it.** Run an independent check whose explicit job is to prove the
> signal wrong, defaulting to "refuted" under uncertainty. Is the job posting already filled? Is that
> "IVR" just a business-hours greeting? Is the slow Yelp response an artifact of how Yelp computes it? Is
> this even the right entity, or a similarly-named one? Only signals that survive a hostile reading earn
> a call.
>
> ## BOUNDING THE AUTONOMOUS REPLY AGENT
>
> Stage 6 replies in seconds without human review. Its dominant failure mode is **inventing
> commitments** — pricing, integrations, timelines nobody agreed to. Build these before the agent sends
> anything:
>
> - **A versioned claim registry.** The agent may assert only approved facts. Anything outside it
>   escalates rather than improvises. **This is the most important guardrail in the build** — design it
>   first and tell me how you enforce it, not just that you will.
> - **Instant opt-out.** STOP works on the first attempt, across both channels, permanently.
> - **Escalation triggers:** legal threat, opt-out, anger, competitor mention, enterprise scale, pricing
>   past published terms, or any question the registry can't cover.
> - **Bounded calendar authority.** Which slots, how many per week, and a minimum qualification bar
>   before booking. An agent that fills two closers' calendars with bad fits is worse than one that books
>   nothing. The CRO council role owns this.
> - **Quiet hours** by state, enforced in code.
> - **AI disclosure.** Recommended: disclose plainly. We sell AI agents — a prospect having a sharp
>   exchange with our AI SDR is experiencing the product. Disclosure turns it into a demo; concealment
>   turns it into a credibility risk with the exact buyer who'd care. Research any state disclosure
>   requirements and the status of the FCC's August 2024 NPRM on mandatory AI disclosure.
> - **Hard volume cap and a kill switch** any of five named people can pull.
>
> ## RESEARCH ASSIGNMENT ONE — compliance, and you hold a veto
>
> **This section outranks every other instruction here. If compliance and the mission conflict,
> compliance wins, you stop, and you tell me.**
>
> Establish and cite:
> - PEWC for marketing SMS: what qualifies as written, whether verbal suffices, and what a defensible
>   consent record contains.
> - The FCC's 8 February 2024 AI-voice Declaratory Ruling and what it means for outbound calling.
> - A2P 10DLC: carrier consent expectations, and specifically **whether a violation can suspend a brand
>   registration that also serves client delivery.** Highest-stakes open question in the build.
> - CAN-SPAM for the email leg: identification, opt-out, physical address.
> - State laws stricter than federal on SMS, calling hours, and telemarketing. Florida and Oklahoma are
>   known examples — verify and find the rest.
> - **Call recording consent:** which states require all-party consent, and the exact disclosure sentence
>   for the opener.
> - Whether prospecting SMS and client-delivery SMS can share infrastructure. My strong prior is no.
>
> **Deliver a one-page compliance boundary document first, before any code.**
>
> ## RESEARCH ASSIGNMENT TWO — the buildout
>
> Confirm rather than assume. Tell me where Part A of the brief is wrong.
>
> **GoHighLevel**
> - Official GHL MCP server: exact tool coverage, auth model, rate limits, and what it *cannot* do.
>   Verify it's included on Unlimited and SaaS Pro and confirm current pricing.
> - The one-connection-per-sub-account scoping constraint — what architecture does that force for
>   multiple locations or clients? A design decision, not a detail.
> - Official vs. community servers (some claim 500+ tools). Assess maintenance, security and token
>   handling. **A community MCP server holding a token that can read every client contact is a
>   supply-chain risk — evaluate it as one.**
> - Which cadence, SMS and email primitives are API-accessible vs. UI-only.
> - Whether GHL's Agent Studio API (March 2026) changes build-vs-configure.
> - How consent records and opt-out state are stored and honored in GHL, and whether that is sufficient
>   as the system of record.
>
> **Agent architecture**
> - Claude Agent SDK: session persistence, permissions, hooks, multi-agent coordination. Map each onto
>   the seven cadence stages. Name the mechanism that implements the stage-5 gate.
> - Compare with the Claude API directly, and LangGraph / AutoGen / Mastra. Recommend one and state what
>   you give up.
> - **Design the prospect dossier first.** A durable record that survives runs, accumulates evidence, and
>   is auditable later. It is the actual product; messages are a by-product.
> - Reply latency architecture: what it takes to answer in seconds, and where the real bottleneck sits.
> - Cost model: tokens per dossier at required depth, therefore cost per dossier and per booked meeting.
>
> **Deliverability**
> - Confirm the Gmail bulk-sender threshold, the permanence of the classification, and complaint-rate
>   targets. Build a cap that cannot be exceeded by mistake.
> - SPF, DKIM, aligned DMARC, one-click unsubscribe. What breaks each.
> - Warmup plan for a brand-new prospecting domain, with a realistic timeline.
>
> **Config and the command center** — five non-engineers (Aaron, Shally, Alec, Javid, Hamza) must be able
> to edit the project, SDR settings, tools, goals and outcomes.
> - **Strong recommendation to validate or refute: behavior lives in version-controlled YAML and markdown
>   read at runtime — not in code, not in a database.** Five people editing agent behavior need diff,
>   blame, rollback and review. When quality drops on a Thursday, `git log` answers why in seconds and a
>   database answers never.
> - Assess GitHub's web editor plus pull requests as the day-one frontend: free, phone-accessible, audit
>   trail included. Argue for or against.
> - If a custom UI is warranted, spec it as a thin wrapper committing to those same files — never a
>   separate store. Estimate honestly, and say plainly whether an intern should own the production build.
> - Design the config schema so a non-engineer can safely change goals and messaging but **cannot**
>   disable a compliance guardrail. That asymmetry is the point.
>
> ## THE COUNCIL — seven adversaries, run before anything ships
>
> Every deliverable passes all seven. Each speaks in its own voice, gives a verdict, cites reasons. **Do
> not soften them and do not let them converge — a council that agrees with me is useless and I will know
> you faked it.** Report dissent verbatim.
>
> **1. The Compliance Officer** — *the only absolute veto.* Every message and mechanism against TCPA,
> PEWC, A2P, CAN-SPAM, recording law and state statutes. Assumes we get sued and asks what the discovery
> file looks like. A veto stops the project until resolved.
>
> **2. The Refuter** — tries to kill every pain signal. Default position: stale, wrong, or misattributed
> entity. Must actively attempt refutation, not merely consider it.
>
> **3. The Prospect** — reads it as the owner receiving it on a Tuesday morning. Rules on one question:
> *does this feel researched, or surveilled?* Veto over tone. Exists because the failure mode of deep
> research is creepiness and we cannot see it ourselves.
>
> **4. The Deliverability Engineer** — owns the sending domain and A2P brand as balance-sheet assets.
> Models cumulative risk across a quarter. Asks what happens on the 400th send.
>
> **5. The CRO** — asks whether this prospect deserves the time of two closers whose muscle is
> $200K–$1.9M complex deals. Kills anything wasting elite capacity on commodity deals. Also owns the
> booking bar: every bad meeting booked is a real cost. Enforces
> `01-pain-signal-matrix-and-icp.md` §4.
>
> **6. The Data Skeptic** — challenges whether the scrape measured what it claims. Demands a false
> positive rate per detection method. Recurring question: *how many of these are wrong, and how would we
> know?*
>
> **7. The Voice Auditor** — judges whether copy sounds like Aaron and Alec or like an AI imitating them.
> Blocks AI tells: "I hope this finds you well," "I noticed that you," "quick question," hollow
> flattery, three-part lists. **Until call recordings and won-deal messages exist, this role returns
> "cannot assess" — say so rather than guessing.**
>
> ## BLIND SPOTS — live risks. Report on each; add as you find more
>
> 1. **The A2P brand may be shared with client delivery.** Losing it stops paying customers' SMS, not
>    just prospecting. Confirm or refute the coupling — highest-stakes open question here.
> 2. **A verbal yes is not written consent.** The cadence's weakest link. Fix at stage 5 or the whole
>    thing carries per-message exposure.
> 3. **AI voice on cold calls is prohibited without written consent** we won't have yet. Tempting because
>    we sell it. Selling it doesn't exempt us.
> 4. **Stale signals destroy credibility precisely because they're specific.** "I saw your receptionist
>    opening" lands worse than a generic email if they filled it a month ago — it proves we didn't
>    actually look. Hence the 7-day rule. Test it.
> 5. **The specificity paradox.** A line exists between "did their homework" and "is watching me." "Your
>    posting has been open 47 days" crosses it. Find the line. The Prospect role owns it.
> 6. **Unmeasured false positive rate.** If IVR detection is wrong 15% of the time, 15% of openers are
>    factually false to the one person who knows. Measure before trusting.
> 7. **The reply agent will invent commitments** unless the claim registry is hard-bounded. Assume it
>    will try.
> 8. **Booking bad fits is a real cost,** not a neutral outcome. Two closers' calendars are the scarcest
>    resource in the company.
> 9. **No learning loop is defined.** Nothing specifies how the system learns which signals actually
>    convert. Without it every score weight is a permanent guess. Design the loop.
> 10. **Sniper volume makes statistical testing impossible.** At 20–50/day you cannot A/B test to
>     significance in a useful timeframe. Iteration must be qualitative — call reviews, reply reading,
>     loss reasons. Say so rather than building a dashboard implying otherwise.
> 11. **Every unrecorded cold call is training data lost forever.** Recording must start with call one,
>     with the right disclosure.
> 12. **Five people editing agent behavior will break something.** Config-as-code with review is the
>     mitigation. Guardrails must be structurally uneditable by non-engineers.
> 13. **The scoring model has never been validated against a real win.** Josh Astone and JJ Jardina — the
>     two reference accounts — aren't in the repo. Until they are, the scorer is calibrated against
>     nothing. Note this in every scoring output.
> 14. **We would be committing our own sin if replies lag.** Our pitch is "you lose money responding
>     slowly." Stage 6 latency is not a feature request, it's credibility. Instrument it.
>
> ## HOW TO REPORT
>
> Phase-gated. **Stop at each gate and wait.** A wrong assumption compounds.
>
> | Gate | Deliverable | Blocks on |
> |---|---|---|
> | **1** | Compliance boundary doc, one page, sourced. Consent mechanic recommended with tradeoffs | Human sign-off. Nothing proceeds |
> | **2** | Tooling recommendation: GHL path, agent framework, dossier schema, config architecture, cost per dossier | Human sign-off |
> | **3** | Evidence gate + consent gate implemented, tested against 20 hand-checked prospects. Report the false positive rate you actually measured | Human sign-off |
> | **4** | Ten complete dossiers with call sheets, through all seven council roles, dissent verbatim | Human review of all ten |
> | **5** | The reply agent with claim registry, escalation, opt-out, quiet hours — in sandbox, against team-owned numbers only | Human sign-off |
> | **6** | Config-as-code + frontend editing path demonstrated with all five users | Aaron and Alec only |
>
> At every gate include: what you verified, what you inferred, what you could not determine, and **what
> you think I'm wrong about.** That last one is mandatory and "nothing" is not an acceptable answer.
>
> ## FINAL INSTRUCTION
>
> The measure of this system is not messages sent, or even meetings booked. It is **the percentage of
> conversations where the prospect recognizes our central claim as true and important about their own
> business.**
>
> Optimize for that. It is the only number that compounds.

---

# PART C — Sources

**TCPA consent and PEWC:** [activeprospect.com — TCPA consent](https://activeprospect.com/blog/tcpa-consent/) ·
[activeprospect.com — text messages](https://activeprospect.com/blog/tcpa-text-messages/) ·
[termsfeed.com](https://www.termsfeed.com/blog/sms-marketing-consent/) ·
[leadcompliant.com](https://leadcompliant.com/articles/consent-and-optin/tcpa-sms-marketing-requires-prior-express-written-consent-opt-in) ·
[nelsonmullins.com](https://www.nelsonmullins.com/insights/alerts/fcc-download/all/the-fcc-s-prior-express-written-consent-rule-is-changing-this-month-what-marketers-need-to-know) ·
[FCC one-to-one consent rule (PDF)](https://docs.fcc.gov/public/attachments/DOC-408396A1.pdf)

**AI voice under TCPA:** [wiley.law](https://www.wiley.law/alert-FCC-Extends-Regulatory-Reach-Over-AI-Announces-TCPA-Restrictions-Cover-AI-Generated-Voices-in-Outbound-Calls) ·
[henson-legal.com](https://www.henson-legal.com/ai-voice-compliance) ·
[celloip.com](https://celloip.com/blog/tcpa-compliance-ai-outbound-calling/) ·
[klariqo.com](https://klariqo.com/blog/tcpa-compliance-ai-voice-agents/) ·
[retellai.com](https://www.retellai.com/blog/tcpa-compliance-playbook-voice-ai-outbound) ·
[agxntsix.ai](https://agxntsix.ai/blog/tcpa-rules-ai-voice-calls-2026)

**A2P 10DLC:** [messageiq.io — 10DLC](https://messageiq.io/blogs/10dlc-registration-sms-compliance/) ·
[messageiq.io — TCPA/CAN-SPAM](https://messageiq.io/blogs/avoid-costly-fines-a-guide-to-tcpa-and-can-spam-for-sms-marketing/) ·
[subscriberverify.com](https://subscriberverify.com/blog/tcpa-sms-carrier-restrictions-cold-calling-2026) ·
[justcall.io](https://justcall.io/blog/10dlc-compliance-guide.html)

**Email deliverability:** [inboxkit.com](https://www.inboxkit.com/learn/google-yahoo-sender-requirements-2026) ·
[powerdmarc.com](https://powerdmarc.com/bulk-email-sender-requirements/) ·
[mailover.ai](https://mailover.ai/blog/bulk-sender-requirements.html) ·
[redsift.com](https://redsift.com/guides/bulk-email-sender-requirements)

**GoHighLevel MCP:** [thestackinsiders.com](https://www.thestackinsiders.com/blog/gohighlevel-mcp-server) ·
[netpartners.marketing](https://netpartners.marketing/how-to-use-the-highlevel-mcp-server-ai-powered-gohighlevel-workflows/) ·
[ai.exoticaitsolutions.com](https://ai.exoticaitsolutions.com/blog/gohighlevel-mcp/) ·
[imisofts.com](https://imisofts.com/blog/gohighlevel-mcp-server-ai-agents-news-june-7-2026/)

**Claude Agent SDK:** [beginnersinai.org](https://beginnersinai.org/claude-agent-sdk/) ·
[o-mega.ai](https://o-mega.ai/articles/claude-agent-sdk-the-2026-deep-dive) ·
[technspire.com](https://technspire.com/en/blog/choosing-agent-sdk-2026-claude-langgraph-autogen)

**Not legal advice.** All compliance findings are cited secondary sources. I am not an attorney. The
exposure is large enough that an opinion letter on the consent mechanic is cheap insurance.
