#!/usr/bin/env python3
"""
全HTMLファイルから画像パスを収集し、assets/images/2021/05/ に存在しない画像を
Wayback Machine からダウンロードする。
"""
import os
import re
import time
import urllib.request

SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "asahigousen")
IMAGE_DIR = os.path.join(SITE_DIR, "assets", "images", "2021", "05")
WAYBACK_BASE = "https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/cms/wp-content/uploads/2021/05/"
DOWNLOAD_BASE = "https://web.archive.org/web/20250122000000if_/https://asahigousen.co.jp/cms/wp-content/uploads/2021/05/"

os.makedirs(IMAGE_DIR, exist_ok=True)

# 全HTMLから 2021/05/ の画像ファイル名を収集
image_names = set()
for root, dirs, files in os.walk(SITE_DIR):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        with open(os.path.join(root, fname), encoding="utf-8", errors="ignore") as f:
            content = f.read()
        found = re.findall(r'assets/images/2021/05/([^"\')\s<>]+)', content)
        image_names.update(found)

print(f"全HTMLで参照されている 2021/05/ の画像数: {len(image_names)}")

missing = [n for n in sorted(image_names) if not os.path.exists(os.path.join(IMAGE_DIR, n))]
print(f"未ダウンロード: {len(missing)} 件\n")

for name in missing:
    url = f"{DOWNLOAD_BASE}{name}"
    dest = os.path.join(IMAGE_DIR, name)
    print(f"取得中: {name} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        with open(dest, "wb") as out:
            out.write(data)
        print(f"OK ({len(data):,} bytes)")
    except Exception as e:
        print(f"NG ({e})")
    time.sleep(0.5)

print("\n完了。配置済み画像一覧:")
for f in sorted(os.listdir(IMAGE_DIR)):
    print(f"  {f}")
