# LEAP OS — Documentation

Two kinds of document live here, and the distinction matters.

**[`/constitution`](../constitution/)** (one level up) holds the standards — the durable rules that govern how LEAP OS is designed, built, secured, and shipped. They change rarely and deliberately.

**`/docs`** holds the work — decisions and plans that apply those standards to specific features. They accumulate.

## Contents

| Directory | Contents |
|---|---|
| [`decisions/`](decisions/) | Architecture Decision Records. Written before implementation, immutable afterward; a changed decision gets a new ADR that supersedes the old one. |
| [`phase-1/`](phase-1/) | Planning artifacts for the Chief of Staff MVP: PRD, architecture, domain and data models, API contracts, workflows, threat/privacy/permission models, failure analysis, testing, deployment, observability, rollback, risk register, definition of done. |

## Where to start

New to the project: read [`../constitution/MASTER_CONSTITUTION.md`](../constitution/MASTER_CONSTITUTION.md), then [`phase-1/README.md`](phase-1/README.md).

Implementing something: read the relevant ADRs, then `phase-1/ARCHITECTURE.md` and `phase-1/API_CONTRACTS.md`. The contracts are the reviewed artifact; changing one requires updating that document in the same change.

## The rule that generates this structure

`MASTER_CONSTITUTION.md` §6 forbids production code until the planning artifacts for a feature exist and have been critically reviewed, and §17 specifies what every major decision must document. This directory is where that obligation is discharged. `constitution/DEFINITION_OF_DONE.md` lists the artifacts required per feature; each phase directory here carries its own instantiation of that list.

The point is not documentation for its own sake. It is that a decision with no recorded alternatives will be re-litigated for free later, and a plan that was never challenged will be challenged by production instead.
