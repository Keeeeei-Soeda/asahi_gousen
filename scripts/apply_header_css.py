#!/usr/bin/env python3
"""全 HTML にヘッダー用 CSS のリンクを挿入する。"""
import os
import re

ASAHI = os.path.join(os.path.dirname(__file__), "..", "asahigousen")


def rel_path_to_assets(filepath: str) -> str:
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
            if "site-header.css" in content:
                continue
            css_href = rel_path_to_assets(path)
            link = f'<link rel="stylesheet" href="{css_href}" id="site-header-custom-css"/>'
            content = content.replace("</head>", f"{link}\n</head>")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Applied: {path}")


if __name__ == "__main__":
    main()
