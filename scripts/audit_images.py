#!/usr/bin/env python3
"""
全HTMLファイルから画像参照を収集し、実際のファイルとの差分を報告する。
ページごとの相対パスを正規化して絶対パスとして照合する。
"""
import os
import re
from pathlib import Path

SITE_DIR = Path(__file__).parent.parent / "asahigousen"
IMAGE_BASE = SITE_DIR / "assets" / "images"

# HTMLファイルをすべて収集
html_files = sorted(SITE_DIR.rglob("*.html"))

# 結果格納
all_refs = {}   # {絶対パス: [参照元HTMLパス, ...]}
missing = {}    # {絶対パス: [参照元HTMLパス, ...]}
ok = {}         # {絶対パス: [参照元HTMLパス, ...]}

pattern = re.compile(r'(?:src|data-src|href|data-srcset|srcset|content)=["\']([^"\']*assets/images/[^"\'<>\s]+)["\']')

for html_path in html_files:
    rel_html = html_path.relative_to(SITE_DIR)
    html_dir = html_path.parent
    content = html_path.read_text(encoding="utf-8", errors="ignore")

    matches = pattern.findall(content)
    # srcset の中に複数パスが含まれる場合を展開
    all_paths = []
    for m in matches:
        # srcset は "path 300w, path2 768w" 形式
        for part in m.split(","):
            p = part.strip().split()[0]
            if "assets/images/" in p:
                all_paths.append(p)

    for img_path_str in set(all_paths):
        # 相対パス → 絶対パス に解決
        if img_path_str.startswith("../"):
            resolved = (html_dir / img_path_str).resolve()
        elif img_path_str.startswith("/"):
            # /assets/images/... のような絶対パス
            resolved = (SITE_DIR / img_path_str.lstrip("/")).resolve()
        else:
            resolved = (html_dir / img_path_str).resolve()

        key = str(resolved)
        all_refs.setdefault(key, []).append(str(rel_html))
        if resolved.exists():
            ok.setdefault(key, []).append(str(rel_html))
        else:
            missing.setdefault(key, []).append(str(rel_html))

print("=" * 70)
print(f"参照画像パス 総数 : {len(all_refs)}")
print(f"存在する        : {len(ok)}")
print(f"存在しない (不足): {len(missing)}")
print("=" * 70)

if missing:
    print("\n【不足している画像】")
    for abs_path, refs in sorted(missing.items()):
        rel = Path(abs_path).relative_to(SITE_DIR.parent) if SITE_DIR.parent in Path(abs_path).parents else abs_path
        print(f"  {rel}")
        for r in sorted(set(refs)):
            print(f"    参照元: {r}")
else:
    print("\n不足している画像はありません ✅")

print("\n【存在確認済み画像パス一覧】")
for abs_path in sorted(ok.keys()):
    rel = Path(abs_path).relative_to(SITE_DIR.parent) if SITE_DIR.parent in Path(abs_path).parents else abs_path
    print(f"  ✓ {rel}")
