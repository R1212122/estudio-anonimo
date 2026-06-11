"""Sanity-check the JSONL traces file."""
import json
from pathlib import Path

HERE = Path(__file__).parent
JSONL = HERE / "estudio-anonimo-traces.jsonl"

with open(JSONL, encoding="utf-8") as f:
    events = [json.loads(line) for line in f if line.strip() and not line.startswith("#")]

print(f"Total events: {len(events)}")
print()
print("Per-event summary:")
for e in events:
    eid = e["event_id"]
    etype = e["event_type"]
    actor = e["actor"]
    model = e["model"]
    msgs = len(e["messages"])
    files = e["metadata"].get("files_written", [])
    eid_str = "[" + eid + "]"
    print(f"  {eid_str:30s} {etype:30s} actor={actor:18s} model={model:25s} msgs={msgs} files={len(files)}")

print()
print("Schema check:")
required = ["event_id", "event_type", "actor", "model", "timestamp", "messages", "metadata"]
all_ok = True
for e in events:
    missing = [k for k in required if k not in e]
    if missing:
        all_ok = False
        print(f"  MISSING in {e['event_id']}: {missing}")
if all_ok:
    print("  all events have all required keys")

print()
print("JSON validity:")
print(f"  parseable: {len(events)}/{len(events)}")

# Count characters and tokens roughly
total_chars = sum(len(json.dumps(e, ensure_ascii=False)) for e in events)
print(f"  total chars (events only, no header): {total_chars}")
print(f"  approx tokens (@4 chars/token): {total_chars // 4}")
