# Pre-Flight Checker · 50 items to kill the AI tells

> A 50-item checklist, derived from taste-skill §14, that gates whether a page is
> ready to ship as "premium / editorial / not-AI-ish." Run this against any
> landing page and you'll find the cracks.

**How to use this:**

1. Open your `index.html` and `style.css` in your editor.
2. For each item below, check whether your page passes.
3. **Any single MISSING is a fail.** A PARTIAL is a fail. The list is intentionally strict.
4. Don't argue with the list. If a check fails, fix the page, not the check.

The items are grouped by what they protect against.

---

## Group 1 · Reading & dial-setting (1–4)

These are the gates that come *before* you write a single line of CSS. If these aren't true, everything downstream is suspect.

- [ ] **1.** You can describe the page in **one line**: page kind + audience + layout language. ("An editorial-magazine campaign homepage for design-sensitive consumers.")
- [ ] **2.** You have explicitly chosen values for **3 dials**: `DESIGN_VARIANCE` (1–10), `MOTION_INTENSITY` (1–10), `VISUAL_DENSITY` (1–10). Not vibes — numbers.
- [ ] **3.** Your `MOTION_INTENSITY` ≤ 4 means you have **zero** scroll listeners.
- [ ] **4.** Your `VISUAL_DENSITY` ≤ 3 means you have **80–160px** section padding and `gap: 32–56px` in grids.

---

## Group 2 · Anti-AI-tell: typography (5–10)

- [ ] **5.** **Display font is NOT Inter, NOT Fraunces, NOT Instrument_Serif.** The last two are 2024–2025 AI tells. Cormorant Garamond, Tiempos, Söhne, GT Sectra, Lyon, Recoleta are valid. (Fraunces is technically a Google Font but it's *only* in AI output now.)
- [ ] **6.** **Inter is not your page voice.** Inter Tight / Söhne / Neue Haas Grotesk may appear as a *micro-label* (eyebrow, CTA, nav link) but never as the body or display.
- [ ] **7.** **You have exactly ONE monospace font** (JetBrains Mono / IBM Plex Mono / Fragment Mono). Not two.
- [ ] **8.** **Italic display only on quotes**, not on headlines. (`font-style: italic` for pull-quotes; headlines stay upright.)
- [ ] **9.** **Display font has `letter-spacing: -0.02em`** (or tighter). Tighter spacing = more editorial.
- [ ] **10.** **No all-caps body text.** Eyebrows, nav links, CTAs can be all-caps. Body, sub, lede cannot.

---

## Group 3 · Anti-AI-tell: color (11–17)

- [ ] **11.** **One theme, light only.** No dark mode. No dark hero. No dark section. (Unless the brief explicitly says "dark editorial" — which is rare and requires a totally different motion/density pass.)
- [ ] **12.** **One accent color, used 5–10 times max.** Count every occurrence. If you can't count, you're using it too much.
- [ ] **13.** **Accent is NOT AI purple (`#6366F1`, `#8B5CF6`, `#A855F7`)**, NOT Tailwind blue-500, NOT a Tailwind gradient. Valid accents: oxblood, ink, stone, terracotta, ochre, sage.
- [ ] **14.** **Background is NOT pure white `#FFFFFF`.** Use a tinted neutral: bone, paper, off-white, warm-white, or stone-50. Pure white reads as "Bootstrap default."
- [ ] **15.** **Body text contrast is WCAG AA (4.5:1) or better.** Run your foreground/background through a contrast checker. No exceptions.
- [ ] **16.** **No "blue links"**. Inline links inherit the body color and get a `text-decoration` only on hover. The default `color: blue` is a 1998 tell.
- [ ] **17.** **Your accent does not appear on more than one section's background.** It can appear on text, borders, and hovers. It cannot fill a panel.

---

## Group 4 · Anti-AI-tell: shape (18–22)

- [ ] **18.** **All borders are 1px hairlines**, not 2px, not 3px. The hairline is a *shape language*, not a stroke.
- [ ] **19.** **All images are 0px border-radius.** Not 4px, not 8px, not 16px. Sharp.
- [ ] **20.** **All buttons are 0px border-radius.** Not 9999px (pill), not 8px (Material), not 4px (iOS).
- [ ] **21.** **CTAs are text + underline**, not filled rectangles. Even the "primary" CTA. Primary is a *position* in the page, not a *style*.
- [ ] **22.** **Cards (if you must use them) have no `box-shadow`.** Hairline border only.

---

## Group 5 · Anti-AI-tell: layout (23–32)

- [ ] **23.** **No centered hero.** The hero is anchored to one side (usually left), with a photograph on the other. Centering reads as "I gave up on composition."
- [ ] **24.** **Hero fits in 100vh on a 1024×800 laptop.** Headline 2 lines max, subtext ≤ 20 words, CTA visible without scroll.
- [ ] **25.** **Section padding is 80–160px on desktop**, not 48px, not 64px. Generous padding = "we're not desperate for clicks."
- [ ] **26.** **No 3-equal-cards feature grid.** If you have 3 things, make them asymmetric: 1 large + 2 normal, or 2 + 1, never 3 = 3.
- [ ] **27.** **Zigzag alternation caps at 2 consecutive.** Image+text → text+image → text+image→STOP. Three image+text rows in a row is the SaaS-landing page tell.
- [ ] **28.** **No more than 1 marquee per page.** (We use 0.) A marquee is a "social proof" filler.
- [ ] **29.]** **Nav is on one line, height ≤ 80px on desktop.** 56–72px is the sweet spot. Hamburger menus on desktop are an AI tell.
- [ ] **30.** **Section headers are stacked vertically** (eyebrow → title → lede), not split-header (`<h2>` left + `<p>` right) unless the section is 1200+ px wide.
- [ ] **31.** **No "Trusted by" / "Used by" / "Loved by" logo walls** — or if you must, use *real* logos with permission, not plain-text wordmarks.
- [ ] **32.** **No scroll cues.** No "Scroll ↓" text, no animated mouse icon. The page rhythm does the work.

---

## Group 6 · Anti-AI-tell: motion (33–40)

- [ ] **33.** **Zero `window.addEventListener('scroll', ...)` calls.** No scroll listeners. Period.
- [ ] **34.** **No GSAP, no Framer Motion, no Lottie, no `react-spring`.** CSS keyframes are enough.
- [ ] **35.** **All animations are ≤ 800ms.** Slow animation = "I'm trying to look cinematic" = AI-real-estate.
- [ ] **36.** **`prefers-reduced-motion: reduce` wraps every animation.** If you have 5 animations, you have 5 reduced-motion overrides. No exceptions.
- [ ] **37.** **No magnetic hovers.** Magnetic cursor following is a 2024 AI-default. (It also hurts accessibility.)
- [ ] **38.** **No parallax.** Background-attachment: fixed is a 2010s tell. Modern pages do not parallax.
- [ ] **39.** **CTAs animate color/border on hover, not position.** Moving a CTA on hover is jarring; changing color is feedback.
- [ ] **40.** **First-paint animations have a delay of 100–300ms**, not 0. Zero-delay animations feel like a glitch.

---

## Group 7 · Anti-AI-tell: copy (41–47)

- [ ] **41.** **No em-dashes (`—`)** anywhere on the page. Use commas, periods, or middle-dots (`·`). Em-dashes are the single biggest AI tells in copy. Run a grep: `grep "—" index.html style.css` must return zero results.
- [ ] **42.** **No en-dashes (`–`)** either. Use hyphens.
- [ ] **43.** **No "Quietly in use at…" / "Loved by 10,000+ teams" / "Built for the next generation of…"** headers. These are AI marketing-cliché phrases.
- [ ] **44.]** **No "Jane Doe" / "Acme Co" / "Lorem Ipsum" placeholders.** Use the brand name even if it's a placeholder; "Estudio Anonimo, Lisbon" beats "Your Brand Here."
- [ ] **45.** **Studio/founder attribution has a real-sounding place**, not "Founded by Jane Doe in 2018." "Founders · Estudio Anonimo, Lisbon" is specific and unfake-able.
- [ ] **46.** **Pull-quotes are 1–3 sentences**, not paragraphs. A 100-word blockquote is not a pull-quote; it's a wall.
- [ ] **47.** **No micro-meta sentences under eyebrows** ("we ship today, not a roadmap promise"). Eyebrows are 1–4 words max.

---

## Group 8 · Anti-AI-tell: meta (48–50)

- [ ] **48.** **Footer has no version number** ("v1.4.2", "Build 0048"). Marketing pages don't ship versions.
- [ ] **49.** **No "Try for free" / "Get started" / "Sign up" as the primary CTA.** Those are SaaS tells. For premium consumer brands, the CTA is one of: "Begin", "View the collection", "Send a note", "Read the journal".
- [ ] **50.** **No locale / city / time / weather strips** ("San Francisco · 14:32 · 18°C"). They signal "we have an API and we want to show it off."

---

## How to actually run this checklist

```bash
# In your project root:

# 1. Em-dash / en-dash hunt (the single most important check)
grep -n "—\|–" index.html style.css

# 2. Inter as page voice
grep -n "font-family: 'Inter'" index.html style.css

# 3. AI purple / Tailwind default
grep -nE "#6366F1|#8B5CF6|#A855F7|#3B82F6|#[0-9A-F]{6}" index.html style.css

# 4. Border-radius (anything > 0 is suspect)
grep -nE "border-radius:.*[1-9]" index.html style.css

# 5. Scroll listeners
grep -n "addEventListener.*scroll" *.js

# 6. Verify the dial values you wrote down
grep -n "MOTION_INTENSITY\|DESIGN_VARIANCE\|VISUAL_DENSITY" README.md
```

If any of these return a hit, **fix the page, then re-run**.

---

## What this checklist is not

It is not a quality bar for "any website." It is a quality bar for **"premium / editorial / not-AI-ish"** specifically. A SaaS dashboard, a docs site, a community forum — these are different page kinds, and the rules differ. If you're building one of those, write a different checklist (and consider contributing it to this repo).
