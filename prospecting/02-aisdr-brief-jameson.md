# AI SDR Build Brief — Jameson

**Date:** 2026-08-05
**Depends on:** `00-readback-and-research-backlog.md`, `01-pain-signal-matrix-and-icp.md`
**Structure:** Part A is for Aaron and Alec only. Part B is the prompt Jameson uses.

---

# PART A — Read before handing anything to Jameson

Three findings from the research pass. The first one is a bigger risk than the email domain risk Alec
was so careful about, and it is not obvious.

## A.1 The SMS plan risks the asset your clients run on

Alec's rule on email was absolute and correct: protect the sending domain, never burn it. The SMS half
of this request carries a **larger** exposure, because the asset at risk isn't yours alone.

| Fact | Source |
|---|---|
| Automated marketing texts to a cell phone without prior express written consent carry **$500 per message, trebled to $1,500 for willful violations, with no cap** | [messageiq.io](https://messageiq.io/blogs/avoid-costly-fines-a-guide-to-tcpa-and-can-spam-for-sms-marketing/), [activeprospect.com](https://activeprospect.com/blog/tcpa-text-messages/) |
| A non-compliant campaign to 10,000 contacts is **$5M–$15M** of exposure | [messageiq.io](https://messageiq.io/blogs/avoid-costly-fines-a-guide-to-tcpa-and-can-spam-for-sms-marketing/) |
| **880 TCPA lawsuits filed in the first four months of 2025 alone — up 44% year over year** | [subscriberverify.com](https://subscriberverify.com/blog/tcpa-sms-carrier-restrictions-cold-calling-2026) |
| **B2B is not exempt.** "Dual-purpose mobile numbers trigger the same consent rules as consumer lines" | [prospeo.io](https://prospeo.io/s/is-cold-texting-illegal) |
| **A2P 10DLC registration is about deliverability, not legality.** Being registered does not give you consent | [subscriberverify.com](https://subscriberverify.com/blog/tcpa-sms-carrier-restrictions-cold-calling-2026) |
| Sending prohibited or unsolicited content "will result in campaign termination and can lead to **the suspension of your entire brand registration**" | [messageiq.io](https://messageiq.io/blogs/10dlc-registration-sms-compliance/) |

**Why this is worse than burning a domain.** Your A2P 10DLC brand registration is the infrastructure
your *clients'* SMS runs on. A burned domain costs you outbound prospecting. A suspended brand
registration stops SMS delivery for every paying customer you have. You would be risking the product
to prospect for the product.

### And there's a direct collision with your own targeting

The strongest signal in the entire matrix — the one I scored `●●●` and called the best combined
signal — is **"main line rings to a mobile number."** That signal exists because it means the owner is
reachable.

That is also **precisely the highest-risk number to cold text.** A dual-purpose owner cell is treated
as a consumer line for consent purposes. Your best prospecting signal and your proposed SMS channel are
in direct opposition.

**Recommendation:** cold SMS to prospects is off the table. Keep SMS **as a product you deliver inside
the client's own consented database** — which is what the reactivation motion already is, and it is
fully defensible there because the consent belongs to the client and their customers opted in. Prospect
by email, phone (a human dialing is a different legal regime from automated texting), LinkedIn, and
referral. **Do not blur delivery SMS and prospecting SMS onto the same brand registration.**

I'd want a telecom attorney to confirm before any prospect-facing SMS is sent. I am not one, and this
is the kind of exposure where a $2K opinion letter is cheap.

## A.2 The email numbers actually validate the sniper strategy

| Fact | Source |
|---|---|
| Any domain sending **5,000+ messages/day to Gmail is permanently classified a bulk sender** — and the classification never expires, even if volume drops | [inboxkit.com](https://www.inboxkit.com/learn/google-yahoo-sender-requirements-2026), [mailover.ai](https://mailover.ai/blog/bulk-sender-requirements.html) |
| Spam complaint rate must stay under **0.30%**; Google recommends under **0.1%** for reliable placement | [powerdmarc.com](https://powerdmarc.com/bulk-email-sender-requirements/) |
| In 2026 the penalty for failing sender checks "isn't the spam folder any more. It's outright rejection" | [inboxkit.com](https://www.inboxkit.com/learn/google-yahoo-sender-requirements-2026) |

At sniper volume — 20 to 50 sends a day — you sit two orders of magnitude below the bulk-sender line
and have enormous headroom on complaint rate. **The constraint Alec was worried about and the strategy
he wants are the same thing.** Sniper isn't a compromise forced by deliverability; it's the only motion
that's actually safe, and it happens to be the one that suits the ICP.

The corollary is a hard ceiling to write into the system: **never exceed 5,000/day/domain, ever.** That
classification is permanent.

## A.3 The tooling exists, and it's cheaper than expected

| Fact | Source |
|---|---|
| GoHighLevel ships an **official MCP server** — AI agents read and write GHL data with no custom integration | [thestackinsiders.com](https://www.thestackinsiders.com/blog/gohighlevel-mcp-server), [netpartners.marketing](https://netpartners.marketing/how-to-use-the-highlevel-mcp-server-ai-powered-gohighlevel-workflows/) |
| Included at no additional cost on **Unlimited ($297)** and **SaaS Pro ($497)** plans | [thestackinsiders.com](https://www.thestackinsiders.com/blog/gohighlevel-mcp-server) |
| Auth via **Private Integration Token or OAuth**; each connection is **scoped to one sub-account (location)** | [ai.exoticaitsolutions.com](https://ai.exoticaitsolutions.com/blog/gohighlevel-mcp/) |
| Official server covers ~21 core tools; community servers on GitHub reach 500+ | [thestackinsiders.com](https://www.thestackinsiders.com/blog/gohighlevel-mcp-server), [github.com/NerdSnipe-Inc](https://github.com/NerdSnipe-Inc/ghl-mcp-server) |
| GHL released an **Agent Studio API in March 2026** | [imisofts.com](https://imisofts.com/blog/gohighlevel-mcp-server-ai-agents-news-june-7-2026/) |
| **Claude Agent SDK** — Python/TS, ships subprocess model, tool execution, session persistence, permission system, hooks, multi-agent coordination, memory, native MCP | [beginnersinai.org](https://beginnersinai.org/claude-agent-sdk/), [o-mega.ai](https://o-mega.ai/articles/claude-agent-sdk-the-2026-deep-dive) |

Note the one-location-per-connection scoping — it shapes the architecture and Jameson should design
around it rather than discover it late.

## A.4 The reframe I'd push hardest on

**"AI SDR" in the market sense means automated sending. That is the one part of this you should not
build.**

Split the system into four stages and notice where the value and the risk live:

| Stage | Value Claude adds | Risk | Autonomy |
|---|---|---|---|
| Discovery — find candidates | High | Near zero (public data, read-only) | **Autonomous** |
| Research — build the dossier, form the hypothesis | **Highest. This is the whole edge** | Near zero | **Autonomous** |
| Draft — write the message | High | Near zero (nothing sent) | **Autonomous** |
| **Send** | **Near zero** | **All of it — legal, domain, brand, reputation** | **Human gate, always** |

100% of the risk and roughly none of the differentiated value sits in the send step. Automating it buys
you almost nothing and puts everything on the table.

So: **build an AI research and qualification engine with a human trigger, not an auto-sending SDR.** At
20–50 sends a day, a human approving each one costs minutes and is the cheapest insurance available.
Calling it an "AI SDR" invites the wrong architecture — the name is doing damage.

Devil's advocate against myself: at real scale, human approval becomes the bottleneck. That's true —
and it's the right problem to have later. Earn the volume first, and the approval data becomes the
training set that would justify relaxing the gate.

## A.5 The blocker on "best-trained Straz ever"

You cannot train a Straz without Straz training data, and none of it is in this repo. Specifically
needed: recordings or transcripts of Aaron and Alec running real discovery calls; the actual messages
that produced booked meetings; the Jobber/HouseCall Pro win narrative; and the objection library from
the ~700 voice AI test calls. **Without these, the "Straz voice" will be a generic AI sales voice with
your names on it** — which is worse than neutral, because it will sound like every other tool.

## A.6 Access boundary for Jameson

Jameson is an intern. The system he is building can generate six-figure legal liability and disable your
clients' SMS. He should have: a **sandbox GHL sub-account** with no real client data, **no production
sending credentials**, and **no A2P brand access**. He builds and demonstrates; you hold the keys. This
is in the prompt, but it needs enforcing on your side too.

---

# PART B — The prompt for Jameson

Copy everything between the rules. It's written to be pasted into Claude with the two prospecting docs
and this file attached.

---

> ## MISSION
>
> You are building the research and qualification engine behind a sniper outbound motion for Leep AI, a
> boutique AI services firm selling voice AI receptionists, SMS and web chat agents, SEO, Yelp agents,
> SMS reactivation, website services, and CRM data consulting into home services and med spa businesses.
>
> I am Jameson. I am an intern. Treat me as competent but unproven — explain your reasoning, and do not
> let me ship something dangerous because I asked confidently.
>
> **The doctrine is sniper, not spray.** We will send 20–50 messages a day, not 5,000. Every message must
> be earned by evidence. A message we cannot defend line by line is worse than no message, because our
> entire differentiation is that we did the work.
>
> ## NON-NEGOTIABLE RULES
>
> 1. **Never state anything you cannot cite.** Every factual claim about a tool, a law, a price, a
>    capability, or a prospect carries a source — a URL, an API response, a file path, or a timestamped
>    artifact. If you cannot source it, say "unsourced" and mark it as a question, not a finding.
> 2. **Never fabricate.** Not a statistic, not a capability, not a prospect detail, not an integration
>    that exists. If you are unsure whether an API endpoint exists, check it or say you didn't.
> 3. **Distinguish verified from inferred, always.** Tag every claim `[VERIFIED]`, `[INFERRED]`, or
>    `[UNKNOWN]`. An inference presented as a fact is the failure mode that ends this project.
> 4. **Never send anything to a real prospect.** You are building and demonstrating. A human approves
>    every outbound message. Do not build an auto-send path, do not add one "for testing," and do not
>    connect production credentials.
> 5. **No prospect-facing SMS. At all.** See the compliance section — this is a legal boundary, not a
>    preference.
> 6. **Surface bad news early and plainly.** If the architecture won't work, if a tool doesn't do what
>    the marketing says, if the plan has a hole — say so in the first paragraph, not the appendix. You
>    will never be penalized for reporting a problem. You will be penalized for hiding one.
>
> ## WHAT YOU ARE BUILDING — FOUR STAGES, ONE GATE
>
> ```
>   [1] DISCOVER          [2] RESEARCH           [3] DRAFT            [4] SEND
>   autonomous            autonomous             autonomous           HUMAN GATE
>   ──────────────        ──────────────         ──────────────       ──────────────
>   Scrape one pain       Build the dossier.     Write the message    A human reads the
>   signal at a time      Form and stress-test   from the evidence.   dossier, the
>   at scale. Merge on    the hypothesis.        Cite each claim to   evidence, and the
>   entity. Score.        Verify. Try to         a dossier line.      draft, and decides.
>                         refute it.                                  Never automated.
> ```
>
> All the differentiated value is in stage 2. All the risk is in stage 4. Build accordingly.
>
> ## THE EVIDENCE GATE — operationalizing "cannot be refuted"
>
> A prospect may only reach the human approval queue when **every** condition below is true. This is a
> checklist your system enforces in code, not a guideline.
>
> | # | Condition | Fails if |
> |---|---|---|
> | 1 | **Fresh.** The signal was independently re-verified within the last 7 days | Pulled from a cache older than 7 days |
> | 2 | **Artifacted.** A timestamped raw artifact exists — screenshot, HTTP response, API payload, archived URL | The claim exists only as a model assertion |
> | 3 | **Refuted and survived.** A separate adversarial pass tried to kill the signal and failed | No refutation attempt was run |
> | 4 | **Specific.** The signal names one product and one claim we can defend in a sentence | The signal is generic ("could use marketing help") |
> | 5 | **Can pay.** At least two independent ability-to-pay proxies present | Pain only, no solvency evidence |
> | 6 | **Reachable.** Owner-operator markers present; below the committee threshold | Committee-scale, or no identified decision maker |
> | 7 | **Not a false positive class.** The detection method's known error modes were checked | The method has an unmeasured false-positive rate |
>
> Multiplicative, not additive: **Pain × Ability to Pay × Reachability.** Any factor near zero zeroes
> the prospect. Counting boxes floats badly-run, insolvent businesses to the top — read
> `01-pain-signal-matrix-and-icp.md` §2 before you write the scorer.
>
> **The refutation pass (condition 3) is the heart of it.** Spawn an independent check whose explicit
> job is to prove the signal wrong, defaulting to "refuted" when uncertain. Ask it: is this a stale
> posting already filled? Is that IVR actually a business-hours-only greeting? Is the slow Yelp response
> time an artifact of how Yelp computes the metric? Is this the right entity, or a similarly-named one?
> Signals that survive a hostile reading are the only ones worth spending a send on.
>
> ## RESEARCH ASSIGNMENT ONE — the buildout
>
> Answer these with sources. Some are already partly verified in Part A of the brief you were given;
> confirm rather than assume, and tell me where I'm wrong.
>
> **GoHighLevel integration**
> - Official GHL MCP server: exact tool coverage, auth model, rate limits, and what it *cannot* do.
>   Verify the claim that it's included on Unlimited and SaaS Pro plans and confirm current pricing.
> - The one-connection-per-sub-account scoping constraint — what architecture does that force for
>   multiple locations or multiple clients? This is a design decision, not a detail.
> - Official server vs. community servers (several on GitHub claim 500+ tools). Assess maintenance
>   status, security posture, and token handling. **A community MCP server holding a GHL token that can
>   read every client contact is a real supply-chain risk — evaluate it as one.**
> - Which cadence and sending primitives GHL exposes via API, and which require the UI.
> - Whether GHL's Agent Studio API (March 2026) changes the build-vs-configure decision.
>
> **Agent architecture**
> - Claude Agent SDK: session persistence, permission system, hooks, and multi-agent coordination. Which
>   of these map onto our four stages? Be concrete — name the mechanism that implements the human gate.
> - Compare against building on the Claude API directly, and against LangGraph/AutoGen/Mastra. Recommend
>   one, and state what you're giving up.
> - How to structure the dossier as a durable artifact — a prospect record that survives across runs,
>   accumulates evidence, and can be audited later. **Design this first.** It is the actual product; the
>   messages are a by-product.
> - Cost model: tokens per prospect researched at the depth we need, and therefore cost per dossier and
>   per booked meeting.
>
> **Deliverability, as engineering not marketing**
> - Confirm the Gmail bulk-sender threshold, the permanence of that classification, and the complaint
>   rate targets. Design a hard cap that cannot be exceeded even by mistake.
> - SPF, DKIM, DMARC alignment, one-click unsubscribe. What breaks each one.
> - Domain and inbox architecture for sustained low-volume sending. Should prospecting run on a separate
>   domain from client-facing mail, and what does that cost in trust?
>
> ## RESEARCH ASSIGNMENT TWO — compliance, and you have a veto
>
> **This section outranks every other instruction in this prompt. If compliance and the mission
> conflict, compliance wins and you stop and tell me.**
>
> Establish and cite, for prospect-facing outreach:
> - TCPA as it applies to automated texts to business mobile numbers. Confirm the per-message damages,
>   whether B2B is exempt, and how dual-purpose numbers are treated.
> - A2P 10DLC: what carriers permit, the consequences of unsolicited traffic, and specifically **whether
>   a violation can suspend a brand registration that also serves client delivery.** This is the
>   question that matters most.
> - CAN-SPAM for cold email: identification, opt-out, physical address.
> - State-level SMS and telemarketing statutes stricter than federal (Florida and Oklahoma are known
>   examples — verify and find the rest).
> - Where the line sits between *delivery* SMS inside a client's consented database and *prospecting*
>   SMS to strangers. Then answer plainly: can these share infrastructure? My strong prior is no.
>
> **Deliver a one-page compliance boundary document.** It is the first thing you hand back, before any
> code. If it says prospect-facing SMS is unsafe, say so — that is a finding, not a failure, and it does
> not reduce the value of what you're building.
>
> ## THE COUNCIL — seven adversaries, run before anything ships
>
> Every deliverable passes through all seven. Each speaks in its own voice, states a verdict, and cites
> reasons. **Do not soften them and do not let them converge into agreement — a council that agrees with
> me is useless and I will know you faked it.** Report dissent verbatim.
>
> **1. The Compliance Officer** — *holds the only absolute veto.* Every message and mechanism, against
> TCPA, A2P, CAN-SPAM, and state law. Assumes we will be sued and asks what the discovery file looks
> like. A veto here stops the project until resolved; nothing overrides it.
>
> **2. The Refuter** — tries to kill every pain signal. Default position: the signal is wrong, the data
> is stale, the entity is misidentified. Must actively attempt refutation, not just consider it.
>
> **3. The Prospect** — reads the message as the actual owner receiving it on a Tuesday morning. Rules
> on one question: *does this feel researched, or does it feel surveilled?* Has veto over tone. This
> role exists because the failure mode of deep research is creepiness, and we will not see it ourselves.
>
> **4. The Deliverability Engineer** — owns the sending domain and the A2P brand as balance-sheet
> assets. Models cumulative risk across a quarter, not per message. Asks what happens on the 400th send.
>
> **5. The CRO** — asks whether this prospect is worth the time of two closers whose muscle is
> $200K–$1.9M complex deals. Kills anything that wastes elite sales capacity on a commodity deal. Reads
> `01-pain-signal-matrix-and-icp.md` §4 and enforces it.
>
> **6. The Data Skeptic** — challenges whether the scrape measured what it claims. Demands a false
> positive rate for every detection method. Its recurring question: *how many of these are wrong, and
> how would we know?*
>
> **7. The Voice Auditor** — judges whether the copy sounds like Aaron and Alec or like an AI pretending
> to. Blocks anything with AI tells: "I hope this finds you well," "I noticed that you," "quick
> question," em-dash-heavy cadence, three-part lists, hollow flattery. **If Straz training data hasn't
> been supplied, this role's verdict is automatically "cannot assess" — say so rather than guessing.**
>
> ## BLIND SPOTS — treat as live risks, add to the register as you find more
>
> Report on each. Do not skip one because it looks handled.
>
> 1. **The A2P brand is shared with client delivery.** Losing it stops paying customers' SMS, not just
>    prospecting. Confirm or refute this coupling — it is the highest-stakes open question here.
> 2. **Our best signal is our worst channel.** "Main line rings to a mobile" is the strongest
>    reachability signal and the highest-risk cold-text target. Design around the collision.
> 3. **Stale signals destroy credibility precisely because they're specific.** "I saw your receptionist
>    opening" lands badly if they filled it a month ago — worse than a generic email, because it proves
>    we didn't actually look. Hence the 7-day freshness rule. Test it.
> 4. **The specificity paradox.** There is a line between "did their homework" and "is watching me."
>    "Your job posting has been open 47 days" crosses it. Find the line. The Prospect role owns this.
> 5. **Unmeasured false positive rate.** If IVR detection is wrong 15% of the time, 15% of our openers
>    are factually false to the one person who knows the truth. Measure it before trusting it.
> 6. **No learning loop is defined.** Nothing here specifies how the system discovers which signals
>    actually convert. Without it, every score weight is a permanent guess. Design the loop.
> 7. **Reply handling is unplanned — and this one is embarrassing.** Our entire pitch is "you're losing
>    money because you respond slowly." If our own replies sit for six hours, we lose on the first
>    objection and deserve to. Who answers, how fast, and what is the SLA? Answer before the first send.
> 8. **Sniper volume makes statistical testing impossible.** At 20–50 sends a day you cannot A/B test to
>    significance in any useful timeframe. Iteration has to be qualitative — call reviews, reply
>    reading, loss reasons. Say so explicitly rather than building a dashboard that implies otherwise.
> 9. **Straz training data does not exist in the repo.** Without it the voice will be generic AI with
>    our names on it. Flag this as blocking for stage 3, not for stages 1 and 2.
> 10. **Intern access.** You should be working in a sandbox sub-account with no real client data, no
>     production sending credentials, and no A2P brand access. If you have been given any of those, stop
>     and say so.
> 11. **The scoring model has never been validated against a real win.** Josh Astone and JJ Jardina —
>     the two reference accounts — are not in the repo. Until they are, the scorer is calibrated against
>     nothing. Note this in every scoring output.
>
> ## HOW TO REPORT
>
> Phase-gated. **Stop at each gate and wait.** Do not run ahead — a wrong assumption compounds.
>
> | Gate | Deliverable | Blocks on |
> |---|---|---|
> | **1** | Compliance boundary document, one page, sourced. Plus the SMS question answered plainly | Human sign-off. Nothing proceeds without it |
> | **2** | Tooling recommendation: GHL integration path, agent framework, dossier schema, cost per dossier. With what you'd give up | Human sign-off |
> | **3** | Evidence gate implemented and tested against 20 hand-checked prospects. Report the false positive rate you actually measured | Human sign-off |
> | **4** | Ten complete dossiers with drafts, each through all seven council roles, dissent reported verbatim | Human review of all ten |
> | **5** | Only then: the sending mechanism — with the human gate, the volume cap, and the kill switch | Aaron and Alec only |
>
> At every gate, include: what you verified, what you inferred, what you could not determine, and what
> you think I'm wrong about. **That last one is not optional and "nothing" is not an acceptable answer.**
>
> ## FINAL INSTRUCTION
>
> The measure of this system is not messages sent. It is the percentage of sent messages whose central
> claim the recipient recognizes as true and important about their own business.
>
> Optimize for that number. It is the only one that compounds.

---

# PART C — What I'd want decided before Jameson starts

1. **Is prospect-facing SMS dead?** My recommendation is yes — and that a telecom attorney confirms
   before any is sent. This is Gate 1 and it changes the whole build.
2. **Does prospecting email run on a separate domain from client mail?** Isolation protects the client
   relationship; a fresh domain costs trust and warmup time.
3. **Who answers replies, within what SLA?** Blind spot 7. Unanswered, the first send is a liability.
4. **Will Straz training data be supplied?** If not, stage 3 produces generic copy and the Voice Auditor
   is permanently blind.
5. **What sandbox does Jameson get?** He needs one before day one, not after an incident.

# PART D — Sources

**TCPA and A2P 10DLC:** [messageiq.io — TCPA/CAN-SPAM for SMS](https://messageiq.io/blogs/avoid-costly-fines-a-guide-to-tcpa-and-can-spam-for-sms-marketing/) ·
[messageiq.io — 10DLC compliance](https://messageiq.io/blogs/10dlc-registration-sms-compliance/) ·
[subscriberverify.com](https://subscriberverify.com/blog/tcpa-sms-carrier-restrictions-cold-calling-2026) ·
[activeprospect.com](https://activeprospect.com/blog/tcpa-text-messages/) ·
[prospeo.io](https://prospeo.io/s/is-cold-texting-illegal) ·
[justcall.io](https://justcall.io/blog/10dlc-compliance-guide.html) ·
[infobip.com](https://www.infobip.com/blog/tcpa-compliance-sms)

**Email deliverability:** [inboxkit.com](https://www.inboxkit.com/learn/google-yahoo-sender-requirements-2026) ·
[powerdmarc.com](https://powerdmarc.com/bulk-email-sender-requirements/) ·
[mailover.ai](https://mailover.ai/blog/bulk-sender-requirements.html) ·
[redsift.com](https://redsift.com/guides/bulk-email-sender-requirements)

**GoHighLevel MCP:** [thestackinsiders.com](https://www.thestackinsiders.com/blog/gohighlevel-mcp-server) ·
[netpartners.marketing](https://netpartners.marketing/how-to-use-the-highlevel-mcp-server-ai-powered-gohighlevel-workflows/) ·
[ai.exoticaitsolutions.com](https://ai.exoticaitsolutions.com/blog/gohighlevel-mcp/) ·
[imisofts.com](https://imisofts.com/blog/gohighlevel-mcp-server-ai-agents-news-june-7-2026/) ·
[github.com/NerdSnipe-Inc/ghl-mcp-server](https://github.com/NerdSnipe-Inc/ghl-mcp-server)

**Claude Agent SDK:** [beginnersinai.org](https://beginnersinai.org/claude-agent-sdk/) ·
[o-mega.ai](https://o-mega.ai/articles/claude-agent-sdk-the-2026-deep-dive) ·
[technspire.com](https://technspire.com/en/blog/choosing-agent-sdk-2026-claude-langgraph-autogen)

**Not a lawyer.** The compliance findings above are cited secondary sources, not legal advice. The TCPA
exposure here is large enough that a telecom attorney's opinion letter is cheap insurance.
