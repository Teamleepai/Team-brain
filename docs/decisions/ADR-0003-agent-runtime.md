# ADR-0003 — Claude Agent SDK as the agent execution substrate

**Date:** 2026-08-03

## Status

Accepted.

## Context

`AI_AGENT_STANDARDS.md` specifies an ecosystem of narrow, single-responsibility agents coordinated by a Chief of Staff orchestrator, with a hard set of constraints:

- Every agent declares its responsibility, inputs, outputs, current trust level, and a least-privilege tool list.
- Only the orchestrator routes work between agents; agents never call each other directly outside logged routing.
- No agent may act above its declared trust level, **even if technically capable of the action**.
- Conflicting recommendations from two agents are surfaced to the human, never silently resolved.

`OBSERVABILITY.md` requires every agent action to be logged with actor, trust level, inputs, outputs, decision rationale, and approval chain, and requires that any action be able to explain, on demand, what data it used and what authorized it.

And then `PRODUCT_PHILOSOPHY.md` §7 asks for something that appears, at first reading, to be in direct conflict with using a language model at all: *deterministic behavior over hidden magic*, with the standard that if a user or developer cannot predict what the system will do from its documented behavior, the design has failed.

Resolving that apparent conflict is the real content of this decision, and it matters more than which SDK we pick.

## Decision

**The Claude Agent SDK as the execution substrate, beneath a thin LEAP-owned orchestration layer that holds all authority.**

The load-bearing part is the boundary between those two things:

> **The model decides what to propose. Deterministic code decides what is permitted.**

Every constitutional guarantee — trust levels, tool scoping, approval gates, audit logging, conflict surfacing — is implemented in ordinary TypeScript that the agent loop runs *inside of* and cannot reach around. Concretely:

- **Tool scoping is enforced at construction, not by instruction.** An agent's permitted tools are determined by its declared contract before the loop starts. An Email Intelligence agent does not have a delete tool available and told not to use it; it does not have the tool. Prompt-level instruction is not a security control, because ingested content is untrusted (`SECURITY_STANDARDS.md`) and instructions can be argued with.
- **Trust-level gating sits between proposal and effect.** Agent output is a *proposed action object*, not an executed one. A deterministic gate reads the agent's declared trust level and the action's impact class, then routes the proposal to: discard, present as recommendation, render as draft, queue for approval, or execute. The same proposal from the same agent produces the same routing decision every time, regardless of how the model phrased it.
- **The orchestrator owns routing.** Agents receive work and return proposals; they have no capability to invoke each other. Agent-to-agent communication is structurally impossible rather than discouraged.
- **Audit logging wraps the boundary, not the agent.** Because every proposal passes through our gate, the gate is the natural and unavoidable logging point. There is no code path that executes an action without producing an audit record, because the code path that executes actions *is* the code path that logs them.

Under this arrangement the system is deterministic where determinism matters — in what it is *allowed to do* — while remaining generative in what it *thinks of*. That is the correct reading of the philosophy: the constitution asks for predictable authority, not for a language model that always emits identical tokens.

## Alternatives considered

**Direct Claude API calls with a fully custom orchestrator.** The instinctive choice for a project this insistent on control, and worth taking seriously. Rejected because it misidentifies where the control needs to live. The things we cannot compromise on — gating, scoping, audit, conflict surfacing — are all in the layer we are writing ourselves under this decision anyway. What the SDK provides is the plumbing we do not need to own opinions about: tool-use loops, session and context management, MCP connector handling, retry and streaming behavior. Rebuilding that plumbing buys no additional authority and costs weeks. Notably, choosing the SDK does not forfeit anything the custom path would have given us, because the authority boundary is ours in both cases.

**LangGraph or a comparable orchestration framework.** Its genuine strength — explicit graph state machines with durable execution and replay — maps well onto long-running approval workflows, which is exactly what Phase 2 and Phase 3 need. Rejected for now on two grounds. It inserts a substantial abstraction between us and model behavior, which conflicts with transparency over magic at precisely the moment we are trying to understand why an agent produced a bad recommendation. And it is a heavy dependency adopted for a capability we do not need until Phase 3. This is the strongest alternative and it should be genuinely re-evaluated when durable multi-step workflows arrive, rather than dismissed permanently here.

**A single large prompt handling all responsibilities.** Rejected outright — `AI_AGENT_STANDARDS.md` opens by forbidding it. Worth recording why the prohibition is correct rather than just citing it: a monolithic prompt cannot have per-agent tool scoping, cannot have per-responsibility trust levels, cannot produce conflicting recommendations to surface, and degrades unpredictably as responsibilities accumulate. Every property the trust framework depends on requires that responsibilities be separable.

## Tradeoffs

We accept a dependency on a vendor SDK's evolution, including breaking changes and the possibility that its opinions diverge from ours. Mitigated by the orchestration layer sitting above it, but not eliminated.

We accept that the agent loop itself is not reproducible. Identical inputs may yield differently-worded proposals. This is a real limitation with real consequences for testing: assertions must target the *structure and permissibility* of proposals rather than their exact text, and prompt regression testing (`TESTING_STANDARDS.md`) has to be statistical over an evaluation set rather than exact-match. Anyone expecting golden-file testing of agent output will be disappointed, correctly.

We accept some duplication of concern: the SDK has its own notion of tool permissions, and we are layering ours on top. Two permission systems in a stack is a place where a mismatch could hide, and the threat model treats it accordingly.

## Future implications

Easier: adding a new specialized agent becomes writing a contract plus a prompt, because routing, gating, logging, and tool scoping are already generic. MCP connectors give us integration reach without bespoke client code. Trust-level advancement becomes a configuration change against an agent contract rather than a code change.

Harder: anything requiring exact reproducibility of agent reasoning, and any workflow needing durable multi-day state, which we will have to build or adopt separately when Phase 3 arrives.

## Migration path

Deliberately cheap, and this is the main defense of the decision. Because trust gating, tool scoping, audit logging, and routing are ours rather than the SDK's, replacing the substrate means reimplementing the call into the model loop while the orchestration layer, the agent contracts, and every guarantee they encode stay untouched. The SDK is positioned as a replaceable component behind an interface, exactly as `ENGINEERING_STANDARDS.md` requires of everything.

The interface to define now, before any agent exists, is roughly: *given an agent contract and an input, return a set of proposed actions.* Anything the SDK offers that does not fit through that interface should be treated with suspicion, because using it would leak the substrate into our architecture.

## Technical debt

None incurred intentionally. Two obligations to carry forward:

1. **The two-permission-system seam** between SDK-level tool availability and our trust gate needs an explicit test proving the gate holds even when the SDK would have permitted an action. A gate that is only tested on the paths where it agrees with the layer beneath it has not been tested.
2. **Durable workflow state** is unbuilt and will be needed by Phase 3. Recorded in the risk register rather than solved prematurely — but recorded, so that Phase 3 does not discover it as a surprise.
