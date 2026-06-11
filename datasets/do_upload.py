"""Upload the dataset to HF Hub via hf-mirror.com (bypasses the GFW)."""
import os

# CRITICAL: set HF_ENDPOINT BEFORE importing huggingface_hub.
# HfApi reads the endpoint at instantiation; setting it later is a no-op.
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from huggingface_hub import HfApi

token = open(os.path.expanduser("~/.huggingface/token.txt")).read().strip()

api = HfApi(token=token)

# 1. whoami
who = api.whoami()
user = who["name"]
print(f"User: {user}")

# 2. Create repo (idempotent)
api.create_repo("estudio-anonimo-traces", repo_type="dataset", exist_ok=True)
print("Repo ready")

repo_id = f"{user}/estudio-anonimo-traces"

# 3. Upload JSONL
here = os.path.dirname(os.path.abspath(__file__))
jsonl_path = os.path.join(here, "estudio-anonimo-traces.jsonl")
card_path = os.path.join(here, "README_HF.md")

api.upload_file(
    path_or_fileobj=jsonl_path,
    path_in_repo="estudio-anonimo-traces.jsonl",
    repo_id=repo_id,
    repo_type="dataset",
    commit_message="Upload estudio-anonimo agent traces (7 events)",
)
print("JSONL uploaded")

# 4. Upload model card
api.upload_file(
    path_or_fileobj=card_path,
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type="dataset",
    commit_message="Add model card",
)
print("Model card uploaded")

print()
print("DONE. View at:")
print(f"https://hf-mirror.com/datasets/{user}/estudio-anonimo-traces")
print(f"Or (if direct HF works): https://huggingface.co/datasets/{user}/estudio-anonimo-traces")
