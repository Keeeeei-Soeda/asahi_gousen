#!/usr/bin/env python3
"""
Wayback Machine のツールバー・埋め込みスクリプトを除去し、
URLプレフィックスを相対化する。
"""
import os
import re

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "asahigousen")


def clean_html(content: str) -> str:
    # 1. head 内の Wayback 用 script/link（先頭〜End Wayback Rewrite JS Include）を除去
    content = re.sub(
        r'<script type="text/javascript" src="https://web-static\.archive\.org[^>]*>.*?'
        r'<!-- End Wayback Rewrite JS Include -->\s*',
        '',
        content,
        count=1,
        flags=re.DOTALL,
    )

    # 2. 末尾の FILE ARCHIVED / playback timings コメントを除去
    content = re.sub(
        r'<!--\s*FILE ARCHIVED ON.*$',
        '',
        content,
        flags=re.DOTALL,
    )

    # 3. web.archive.org の URL プレフィックスを除去（cs_, js_, im_ 等の接尾辞付きも）
    content = re.sub(
        r'https://web\.archive\.org/web/\d+[a-z_]*/',
        '',
        content,
    )

    # 4. web-static.archive.org 参照が残っていれば除去（念のため）
    content = re.sub(
        r'https://web-static\.archive\.org/[^"\']+',
        '',
        content,
    )

    return content.strip()


def main():
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except Exception as e:
                print(f"Read error {path}: {e}")
                continue
            cleaned = clean_html(content)
            with open(path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"Cleaned: {path}")


if __name__ == "__main__":
    main()
