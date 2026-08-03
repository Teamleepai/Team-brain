# Coding Standards

Governs how code is written. Subordinate to `MASTER_CONSTITUTION.md`.

## Baseline

Write production-quality code only, on the first pass. There is no "prototype now, clean up later" mode in this project — see `PRODUCT_PHILOSOPHY.md` on intentional technical debt.

## Rules

- **Readable over clever.** If a reviewer needs to pause and decode an expression, rewrite it.
- **Maintainable over short.** Do not sacrifice clarity to save lines.
- **Explicit over implicit.** No relying on subtle language behavior, implicit type coercion, or "magic" configuration a reader can't see.
- **Document public interfaces.** Every exported function, class, API endpoint, and schema has a short doc comment stating purpose, inputs, outputs, and error conditions — not restating the obvious, but capturing intent and constraints a signature can't express.
- **Small functions, focused modules.** A function does one thing; a module owns one responsibility (mirrors `ENGINEERING_STANDARDS.md` at the code level).
- **Remove dead code immediately.** Commented-out code, unused branches, and unreachable paths are deleted, not preserved "just in case" — version control is the safety net.
- **No placeholder implementations unless explicitly requested.** A stubbed function that silently does nothing is worse than a missing one — it's a bug wearing a disguise.
- **No comments explaining what code does.** Well-named identifiers do that. Comment only the non-obvious *why*: a workaround, a constraint from an external system, an invariant that isn't visible locally.
- **No unnecessary abstraction.** Three similar lines beat a premature helper built for a future that hasn't arrived.

## Review checklist (applied before merge)

- [ ] Does this introduce hidden coupling to another module?
- [ ] Is every public interface documented?
- [ ] Are there placeholder/stub implementations that weren't explicitly requested?
- [ ] Is there dead code left behind?
- [ ] Would a new engineer understand this from the code + its doc comments alone?
- [ ] Are secrets, credentials, or PII anywhere in the diff? (see `SECURITY_STANDARDS.md`)
