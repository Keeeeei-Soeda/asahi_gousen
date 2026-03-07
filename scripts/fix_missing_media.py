#!/usr/bin/env python3
"""
不足メディアファイルへの対処:
1. 動画タグ(<video>…</video>)をコメントアウト（machine / message / index）
2. GIF プレースホルダーを既存の工場写真から生成（Pillow）
"""
import os
import re
import shutil
from pathlib import Path

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

SITE_DIR = Path(__file__).parent.parent / "asahigousen"

# ---- 1. 動画タグのコメントアウト ----------------------------------------
video_targets = [
    SITE_DIR / "index.html",
    SITE_DIR / "machine" / "index.html",
    SITE_DIR / "message" / "index.html",
]

VIDEO_PATTERN = re.compile(
    r'(<div class="elementor-widget-container">)'
    r'(<div class="e-hosted-video elementor-wrapper[^"]*">)'
    r'(<video[^>]*>.*?</video>)'
    r'(</div></div>)',
    re.DOTALL
)

for html_path in video_targets:
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    original = content

    def replace_video(m):
        return (
            m.group(1)
            + "<!-- 動画は準備中のためコメントアウト -->"
            + m.group(4)
        )

    content = VIDEO_PATTERN.sub(replace_video, content)
    if content != original:
        html_path.write_text(content, encoding="utf-8")
        count = len(VIDEO_PATTERN.findall(original))
        print(f"  [動画コメントアウト] {html_path.relative_to(SITE_DIR)} ({count}箇所)")
    else:
        print(f"  [変更なし] {html_path.relative_to(SITE_DIR)}")

# ---- 2. GIF プレースホルダー ------------------------------------------------
gif_dest = SITE_DIR / "assets" / "images" / "2024" / "11" / "asahigousen.gif"
gif_dest.parent.mkdir(parents=True, exist_ok=True)

if not gif_dest.exists():
    # 手持ちの写真からシンプルな GIF を生成（アニメーションなし、静止画）
    src_jpg = SITE_DIR / "assets" / "images" / "2021" / "05" / "company.jpg"
    if HAS_PILLOW and src_jpg.exists():
        img = Image.open(src_jpg).convert("RGB")
        img = img.resize((800, 558), Image.LANCZOS)  # 元の比率に近いサイズ
        img.save(str(gif_dest), format="GIF")
        print(f"  [GIF生成] {gif_dest.relative_to(SITE_DIR)}")
    elif src_jpg.exists():
        shutil.copy2(src_jpg, gif_dest)
        print(f"  [GIFコピー(Pillow無)] {gif_dest.relative_to(SITE_DIR)}")
    else:
        print(f"  [スキップ] GIF 生成元画像がありません")
else:
    print(f"  [既存] {gif_dest.relative_to(SITE_DIR)}")

print("\n完了")
