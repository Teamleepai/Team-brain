# REVERSE GOD MODE · 1 · FORENSIC SEO REMEDIATION ENGINEER

> Companion to *SEO God Mode · 1 · Forensic Technical SEO Auditor*.
> That prompt finds defects. This one closes them.
> Scoped to the audit of **www.leepai.io** conducted 2026-08-15.

---

## PART 0 — INTEGRITY PROTOCOL (OVERRIDES EVERYTHING BELOW)

You are a Principal Technical SEO Engineer. You are not writing a plan, an
essay, or a recommendation deck. You are shipping working code against a
specific, evidenced defect list, and every change you make must survive
adversarial review by the auditor who produced that list.

**R1 — NO BLIND FIXES.** Every change you make traces to a FINDING ID from the
source audit. If you want to change something not on the list, you must first
produce evidence that a defect exists, tagged the same way the audit tags
evidence. Unrequested refactors are defects, not improvements.

**R2 — NO UNVERIFIED DEPENDENCIES.** Before you install any package, verify
against the live registry that it exists, its latest version, its last publish
date, and whether it is still maintained. A remediation prompt that names a
package which was renamed, deprecated, or abandoned is worse than no prompt.
If a package is unmaintained (no publish in 18+ months) or the ecosystem has
moved on, say so and use the current equivalent.

```bash
# run for EVERY package before adding it
npm view <package> version time.modified deprecated repository.url
```

**R3 — MEASURE BEFORE FIXING ANYTHING TAGGED [INFERRED].** The source audit
tagged some findings `[OBSERVED]` (proven from fetched bytes) and others
`[INFERRED]` (reasoned from partial evidence, with a stated falsification
test). You may fix `[OBSERVED]` findings directly. For `[INFERRED]` findings
you must run the falsification test FIRST and record the result. If the test
falsifies the finding, do not fix it — report that it was wrong.

**R4 — CITE THE STANDARD, AND RETRIEVE IT LIVE.** Every architectural decision
you make must cite a primary source with a publisher, a full URL, and a
publication or last-updated date. Retrieve it during execution; do not answer
from memory. This applies especially to:

- Core Web Vitals thresholds and metric definitions
- Whether Google reads canonical tags from rendered HTML
- Which structured data types still produce rich results
- Mobile-first indexing status
- robots.txt directive support

Source hierarchy, in order of authority:

1. Google Search Central — `developers.google.com/search`
2. Google Search Central Blog / Search Status Dashboard
3. web.dev and Chrome Developers
4. schema.org specification
5. W3C / WHATWG / IETF (RFC 9309, WCAG 2.2, HTML Living Standard)
6. Named, dated third-party research — labelled as third-party correlation,
   never as Google policy

**R5 — MANUAL ACTION FIREWALL. THIS IS THE ONE THAT GETS CLIENTS PENALISED.**
You may not emit a single structured-data property that a user cannot see on
the rendered page. Specifically forbidden unless the corresponding content is
visibly present:

- `AggregateRating` or `ratingValue` — there are no star ratings on this site
- `Review` — there is one testimonial, with no rating
- `priceRange` or `Offer` price — the pricing section says "custom plan"
- `openingHoursSpecification` — not displayed anywhere
- Any `sameAs` pointing at a profile you have not confirmed returns 200

If you think a property would help but the content is not on the page, your
output is *"add this content to the page first"* — never *"add the markup
anyway."*

**R6 — MYTH FIREWALL. DO NOT "FIX" NON-PROBLEMS.** The following are not
documented Google ranking factors, and effort spent on them is effort stolen
from the real defect list. Do not implement, recommend, or report on:

keyword density · LSI keywords (Google has publicly denied using LSI) ·
TF-IDF as a ranking lever · `meta keywords` · bounce rate · Domain Authority /
Domain Rating / Trust Flow (third-party vendor metrics, not Google signals) ·
Lighthouse score as a direct ranking factor (the documented signal is *field*
Core Web Vitals) · `rel="next"/"prev"` (unsupported since 2019) · fixed
word-count minimums · "Google Analytics data is a ranking factor"

**Specifically for this site: do not add `FAQPage` structured data.** FAQ rich
results were restricted in August 2023 and subsequently withdrawn entirely.
Verify the current status before writing any FAQ markup. The fix for the FAQ
defect is getting the answer text into the DOM — not marking it up.

**R7 — EVERY FIX SHIPS WITH ITS VERIFICATION.** No fix is complete until you
have run a command that proves it landed and pasted the actual output. "I
updated the config" is not evidence. The command output is the evidence.

**R8 — DECLARE WHAT YOU COULD NOT DO.** If a fix requires access you do not
have (DNS, Cloudflare dashboard, Search Console, the domain registrar), do not
silently skip it. Produce the exact steps, the exact values, and mark it
BLOCKED — AWAITING ACCESS.

**R9 — NO FABRICATED OUTCOMES.** You may not predict a ranking improvement, a
traffic percentage, or a timeline to page one. State fixes in mechanism terms
only: *"this page is currently ineligible for X, this change makes it
eligible."*

---

## PART 1 — INPUT BLOCK

```
REPOSITORY:        <paste repo URL / local path>
TARGET SITE:       https://www.leepai.io
HOST:              Cloudflare (confirmed via `server: cloudflare` response header)
SOURCE AUDIT:      Leep AI Site Inspection, 2026-08-15
                   Score 12/85 possible · Confidence Grade C
ACCESS AVAILABLE:  <repo write? Cloudflare dashboard? DNS? Search Console? PSI key? CrUX key?>
DEPLOY TARGET:     <Cloudflare Pages? Workers? other?>
CONSTRAINT:        Remediate in place. Do NOT rewrite in Next.js.
```

### Verified facts about the codebase — established, do not re-derive

These were confirmed by direct inspection of the production bundle
`/assets/index-CAptjTRU.js` on 2026-08-15. Treat as `[OBSERVED]`:

| Fact | Value | How it was established |
|---|---|---|
| React version | **18.3.1** | `version:"18.3.1"` in bundle |
| Build tool | Vite | `<script type="module" crossorigin>` + hashed `/assets/` output |
| Router | React Router (inferred) | `useNavigate` ×2, `Navigate` ×6 present; package name minified away |
| UI primitives | Radix UI | 43 `radix` references; `forceMount` available (17 refs) |
| Icons | Lucide | 55 references |
| Head manager | **NONE** | `document.title` appears **0 times**; no `react-helmet` |
| Bundle size | 1,156,970 B raw / 330,581 B Brotli | `wc -c` and `curl --compressed` |
| Code splitting | None | single `index-*.js` entry |
| Routes | 5 | `/`, `/demo`, `/privacy`, `/terms`, `/sms-terms` |

**Why the React version matters and changes the fix:** React 19 hoists
`<title>`, `<meta>` and `<link>` rendered anywhere in the component tree into
`<head>` natively, which removes the need for a head-manager library. **This
site is on 18.3.1, so that capability is not available.** You have a real fork
in the road at FIX-02 — resolve it explicitly, do not assume.

---

## PART 2 — MANDATORY PRE-FLIGHT (DO NOT WRITE CODE UNTIL THIS IS DONE)

Execute in order. Paste real output for each. If any step fails, stop and
report rather than proceeding on assumption.

### P0.1 — Capture the baseline you will be judged against

```bash
mkdir -p ./seo-baseline && cd ./seo-baseline

# raw HTML for every route, as the crawler first receives it
for p in "" demo privacy terms sms-terms; do
  curl -sSL -A "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" \
    "https://www.leepai.io/$p" -o "raw${p:-index}.html"
done

curl -sSL https://www.leepai.io/robots.txt  -o robots.txt
curl -sSL https://www.leepai.io/sitemap.xml -o sitemap.xml
curl -sSI https://www.leepai.io/            -o headers.txt

# status matrix — record it, you must not regress any of these
for u in "http://leepai.io/" "https://leepai.io/" "http://www.leepai.io/" \
         "https://www.leepai.io/" "https://www.leepai.io/index.html" \
         "https://www.leepai.io//" "https://www.leepai.io/?utm_source=test" \
         "https://www.leepai.io/zzz-does-not-exist"; do
  printf '%-46s ' "$u"
  curl -sSIL -o /dev/null -w '%{http_code} hops=%{num_redirects} -> %{url_effective}\n' "$u"
done | tee status-matrix-before.txt
```

### P0.2 — Resolve the audit's single biggest blind spot

The source audit could not reach the apex domain — its proxy blocked it, not
the origin. This is FINDING **V1-06** and it is unscored. Resolve it first,
because it changes the priority of everything else.

```bash
for u in "http://leepai.io/" "https://leepai.io/" "https://leepai.io/demo"; do
  printf '%-32s ' "$u"
  curl -sSIL -o /dev/null -w '%{http_code} hops=%{num_redirects} -> %{url_effective}\n' "$u"
done
```

- **If every line 301s to `https://www.leepai.io/...`** → V1-06 is clear. Note
  it and continue.
- **If the apex returns 200** → you have a complete duplicate of the site at a
  second hostname with no canonical on either side. Escalate to CRITICAL,
  promote to the top of Phase 1, and fix via Cloudflare Bulk Redirect
  (`leepai.io/*` → `https://www.leepai.io/$1`, 301) before anything else.

### P0.3 — Measure what the audit could not

The audit marked Vector 3 UNSCORED because CrUX, PageSpeed Insights and
Lighthouse were all unreachable from its environment. You must close that gap
or the score cannot exceed 85.

```bash
# lab
npx -y lighthouse "https://www.leepai.io/" --form-factor=mobile \
  --throttling-method=simulate --output=json --output-path=./lh-mobile-before.json
npx -y lighthouse "https://www.leepai.io/" --preset=desktop \
  --output=json --output-path=./lh-desktop-before.json

# read the numbers that matter — NOT the overall score
node -e "const a=require('./lh-mobile-before.json').audits;
 console.log('LCP        ', a['largest-contentful-paint'].displayValue);
 console.log('TBT        ', a['total-blocking-time'].displayValue, '(INP lab proxy)');
 console.log('CLS        ', a['cumulative-layout-shift'].displayValue);
 console.log('LCP element', JSON.stringify(a['largest-contentful-paint-element']?.details?.items?.[0]));
 console.log('3rd party  ', JSON.stringify(a['third-party-summary']?.details?.items,null,1));"

# field — the signal Google actually documents for page experience
curl -s "https://chromeuxreport.googleapis.com/v1/records:queryRecord?key=$CRUX_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"url":"https://www.leepai.io/","formFactor":"PHONE"}'
```

**If CrUX returns no URL-level data, fall back to origin level and label the
fallback.** If there is no origin-level data either, the site does not yet
have enough traffic to appear in the dataset — record that as a fact, do not
treat it as a pass or a failure. See PART 6.

### P0.4 — Retrieve the standards you are about to cite

Do not proceed on memory. Retrieve and record the last-updated date of each:

| What you need | Where | Used to justify |
|---|---|---|
| LCP / INP / CLS definitions + thresholds | web.dev | Phase 5 targets |
| Crawl / render / index model | Search Central, JavaScript SEO basics | FIX-01 |
| Canonical: rendered-HTML handling | Search Central + I/O 2018 statements | FIX-01, FIX-03 |
| Soft 404 handling | Search Central | FIX-04 |
| Structured data general guidelines | Search Central | FIX-06 |
| FAQPage rich result status | Search Central structured data docs | FIX-07 (confirm it is dead) |
| robots.txt group merging | RFC 9309 | FIX-10 |
| `og:image` absolute URL requirement | ogp.me | FIX-09 |

### P0.5 — Verify every package before you install it

```bash
for p in react-helmet-async vite-react-ssg vike @vitejs/plugin-react react react-dom; do
  echo "--- $p"; npm view "$p" version time.modified deprecated 2>&1 | head -4
done
```

Record the results. **If a package named in this prompt does not exist, is
deprecated, or has not published in 18+ months, substitute the current
equivalent and document the substitution with your reasoning.** This prompt
was written in an environment where the npm registry was unreachable, so
package names here are candidates to verify, not verified facts.

---

## PART 3 — THE REMEDIATION SEQUENCE

Ordered by **dependency**, not by audit severity. Phase 1 gates everything:
several later fixes are pointless or actively wrong if shipped before it.

---

### PHASE 1 — THE FOUNDATION (gates all downstream work)

#### FIX-01 · Get the content into the raw HTML
**Closes:** V2-01 (CRITICAL) · **Enables:** FIX-02, FIX-03, FIX-06
**Evidence of defect:** raw HTML contains 9 content words and 5 links;
rendered DOM contains 1,209 words and 39 links.

**The decision, and why it is not optional.**

The audit's own remediation section suggested a head manager could deliver the
canonical client-side. **That was wrong, and this prompt corrects it.** Google
stated at I/O 2018 (Tom Greenaway; subsequently confirmed by John Mueller)
that it does **not** look for `rel="canonical"` in rendered HTML. Third-party
testing indicates JS-injected canonicals are sometimes eventually honoured,
but slowly and unreliably.

**Verify this claim yourself before building on it** — it is the load-bearing
justification for the entire architecture below. If current Google
documentation contradicts it, re-plan and say so.

The consequence: **the canonical must exist in the raw server response.** That
makes static pre-rendering mandatory rather than merely preferable, and it is
why this phase comes first.

**Choose one path. Justify the choice with retrieved sources.**

| Path | What it is | Choose when |
|---|---|---|
| **A — Build-time prerender** | Render all 5 routes to static HTML at build | Default. 5 static marketing routes, no per-request data. Lowest risk. |
| **B — React Router v7 SSG** | Migrate router to v7, use its built-in prerendering | Already on React Router and willing to take the v7 migration |
| **C — Framework migration** | Astro / Next.js | **Explicitly out of scope per the input block. Do not choose this.** |

Path A is the recommendation. Rationale: five routes, all static content, no
per-request personalisation, existing Vite build, and the smallest possible
diff against a working production site. Note that the maintainer of
`vite-react-ssg` recommends React Router v7's official SSG when the project is
already on React Router v7 — so **check the installed React Router major
version first** and prefer Path B if it is already v7.

```bash
# establish which path you are on before choosing
npm ls react-router react-router-dom 2>/dev/null
```

**Acceptance test — this is the whole point of the phase:**

```bash
curl -sSL -A Googlebot https://www.leepai.io/ | grep -c "Every Text and Call Answered"
# MUST return 1. Currently returns 0.
```

Whatever path you choose, it is not done until that command returns 1 and the
canonical, title, and JSON-LD are all present in `view-source`, not just in
the rendered DOM.

---

#### FIX-02 · Install per-route document metadata
**Closes:** V5-01 (HIGH), V5-02 (HIGH), V5-04 (MEDIUM)
**Evidence:** all 5 URLs serve byte-identical HTML (3,760 bytes) with one
shared `<title>` and one shared description. `document.title` appears 0 times
in the bundle.

**The React 18 fork — resolve explicitly:**

- **Option 1 — stay on React 18.3.1, add a head manager.** Smaller change,
  no upgrade risk. Verify the package is current (R2) before installing.
- **Option 2 — upgrade to React 19, use native metadata hoisting.** Removes a
  dependency permanently; `<title>` and `<meta>` rendered anywhere in the tree
  are hoisted to `<head>` natively. Larger blast radius — it is a major
  version upgrade against Radix and Lucide.

State which you chose and why. **If you choose Option 2, run the full React 19
upgrade checklist and test every Radix component**, because a broken
accordion silently re-breaks FIX-07.

Single source of truth for route metadata either way:

```js
// src/seo/routes.js
export const ORIGIN = 'https://www.leepai.io';

export const SEO = {
  '/': {
    title: 'Leep AI — AI Receptionist for Home Service Businesses',
    description:
      'Leep AI answers every call and text, books appointments, and follows up on every lead 24/7 for HVAC, plumbing, electrical and home service teams.',
  },
  '/demo': {
    title: 'Book a Leep AI Demo — See the AI Receptionist Live',
    description:
      'Watch Leep AI answer a live call, book an appointment, and follow up on a lead. 20-minute walkthrough for home service operators.',
  },
  '/privacy': {
    title: 'Privacy Policy — Leep AI',
    description:
      'How Leepai, Inc. collects, uses, and protects customer and caller data.',
  },
  '/terms': {
    title: 'Terms of Service — Leep AI',
    description:
      'The terms governing use of Leep AI products and services.',
  },
  '/sms-terms': {
    title: 'SMS Terms & Conditions — Leep AI',
    description:
      'Messaging terms, opt-in and opt-out instructions, and carrier disclosures for Leep AI SMS.',
  },
};
```

**Constraints on the copy you write:**
- Titles must be unique across all 5 routes.
- SERP truncation is pixel-driven, not character-driven — roughly 580px mobile
  / 600px desktop is a working heuristic, not a rule. Do not pad to a
  character count.
- The meta description is **not a ranking factor**. It affects click-through.
  Write it for a human deciding whether to click.
- Google rewrites title links frequently. Treat the title as a strong input,
  not a guarantee.

**Verify:**
```bash
for p in "" demo privacy terms sms-terms; do
  curl -sSL "https://www.leepai.io/$p" | grep -oE '<title>[^<]*'
done | sort -u | wc -l    # MUST equal 5
```

---

#### FIX-03 · Emit a self-referencing canonical on every route
**Closes:** V1-01 (CRITICAL), V1-04 (MEDIUM)
**Depends on:** FIX-01 (must be in raw HTML — see the correction above)

```jsx
// src/seo/Seo.jsx — used by every route
import { SEO, ORIGIN } from './routes';

export default function Seo({ path }) {
  const { title, description } = SEO[path];
  const url = ORIGIN + path;
  const image = `${ORIGIN}/leep-ai-og.jpg`;   // absolute — see FIX-09

  return (
    <>
      <title>{title}</title>
      <meta name="description" content={description} />
      <link rel="canonical" href={url} />
      <meta property="og:url" content={url} />
      <meta property="og:site_name" content="Leep AI" />
      <meta property="og:type" content="website" />
      <meta property="og:title" content={title} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:image:width" content="1200" />
      <meta property="og:image:height" content="630" />
      <meta property="og:image:alt" content="Leep AI — AI workforce for home service businesses" />
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:site" content="@LeepAI" />
      <meta name="twitter:title" content={title} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
      <meta name="theme-color" content="#d4a84c" />
    </>
  );
}
```

*(Shown in React 19 native-metadata form. On React 18, wrap the same tags in
your chosen head manager's component.)*

**Canonical correctness checklist — verify every line:**
- Absolute URL, not relative ✓
- Exactly one per page ✓
- In `<head>`, not injected into `<body>` — Google ignores canonicals in `<body>`
- Self-referencing on all 5 routes ✓
- Agrees with the sitemap's URL form (`www`) ✓
- Points at a URL that returns 200 and is not `noindex` ✓
- No parameters in the canonical value ✓

**Verify:**
```bash
curl -sSL https://www.leepai.io/demo | grep -i canonical
# expect exactly: <link rel="canonical" href="https://www.leepai.io/demo"/>
```

---

#### FIX-04 · Return a real 404 status for unmatched routes
**Closes:** V1-02 (CRITICAL)
**Evidence:** `/this-page-does-not-exist-xyz` returns HTTP 200 with md5
`c304036f5f130a7450d925cb155247c0` — byte-identical to the homepage.

Keep the client-side 404 view; it is good UX. Only the wire status is wrong.

```js
// functions/_middleware.js  (Cloudflare Pages Functions)
const KNOWN = new Set(['/', '/demo', '/privacy', '/terms', '/sms-terms']);

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);

  // collapse repeated slashes -> 301 (closes V1-04)
  if (/\/{2,}/.test(url.pathname)) {
    url.pathname = url.pathname.replace(/\/{2,}/g, '/');
    return Response.redirect(url.toString(), 301);
  }

  const path = url.pathname.replace(/\/+$/, '') || '/';
  const isAsset = /\.[a-z0-9]+$/i.test(path);

  if (isAsset || KNOWN.has(path)) return next();

  const shell = await next(new Request(new URL('/', url), request));
  return new Response(shell.body, { status: 404, headers: shell.headers });
}
```

**If the deploy target is not Cloudflare Pages, produce the equivalent for the
actual platform and say which platform you targeted.** Do not ship a Pages
Function to a non-Pages host and call it done.

**Verify:**
```bash
curl -sSI -o /dev/null -w '%{http_code}\n' https://www.leepai.io/zzz-should-404   # 404
curl -sSI -o /dev/null -w '%{http_code}\n' https://www.leepai.io/demo             # 200
curl -sSIL -o /dev/null -w '%{http_code} %{url_effective}\n' 'https://www.leepai.io//'
```

**Regression guard:** re-run the full status matrix from P0.1 and diff it. A
404 fix that accidentally 404s a real route is a worse outcome than the
original defect.

---

### PHASE 2 — IDENTITY

#### FIX-05 · Standardise on one URL form everywhere
**Closes:** V2-03 (MEDIUM), V7-03 (LOW)
**Evidence:** the `<noscript>` block links to `https://leepai.io` (apex) while
the sitemap declares `https://www.leepai.io/`. `/demo` is linked in two forms
from the same page.

Canonical host: **`https://www.leepai.io`** — it is what the sitemap already
declares, which makes it the lowest-churn choice.

- Internal links → root-relative (`/demo`) so the form cannot drift
- Absolute URLs → only in canonical, Open Graph, sitemap, and schema `@id`
- Fix the `<noscript>` link in `index.html` to the `www` form

```bash
# should both return 0 after the fix
curl -sSL https://www.leepai.io/ | grep -c 'href="https://leepai.io"'
curl -sSL https://www.leepai.io/ | grep -c 'href="https://www.leepai.io/demo"'
```

---

#### FIX-06 · Ship a connected `@graph` — rung 4, not scattered blocks
**Closes:** V4-01 (CRITICAL), and partially V6-02
**Evidence:** 0 JSON-LD blocks, 0 Microdata, 0 RDFa on all 5 routes.
Connectivity ladder rung 0 of 4.

Every node carries an `@id`. Every relationship is an `@id` pointer. No orphan
nodes, no dangling pointers.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://www.leepai.io/#organization",
      "name": "Leep AI",
      "legalName": "Leepai, Inc.",
      "url": "https://www.leepai.io/",
      "email": "support@leepai.io",
      "telephone": "+1-714-906-6080",
      "logo": {
        "@type": "ImageObject",
        "@id": "https://www.leepai.io/#logo",
        "url": "https://www.leepai.io/leep-ai-icon.png",
        "width": 180,
        "height": 180
      },
      "image": { "@id": "https://www.leepai.io/#logo" },
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "2409 Huntington Ln #A",
        "addressLocality": "Redondo Beach",
        "addressRegion": "CA",
        "postalCode": "90278",
        "addressCountry": "US"
      },
      "founder": { "@id": "https://www.leepai.io/#aaron-strazicich" },
      "sameAs": [
        "https://www.linkedin.com/company/leep-ai/",
        "https://www.instagram.com/leep_ai/",
        "https://www.facebook.com/profile.php?id=61590516056846"
      ]
    },
    {
      "@type": "Person",
      "@id": "https://www.leepai.io/#aaron-strazicich",
      "name": "Aaron Strazicich",
      "jobTitle": "Founder",
      "worksFor": { "@id": "https://www.leepai.io/#organization" }
    },
    {
      "@type": "WebSite",
      "@id": "https://www.leepai.io/#website",
      "url": "https://www.leepai.io/",
      "name": "Leep AI",
      "publisher": { "@id": "https://www.leepai.io/#organization" },
      "inLanguage": "en-US"
    },
    {
      "@type": "WebPage",
      "@id": "https://www.leepai.io/#webpage",
      "url": "https://www.leepai.io/",
      "name": "Leep AI - AI Workforce for Home Service Businesses",
      "isPartOf": { "@id": "https://www.leepai.io/#website" },
      "about": { "@id": "https://www.leepai.io/#organization" },
      "primaryImageOfPage": { "@id": "https://www.leepai.io/#logo" },
      "inLanguage": "en-US"
    },
    {
      "@type": "Service",
      "@id": "https://www.leepai.io/#service",
      "name": "AI Workforce for Home Service Businesses",
      "serviceType": "AI receptionist and lead response automation",
      "description": "AI voice and messaging agents that answer every call and text, book appointments, and follow up on leads 24/7 for home service businesses.",
      "provider": { "@id": "https://www.leepai.io/#organization" },
      "areaServed": { "@type": "Country", "name": "United States" },
      "audience": { "@type": "BusinessAudience", "name": "Home service businesses" }
    }
  ]
}
</script>
```

**Deliberately omitted — do not add these (R5):**

| Omitted | Why |
|---|---|
| `AggregateRating`, `Review` | No star ratings visible anywhere on the page. Manual action risk. |
| `priceRange`, `Offer` price | Pricing section says "Let's Build Your Custom Plan" — no visible prices. |
| `FAQPage` | Rich result withdrawn. Verify current status; do not add. |
| `LocalBusiness` | Real street address, but the business sells nationally rather than serving walk-ins. `Organization` + `PostalAddress` is the honest model. |
| `BreadcrumbList` | Add when the site gains depth — see FIX-14. |

**Per-route note:** the `WebPage` node's `@id`, `url` and `name` must change
per route. Generate it from the same `SEO` map as FIX-02 so it cannot drift.

**Verify — two different questions, run both:**
```bash
curl -sSL https://www.leepai.io/ | grep -c 'application/ld+json'   # 1
curl -sSL https://www.leepai.io/ | grep -c 'AggregateRating'       # 0 — must stay 0
```
- Spec conformance → https://validator.schema.org/
- Google eligibility → https://search.google.com/test/rich-results

These answer different questions. Passing one does not imply the other.

---

#### FIX-07 · Mount the FAQ answers into the DOM
**Closes:** V2-02 (HIGH)
**Evidence:** 7 questions render; 0 answers. Probes for "onboarding",
"contract", "typically" all return 0 occurrences in rendered text. The answers
exist in the bundle (~350 words) but Radix unmounts collapsed content.

`forceMount` is already present in the bundle (17 references) — it is simply
not applied here.

```jsx
<Accordion.Root type="single" collapsible>
  {FAQS.map(({ q, a }, i) => (
    <Accordion.Item key={i} value={`faq-${i}`}>
      <Accordion.Header>
        <Accordion.Trigger>{q}</Accordion.Trigger>
      </Accordion.Header>

      {/* forceMount keeps the answer in the DOM at all times.
          Radix still sets data-state, so CSS handles the collapse. */}
      <Accordion.Content forceMount className="faq-content">
        <p>{a}</p>
      </Accordion.Content>
    </Accordion.Item>
  ))}
</Accordion.Root>
```

```css
.faq-content { overflow: hidden; }
.faq-content[data-state="closed"] { height: 0; visibility: hidden; }
.faq-content[data-state="open"]   { height: auto; visibility: visible; }
```

**Do not add `FAQPage` markup (R6).** The win here is the text being in the
DOM. Verify the rich-result status yourself and record what you found.

**Verify:**
```bash
curl -sSL https://www.leepai.io/ | grep -c "dedicated onboarding specialist"   # 1
```

---

#### FIX-08 · Truthful `<lastmod>` in the sitemap
**Closes:** V1-03 (MEDIUM)
**Evidence:** 0 `<lastmod>` elements across 5 URLs; `changefreq` and
`priority` present instead.

```js
// scripts/sitemap.mjs — run in the build
import { writeFileSync, statSync } from 'node:fs';

const ORIGIN = 'https://www.leepai.io';
const ROUTES = [
  { path: '/',          src: 'src/pages/Home.jsx' },
  { path: '/demo',      src: 'src/pages/Demo.jsx' },
  { path: '/privacy',   src: 'src/pages/Privacy.jsx' },
  { path: '/terms',     src: 'src/pages/Terms.jsx' },
  { path: '/sms-terms', src: 'src/pages/SmsTerms.jsx' },
];

const body = ROUTES.map(({ path, src }) => {
  const lastmod = statSync(src).mtime.toISOString().slice(0, 10);
  return `  <url>\n    <loc>${ORIGIN}${path}</loc>\n    <lastmod>${lastmod}</lastmod>\n  </url>`;
}).join('\n');

writeFileSync('public/sitemap.xml',
  `<?xml version="1.0" encoding="UTF-8"?>\n` +
  `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`);
```

**Do not stamp every URL with today's date on every deploy.** That trains
Google to ignore the field. Derive it from real file mtimes or git history.

Sitemap integrity checklist: valid XML · within documented size and URL limits
· only canonical, indexable, 200-status URLs · no robots-disallowed URLs ·
referenced in robots.txt · submitted in Search Console.

**Verify:** `curl -sSL https://www.leepai.io/sitemap.xml | grep -c lastmod` → 5

---

### PHASE 3 — DELIVERY

#### FIX-09 · Image optimisation and the Open Graph image
**Closes:** V5-03 (MEDIUM), V8-02 (MEDIUM), and the CLS half of V2-04
**Evidence (all measured against the live origin):**

| Asset | Bytes | Problem |
|---|---|---|
| `/leep-ai-og.png` | 2,264,100 | 2.26 MB, and referenced by a **relative** URL |
| `/founder-family.jpg` | 1,032,306 | 1.03 MB |
| `/danny-thumbnail.jpg` | 903,375 | 903 KB, not lazy-loaded |
| `/leep-ai-icon.png` | 543,899 | 544 KB favicon |
| `/assets/leepai-logo-*.png` | 285,870 | 286 KB for a 40px-tall logo |
| **Total** | **~5.03 MB** | none in WebP/AVIF; no format negotiation |

```bash
# verify sizes and package before converting (R2)
npm view sharp-cli version time.modified

npx -y sharp-cli -i public/founder-family.jpg  -o public/founder-family.webp  -f webp -q 82
npx -y sharp-cli -i public/danny-thumbnail.jpg -o public/danny-thumbnail.webp -f webp -q 82
npx -y sharp-cli -i public/leep-ai-og.png      -o public/leep-ai-og.jpg       -f jpeg -q 85 --width 1200 --height 630 --fit cover
npx -y sharp-cli -i src/assets/leepai-logo.png -o src/assets/leepai-logo.webp -f webp -q 90 --width 160
npx -y sharp-cli -i public/leep-ai-icon.png    -o public/leep-ai-icon.png     -f png  --width 180
```

Also enable **Cloudflare Polish** (Speed → Optimization → Polish: Lossy, WebP
on) — it fixes format negotiation at the edge with no code change.

**Every `<img>` needs explicit `width` and `height`** — currently none carry
them, which is a direct CLS contributor:

```html
<!-- LCP candidate: never lazy, always high priority -->
<img src="/assets/leepai-logo.webp" alt="Leep AI"
     width="160" height="40" fetchpriority="high" decoding="async">

<!-- below the fold: always lazy, always dimensioned -->
<img src="/danny-thumbnail.webp"
     alt="Danny Reyes, owner of South Bay Royal Detailing"
     width="640" height="360" loading="lazy" decoding="async">
```

That `alt` also closes **V8-03 (LOW)** — the thumbnail currently carries
`alt=""` although it is content, not decoration.

**Do not apply `fetchpriority="high"` until FIX-13 tells you what the real LCP
element is.** Guessing the LCP element and preloading the wrong thing makes
LCP worse.

**Verify:**
```bash
curl -sSI -H 'Accept: image/webp' https://www.leepai.io/founder-family.jpg | grep -i content-type
curl -sSL https://www.leepai.io/ | grep -c 'og:image" content="https://'   # 1
```

---

#### FIX-10 · Security headers and immutable asset caching
**Closes:** V8-01 (HIGH)
**Evidence:** only `x-content-type-options` and `referrer-policy` present.
Missing: HSTS, CSP, X-Frame-Options, Permissions-Policy. Hashed build assets
ship `max-age=14400, must-revalidate`.

```
# public/_headers
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), interest-cohort=()
  Content-Security-Policy-Report-Only: default-src 'self'; script-src 'self' 'unsafe-inline' https://widgets.leadconnectorhq.com https://r2.leadsy.ai; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.leadconnectorhq.com https://api.elevenlabs.io https://r2.leadsy.ai; frame-src https://api.leadconnectorhq.com https://meetings-na2.hubspot.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self' https://api.leadconnectorhq.com

/assets/*
  Cache-Control: public, max-age=31536000, immutable
```

**Ship the CSP in `Report-Only` first and watch for a week.** The chat widget,
the booking widget and the ElevenLabs voice agent will surface any missing
origins before you enforce. Only then rename the header to
`Content-Security-Policy`.

**These are not ranking factors and you may not present them as such.** This
is a security fix on a site that collects phone numbers and runs an SMS
programme.

Also fix **V1-05 (LOW)** — `robots.txt` has two `User-agent: *` groups. Delete
the hand-written trailing block; the Cloudflare-managed one already allows
everything unnamed. Keep only the `Sitemap:` line.

**Verify:**
```bash
curl -sSI https://www.leepai.io/ | grep -Ei 'strict-transport|content-security|x-frame|permissions-policy'
curl -sSI https://www.leepai.io/assets/index-*.js | grep -i immutable
curl -sSL https://www.leepai.io/robots.txt | grep -c '^User-agent: \*'   # 1
```

---

### PHASE 4 — THE INFERRED FINDINGS (MEASURE FIRST — R3)

Everything in this phase was tagged `[INFERRED]` by the source audit. Each
carries a falsification test. **Run the test. Record the result. Only fix if
the test confirms the defect.**

#### FIX-11 · Entrance animations and layout shift
**Tests:** V2-04 (LOW, INFERRED)
**Claim to test:** 75 elements render at `opacity: 0` with
`translateY(20px)` entrance transforms, which the audit reasoned may
contribute to CLS.

```bash
node -e "const a=require('./lh-mobile-before.json').audits;
 console.log('CLS:', a['cumulative-layout-shift'].numericValue);
 console.log(JSON.stringify(a['layout-shift-elements']?.details?.items, null, 1));"
```

- **If CLS is within the current "good" threshold** (retrieve it — do not
  quote from memory) **and no shift is attributed to these elements** → the
  inference is falsified. Record that and do not change the animations.
- **If confirmed** → make the animation additive rather than gating, so
  content is never dependent on an observer firing:

```css
.reveal { opacity: 1; }              /* visible by default */

@media (prefers-reduced-motion: no-preference) {
  .reveal { opacity: 0; transform: translateY(20px);
            transition: opacity .5s ease, transform .5s ease; }
  .reveal.is-visible { opacity: 1; transform: none; }
}
```

Reserve space with `min-height` on animated containers regardless — that is
cheap and correct either way.

---

#### FIX-12 · Non-passive listeners and INP
**Tests:** V3-02 (INFERRED)
**Claim to test:** 4 of 6 `scroll` listeners, plus `touchstart`, `touchmove`,
`wheel` and 3 `resize` listeners, are registered without `{ passive: true }`;
combined with 14 `getBoundingClientRect` and 17 `getComputedStyle` calls, the
audit inferred layout-thrash risk. **The audit did not prove these run inside
an interaction handler.**

**Lighthouse does not report INP.** INP requires real user interaction; TBT is
the lab proxy. Any tool claiming a "Lighthouse INP score" is fabricating it.

Test properly:
1. Chrome DevTools → Performance → record while clicking the FAQ items, the
   pricing tabs, and the ROI calculator inputs.
2. Read long-task attribution. Identify the top 5 tasks >50ms and attribute
   each to a specific script.
3. Or instrument the field directly:

```js
import { onINP, onLCP, onCLS } from 'web-vitals';

function send(metric) {
  navigator.sendBeacon('/api/vitals', JSON.stringify({
    name: metric.name, value: metric.value,
    rating: metric.rating, id: metric.id, path: location.pathname,
  }));
}
onINP(send); onLCP(send); onCLS(send);
```

**Only if long tasks are attributed to these handlers**, fix them — passive by
default, reads batched before writes:

```js
let ticking = false;

function onScroll() {
  if (ticking) return;
  ticking = true;

  requestAnimationFrame(() => {
    // READ phase — all measurements first
    const y = window.scrollY;
    const rect = el.getBoundingClientRect();

    // WRITE phase — all mutations after
    header.classList.toggle('is-stuck', y > 80);
    el.style.setProperty('--offset', `${rect.top}px`);

    ticking = false;
  });
}

window.addEventListener('scroll',    onScroll,    { passive: true });
window.addEventListener('touchmove', onTouchMove, { passive: true });
window.addEventListener('wheel',     onWheel,     { passive: true });
```

Note: many of these registrations may belong to Radix or Lucide rather than
first-party code. **Do not patch a dependency's internals.** If the long tasks
trace to a library, upgrade it or report the constraint.

---

#### FIX-13 · LCP element and third-party cost
**Tests:** V3-01, V3-03 (both INFERRED)
**Claim to test:** the audit inferred that a 286 KB logo and a 903 KB
non-lazy thumbnail compete for bandwidth during load, with no
`fetchpriority` hint. It explicitly did not identify the real LCP element.

```bash
node -e "const a=require('./lh-mobile-before.json').audits;
 console.log('LCP element:', JSON.stringify(a['largest-contentful-paint-element']?.details?.items,null,1));
 console.log('3rd party:',   JSON.stringify(a['third-party-summary']?.details?.items,null,1));
 console.log('render-block:',JSON.stringify(a['render-blocking-resources']?.details?.items,null,1));"
```

- **If LCP resolves to the H1 text node and is within threshold** → the image
  inference is falsified for LCP. The bandwidth waste is still real (FIX-09
  stands as a delivery fix), but do not claim an LCP benefit you did not
  measure.
- **If LCP is an image** → apply `fetchpriority="high"` to *that* element and
  preload it. Never lazy-load the LCP image.

The LeadConnector chat widget script carries no `async` or `defer` — that part
is `[OBSERVED]`, not inferred, and is worth deferring on its own merits:

```html
<script>
  (function () {
    function loadChat() {
      var s = document.createElement('script');
      s.src = 'https://widgets.leadconnectorhq.com/loader.js';
      s.setAttribute('data-resources-url', 'https://widgets.leadconnectorhq.com/chat-widget/loader.js');
      s.setAttribute('data-widget-id', '6a0d44a9ce8bed0f821020ca');
      s.setAttribute('data-source', 'WEB_USER');
      s.async = true;
      document.body.appendChild(s);
    }
    if ('requestIdleCallback' in window) {
      requestIdleCallback(loadChat, { timeout: 4000 });
    } else {
      window.addEventListener('load', function () { setTimeout(loadChat, 2000); });
    }
  })();
</script>
<link rel="preconnect" href="https://widgets.leadconnectorhq.com" crossorigin>
<link rel="dns-prefetch" href="https://r2.leadsy.ai">
```

**Verify the chat widget still works after deferring it.** A silently broken
lead-capture widget costs more than the milliseconds it saves.

Also consider code-splitting the 1.13 MB single bundle by route — but
**measure the benefit before and after**, and do not claim one you did not
observe.

---

### PHASE 5 — CONTENT ARCHITECTURE

#### FIX-14 · Give the ROI calculator its own URL
**Closes:** part of V6-01 (MEDIUM)

The ROI calculator is genuine information gain — original, interactive,
specific to the vertical, and hard for a competitor to copy. It is currently
an anchor (`#roi-calculator`) on the homepage, so it cannot rank on its own.

Promote it to `/missed-call-revenue-calculator` with its own title,
description, canonical, and surrounding explanatory copy. Keep the homepage
section; link the two.

Add `BreadcrumbList` at this point — closes **V7-01 (MEDIUM)**, which was
correctly deprioritised while the site was flat:

```json
{
  "@type": "BreadcrumbList",
  "@id": "https://www.leepai.io/missed-call-revenue-calculator#breadcrumb",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home",
      "item": "https://www.leepai.io/" },
    { "@type": "ListItem", "position": 2, "name": "Missed Call Revenue Calculator",
      "item": "https://www.leepai.io/missed-call-revenue-calculator" }
  ]
}
```

Reference it from the `WebPage` node via
`"breadcrumb": { "@id": "..." }` so it is not an orphan node.

Also clean up **V7-02 (LOW)** — 2 anchors use `href="#"`. If the element
performs an action, it is a `<button>`, not a link.

---

#### FIX-15 · Build the informational content surface
**Closes:** the rest of V6-01 (MEDIUM)

**Before writing anything, close the audit's own stated gap.** The source
audit could not retrieve live SERPs and inferred the query set from the page's
title, H1 and nav. Its inferred set was:

> AI receptionist for home service businesses · AI answering service for
> contractors · missed call text back · AI voice agent for HVAC/plumbing ·
> speed to lead automation

**The audit explicitly flagged that if this is the wrong query set, all of
Vector 6 is audited against the wrong target.** Confirm or replace it before
building content. Then:

1. Classify dominant intent **from the actual SERP** for each query
   (informational / commercial investigation / transactional / navigational /
   local). Do not assume.
2. For informational-intent queries, the homepage cannot win regardless of
   optimisation — that is a format mismatch, not a tuning problem. Build pages
   shaped for those queries.
3. Compare against pages currently ranking. Report coverage gaps as
   information gain and intent coverage.

**Never prescribe a word count.** The homepage's 1,209 words is a measurement,
not a target.

Content rules — non-negotiable (R5, R6):
- No spun or mass-produced pages. No near-duplicate city pages with the
  place-name swapped — that is a doorway pattern.
- No unedited AI output shipped as-is.
- Truthful publish and last-updated dates. Never auto-stamp on deploy.
  This also closes **V6-03 (LOW)**: add `<time datetime="…">` to the legal
  pages, which SMS carrier compliance review typically looks for.

---

#### FIX-16 · Decide the AI-crawler policy deliberately
**Closes:** the open question raised in §4 of the audit.

The Cloudflare-managed `robots.txt` block currently disallows `GPTBot`,
`ClaudeBot`, `Google-Extended`, `CCBot`, `Bytespider` and
`meta-externalagent`, and sets `Content-Signal: ai-train=no`.

**This does not affect Google Search ranking** — `Google-Extended` is separate
from Googlebot, and Googlebot is explicitly allowed. It does mean opting out
of AI assistant surfaces.

For a company selling AI to contractors, whose buyers increasingly ask an
assistant for vendor recommendations, this deserves a deliberate decision
rather than an inherited Cloudflare default. **Do not change it unilaterally
— surface it to the business owner as a decision with both consequences
stated.**

---

## PART 4 — ACCEPTANCE GATE

No phase is complete until its verification passes. Run this in full before
declaring the work done.

```bash
#!/usr/bin/env bash
# Leep AI — remediation acceptance gate
SITE="https://www.leepai.io"
pass=0; fail=0
chk(){ if [ "$2" = "$3" ]; then printf '  PASS  %-50s %s\n' "$1" "$3"; pass=$((pass+1));
       else printf '  FAIL  %-50s got=%s want=%s\n' "$1" "$3" "$2"; fail=$((fail+1)); fi; }

echo "== PHASE 1 — foundation =="
chk "content in raw HTML" "1" \
  "$(curl -sSL -A Googlebot "$SITE/" | grep -c 'Every Text and Call Answered')"
chk "5 unique titles" "5" \
  "$(for p in "" demo privacy terms sms-terms; do curl -sSL "$SITE/$p" | grep -oE '<title>[^<]*'; done | sort -u | wc -l | tr -d ' ')"
chk "canonical on /demo" "1" "$(curl -sSL "$SITE/demo" | grep -ci 'rel="canonical"')"
chk "unmatched route 404s" "404" "$(curl -sSI -o /dev/null -w '%{http_code}' "$SITE/zzz-should-404")"
chk "real route still 200" "200" "$(curl -sSI -o /dev/null -w '%{http_code}' "$SITE/demo")"
chk "apex 301s to www" "https://www.leepai.io/" \
  "$(curl -sSIL -o /dev/null -w '%{url_effective}' 'https://leepai.io/')"

echo "== PHASE 2 — identity =="
chk "JSON-LD present" "1" "$(curl -sSL "$SITE/" | grep -c 'application/ld+json')"
chk "Organization node" "1" "$(curl -sSL "$SITE/" | grep -c '"@type": "Organization"')"
chk "NO fabricated rating" "0" "$(curl -sSL "$SITE/" | grep -c 'AggregateRating')"
chk "NO FAQPage markup" "0" "$(curl -sSL "$SITE/" | grep -c 'FAQPage')"
chk "FAQ answers in DOM" "1" "$(curl -sSL "$SITE/" | grep -c 'dedicated onboarding specialist')"
chk "lastmod on 5 URLs" "5" "$(curl -sSL "$SITE/sitemap.xml" | grep -c lastmod)"
chk "no apex self-link" "0" "$(curl -sSL "$SITE/" | grep -c 'href="https://leepai.io"')"

echo "== PHASE 3 — delivery =="
H=$(curl -sSI "$SITE/")
for h in strict-transport-security x-frame-options permissions-policy; do
  chk "$h" "1" "$(echo "$H" | grep -ci "^$h")"
done
chk "og:image absolute" "1" "$(curl -sSL "$SITE/" | grep -c 'og:image" content="https://')"
chk "single UA:* group" "1" "$(curl -sSL "$SITE/robots.txt" | grep -c '^User-agent: \*')"

echo; echo "  ---- $pass passed, $fail failed ----"
[ "$fail" -eq 0 ] || exit 1
```

Then re-run the measurement suite and diff against the P0.3 baseline:

```bash
npx -y lighthouse "https://www.leepai.io/" --form-factor=mobile \
  --throttling-method=simulate --output=json --output-path=./lh-mobile-after.json
npx -y @axe-core/cli https://www.leepai.io/ --exit
```

And in Search Console: **URL Inspection → View crawled page** → confirm the
HTML Google holds now contains the content, the canonical, and the JSON-LD.
That is the only test that directly proves FIX-01 worked from Google's side.

---

## PART 5 — OUTPUT FORMAT

Report in exactly this order:

**§0 — PRE-FLIGHT RESULTS.** Baseline captured. Apex resolved (V1-06 outcome).
Packages verified with versions and dates. Standards retrieved with dates.
Anything blocked.

**§1 — FIXES SHIPPED.** Per fix:

```
FIX ID:        FIX-04
CLOSES:        V1-02 (CRITICAL)
DECISION:      Cloudflare Pages Function middleware
WHY THIS WAY:  <reasoning + retrieved citation, publisher + URL + date>
FILES CHANGED: functions/_middleware.js (new)
VERIFICATION:  $ curl -sSI -o /dev/null -w '%{http_code}' .../zzz-should-404
               404
STATUS:        SHIPPED / BLOCKED — AWAITING ACCESS
```

**§2 — INFERRED FINDINGS: TEST RESULTS.** For each `[INFERRED]` finding, state
the test run, the actual measured result, and whether it was CONFIRMED or
FALSIFIED. Falsified findings must be reported as falsified — that is a
successful outcome, not a gap.

**§3 — MEASUREMENT DELTA.** Before/after table for LCP, TBT, CLS, payload
bytes, raw-HTML word count. Field data separately from lab data, clearly
labelled. If field data is unavailable, say so.

**§4 — NOT SHIPPED, AND WHY.** Anything blocked on access, anything
deliberately declined under R5/R6, anything the business owner must decide.

**§5 — REGRESSION RISK.** What could break, and what to watch after deploy.
Minimum: the chat widget after FIX-13, Radix components if React was upgraded,
and the full status matrix after FIX-04.

**§6 — SOURCES.** Numbered. Publisher, full URL, publication or last-updated
date. Third-party sources labelled as such. Any claim not traceable to this
list or to pasted command output must be deleted before responding.

---

## PART 6 — THE HONEST CEILING (READ THIS BEFORE PROMISING ANYTHING)

**This prompt cannot guarantee a 100/100 score, and any prompt that claims it
can is lying to you.** Four reasons, stated plainly:

**1. The rubric is bespoke and partly subjective.** The 100-point scale comes
from the companion audit prompt, not from Google. Its LOW-severity findings
are auditor's-judgement calls. A different auditor — or the same auditor on a
different day — will find a different set of cosmetic issues. There is no
external body that certifies a 100.

**2. Vector 3 cannot be scored without field data you may not be able to
generate.** Core Web Vitals field data comes from CrUX, which requires enough
real traffic at the URL or origin level to meet its reporting threshold, over
a 28-day collection window. **A low-traffic site may never have URL-level CrUX
data at all.** If that is the case here, Vector 3 stays UNSCORED — through no
fault of the code — and the maximum honest score is 85, exactly as the source
audit reported. Fixing this is a traffic problem, not an engineering problem.

**3. Some fixes take time to be reflected, not just to ship.** Canonical
consolidation, index bloat cleanup from the soft-404 fix, and re-indexing of
prerendered content all depend on Google's recrawl schedule. The code can be
correct on day one and the audit still finds symptoms on day two.

**4. Vector 6 is scored against a query set that is currently inferred.** The
source audit explicitly flagged that it derived the query set from the page
itself and may be auditing against the wrong target. Until that is confirmed
(FIX-15), the content score is measured against a guess.

**What this prompt *can* deterministically achieve:**

- Every `[OBSERVED]` finding closed, with command output proving it
- Every `[INFERRED]` finding either fixed or falsified on measured evidence
- The CRITICAL hard cap lifted — no `noindex`, no `Disallow: /`, no off-page
  canonical, no JS-only primary content, HTTPS enforced
- Vectors 1, 2, 4, 5, 7 and 8 driven to their full weight, because every
  finding in them is deterministic and verifiable
- Vector 3 moved from UNSCORED to measured, *if* field data exists
- Confidence Grade raised from **C** to **A**, by establishing Search Console
  and field data access — which is the single highest-leverage thing on this
  list, because it removes the blindness rather than the symptoms

**Report the ceiling honestly in §0 of your output.** If you cannot reach 100,
say what the real maximum is and why. A short honest report beats a long
confident one.

---

## PART 7 — SELF-AUDIT BEFORE RESPONDING

Run silently, fix, then answer:

1. Did I install a package without verifying it exists and is maintained? → verify or remove.
2. Did I fix an `[INFERRED]` finding without running its falsification test? → test it.
3. Did I add any structured-data property not visible on the page? → **delete it.**
4. Did I add `FAQPage` markup? → delete it, and cite the current status.
5. Did I cite Google without a dated, retrieved URL? → retrieve or remove the claim.
6. Did I quote a Core Web Vitals threshold from memory? → retrieve it.
7. Did I claim a fix landed without pasting the command output? → run it.
8. Did I touch anything not traceable to a FINDING ID? → justify with evidence or revert.
9. Did I predict a traffic or ranking outcome? → **delete it.** Mechanisms only.
10. Did I report a partial job as complete? → fix §0.
11. Did I break something that previously passed? → re-run the full status matrix and §4 of the audit.

---

### Provenance of this prompt

Written 2026-08-15 against the *Leep AI Site Inspection* audit of the same
date. Codebase facts in PART 1 were established by direct inspection of the
production bundle and are tagged `[OBSERVED]`.

**Two honest limitations you should know about:**

1. **The environment that produced this prompt had no access to primary
   documentation or the npm registry.** `developers.google.com`, `web.dev`,
   `schema.org`, `rfc-editor.org` and `registry.npmjs.org` were all blocked by
   network policy. Every package name and every standards claim in this
   document is therefore a **candidate to verify, not a verified fact** —
   which is exactly why R2 and R4 are mandatory pre-flight gates rather than
   suggestions.

2. **This prompt corrects an error in the source audit.** The audit's V1-01
   remediation stated that a client-side canonical "is accepted because it is
   emitted into `<head>` during render." Google's stated position (I/O 2018,
   Tom Greenaway; subsequently confirmed by John Mueller) is that it does
   **not** read canonical tags from rendered HTML. This is why FIX-01
   (prerendering) is a hard prerequisite for FIX-03 rather than an optional
   improvement. Verify this before building on it.
