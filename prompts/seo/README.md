# SEO God Mode Prompt Pack

Two prompts that work as a closed loop for client site work.

| File | Use it when | Feed it |
|---|---|---|
| `01-auditor-god-mode.md` | Diagnosing an existing site — pitch material, pre-rebuild scoping, post-launch QA | A live URL + the Input Block |
| `02-builder-god-mode.md` | Building or rebuilding a client site | The Build Brief |

Shareable PDFs of both live in `pdf/`. They are generated from the markdown —
edit the `.md` files, then run `python3 build-pdfs.py` to regenerate. Never
edit the PDFs directly, or the two will drift apart.

```
pip install markdown pygments pypdf reportlab cffi   # one-time
python3 build-pdfs.py                                 # needs Chrome/Chromium
```

## The loop

1. **Audit the current site** with Prompt 1 → gives you a scored deficiency
   report you can put in front of a prospect.
2. **Build with Prompt 2** → the Build Brief inherits the audit's findings, and
   the redirect map (Part 8.4) is generated from the old URL inventory.
3. **Re-audit the new build** with Prompt 1 before handoff → the score is now
   the proof of work, produced by the same rubric the pitch used.

## The four blind spots this pack targets

Called out as dedicated deep-dive modules in Prompt 1 (M1–M4) and as hard
build directives in Prompt 2:

- **Canonical drift** — variant matrix in Prompt 1 §1.1, URL spec in Prompt 2 Part 2
- **Schema nesting** — graph connectivity ladder in Prompt 1 §4.2, `@graph` template in Prompt 2 Part 6
- **Interaction to Next Paint** — root-cause hunt in Prompt 1 §3.4, engineering rules in Prompt 2 Part 5
- **JavaScript-only rendering** — parity diff in Prompt 1 §2.1, Raw-HTML Rule in Prompt 2 Part 3

## Two things not to strip out

**The Integrity Protocol / Truth Contract.** These are what stop a model from
inventing a Lighthouse score, a backlink count, or a fake `AggregateRating`.
The scoring rubric in Prompt 1 Part 4 is deterministic on purpose — a
"X/100" with no rubric behind it is a hallucinated number, which is worse than
no number in front of a client.

**The Lighthouse Reality Statement (Prompt 2, T4).** Lighthouse does not
measure INP — INP is a field metric, and TBT is the lab proxy. Lighthouse
Accessibility 100 is not WCAG compliance; automated tooling covers roughly a
third of the success criteria. Promising a client "100/100 including INP" is
promising something that does not exist as a measurement, and it is the kind
of claim that comes back at handoff.
