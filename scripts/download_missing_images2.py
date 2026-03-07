#!/usr/bin/env python3
"""
1回目で取得できなかった画像を、複数のタイムスタンプと間隔をあけて再試行する。
"""
import os
import re
import time
import urllib.request

SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "asahigousen")
IMAGE_DIR = os.path.join(SITE_DIR, "assets", "images", "2021", "05")

# 試行するタイムスタンプ（新しい順）
TIMESTAMPS = [
    "20250101000000",
    "20241201000000",
    "20241001000000",
    "20240601000000",
    "20231201000000",
    "20230601000000",
    "20220601000000",
    "20211201000000",
]

BASE_URL = "https://asahigousen.co.jp/cms/wp-content/uploads/2021/05/"

os.makedirs(IMAGE_DIR, exist_ok=True)

# 全HTMLから参照画像を収集
image_names = set()
for root, dirs, files in os.walk(SITE_DIR):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        with open(os.path.join(root, fname), encoding="utf-8", errors="ignore") as f:
            content = f.read()
        found = re.findall(r'assets/images/2021/05/([^"\')\s<>]+)', content)
        image_names.update(found)

# 動画ファイルは除外
skip_exts = {".mov", ".mp4"}
image_names = {n for n in image_names if not any(n.endswith(e) for e in skip_exts)}

missing = [n for n in sorted(image_names) if not os.path.exists(os.path.join(IMAGE_DIR, n))]
print(f"取得待ち: {len(missing)} 件\n")

for name in missing:
    dest = os.path.join(IMAGE_DIR, name)
    success = False
    for ts in TIMESTAMPS:
        url = f"https://web.archive.org/web/{ts}if_/{BASE_URL}{name}"
        print(f"  [{ts}] {name} ...", end=" ", flush=True)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            if len(data) < 100:
                print("小さすぎるためスキップ")
                time.sleep(1)
                continue
            with open(dest, "wb") as out:
                out.write(data)
            print(f"OK ({len(data):,} bytes)")
            success = True
            time.sleep(1)
            break
        except Exception as e:
            print(f"NG ({e})")
            time.sleep(2)
    if not success:
        print(f"  → {name} は取得できませんでした")

print("\n完了。配置済み画像一覧:")
for f in sorted(os.listdir(IMAGE_DIR)):
    size = os.path.getsize(os.path.join(IMAGE_DIR, f))
    print(f"  {f} ({size:,} bytes)")
