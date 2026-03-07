#!/usr/bin/env python3
"""
既存画像からサムネイルを生成し、不足しているカルーセル画像に代替画像をコピーする。
Pillow が必要: pip install Pillow
"""
import os
import re
import shutil

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False
    print("Pillow 未インストール。サムネイル生成はスキップします（pip install Pillow）")

SITE_DIR = os.path.join(os.path.dirname(__file__), "..", "asahigousen")
IMAGE_DIR = os.path.join(SITE_DIR, "assets", "images", "2021", "05")

os.makedirs(IMAGE_DIR, exist_ok=True)

# 全HTMLから必要な画像ファイル名を収集
image_names = set()
for root, dirs, files in os.walk(SITE_DIR):
    for fname in files:
        if not fname.endswith(".html"):
            continue
        with open(os.path.join(root, fname), encoding="utf-8", errors="ignore") as f:
            content = f.read()
        found = re.findall(r'assets/images/2021/05/([^"\')\s<>]+)', content)
        image_names.update(found)

# 動画を除外
image_names = {n for n in image_names if not n.endswith((".mov", ".mp4"))}

existing = {f for f in os.listdir(IMAGE_DIR)}
missing = sorted(image_names - existing)
print(f"必要な画像: {len(image_names)} 件 / 既存: {len(existing)} 件 / 不足: {len(missing)} 件\n")

# --- サムネイル生成（元ファイルから） ---
if HAS_PILLOW:
    thumbnail_specs = {
        "K2A6376-300x136.jpg": ("K2A6376.jpg", (300, 136)),
        "K2A6376-768x349.jpg": ("K2A6376.jpg", (768, 349)),
        "K2A6376-1024x465.jpg": ("K2A6376.jpg", (1024, 465)),
        "K2A6376-1536x698.jpg": ("K2A6376.jpg", (1536, 698)),
        "K2A6528-300x200.jpg": ("K2A6528.jpg", (300, 200)),
        "K2A6528-768x512.jpg": ("K2A6528.jpg", (768, 512)),
        "company-300x169.jpg": ("company.jpg", (300, 169)),
        "company-768x432.jpg": ("company.jpg", (768, 432)),
        "hirohitotanaka-300x200.jpg": ("hirohitotanaka.jpg", (300, 200)),
        "flow3.fw_-267x300.png": ("flow3.fw_.png", (267, 300)),
        "fv.fw_-150x150.png": ("company.jpg", (150, 150)),
        "fv.fw_-300x300.png": ("company.jpg", (300, 300)),
    }
    for dest_name, (src_name, size) in thumbnail_specs.items():
        src = os.path.join(IMAGE_DIR, src_name)
        dest = os.path.join(IMAGE_DIR, dest_name)
        if os.path.exists(dest):
            continue
        if not os.path.exists(src):
            print(f"  [スキップ] {dest_name} ← 元画像 {src_name} がない")
            continue
        try:
            img = Image.open(src)
            img = img.resize(size, Image.LANCZOS)
            img.save(dest)
            print(f"  [サムネイル] {dest_name} ({size[0]}x{size[1]})")
        except Exception as e:
            print(f"  [エラー] {dest_name}: {e}")

# --- ロゴ・ブランド画像の代替 ---
# 手持ちの画像ファイルが存在する場合に限りコピー
logo_fallbacks = {
    "logo_ag.fw_.png": "company.jpg",
    "logo_agre.fw_.png": "company.jpg",
    "logo_footer.fw_.png": "company.jpg",
    "logo_footer.fw_-300x33.png": "company.jpg",
    "knit.fw_.png": "K2A6528.jpg",
    "knit.fw_-240x300.png": "K2A6528.jpg",
    "d3006ae5cda4095674a1a709802fc97c.png": "company.jpg",
    "d3006ae5cda4095674a1a709802fc97c-300x65.png": "company.jpg",
    "d3006ae5cda4095674a1a709802fc97c-768x166.png": "company.jpg",
}

# カルーセル用の代替画像（展開分野ページの10枚スライド）
# 手持ちの工場・製品写真を順番に割り当て
carousel_fallbacks_src = ["K2A6376.jpg", "K2A6396.jpg", "K2A6405.jpg", "K2A6528.jpg",
                           "K2A6376-2.jpg", "K2A6528-2.jpg", "company.jpg", "hirohitotanaka.jpg"]
carousel_missing = [
    n for n in sorted(image_names)
    if re.match(r'^K2A6(392|403|406|416|419|422|437|444)\.jpg$', n)
    and not os.path.exists(os.path.join(IMAGE_DIR, n))
]

for i, dest_name in enumerate(carousel_missing):
    src_name = carousel_fallbacks_src[i % len(carousel_fallbacks_src)]
    src = os.path.join(IMAGE_DIR, src_name)
    dest = os.path.join(IMAGE_DIR, dest_name)
    if os.path.exists(dest):
        continue
    if os.path.exists(src):
        shutil.copy2(src, dest)
        print(f"  [代替] {dest_name} ← {src_name}")

for dest_name, src_name in logo_fallbacks.items():
    src = os.path.join(IMAGE_DIR, src_name)
    dest = os.path.join(IMAGE_DIR, dest_name)
    if os.path.exists(dest):
        continue
    if os.path.exists(src):
        shutil.copy2(src, dest)
        print(f"  [代替] {dest_name} ← {src_name}")

print("\n最終結果:")
still_missing = [n for n in sorted(image_names) if not os.path.exists(os.path.join(IMAGE_DIR, n))]
print(f"  配置済み: {len(os.listdir(IMAGE_DIR))} 件")
print(f"  まだ不足: {len(still_missing)} 件")
for n in still_missing:
    print(f"    - {n}")
