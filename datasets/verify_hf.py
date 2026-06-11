"""Verify the dataset is live on HF mirror."""
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from huggingface_hub import HfApi

api = HfApi(token=open(os.path.expanduser("~/.huggingface/token.txt")).read().strip())

info = api.dataset_info("Fnn123/estudio-anonimo-traces")
print("=== Dataset info ===")
print("  id:      ", info.id)
print("  private: ", info.private)
print("  files:")
for s in info.siblings:
    size = "?" if not hasattr(s, "size") or s.size is None else str(s.size)
    print(f"    - {s.rfilename:40s} {size} B")

print()
print("=== Card metadata (YAML frontmatter) ===")
if info.card_data:
    print(info.card_data)
else:
    print("  (none)")

print()
print("=== URLs ===")
print("  mirror:    https://hf-mirror.com/datasets/Fnn123/estudio-anonimo-traces")
print("  canonical: https://huggingface.co/datasets/Fnn123/estudio-anonimo-traces")
print("  raw file:  https://hf-mirror.com/datasets/Fnn123/estudio-anonimo-traces/resolve/main/estudio-anonimo-traces.jsonl")
