---
license: mit
task_categories:
  - text-generation
tags:
  - multi-agent
  - agent-traces
  - tool-use
  - self-improvement
  - design
  - editorial
  - taste-skill
size_categories:
  - n<1K
---

# Estudio Anonimo · Agent Trace Dataset

A 7-event, multi-agent, multi-turn, multi-tool trace documenting the
end-to-end construction of an editorial-magazine landing page for a
fictional high-end furniture studio ("Estudio Anonimo · Autumn Edition
2026"). The full design is open-sourced at
[R1212122/estudio-anonimo](https://github.com/R1212122/estudio-anonimo).

## What's in this dataset

**One file, 7 events, ~3K tokens.** Each line is a JSON object representing
one event in a complete multi-agent design task:

| # | Event | Actor | What happens |
|---|-------|-------|--------------|
| 1 | `user_brief` | user | The human gives a one-paragraph goal (no system prompt, no example) |
| 2 | `luma_design_read` | scheduler | Lio paraphrases the brief + sets 3 dials + spawns subagent |
| 3 | `subagent_3_variants` | designer | Pixel produces 3 design alternatives + recommendation matrix |
| 4 | `subagent_chosen_impl` | designer | Pixel builds Variant B (split-frame hero, 18 KB static HTML) |
| 5 | `preflight_check` | designer | Pixel runs a 50-item grep-based audit; all pass |
| 6 | `luma_two_stage_review` | scheduler | Lio runs spec-compliance (M3) + code-quality (GLM-flash) review |
| 7 | `skill_distillation` | scheduler | Lio writes a new skill proposal (`github-auto-push`) for future reuse |

The seven events are sequential: event N depends on the result of event N-1.

## Why this dataset is rare

Most public "AI agent" datasets are missing at least one of: **multi-turn
planning, tool use, multi-agent collaboration, reflection, or
self-improvement.** This dataset has all five, in one trace, with verifiable
git history.

| Dataset family | Multi-turn | Tools | Multi-agent | Reflection | Self-improvement |
|----------------|:---:|:---:|:---:|:---:|:---:|
| Alpaca / Dolly | ❌ | ❌ | ❌ | ❌ | ❌ |
| HumanEval / MBPP | ❌ | ❌ | ❌ | ❌ | ❌ |
| ToolBench / Gorilla | ❌ | ✅ | ❌ | ❌ | ❌ |
| WebArena / Mind2Web | ❌ | ✅ | ❌ | ❌ | ❌ |
| SWE-Agent / OpenHands | ✅ | ✅ | ❌ | partial | ❌ |
| **This dataset** | **✅** | **✅** | **✅** | **✅** | **✅** |

## Schema

Each event is an object with the following shape:

```json
{
  "event_id": "1_user_brief",
  "event_type": "user_brief | luma_design_read | subagent_3_variants | subagent_implementation | preflight_check | luma_review | skill_distillation",
  "actor": "user | luma_scheduler | pixel_subagent",
  "model": "<model id, e.g. minimax/MiniMax-M2.7>",
  "timestamp": "<ISO 8601 with timezone>",
  "messages": [
    { "role": "user | assistant | tool", "content": "...", "name": "...", "arguments": {...} }
  ],
  "metadata": {
    "task_id": "...",
    "agent": "...",
    "skills_loaded": [...],
    "files_written": [...]
  }
}
```

The full schema is documented at the top of `estudio-anonimo-traces.jsonl`
itself (in `#` comment lines that JSONL parsers ignore).

## How to load

```python
import json

events = []
with open("estudio-anonimo-traces.jsonl") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            events.append(json.loads(line))

print(f"Loaded {len(events)} events")
# 7
```

## How to convert to OpenAI fine-tuning format

```python
import json

training_examples = []
context = []
with open("estudio-anonimo-traces.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        event = json.loads(line)
        for msg in event["messages"]:
            context.append({"role": msg["role"], "content": msg["content"]})
        training_examples.append({"messages": list(context)})

with open("estudio-anonimo-finetune.jsonl", "w") as f:
    for ex in training_examples:
        f.write(json.dumps(ex) + "\n")
```

## How to extend it

Re-run the same 7-event structure on a different brief and append. The
structure is task-agnostic. It works for "build a SaaS landing page",
"write a marketing email", "design a logo system", "draft a legal
contract" — as long as the task has a verifiable deliverable.

If you fork this and add new traces, **please open a PR** to the source
repo. A corpus of 100 such traces would be a meaningful research
contribution; a corpus of 1,000 would be a *finetune* contribution.

## Provenance

- **Project repo:** [R1212122/estudio-anonimo](https://github.com/R1212122/estudio-anonimo)
- **Git commit:** `68ced83`
- **Task id:** `task-20260609-interior-design-hero`
- **Full task artifacts:** `tasks/task-20260609-interior-design-hero/outbox/`
- **Skills used:** `taste-skill` §0-5 + §14, `using-openclaw` Iron Law
- **Author:** Lio (AI research team lead), 2026-06-11
- **License:** MIT

## Limitations (for honesty)

- **N=1.** One task, one design domain. A real training corpus needs
  hundreds of tasks. The 7-event *structure* is task-agnostic; the
  *content* is one example.
- **Single language (English).** A Chinese-language version requires
  re-running the workflow with a Chinese brief.
- **No negative examples.** Every event is a successful path. A
  *failure-mode* companion dataset would be more valuable.
- **Self-reported.** The subagent reports its own status; a real eval
  pipeline would add an external grader.
- **Synthetic agent boundary.** "Lio scheduler" and "Pixel subagent"
  are roles, not separate model instances. Production systems back
  each role with a different model checkpoint.
