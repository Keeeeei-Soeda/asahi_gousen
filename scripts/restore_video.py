#!/usr/bin/env python3
"""
commentout_video.py でコメントアウトした動画セクションを復元する。
動画ファイル（asahigousenPV.mp4）を assets/images/2021/06/ に配置してから実行すること。
"""
import os
import re

ASAHI = os.path.join(os.path.dirname(__file__), "..", "asahigousen")

PATTERN = re.compile(
    r'<!-- \[VIDEO_SECTION_START\] 動画ファイル入手後にコメントを外してください\n(.*?)\n\[VIDEO_SECTION_END\] -->',
    re.DOTALL,
)


def main():
    for root, dirs, files in os.walk(ASAHI):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            if "[VIDEO_SECTION_START]" not in content:
                continue

            new_content = PATTERN.sub(r'\1', content)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Restored: {path}")


if __name__ == "__main__":
    main()
