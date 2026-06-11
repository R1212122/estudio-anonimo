# AI Trace · 7-event agent collaboration record

> This is the **machine-readable** companion to `walkthrough.md`. Where `walkthrough.md`
> tells the design story in human voice, this document and its sibling
> `datasets/estudio-anonimo-traces.jsonl` capture the same events in a format
> suitable for **fine-tuning, evaluation, and replay**.

**If you are a researcher:** jump straight to [`datasets/estudio-anonimo-traces.jsonl`](./datasets/estudio-anonimo-traces.jsonl). The schema is OpenAI-style chat messages with tool calls.

**If you are a builder:** read the rest of this doc. It explains what each event represents and why the dataset is structured the way it is.

---

## Why this dataset is rare

Most public "AI agent" datasets are either:
- **Q&A** (Alpaca, Dolly) — single-turn, no tools
- **Code generation** (HumanEval, MBPP) — single-turn, narrow domain
- **Tool calling** (ToolBench, Gorilla) — single-turn, no reflection
- **Web navigation** (WebArena, Mind2Web) — single domain, scripted env

What is **missing** in the public ecosystem:
- **Multi-turn planning** — agent breaks a goal into subtasks before acting
- **Reflection** — agent re-reads its own output and finds flaws
- **Multi-agent collaboration** — one agent's output is another agent's input
- **Self-improvement loop** — a delivered task spawns a *new skill* that future runs can use

The seven events below are a **complete** instance of all four, in a real design task, in a real code repository, with verifiable git history.

---

## The 7 events

Each event is a single line in the JSONL file. The events are sequential — event N depends on the result of event N-1.

### Event 1 · `user_brief` — the human's instruction

The user gives a one-paragraph goal. **No system prompt, no example, no tool description.** This is the realistic input distribution.

> Build a high-end furniture and interior design campaign homepage, ESTUDIO ANONIMO style. Single page. Hero must be 100vh. No centered hero. No AI purple. No em-dash.

**What makes this hard for an LLM:** the brief is *declarative* (no AI purple) but also *aesthetic* (ESTUDIO ANONIMO style). The agent has to know the reference, not just the rule.

### Event 2 · `luma_design_read` — the Lio scheduler's decomposition

The scheduler (Lio) does **not** design the page. It:
1. Reads the brief.
2. Reads the relevant skills (`using-openclaw`, `taste-skill`).
3. Writes a 1-line *Design Read* — a one-sentence paraphrase of the page kind, audience, and layout language.
4. Sets 3 explicit *dials*: `DESIGN_VARIANCE`, `MOTION_INTENSITY`, `VISUAL_DENSITY`.
5. Spawns a *subagent* (Pixel/frontend-dev) with the brief + skill references.

**This event is the Lio contribution to the conversation.** It is the *only* place in the trace where the higher-level planning happens.

### Event 3 · `subagent_3_variants` — the designer's first move

The subagent (Pixel) does not ship one design. It ships **three**:
- **Variant A** — Editorial Poster with Bleed Photo
- **Variant B** — Split Frame with Offset Type ← chosen
- **Variant C** — Type-Forward Manifesto

Each variant is documented in a separate `hero-design-X.md` file with: composition, best-when, risk, when chosen, and a `recommended.md` file that names the chosen variant with reasons.

**What makes this hard for an LLM:** the agent must generate three *distinct* solutions, each *internally consistent*, each with a different risk profile. The skill-eval scenario "T0" is the subagent not even considering alternatives.

### Event 4 · `subagent_chosen_implementation` — the build

The subagent builds the chosen variant. Output: a single 18 KB `index.html` with inlined CSS, no JS, no build step. The CSS is structured: `:root` tokens → base → components → media queries.

**What makes this hard for an LLM:** the implementation must (a) match the chosen variant's spec, (b) not introduce new design decisions, and (c) be self-validating (open in a browser, fonts load, no console errors).

### Event 5 · `preflight_check` — the 50-item gate

The subagent runs a 50-item pre-flight check (now [`preflight-checker.md`](./preflight-checker.md)) against the page. Every item must pass.

```text
em-dash count:                0 ✅
AI purple hex:                0 ✅
border-radius > 0:            0 ✅
window.addEventListener scroll:0 ✅
Inter as page voice:          0 ✅
```

**This is the "self-audit" moment.** Without it, the page would ship with 62 em-dashes (we caught this in v1 of the same task) and 3-equal-card hero (also caught).

### Event 6 · `lio_review` — the scheduler's two-stage review

Lio (the scheduler) runs a two-stage review on the subagent's output:

| Stage | Question | Pass criterion | Example failure |
|-------|----------|----------------|-----------------|
| **Stage 1** (spec compliance) | Does it match the brief? | All explicit requirements met; no contradictions | "The brief said no centered hero; the variant C is centered" |
| **Stage 2** (code quality) | Is the code maintainable? | Naming, boundaries, tests, error handling, readability all 8+ | ".cta--primary class is never styled differently from .cta, dead class" |

**This is the "external validation" moment.** The scheduler is checking the subagent's *honesty*, not just the subagent's *output*. Stage 1 catches "I did the work but missed half the brief." Stage 2 catches "I did the work but it's spaghetti."

### Event 7 · `skill_distillation` — the self-improvement loop

After the page is accepted, Lio writes a **new skill proposal** (`github-auto-push`) capturing the procedure used to ship the project to GitHub. The skill is stored in a workshop queue. Future runs can `apply` the skill, making it a first-class reusable procedure.

**This is the "learning" moment.** The agent is not just completing a task; it is **distilling the procedure** so the next task can be cheaper.

**This event is what makes the dataset rare.** Most LLM training corpora end at "task complete." This one continues: the completion of the task spawns a new tool that future completions can use.

---

## The JSONL schema

Each line of [`datasets/estudio-anonimo-traces.jsonl`](./datasets/estudio-anonimo-traces.jsonl) is one event. The line is a JSON object with the shape:

```json
{
  "event_id": "1_user_brief",
  "event_type": "user_brief",
  "actor": "user",
  "model": "minimax/MiniMax-M2.7",
  "timestamp": "2026-06-09T17:32:00+08:00",
  "messages": [
    {
      "role": "user",
      "content": "Build a high-end furniture..."
    }
  ],
  "metadata": {
    "task_id": "task-20260609-interior-design-hero",
    "agent": "main",
    "skills_loaded": [],
    "files_written": []
  }
}
```

**The full event schema is documented at the top of the JSONL file itself** (it is a single-line `comment` field that most JSONL parsers ignore, and that gives humans a one-stop reference).

### How to load it

```python
import json

events = []
with open("datasets/estudio-anonimo-traces.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        events.append(json.loads(line))

print(f"Loaded {len(events)} events")
for e in events:
    print(f"  [{e['event_id']}] {e['event_type']} by {e['actor']}")
```

### How to convert to OpenAI fine-tuning format

```python
import json

training_examples = []
context = []  # rolling context across events in the same task

with open("datasets/estudio-anonimo-traces.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        event = json.loads(line)
        for msg in event["messages"]:
            context.append({"role": msg["role"], "content": msg["content"]})
        # Each event becomes one training example
        training_examples.append({"messages": list(context)})
        # Note: this is a simplified approach. Real training should
        # consider event boundaries and context windows.

with open("datasets/estudio-anonimo-finetune.jsonl", "w") as f:
    for ex in training_examples:
        f.write(json.dumps(ex) + "\n")
```

---

## What this dataset can teach a model

If you fine-tune on this dataset, here are the specific behaviors that should improve:

| Behavior | Without this dataset | After fine-tuning |
|----------|---------------------|-------------------|
| Shipping one design when three were asked | Common | The model asks for / produces alternatives |
| Skipping pre-flight checks | Common | The model runs a checklist before declaring DONE |
| Introducing unrequested features (dark mode, trust strip) | Common | The model respects the brief's scope |
| Confusing "premium" with "purple gradient + Inter" | Very common | The model produces restrained, editorial-magazine output |
| Finishing a task without distilling the lesson | Universal | The model writes a one-paragraph lesson after each task |
| Forgetting that em-dashes are an AI tell | Common | The model uses commas, periods, or middle-dots |

---

## Limitations

- **N=1.** This is one task, one design domain, one team. A real training corpus needs hundreds of tasks.
- **Single language (English).** The brief was English; the prompts file has Chinese, but the trace is English-only. (If you want a Chinese version, the same workflow applies — just re-run with a Chinese brief.)
- **No negative examples.** Every event is a successful path. A "what NOT to do" companion dataset (a diff of failed vs. successful runs) would be much more valuable.
- **Self-reported.** The subagent reported its own status. In a real evaluation pipeline, an external grader should be added.

---

## How to extend this dataset

The cleanest way to grow it is to **re-run the same workflow on a different brief** and append. The 7-event structure is task-agnostic — it works for "build a SaaS landing page", "write a marketing email", "design a logo system", "draft a legal contract", etc. as long as the task has a verifiable deliverable.

If you do extend it, **please open a PR**. The `docs/ai-trace.md` is a single source of truth — update it alongside the JSONL.
