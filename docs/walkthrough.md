# Walkthrough · 7 design stories behind every pixel

> A guided tour of how this landing page was actually built, **in the order decisions were made**.
> Read this top-to-bottom; each story answers one specific design question and references the
> `taste-skill` (Sections 0–5 + 14) that justified the choice.

This is **not** a post-hoc rationalization. It is a faithful record of the design process.
The git history is the proof: commit `26cc97f` ships the final page, but the
`tasks/task-20260609-interior-design-hero/outbox/` directory holds the unedited
decision artifacts (brief → 3 variants → chosen one → pre-flight → final).

---

## Story 1 · "What kind of page is this?" (taste-skill §0)

**Question:** Is this a portfolio? An agency site? An e-commerce shop? A campaign page?

**Decision:** **Campaign page for a season's release** (Autumn Edition 2026).

**Why this matters:** Each kind of page implies a different reading time, density, and CTA strategy. Calling it a "campaign" forces the design to behave like an editorial cover, not a SaaS landing.

**The one-liner taste-skill §0 demanded:**

> *"A high-end furniture and interior design campaign homepage for design-sensitive consumers (collectors, architects, design-literate public), with an editorial-magazine layout language."*

That sentence is the *first* thing written and the *last* thing verified. If you can't write it in one line, you don't know what you're building.

---

## Story 2 · "How big should the variance / motion / density be?" (taste-skill §1)

**Question:** A premium consumer site has how much variance, motion, density?

**Decision matrix:**

| Dial | Value | Reasoning |
|------|-------|-----------|
| `DESIGN_VARIANCE` | **7** | Editorial-magazine lives in 6–8. The brief said "structured but breathing" — 7 keeps the 1/3 + 2/3 split and the asymmetric grid without falling into "Artsy Chaos" (9–10). |
| `MOTION_INTENSITY` | **3** | The brief's literal word was "克制动效" (restrained motion). 3 = one hero fade, one seam-draw, no scroll triggers, no GSAP. Below 4 means `prefers-reduced-motion` is the default. |
| `VISUAL_DENSITY` | **2** | "画廊级呼吸感" (gallery-level breathing). 2 = art-gallery airy. Section padding 80–160px, grid gap 32–56px, headline `clamp(56px, 7.2vw, 96px)`. |

**The lesson:** A "premium consumer" feel is **not** a vibe — it's three numbers. Once you write them down, every subsequent decision (color, type scale, motion) follows.

---

## Story 3 · "Three variants, one decision" (the most important story)

The same brief was answered **three different ways**, and the choice was made explicitly, not by "I'll know it when I see it."

### Variant A · Editorial Poster with Bleed Photo
Full-bleed photograph fills 100vh. Display headline is anchored to the **bottom-left quadrant** of the viewport (not centered), 2 lines, eyebrow + headline + subtext + one CTA. A 1px hairline runs along the right edge of the type column.

> **Best when** the brand has a strong, moody photograph ready to ship.
> **Risk in the sandbox:** without a real image, the variant reads as an empty rectangle.

### Variant B · Split Frame with Offset Type ← **CHOSEN**
Viewport split at the **33% mark from the left** by a single 1px vertical hairline. Left third = solid warm-bone panel carrying eyebrow + headline + subtext + CTA, anchored to the bottom. Right two-thirds = full-bleed editorial photograph with a small `Index 04.26` label top-right.

> **Closest match to the ESTUDIO ANONIMO reference**, lowest visual risk, reads as premium even on a stock photo, and the hairline seam is a strong visual signature that can carry across the rest of the page (the studio block in Section 3 uses the same hairline as a top-border, locking the page's shape language).

### Variant C · Type-Forward Manifesto
Type-led. No full-bleed photograph. The top ~70% of the viewport is a single oversized display headline that starts at the left edge and wraps to ~75vw. A short italic pull-quote and a single CTA live in the bottom ~30%. A tiny 96px square photograph floats in the bottom-right corner as a tonal counterweight.

> **Best when** the brand wants maximum visual signature and is willing to bet on the headline copy doing 80% of the work.
> **Risk:** two weak words in the headline = a flat page.

**Why B won (decision matrix):**

| Risk | A | **B** | C |
|------|---|-------|---|
| Without a strong hero photo, page reads as… | empty rectangle | **quiet monograph** | fine (type-led) |
| On 1024×800 laptop, hero fits in 1st viewport | yes | **yes** | needs 120px headline cap |
| Distinctiveness vs. SaaS templates | high | **high** | very high |
| Faithfulness to ESTUDIO ANONIMO reference | medium | **high (closest match)** | low (more Awwwards) |
| The hairline seam becomes a system | no | **yes** | weak echo only |

**The lesson:** Don't ship one design. Ship three. The decision matrix is the *real* deliverable, not the chosen variant.

---

## Story 4 · "Why no centered hero?" (the anti-pattern that wasn't)

**Question:** Why is the hero split, not centered?

**The trap:** A centered hero is the most common AI default — and the fastest way to make a premium site look generic. Centering reads as "I'm not sure where to put this, so I'll put it everywhere equally."

**What we did instead:**
- The hero is **anchored to the left third**. The right two-thirds is the photograph.
- The 1px vertical hairline at the 33% mark is the strongest visual element on the page — *more important than the headline*.
- The CTA row is anchored to the **bottom of the left panel**, not centered. This creates vertical weight that pulls the eye downward, toward the second section.

**The rule of thumb:** If your hero could be described as "X with Y floating in the center," it is a centered hero. Redesign.

---

## Story 5 · "How many themes, colors, shapes are allowed?" (taste-skill §4)

This is the **anti-AI-tell** part — the part most LLM-generated pages get wrong.

### One theme. Light.
Dark mode is forbidden by the brief ("浅色中性"). No dark hero. No dark section. No dark CTA hover. **One light theme. End.**

### One accent. Oxblood `#7A2E2E`.
Used on **four** things only: hero eyebrow, pull-quote opening mark, CTA hover, page `:selection`. That's it. No brass, no clay, no AI purple. The accent appears **7 times** on the page — counted, not guessed.

### All-sharp. Zero border-radius.
Every image, every placeholder, every CTA. CTAs are text + hairline, **not** pill buttons. The single exception to "no border-radius" is the brand mark in the nav, which is a 26px square — and that's not a pill, it's a hairline-bordered box.

### The "Black and Tan" palette rule (taste-skill §4.2)
The "beige + brass + oxblood + espresso" combo is a banned look (reads as AI-real-estate). We use **bone + oxblood + ink** — the "Black and Tan" branch. The difference: we use **oxblood** for the accent, not brass; **ink** for the text, not espresso. The two are visually similar but tonally distinct, and the AI-real-estate combo is avoided.

**The lesson:** "Premium" is **subtraction**, not addition. Every time you want to add a second color, a dark section, a rounded button — *don't*.

---

## Story 6 · "How did we get rid of the AI tells?" (taste-skill §14)

The pre-flight check is a 50-item gate. Below is the **subset that catches the most AI mistakes**:

| AI tell | What it looks like | How we avoided it |
|---------|-------------------|-------------------|
| **Inter as page voice** | A SaaS look. Inter is so overused in AI output that it now signals "AI made this" | Cormorant Garamond for display, Inter Tight *only* for micro-labels (eyebrow, CTA, nav links) |
| **AI purple** | Tailwind purple-500, blue-500, gradient blue→purple | Oxblood `#7A2E2E` as the only accent. Period. |
| **3-equal cards** | The "feature grid" pattern | 6-column asymmetric grid: one large cell (4 cols), three normal (2 cols each), one wide (6 cols) |
| **Centered hero** | Headline floats in the middle of a 100vh photo | Hero is split 1/3 + 2/3, anchored to the left |
| **Jane Doe / Acme** | Fake names: "Founded by Jane Doe in 2018" | "Estudio Anonimo, Lisbon, Since 2014" — generic enough to be a placeholder, but not a stock-photo name |
| **"Quietly in use at…"** | Phrases like "quietly in use at" / "loved by" / "trusted by 10,000+" | The page has **zero** trust strips, no "Used by", no testimonials |
| **Logo wall** | "Used by Vercel, Linear, Stripe" as fake wordmarks | None. The brand mark in the nav is a 2-letter monogram, no industry label |
| **GSAP scroll listeners** | `window.addEventListener('scroll', ...)` everywhere | Zero JS. Three CSS keyframe animations. |
| **Version footer** | "v1.4.2 · Build 0048" | Footer reads "Estudio Anonimo / Lisbon / Since 2014 / Issue 04.26". No version number. |
| **Decorative dots** | A row of `· · · · ·` as decoration | The only dot characters on the page are: one `·` in the studio attribution (functional separator, allowed) and a single `·` in a hero meta label. **Zero decorative dots.** |

The full list is in [`preflight-checker.md`](./preflight-checker.md).

---

## Story 7 · "Why is the page so quiet?" (the motion story)

`MOTION_INTENSITY: 3` means **three motions total**, no scroll listeners, no JS.

| Motion | What it is | Why it exists |
|--------|-----------|---------------|
| **Hero fade-in** | `.hero__panel > *` staggered by 100ms, total reveal ≈ 1.2s | Establishes hierarchy: eyebrow → headline → subtext → CTA. The eye lands on the eyebrow first because it appears first. |
| **Seam draw** | `.hero__seam` scaleY 0→1 over 800ms, on first paint | The hairline is the page's *shape language* — drawing it tells the user "this page has structure, not just decoration." |
| **CTA hover** | Color + border shift, 200ms | Feedback. Tells the user the CTA is interactive without moving it (no hero wobble). |

**What is NOT on the page:**
- No `window.addEventListener('scroll', ...)` — zero scroll triggers
- No GSAP, no Framer Motion, no Lottie
- No magnetic hovers, no parallax, no horizontal pan
- No animated mouse icon, no "Scroll ↓" cues
- No marquee (max 1 per page, we use 0)

**The rule:** If a motion doesn't *teach the user something about hierarchy or structure*, remove it. Movement is not value; clarity is.

---

## Reading the CSS

The CSS in [`index.html`](./index.html) is inlined and organized in the order it should be read:

1. **`:root` tokens** — every color, type scale, gutter, ease. **Edit these to retheme the entire page.**
2. **Base reset** — minimal. No normalize.css, no Tailwind preflight.
3. **Grain overlay** — fixed, `pointer-events: none`, GPU-cheap. Adds a filmic texture without an extra HTTP request.
4. **Nav** — 64px tall, single line on desktop. Brand mark is a 26px square, not a logo image.
5. **Hero** — `min-height: 100dvh`, `display: grid; grid-template-columns: var(--hero-panel) 1fr;`. The hairline is `position: absolute; left: var(--hero-panel)`.
6. **CTAs** — `border-bottom: 1px solid`, not `border-radius`. The "primary" CTA is a *position* not a *style* — the only visual weight difference is on `:hover`.
7. **Sections** — every section has `padding: clamp(80px, 12vw, 160px) var(--gutter-x)` and `border-top: 1px solid var(--hair-soft)`. The hairline is the visual rhythm.
8. **Collection grid** — `grid-template-columns: repeat(6, 1fr); grid-auto-flow: dense`. The `--lg` cell spans 4 cols, normal cells span 2, `--wide` spans 6.
9. **Mobile collapse** — `@media (max-width: 879px)`. The hero flips to a stacked layout. The seam-draw becomes `scaleX(0) → scaleX(1)`.
10. **Reduced motion** — wraps every animation in `prefers-reduced-motion: reduce`.

**One CSS trick worth highlighting:** the `:root --hero-panel: clamp(340px, 38vw, 520px)` does *all* the responsive work for the hero. Change one number, the whole composition scales.

---

## What you can copy, what you can change

✅ **You can copy:**
- The `:root` token system (rename variables, keep structure)
- The 1/3 + 2/3 hero split (it works for any editorial campaign)
- The hairline-seam-as-shape-language (use it as `border-top` on sections)
- The asymmetric 6-col grid pattern

⚠️ **You can change, but understand the trade-off:**
- **Palette.** Bone + oxblood + ink → retheme by changing 4 variables. *Don't* add a second accent.
- **Type pairing.** Cormorant + Inter Tight + JetBrains Mono is one valid combination. Other valid combinations: Fraunces + Söhne + Mono; Tiempos + Inter Tight + Mono. **Don't** use Inter as page voice.
- **Hero image position.** `object-position: center 30%` was tuned for a specific photo. Change it for yours.

❌ **Don't:**
- Add a "Trusted by" logo wall
- Add dark mode
- Add scroll-triggered animations
- Add a centered hero
- Add a 3-equal-card feature grid
- Use Fraunces or Instrument_Serif as the display font (overused in AI output)
