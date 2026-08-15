# Artifacts

## `signal-matrix.html`

Source for the published visual matrix:
**https://claude.ai/code/artifact/061f2ace-be7d-44ed-a6d2-b3e943b81c29**

**Why this file is here:** it was living only in an ephemeral session scratchpad, which is reclaimed when
the container dies. The published page would have survived; the source to edit it would not. Caught by
the checkpoint protocol on 2026-08-07.

### Contents

| Section | Covers |
|---|---|
| The finding | AI receptionist commoditised at $25–95/mo self-serve |
| Signal matrix | 58 signals across 9 products, with bucket / detection / strength |
| Pay & reach | The two multiplied scoring axes |
| The ceiling | Procurement threshold, sourced |
| ICP scorecard | 7 segments scored on 6 axes |
| By industry | 5 verticals, cross-verified lead product |
| Where to scrape | Per-vertical source map, two tracks |
| Team capacity | The roster model — 175 dials/day, ~79 meetings/mo |
| 16-week plan | Two divisions, week-by-week to 30 November |
| Blocked | Internal sources still missing |

### To republish after editing

In a Claude Code session, edit this file then publish with the **existing URL** so the link doesn't
change:

```
Artifact({
  file_path: "<path>/signal-matrix.html",
  url: "https://claude.ai/code/artifact/061f2ace-be7d-44ed-a6d2-b3e943b81c29",
  favicon: "🎯",
  description: "..."
})
```

Passing `url` is required from any conversation that didn't originally publish it — without it you mint a
new URL and the old link goes stale.

### Constraints when editing

- **No external requests.** Strict CSP: no CDN scripts, external stylesheets, webfonts or remote images.
  Everything is inlined
- **Theme-aware.** Palette is defined as CSS custom properties on `:root`, redefined under
  `@media (prefers-color-scheme: dark)` and again under `:root[data-theme="dark"]` / `["light"]`. Don't
  give a colour its only definition inside a media block
- **Tables scroll in their own container** (`.scroller`) so the page body never scrolls sideways
- Verify tag balance before publishing — a stray unclosed `</div>` silently breaks the layout
