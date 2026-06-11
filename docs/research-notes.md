# Research Notes · Why this dataset matters for fine-tuning

> A short, opinionated note for AI researchers and LLM trainers.
> The companion dataset is at [`datasets/estudio-anonimo-traces.jsonl`](./datasets/estudio-anonimo-traces.jsonl).
> The full event-by-event description is in [`docs/ai-trace.md`](./docs/ai-trace.md).

## TL;DR

The 7-event trace in this repo is the **smallest possible** example of a
multi-agent, multi-turn, multi-tool, self-improving AI workflow. If you
fine-tune a model on a corpus of N=100 such traces, you should see measurable
improvement on three behaviors that current open-weight models struggle with:

1. **Not introducing unrequested features** (the "scope creep" failure)
2. **Running self-checks before declaring DONE** (the "missing pre-flight" failure)
3. **Distilling procedures into reusable skills** (the "no learning across runs" failure)

## The four behaviors the dataset teaches

| # | Behavior | Why current models fail it | What this dataset shows |
|---|----------|---------------------------|-------------------------|
| 1 | **Brief compliance** | Models add features the user did not ask for (dark mode, "Trusted by" strip, scroll-cue text). The model's priors on "what a good landing page looks like" overpower the brief. | Event 1 has a *negative* brief (em-dash forbidden, no AI purple, no centered hero). Events 4–5 produce output that *does not contain* any of these. |
| 2 | **Self-audit before completion** | Models declare DONE without running validation. A test suite, a grep, a screenshot review — none of it is in the default workflow. | Event 5 runs a 50-item grep-based pre-flight. The grep results are *embedded in the event message*, so the model learns to emit them, not just perform them silently. |
| 3 | **Multi-agent hand-off** | Single-agent loops. A failure means re-prompt; a re-prompt means inconsistency. | Events 2 and 6 are Lio (the scheduler). Events 3, 4, 5 are Pixel (the subagent). The hand-off is explicit and structured: scheduler writes a *Design Read* + 3 dials; subagent answers with 3 variants; scheduler reviews with a 2-stage gate. |
| 4 | **Self-improvement loop** | A delivered task is *terminal*. The next similar task starts from scratch. | Event 7 writes a new skill proposal (`github-auto-push`) capturing the procedure used to ship the project. The next similar task can `apply` the skill. This is the rare event in the corpus. |

## What makes this dataset different from existing ones

| Dataset | Multi-turn | Tools | Multi-agent | Reflection | Self-improvement | Open |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| Alpaca / Dolly | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| HumanEval / MBPP | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| ToolBench / Gorilla | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| WebArena / Mind2Web | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| OpenHands / SWE-Agent | ✅ | ✅ | ❌ | partial | ❌ | ✅ |
| **This repo** | **✅** | **✅** | **✅** | **✅** | **✅** | **✅** |

The bottom row is the only one with **all five** properties.

## What it does NOT teach (limitations, repeated for honesty)

- **N=1.** One task, one domain (editorial design), one team. A corpus of N=100+ tasks across domains is needed for serious fine-tuning. The 7-event *structure* is task-agnostic and can be re-applied; the *content* is one example.
- **Single language (English).** A Chinese-language version would require re-running the same workflow with a Chinese brief.
- **No negative examples.** Every event is a successful path. A *failure-mode* companion dataset (e.g., "what the subagent output looked like *before* the 50-item pre-flight caught 62 em-dashes") would be much more valuable for training.
- **Self-reported.** The subagent reports its own status. A real evaluation pipeline adds an external grader.
- **Synthetic agent boundary.** The "Lio scheduler" and "Pixel subagent" are roles in the trace, not separate model instances. The dataset would be more useful if each role were backed by a different model checkpoint (which is what production systems do). Recording *which model* emitted each event is a first step; the current trace records the model ID but does not vary it.

## A worked example: how to extend it

Suppose you want to teach a model the four behaviors above. The cleanest way to grow this dataset is to **re-run the same 7-event structure on a different brief** and append the new run as 7 more lines.

The structure is task-agnostic. It works for:

- "Build a SaaS landing page" → 7 events, same shape
- "Write a marketing email" → 7 events, replace "index.html" with "email.html"
- "Design a logo system" → 7 events, replace "taste-skill" with "logo-skill"
- "Draft a legal contract" → 7 events, replace subagent roles

The key invariant is: **the task must have a verifiable deliverable**. Without a deliverable, the pre-flight check (event 5) has nothing to check, and the whole structure collapses.

## How to fine-tune on this

A minimal fine-tuning recipe (using the OpenAI Python SDK as an example):

```python
import json
import openai

# 1. Load the trace
events = []
with open("estudio-anonimo-traces.jsonl") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            events.append(json.loads(line))

# 2. Build training examples: each event becomes one chat example,
#    with the rolling context of all previous events as messages.
training_examples = []
context = []
for event in events:
    for msg in event["messages"]:
        context.append({"role": msg["role"], "content": msg["content"]})
    training_examples.append({"messages": list(context)})

# 3. Save in OpenAI fine-tuning format
with open("estudio-anonimo-finetune.jsonl", "w") as f:
    for ex in training_examples:
        f.write(json.dumps(ex) + "\n")

# 4. Upload + fine-tune (illustrative)
# openai.files.create(file=open("estudio-anonimo-finetune.jsonl", "rb"), purpose="fine-tune")
# openai.fine_tuning.jobs.create(training_file=file.id, model="gpt-4o-mini-2024-07-18")
```

**A note on context window:** with the rolling-context approach, the 7th event's example contains all 6 previous events' messages. This is realistic — the agent *does* see its history — but it does mean later examples are longer. If you trim for cost, keep the system message + the most recent 2 events.

## A worked evaluation: a probe prompt

To test whether a fine-tuned model has learned the four behaviors, use this probe:

> *"Build a landing page for a tea brand. Mid-century Scandinavian feel, warm."*

Compare the model output against:

| Behavior | Probe failure mode |
|----------|---------------------|
| Brief compliance | Model adds: dark mode toggle, "Trusted by" logo wall, "Free shipping" promo strip. |
| Self-audit | Model declares DONE without mentioning a pre-flight check, validation, or test. |
| Multi-agent | Single-pass generation; no scheduler/subagent split; no review. |
| Self-improvement | Output ends at "here's the page." No mention of a lesson, a reusable procedure, or a future-runnable skill. |

A model fine-tuned on this corpus should: (a) produce a tea landing page with *no unrequested features*; (b) describe a 5+ item self-audit at the end; (c) emit at least one "spawn / delegate / review" hand-off; (d) close with "lesson: ..." and "skill proposal: ..." blocks.

## Final note

The dataset is **open and extensible**. If you fork it, re-run the workflow, and add new traces, please open a PR. The single most valuable contribution you can make is **N+1** — one more task in the same shape. A corpus of 100 such traces would be a meaningful research contribution; a corpus of 1,000 would be a *finetune* contribution.

**The dataset is live on HuggingFace:** [huggingface.co/datasets/Fnn123/estudio-anonimo-traces](https://huggingface.co/datasets/Fnn123/estudio-anonimo-traces) (or its mirror: [hf-mirror.com/datasets/Fnn123/estudio-anonimo-traces](https://hf-mirror.com/datasets/Fnn123/estudio-anonimo-traces)). Anyone can fetch it with `huggingface_hub` or via the web — no account required.

If you publish a paper using this dataset, please cite the repo and link to it from your paper.
