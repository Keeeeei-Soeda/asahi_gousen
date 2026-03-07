# asahigousen.co.jp 静的HTMLサイト復元タスク

## 概要

Web Archive（Wayback Machine）を使って、`asahigousen.co.jp` の静的HTMLサイトを復元する。
取得したHTMLを整形・修正し、ローカルで動作する静的サイトとして再構築することがゴール。

---

## ゴール

- 全対象ページのHTMLを取得・復元
- 画像は別途用意済みのデータを使用（パスを適切に置換）
- CSS・JS・フォントはWeb Archiveから取得 or 再現
- ローカルで `index.html` を開いて全ページが正常に閲覧できる状態にする

---

## 対象ページ一覧

| ページ名 | パス | Wayback Machine URL |
|----------|------|----------------------|
| トップページ | `/` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/ |
| お知らせ一覧 | `/info` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/info |
| お知らせ詳細（例） | `/archives/1271` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/archives/1271 |
| 当社の強み | `/strength` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/strength |
| 当社のものづくり | `/service` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/service |
| 展開分野 | `/business_area` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/business_area |
| 設備紹介 | `/machine` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/machine |
| 会社案内 | `/aboutus` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/aboutus |
| メッセージ | `/message` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/message |
| お問い合わせ | `/contact` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/contact |
| プライバシーポリシー | `/privacy-policy` | https://web.archive.org/web/20250122000000*/https://asahigousen.co.jp/privacy-policy |

---

## 作業手順

### Step 1: Wayback Machine から HTML を取得

以下のコマンドで各ページのHTMLを取得する。
スナップショット日時は `20250122` 前後の最新のものを使用すること。

```bash
# wayback_machine_downloader を使う場合
gem install wayback_machine_downloader
wayback_machine_downloader https://asahigousen.co.jp --all-timestamps

# または wget で個別取得
wget -p -k "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/"
wget -p -k "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/strength"
wget -p -k "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/service"
# （以下、全ページ同様に実行）
```

### Step 2: Wayback Machine の余分なコードを除去

取得したHTMLには Wayback Machine のツールバーや埋め込みスクリプトが含まれる。
以下を全HTMLファイルから除去すること。

- `<!-- BEGIN WAYBACK TOOLBAR INSERT -->` 〜 `<!-- END WAYBACK TOOLBAR INSERT -->` の間のコード
- `https://web.archive.org/web/202501XXXXXX/` のURLプレフィックスをすべて相対パスに変換

```python
# 例：Pythonで一括置換
import os, re

for root, dirs, files in os.walk("output_dir"):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Waybackプレフィックス除去
            content = re.sub(r'https://web\.archive\.org/web/\d+/', '', content)
            # ツールバー除去
            content = re.sub(r'<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->', '', content, flags=re.DOTALL)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
```

### Step 3: ディレクトリ構成を整える

以下の構成でファイルを配置する。

```
asahigousen/
├── index.html              # トップページ
├── info/
│   └── index.html
├── archives/
│   └── 1271/
│       └── index.html
├── strength/
│   └── index.html
├── service/
│   └── index.html
├── business_area/
│   └── index.html
├── machine/
│   └── index.html
├── aboutus/
│   └── index.html
├── message/
│   └── index.html
├── contact/
│   └── index.html
├── privacy-policy/
│   └── index.html
├── assets/
│   ├── images/        # 用意済み画像データをここに配置
│   ├── css/
│   └── js/
```

### Step 4: 画像パスの置換

用意済みの画像データを `assets/images/` に配置し、
HTML内の画像パスをすべて相対パスに書き換える。

```python
# 例：画像パスの置換
content = content.replace('https://asahigousen.co.jp/wp-content/uploads/', '../assets/images/')
```

### Step 5: 内部リンクの修正

ページ間のリンクがすべて相対パスで正しく繋がるよう修正する。

- `href="https://asahigousen.co.jp/strength"` → `href="/strength/"` または `href="../strength/"`
- お問い合わせフォームは静的化（送信機能は削除 or Googleフォームに差し替え）

### Step 6: 動作確認

ローカルサーバーを立てて全ページを確認する。

```bash
# Pythonでローカルサーバー起動
cd asahigousen
python3 -m http.server 8000
# → http://localhost:8000 で確認
```

---

## 注意事項

- WordPress由来のPHP処理（`wp-admin`、`wp-json` など）は不要なので除去
- お問い合わせフォームの `action` はそのままでは動作しないため、静的化が必要
- フォントは Google Fonts などを CDN 経由で参照しているものはそのまま使用可能
- Wayback Machine の取得に失敗するページは日時を変えて再取得する

---

## 完了条件

- [x] 全11ページのHTMLが存在する
- [x] ローカルで全ページが正常に表示される（要: `cd asahigousen && python3 -m http.server 8000` → http://localhost:8000）
- [x] 内部リンクがすべて機能する（ルート相対パス `/info/`, `/strength/` 等に変換済み）
- [ ] 画像が正しく表示される（`assets/images/` に用意済み画像を配置してください）
- [x] Wayback Machineのツールバーが表示されない

---

## 作業結果メモ（復元実施後）

- **取得**: 全11ページを Wayback Machine（20250122153554 前後）から curl で取得
- **配置**: `asahigousen/` 以下に指示通りのディレクトリ構成で配置
- **スクリプト**: `scripts/clean_wayback.py`（Wayback 除去）、`scripts/rewrite_paths.py`（画像パス・内部リンク置換）
- **補足**: CSS/JS は `/cms/...` を参照しているため、スタイルを完全に再現するには Wayback から CSS/JS を取得して `asahigousen/cms/` 等に配置するか、CDN 等で代替する必要があります。