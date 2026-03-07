#!/usr/bin/env python3
"""
動画セクション（elementor-widget-video を含む section）を HTML コメントアウトする。
動画ファイル入手後に restore_video.py で復元可能。
"""
import os
import re

ASAHI = os.path.join(os.path.dirname(__file__), "..", "asahigousen")

# video widget を含む section ブロック全体を対象にする
PATTERN = re.compile(
    r'(<section[^>]*>(?:(?!<section).)*?elementor-widget-video(?:(?!<section).)*?</section>)',
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

            if "elementor-widget-video" not in content:
                continue
            if "<!-- [VIDEO_SECTION_START]" in content:
                print(f"Already commented: {path}")
                continue

            def replacer(m):
                inner = m.group(1)
                return f"<!-- [VIDEO_SECTION_START] 動画ファイル入手後にコメントを外してください\n{inner}\n[VIDEO_SECTION_END] -->"

            new_content = PATTERN.sub(replacer, content)
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Commented out: {path}")


if __name__ == "__main__":
    main()
