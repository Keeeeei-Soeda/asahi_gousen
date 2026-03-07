#!/usr/bin/env python3
"""
2nd_recovery.md Step 2: Wayback Machine から各ページのHTMLを取得し、
メインコンテンツのテキストを抽出してファイルに保存する。
"""
import os
import re
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("必要なパッケージをインストールしてください: pip install -r requirements.txt")
    sys.exit(1)

# スナップショット日時（20250122 前後の利用可能なもの）
SNAPSHOT = "20250122153554"
BASE_URL = f"https://web.archive.org/web/{SNAPSHOT}/https://asahigousen.co.jp"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "wp_content_extract")

PAGES = [
    ("index", "トップページ", "/"),
    ("info", "お知らせ一覧", "/info"),
    ("archives_1271", "お知らせ詳細（例）", "/archives/1271"),
    ("strength", "当社の強み", "/strength"),
    ("service", "当社のものづくり", "/service"),
    ("business_area", "展開分野", "/business_area"),
    ("machine", "設備紹介", "/machine"),
    ("aboutus", "会社案内", "/aboutus"),
    ("message", "メッセージ", "/message"),
    ("contact", "お問い合わせ", "/contact"),
    ("privacy-policy", "プライバシーポリシー", "/privacy-policy"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
}


def extract_main_content(soup: BeautifulSoup) -> str:
    """メインコンテンツ要素からテキストを抽出。"""
    # Wayback ツールバー等を除去
    for selector in ["#wm-ipp-base", "#wm-ipp", ".wb-banner"]:
        for tag in soup.select(selector):
            tag.decompose()
    for tag in soup.find_all("script"):
        tag.decompose()
    for tag in soup.find_all("style"):
        tag.decompose()

    # メインコンテンツを優先
    main = soup.find("main") or soup.find("div", class_=re.compile(r"content-area|site-main"))
    if main:
        return main.get_text(separator="\n", strip=True)
    body = soup.find("body")
    if body:
        return body.get_text(separator="\n", strip=True)
    return soup.get_text(separator="\n", strip=True)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for slug, title, path in PAGES:
        url = BASE_URL + path
        try:
            res = requests.get(url, headers=HEADERS, timeout=30)
            res.raise_for_status()
        except Exception as e:
            print(f"⚠ {slug}: 取得失敗 - {e}")
            continue

        soup = BeautifulSoup(res.text, "html.parser")
        text = extract_main_content(soup)
        # ページタイトル行を先頭に
        content = f"# {title}\n\n{text}\n"
        out_path = os.path.join(OUTPUT_DIR, f"{slug}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {slug} 取得・保存: {out_path}")

    print("\n完了: wp_content_extract/ にテキストを保存しました。")


if __name__ == "__main__":
    main()
