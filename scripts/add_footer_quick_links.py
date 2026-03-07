#!/usr/bin/env python3
"""全HTMLの #footer-inner 直下に、4リンク（当社の強み・設備紹介・当社のものづくり・展開分野）を挿入する。"""
import os

ASAHI = os.path.join(os.path.dirname(__file__), "..", "asahigousen")

FOOTER_QUICK_LINKS = '''<div id="footer-quick-links" class="footer-quick-links"><nav><a href="/strength">当社の強み</a><a href="/machine">設備紹介</a><a href="/service">当社のものづくり</a><a href="/business_area">展開分野</a></nav></div>'''

MARKER = '<div id="footer-inner" class="clr">'


def main():
    for root, dirs, files in os.walk(ASAHI):
        for name in files:
            if not name.endswith(".html"):
                continue
            path = os.path.join(root, name)
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            if "footer-quick-links" in content:
                continue
            if MARKER not in content:
                continue
            content = content.replace(
                MARKER,
                MARKER + "\n" + FOOTER_QUICK_LINKS,
                1,
            )
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Added quick links: {path}")


if __name__ == "__main__":
    main()
