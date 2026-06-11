#!/usr/bin/env python3
"""
upload_hf.py — Upload the JSONL dataset to HuggingFace Hub.

The HF Hub accepts the JSONL via the `huggingface_hub` Python SDK OR via
`git push` to https://huggingface.co/datasets/<owner>/<name>. This script
uses the SDK because it gives a clean error report if anything is wrong.

Usage:
    # Default: upload to R1212122/estudio-anonimo-traces
    python upload_hf.py

    # Or with explicit token (read from env or arg):
    HF_TOKEN=hf_xxx python upload_hf.py
    python upload_hf.py --token hf_xxx

    # Or with custom repo:
    python upload_hf.py --repo-id myname/estudio-anonimo-traces

The script is idempotent: re-running it updates the dataset in place
rather than creating a duplicate.
"""

import argparse
import os
import sys
from pathlib import Path

# 0. Resolve paths
HERE = Path(__file__).parent
JSONL = HERE / "estudio-anonimo-traces.jsonl"
README = HERE / "README_HF.md"  # the model card

# 1. Read token from env or arg
def get_token(args_token):
    if args_token:
        return args_token
    env = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if env:
        return env
    return None


# 2. Verify SDK is installed
def check_sdk():
    try:
        import huggingface_hub
        return huggingface_hub
    except ImportError:
        print("ERROR: huggingface_hub is not installed.")
        print("Install it with: pip install huggingface_hub")
        sys.exit(1)


# 3. Main
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-id",
        default="R1212122/estudio-anonimo-traces",
        help="HF repo id (default: R1212122/estudio-anonimo-traces)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="HF token (or set HF_TOKEN env var)",
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Make the dataset private (default: public)",
    )
    args = parser.parse_args()

    token = get_token(args.token)
    if not token:
        print("ERROR: no HF token provided.")
        print("Generate one at: https://huggingface.co/settings/tokens")
        print("Then run: HF_TOKEN=hf_xxx python upload_hf.py")
        print("Or:        python upload_hf.py --token hf_xxx")
        sys.exit(1)

    if not JSONL.exists():
        print(f"ERROR: {JSONL} does not exist. Run build_traces.py first.")
        sys.exit(1)

    hh = check_sdk()

    # Print what we are about to do (token masked)
    masked = token[:6] + "***" + token[-3:] if len(token) > 9 else "***"
    print(f"Token: {masked} (masked)")
    print(f"Repo:  {args.repo_id}")
    print(f"File:  {JSONL} ({JSONL.stat().st_size} bytes)")
    print(f"Private: {args.private}")
    print()

    # Create the dataset repo
    print(f"[1/3] Creating repo {args.repo_id} (if not exists)...")
    try:
        repo_url = hh.create_repo(
            repo_id=args.repo_id,
            repo_type="dataset",
            token=token,
            private=args.private,
            exist_ok=True,
        )
        print(f"  Repo URL: {repo_url}")
    except Exception as e:
        print(f"  ERROR: {e}")
        sys.exit(1)

    # Upload the JSONL
    print(f"[2/3] Uploading {JSONL.name}...")
    try:
        result = hh.upload_file(
            path_or_fileobj=str(JSONL),
            path_in_repo=JSONL.name,
            repo_id=args.repo_id,
            repo_type="dataset",
            token=token,
            commit_message="Upload estudio-anonimo agent traces (7 events)",
        )
        print(f"  Uploaded: {result}")
    except Exception as e:
        print(f"  ERROR: {e}")
        sys.exit(1)

    # Upload the model card if it exists
    if README.exists():
        print(f"[3/3] Uploading {README.name} (model card)...")
        try:
            result = hh.upload_file(
                path_or_fileobj=str(README),
                path_in_repo="README.md",
                repo_id=args.repo_id,
                repo_type="dataset",
                token=token,
                commit_message="Add model card",
            )
            print(f"  Uploaded: {result}")
        except Exception as e:
            print(f"  WARN: {e}")
    else:
        print(f"[3/3] (skipped model card: {README} not found)")

    print()
    print("=" * 60)
    print("DONE.")
    print(f"View your dataset at: https://huggingface.co/datasets/{args.repo_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
