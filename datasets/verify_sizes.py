"""HEAD requests to confirm file sizes on mirror."""
import urllib.request

for f in ["estudio-anonimo-traces.jsonl", "README.md"]:
    url = f"https://hf-mirror.com/datasets/Fnn123/estudio-anonimo-traces/resolve/main/{f}"
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "verify"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            size = r.headers["Content-Length"]
            print(f"  {f:40s} {size} B  (status {r.status})")
    except Exception as e:
        print(f"  {f:40s} FAIL: {str(e)[:80]}")
