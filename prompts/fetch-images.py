#!/usr/bin/env python3
"""Download high-end furniture images from Unsplash for the Estudio Anonimo page."""

import urllib.request
import os
import json

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT_DIR, exist_ok=True)

# Direct Unsplash photo IDs that match our high-end furniture theme
# These are carefully selected premium furniture/interior photos
PHOTOS = [
    # 1. Hero: quiet interior with daylight on stone (architectural)
    ("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1600&q=85&fit=crop", "hero-interior.jpg"),
    # 2. Forn Table: oak table (dining/wood table)
    ("https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=1600&q=85&fit=crop", "forn-table.jpg"),
    # 3. Sina Chair: elegant chair (armchair/wood chair)
    ("https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=1600&q=85&fit=crop", "sina-chair.jpg"),
    # 4. Aroz Pendant: brass pendant light
    ("https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?w=1600&q=85&fit=crop", "aroz-pendant.jpg"),
    # 5. Maia Shelf: minimal shelf display
    ("https://images.unsplash.com/photo-1582254465498-6bc70419b60a?w=1600&q=85&fit=crop", "maia-shelf.jpg"),
    # 6. Bres Cabinet: walnut cabinet
    ("https://images.unsplash.com/photo-1597006335779-5a9ee0ff358a?w=1600&q=85&fit=crop", "bres-cabinet.jpg"),
    # 7. Detail: wood grain texture
    ("https://images.unsplash.com/photo-1544531585-9844b9c3cb94?w=800&q=85&fit=crop", "wood-detail.jpg"),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

success = 0
for i, (url, filename) in enumerate(PHOTOS, 1):
    path = os.path.join(OUT_DIR, filename)
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        print(f"[{i}/7] SKIP (exists): {filename} ({os.path.getsize(path)} bytes)")
        success += 1
        continue
    
    print(f"[{i}/7] Downloading: {filename}...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(path, 'wb') as f:
                f.write(data)
            print(f"OK ({len(data)} bytes)")
            success += 1
    except Exception as e:
        print(f"FAIL: {e}")
        # Try backup
        try:
            print(f"      Retrying with different quality...")
            backup_url = url.replace("&q=85", "&q=70").replace("w=1600", "w=1200")
            req = urllib.request.Request(backup_url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                with open(path, 'wb') as f:
                    f.write(data)
                print(f"      OK on retry ({len(data)} bytes)")
                success += 1
        except Exception as e2:
            print(f"      FAIL: {e2}")

print(f"\n=== Download complete: {success}/{len(PHOTOS)} ===")
print(f"Directory: {os.path.abspath(OUT_DIR)}")
