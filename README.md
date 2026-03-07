# アサヒゴウセン公式サイト（静的HTML版）

Wayback Machine から復元した [asahigousen.co.jp](https://asahigousen.co.jp/) の静的HTMLサイトです。

---

## 概要

元の WordPress サイトを Wayback Machine のスナップショットから取得し、静的HTMLとして復元しました。XServer 上で公開し、本番環境として運用しています。

---

## 実施済み作業

### 1. 静的サイトの復元

- Wayback Machine から HTML を取得・整形
- 画像パスをローカル構造に合わせて置換
- `asahigousen/` 以下にトップ・各ページを配置

### 2. レイアウト・表示の修正

| 対応内容 | 詳細 |
|----------|------|
| 横スクロール防止 | `site-header.css` に `overflow-x: hidden` を追加 |
| カルーセル（Swiper） | lazyload 対応、Swiper.js 初期化、スライド高さ統一 |
| フル幅ヒーロー画像 | 右側余白をカットし、左側の写真部分を適正表示（`object-fit: cover`, `object-position: left`） |
| 記事サムネイル | 1600×1115px の大きさを画面幅に収める（`max-width: 100%`） |
| コンテンツへスキップ | 全ページから除去 |
| カルーセル空スロット | 展開分野ページの壊れた2スライド（K2A6419, K2A6422）を削除 |

### 3. アップロード・デプロイ

- **XServer**: SFTP（SSH鍵認証）で `public_html/` にアップロード
- **GitHub**: 本リポジトリでバージョン管理

---

## ディレクトリ構成

```
asahigousen/           # 静的サイト一式（本番アップロード対象）
├── index.html         # トップ
├── aboutus/           # 会社案内
├── business_area/     # 展開分野
├── contact/           # お問い合わせ
├── info/              # お知らせ
├── machine/           # 設備紹介
├── message/           # メッセージ
├── privacy-policy/    # プライバシーポリシー
├── service/           # 当社のものづくり
├── strength/          # 当社の強み
├── archives/1271/     # お知らせ詳細（例）
├── assets/
│   ├── css/           # site-header.css（カスタムスタイル）
│   └── images/        # 画像ファイル
└── .htaccess          # 静的HTML用

scripts/               # アップロード・整形スクリプト
├── sftp_upload_static_site.py  # SFTP アップロード（推奨）
└── ...

docs/                  # 手順ドキュメント
├── XServer_静的サイトアップロード手順.md
└── WP_手動作業ガイド.md
```

---

## XServer へのアップロード

### 前提

- プロジェクト直下に `xb300407.key`（SSH秘密鍵）を配置
- `pip install paramiko` を実行済み

### 実行

```bash
cd /Users/soedakei/asahigosen
python3 scripts/sftp_upload_static_site.py
```

アップロード先: `sv886.xbiz.ne.jp` → `/home/xb300407/asahigousen.co.jp/public_html`

詳細は [docs/XServer_静的サイトアップロード手順.md](docs/XServer_静的サイトアップロード手順.md) を参照してください。

---

## 技術スタック

- 静的 HTML
- Elementor 風の構造（元WordPress）
- Swiper.js（カルーセル）
- OceanWP テーマ由来のスタイル

---

## リポジトリ

- **GitHub**: [Keeeeei-Soeda/asahi_gousen](https://github.com/Keeeeei-Soeda/asahi_gousen)
- **本番URL**: https://asahigousen.co.jp/

---

## ライセンス・注意

- アサヒゴウセンの企業サイトです
- 秘密鍵（`*.key`）は `.gitignore` で除外しており、リポジトリには含めていません
