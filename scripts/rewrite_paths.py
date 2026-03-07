#!/usr/bin/env python3
"""
画像パスを assets/images/ への相対パスに、
内部リンクをルート相対パス（/）に書き換える。
"""
import os
import re

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "asahigousen")
UPLOADS_PREFIX = "https://asahigousen.co.jp/cms/wp-content/uploads/"
SITE_ROOT = "https://asahigousen.co.jp"


def depth_from_root(filepath: str) -> int:
    """asahigousen からの相対深度。index.html が 0, info/index.html が 1."""
    rel = os.path.relpath(os.path.dirname(filepath), OUTPUT_DIR)
    if rel == ".":
        return 0
    return len(rel.split(os.sep))


def assets_prefix(depth: int) -> str:
    """画像用の相対パス prefix（末尾スラッシュ付き）."""
    if depth == 0:
        return "assets/images/"
    return "../" * depth + "assets/images/"


def rewrite_file(path: str, content: str, depth: int) -> str:
    prefix = assets_prefix(depth)

    # 画像: asahigousen.co.jp/cms/wp-content/uploads/ → assets/images/
    content = content.replace(
        "https://asahigousen.co.jp/cms/wp-content/uploads/",
        prefix,
    )
    # cms./ の typo パターンも同様
    content = content.replace(
        "https://asahigousen.co.jp/cms./wp-content/uploads/",
        prefix,
    )

    # 内部リンク・リソース: https://asahigousen.co.jp/ → /
    # （外部サイトは触らない）
    content = re.sub(
        r'https://asahigousen\.co\.jp/',
        '/',
        content,
    )

    # JSON 内のエスケープされた web.archive 残骸を除去
    content = re.sub(
        r'https:\\?/\\?/web\.archive\.org\\?/web\\?/\d+[a-z_]*\\?/https:\\?/\\?/asahigousen\.co\.jp\\?/',
        '/',
        content,
    )
    content = re.sub(
        r'https:\\?/\\?/asahigousen\.co\.jp\\?/',
        '/',
        content,
    )

    # dns-prefetch 等で残った web.archive を削除（空 href にならないよう置換）
    content = re.sub(
        r'<link rel="dns-prefetch" href=""/>',
        '<link rel="dns-prefetch" href="https://www.google.com"/>',
        content,
    )

    return content


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
            depth = depth_from_root(path)
            rewritten = rewrite_file(path, content, depth)
            with open(path, "w", encoding="utf-8") as f:
                f.write(rewritten)
            print(f"Rewritten: {path} (depth={depth})")


if __name__ == "__main__":
    main()
