# asahigousen.co.jp WordPress再構築タスク

## 概要

新サーバー（XServer Business）にすでにWordPressがインストールされている。
旧サイトのバックアップは存在しないため、**Wayback Machineを参照しながらページを再構築**する。
テーマはOceanWP、ページビルダーはElementorを使用。

---

## 環境情報

| 項目 | 値 |
|------|-----|
| サイトURL | https://asahigousen.co.jp |
| WP管理画面 | https://asahigousen.co.jp/wp-admin/ |
| サーバー | XServer Business（sv886.xbiz.ne.jp） |
| テーマ | OceanWP |
| ページビルダー | Elementor（無料版） |

---

## ゴール

- 全対象ページをWordPressで再構築
- Wayback MachineのスナップショットをベースにHTMLテキストを抽出
- 画像は用意済みのデータを使用
- デザインはOceanWP＋Elementorで再現

---

## 対象ページ一覧

| ページ名 | スラッグ | Wayback Machine参照URL |
|----------|----------|------------------------|
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

### Step 1: WordPress初期設定 ✅ 完了（2026/03/06）

以下をWP管理画面で設定する。

1. **OceanWPテーマの有効化**
   - 外観 → テーマ → 新規追加 → 「OceanWP」検索 → インストール → 有効化

2. **Elementorプラグインの有効化**
   - プラグイン → 新規追加 → 「Elementor」検索 → インストール → 有効化

3. **パーマリンク設定**
   - 設定 → パーマリンク → 「投稿名」を選択 → 保存
   - これにより `/strength` `/service` などのURLが使用可能になる

---

### Step 2: Wayback MachineからHTMLテキストを抽出 ✅ 完了

各ページのWayback Machine URLにアクセスし、以下の情報をページごとに抽出する。

```python
# Pythonで各ページのテキストを取得する例
import requests
from bs4 import BeautifulSoup

pages = {
    "strength": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/strength",
    "service": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/service",
    "business_area": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/business_area",
    "machine": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/machine",
    "aboutus": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/aboutus",
    "message": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/message",
    "contact": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/contact",
    "privacy-policy": "https://web.archive.org/web/20250122140416/https://asahigousen.co.jp/privacy-policy",
}

for slug, url in pages.items():
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    # Waybackツールバー除去
    for tag in soup.find_all(id="wm-ipp-base"):
        tag.decompose()
    # メインコンテンツ抽出
    content = soup.find("main") or soup.find("div", class_="content-area")
    with open(f"{slug}.txt", "w", encoding="utf-8") as f:
        f.write(content.get_text(separator="\n") if content else soup.get_text())
    print(f"✅ {slug} 取得完了")
```

---

### Step 3: 各ページのWP固定ページを作成

抽出したテキストをもとに、WP管理画面で固定ページを作成する。

#### ページ作成の共通手順
1. 固定ページ → 新規追加
2. タイトルを入力
3. スラッグを設定（例：`strength`）
4. 「Elementorで編集」ボタンをクリック
5. テキスト・画像をElementorブロックで配置

#### 各ページのスラッグ設定

| ページ名 | スラッグ |
|----------|----------|
| 当社の強み | `strength` |
| 当社のものづくり | `service` |
| 展開分野 | `business_area` |
| 設備紹介 | `machine` |
| 会社案内 | `aboutus` |
| メッセージ | `message` |
| お問い合わせ | `contact` |
| プライバシーポリシー | `privacy-policy` |

---

### Step 4: 画像のアップロード

用意済みの画像データをWPメディアライブラリにアップロードする。

- WP管理画面 → メディア → 新規追加
- または XServerファイルマネージャーで
  `/asahigousen.co.jp/public_html/wp-content/uploads/` に直接配置

---

### Step 5: ナビゲーションメニューの設定

外観 → メニュー で以下のメニューを作成する。

```
ホーム          → /
お知らせ        → /info
当社の強み      → /strength
当社のものづくり → /service
展開分野        → /business_area
設備紹介        → /machine
会社案内        → /aboutus
メッセージ      → /message
お問い合わせ    → /contact
```

---

### Step 6: お問い合わせフォームの設置

静的HTMLのフォームは動作しないため、WPプラグインで代替する。

1. プラグイン → 新規追加 → 「Contact Form 7」インストール・有効化
2. お問い合わせ → 新規追加でフォームを作成
3. 生成されたショートコードを `/contact` ページに貼り付け

---

### Step 7: 動作確認チェックリスト

- [ ] トップページが正常に表示される
- [ ] 全11ページが存在しURLでアクセスできる
- [ ] ナビゲーションメニューが機能する
- [ ] 画像が全ページで表示される
- [ ] お問い合わせフォームが送信できる
- [ ] スマートフォン表示が崩れていない
- [ ] プライバシーポリシーページが存在する

---

## 注意事項

- Elementorの無料版で対応できない機能はOceanWPのウィジェットで代替する
- 旧サイトのElementorデータは存在しないため、レイアウトは近似再現とする
- お知らせ（`/info`）はWPの「投稿」機能をそのまま使う
- `/archives/{id}` のURLはWPのパーマリンク設定で自動的に対応される

---

## 作業結果メモ（自動実行分）

- **Step 2 完了**: `scripts/extract_wayback_content.py` で全11ページのテキストを抽出済み。  
  出力先: `wp_content_extract/*.txt`
- **Step 4 用**: 画像を `uploads_for_xserver/` に配置後、  
  `export FTP_PASSWORD='...'` を設定して `python3 scripts/ftp_upload_to_xserver.py` で XServer（sv886.xbiz.ne.jp, ユーザー xb300407）へアップロード可能。
- **手動作業**: Step 3・5・6 の手順は `docs/WP_手動作業ガイド.md` を参照。