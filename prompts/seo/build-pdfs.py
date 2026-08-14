#!/usr/bin/env python3
"""Render the SEO God Mode markdown prompts into typeset PDFs.

Usage:  python3 build-pdfs.py
Deps:   pip install markdown pygments pypdf reportlab cffi
Needs:  a Chromium/Chrome binary (set CHROME_BIN if it is not auto-detected).
Edit the markdown, re-run this, and the PDFs regenerate in ./pdf/.
"""
import glob
import html
import io
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import markdown
from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SRC = Path(__file__).resolve().parent
OUT = SRC / "pdf"
WORK = Path(tempfile.mkdtemp(prefix="seo-pdf-"))


def find_chrome() -> str:
    env = os.environ.get("CHROME_BIN")
    if env and Path(env).exists():
        return env
    for pat in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                "/usr/bin/chromium", "/usr/bin/chromium-browser",
                "/usr/bin/google-chrome",
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    sys.exit("No Chrome/Chromium found. Set CHROME_BIN=/path/to/chrome")


CHROME = find_chrome()

CSS = """
@page { size: Letter; margin: 17mm 15mm 20mm 15mm; }

:root {
  --ink:      #16202a;
  --muted:    #5b6b7a;
  --accent:   #0d5c46;
  --accent-2: #0a3f30;
  --rule:     #d8e0e6;
  --code-bg:  #f5f7f8;
  --warn:     #8a3b12;
}

* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Bitstream Charter", "DejaVu Serif", Georgia, serif;
  font-size: 10.2pt;
  line-height: 1.5;
  color: var(--ink);
  margin: 0;
}

/* ---------- cover ---------- */
.cover { height: 237mm; display: flex; flex-direction: column; page-break-after: always; }
.cover .band { background: var(--accent); color: #fff; padding: 13mm 12mm 11mm; }
.cover .kicker {
  font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
  font-size: 8.5pt; letter-spacing: .22em; text-transform: uppercase;
  opacity: .85; margin: 0 0 7mm;
}
.cover h1 {
  font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
  font-size: 30pt; line-height: 1.1; font-weight: 700; margin: 0; color: #fff;
  border: 0; padding: 0;
}
.cover .sub { font-size: 12.5pt; margin: 5mm 0 0; opacity: .93; max-width: 150mm; }
.cover .body { padding: 12mm 12mm 0; flex: 1; }
.cover .lede { font-size: 11.4pt; line-height: 1.55; max-width: 155mm; margin: 0 0 9mm; }
.cover .meta {
  font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
  font-size: 9pt; border-top: 1.5px solid var(--rule); padding-top: 5mm;
  display: grid; grid-template-columns: 34mm 1fr; row-gap: 2.4mm; max-width: 150mm;
}
.cover .meta dt { color: var(--muted); text-transform: uppercase; letter-spacing: .08em; font-size: 7.8pt; padding-top: .6mm; }
.cover .meta dd { margin: 0; }
.cover .foot {
  margin-top: auto; padding: 0 12mm 8mm;
  font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
  font-size: 8.6pt; color: var(--muted);
}
.cover .foot strong { color: var(--warn); }

/* ---------- headings ---------- */
h1, h2, h3, h4, h5, h6 {
  font-family: "Liberation Sans", "DejaVu Sans", sans-serif;
  color: var(--accent-2); line-height: 1.22;
  break-after: avoid-page; page-break-after: avoid;
}
.doc > h1 { display: none; }          /* title lives on the cover */
h2 {
  font-size: 15pt; margin: 0 0 6mm; padding-bottom: 2.5mm;
  border-bottom: 2px solid var(--accent); letter-spacing: -.01em;
}
h3 {
  font-size: 13.2pt; margin: 9mm 0 3.5mm; padding: 2.6mm 0 2.6mm 4mm;
  border-left: 4px solid var(--accent); background: #eef4f2;
}
h3.part { break-before: page; page-break-before: always; margin-top: 0; }
h4 { font-size: 11.4pt; margin: 7mm 0 2.5mm; color: var(--accent); }
h5, h6 { font-size: 10.4pt; margin: 5mm 0 2mm; }

p { margin: 0 0 3.2mm; }
strong { color: #0b1720; }
a { color: var(--accent); text-decoration: none; word-break: break-word; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 7mm 0; }

ul, ol { margin: 0 0 3.5mm; padding-left: 6.5mm; }
li { margin-bottom: 1.3mm; }
li > ul, li > ol { margin-top: 1.3mm; }

/* ---------- callout ---------- */
blockquote {
  margin: 0 0 6mm; padding: 3.5mm 5mm; background: #fdf6ec;
  border-left: 4px solid #d99a3e; font-size: 9.6pt; color: #4a3a22;
  break-inside: avoid;
}
blockquote p:last-child { margin-bottom: 0; }

/* ---------- code ---------- */
code {
  font-family: "DejaVu Sans Mono", "Liberation Mono", monospace;
  font-size: 8.6pt; background: var(--code-bg); padding: .3mm 1.1mm;
  border-radius: 2px; word-break: break-word; color: #123;
}
pre, div.codehilite {
  background: var(--code-bg); border: 1px solid var(--rule);
  border-left: 3px solid var(--accent); border-radius: 3px;
  padding: 3mm 3.5mm; margin: 0 0 4.5mm; overflow: visible;
}
div.codehilite pre { border: 0; padding: 0; margin: 0; background: none; }
pre code, div.codehilite pre {
  font-family: "DejaVu Sans Mono", "Liberation Mono", monospace;
  font-size: 8.1pt; line-height: 1.42; background: none; padding: 0;
  white-space: pre-wrap; word-break: break-word; color: #1b2a33;
}

/* ---------- tables ---------- */
table {
  width: 100%; border-collapse: collapse; margin: 0 0 5mm;
  font-family: "Liberation Sans", "DejaVu Sans", sans-serif; font-size: 8.6pt;
}
thead { display: table-header-group; }
tr { break-inside: avoid; page-break-inside: avoid; }
th {
  background: var(--accent); color: #fff; text-align: left; font-weight: 600;
  padding: 2.1mm 2.4mm; border: 1px solid var(--accent);
}
td { padding: 2mm 2.4mm; border: 1px solid var(--rule); vertical-align: top; }
tbody tr:nth-child(even) td { background: #f7fafa; }
td code, th code { font-size: 7.9pt; background: rgba(0,0,0,.05); }
th code { background: rgba(255,255,255,.18); color: #fff; }
"""

CONVERTED_HR = re.compile(r"^---\s*$", re.M)


def md_to_html(md_text: str) -> str:
    out = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "codehilite", "sane_lists", "attr_list"],
        extension_configs={
            "codehilite": {"noclasses": True, "guess_lang": False, "pygments_style": "friendly"}
        },
    )
    # Only top-level PART sections start a fresh page.
    return re.sub(r'<h3([^>]*)>(\s*PART\b)', r'<h3 class="part"\1>\2', out)


def cover_html(kicker, title, sub, lede, meta, foot) -> str:
    rows = "".join(f"<dt>{html.escape(k)}</dt><dd>{v}</dd>" for k, v in meta)
    return f"""
<section class="cover">
  <div class="band">
    <p class="kicker">{html.escape(kicker)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="sub">{html.escape(sub)}</p>
  </div>
  <div class="body">
    <p class="lede">{lede}</p>
    <dl class="meta">{rows}</dl>
  </div>
  <div class="foot">{foot}</div>
</section>
"""


def build(md_path: Path, out_pdf: Path, cover: str, footer_label: str):
    body = md_to_html(md_path.read_text())
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{html.escape(footer_label)}</title><style>{CSS}</style></head>
<body>{cover}<main class="doc">{body}</main></body></html>"""

    tmp_html = WORK / (out_pdf.stem + ".html")
    tmp_pdf = WORK / (out_pdf.stem + ".raw.pdf")
    tmp_html.write_text(page)

    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
         "--run-all-compositor-stages-before-draw", "--virtual-time-budget=10000",
         f"--print-to-pdf={tmp_pdf}", tmp_html.as_uri()],
        check=True, capture_output=True,
    )
    stamp(tmp_pdf, out_pdf, footer_label)


def stamp(src_pdf: Path, out_pdf: Path, label: str):
    """Overlay a footer rule with page numbers on every page except the cover."""
    reader = PdfReader(str(src_pdf))
    total = len(reader.pages)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i > 0:
            w = float(page.mediabox.width)
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=(w, float(page.mediabox.height)))
            y = 30
            c.setStrokeColorRGB(0.85, 0.88, 0.90)
            c.setLineWidth(0.6)
            c.line(42, y + 11, w - 42, y + 11)
            c.setFont("Helvetica", 7.4)
            c.setFillColorRGB(0.36, 0.42, 0.48)
            c.drawString(42, y, label)
            c.drawRightString(w - 42, y, f"Page {i + 1} of {total}")
            c.save()
            buf.seek(0)
            page.merge_page(PdfReader(buf).pages[0])
        writer.add_page(page)

    writer.add_metadata({
        "/Title": label,
        "/Subject": "Technical SEO prompt system",
        "/Creator": "SEO God Mode Prompt Pack",
    })
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with open(out_pdf, "wb") as fh:
        writer.write(fh)
    print(f"{out_pdf}  ({total} pages)")


if __name__ == "__main__":
    DATE = "August 2026"

    build(
        SRC / "01-auditor-god-mode.md",
        OUT / "SEO-God-Mode-01-Forensic-Auditor.pdf",
        cover_html(
            "SEO God Mode Prompt Pack · Document 1 of 2",
            "Forensic Technical SEO Auditor",
            "A zero-fabrication audit prompt with a deterministic 100-point scoring rubric.",
            "Paste this prompt into a fresh AI session that has live web access, fill in the "
            "Input Block, and it will produce a reproducible technical audit: every finding "
            "tagged by evidence type, every standard cited with a dated source, every score "
            "derived from a published rubric rather than asserted.",
            [
                ("Use it for", "Diagnosing an existing site — prospect pitches, pre-rebuild scoping, post-launch QA"),
                ("Requires", "A model with live web fetch. Without it, the prompt will correctly declare itself limited."),
                ("Input", "A live URL plus the Input Block in Part 1"),
                ("Output", "Integrity statement, scored deficiency summary, per-finding record, prioritized backlog, sources"),
                ("Version", f"v2 · {DATE}"),
            ],
            "<strong>Do not delete the Integrity Protocol (Part 0) or the scoring rubric "
            "(Part 4).</strong> They are what stop the model from inventing a Lighthouse "
            "score, a backlink count, or a confident number with nothing behind it.",
        ),
        "SEO God Mode · 1 · Forensic Technical SEO Auditor",
    )

    build(
        SRC / "02-builder-god-mode.md",
        OUT / "SEO-God-Mode-02-Build-Engine.pdf",
        cover_html(
            "SEO God Mode Prompt Pack · Document 2 of 2",
            "SEO-Perfect Build Engine",
            "A build-time contract: crawlable HTML, zero canonical drift, connected schema, enforced budgets.",
            "Paste this prompt as the system instruction of a build session, then supply the "
            "Build Brief. Every page produced under it ships index-ready on first delivery — "
            "and nothing is delivered until it passes the 24-row Acceptance Gate, which is "
            "handed to the client as a re-runnable verification script.",
            [
                ("Use it for", "Building or rebuilding client sites at agency quality on a budget timeline"),
                ("Input", "The Build Brief in Part 1 — canonical domain, services, locations, real business data"),
                ("Output", "Production code with zero placeholders, filled acceptance gate, open-inputs table, post-deploy checklist"),
                ("Stacks", "Next.js App Router · Astro · WordPress · static HTML (appendices in Part 11)"),
                ("Version", f"v2 · {DATE}"),
            ],
            "<strong>Two rules that protect the client and you:</strong> never emit "
            "AggregateRating or Review markup without real, visible, sourced reviews (T2), and "
            "never rebuild an existing site without a 1:1 redirect map (Part 8.4).",
        ),
        "SEO God Mode · 2 · SEO-Perfect Build Engine",
    )
