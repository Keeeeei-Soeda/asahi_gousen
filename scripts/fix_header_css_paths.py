#!/usr/bin/env python3
"""既に追加した site-header.css の href を正しい相対パスに修正する。"""
import os

ASAHI = os.path.join(os.path.dirname(__file__), "..", "asahigousen")


def rel_path(filepath: str) -> str:
    rel = os.path.relpath(os.path.dirname(filepath), ASAHI)
    depth = rel.count(os.sep) + (1 if rel != "." else 0)
    return "../" * depth + "assets/css/site-header.css"


def main():
    for root, dirs, files in os.walk(ASAHI):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if "site-header.css" not in content:
                continue
            correct_href = rel_path(path)
            content = content.replace(
                'href="assets/css/site-header.css"',
                f'href="{correct_href}"',
            )
            import re
            content = re.sub(
                r'href="(\.\./)*assets/css/site-header\.css"',
                f'href="{correct_href}"',
                content,
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {path} -> {correct_href}")


if __name__ == "__main__":
    main()
