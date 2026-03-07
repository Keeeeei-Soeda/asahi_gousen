# XServer への静的HTMLサイトアップロード手順

静的HTMLで復元したサイトを XServer にアップロードし、表示するための手順です。

---

## 役割分担

| 担当 | 作業内容 |
|------|----------|
| **Cursor 側** | アップロードスクリプト・.htaccess の用意（完了済み） |
| **作業者** | FTP での準備、スクリプト実行、動作確認 |

---

## 手順（作業者が実施）

### Step 1: FTP でサーバーに接続

- ホスト: `sv886.xbiz.ne.jp`
- ユーザー: `xb300407`
- パスワード: サーバーパスワード（XServer アカウントログインと同じ）

### Step 2: WordPress を無効化（FTP で）

`public_html/wp-config.php` を `wp-config.php.bak` にリネームする。

### Step 3: 既存 .htaccess のバックアップ（FTP で）

`public_html/.htaccess` を `public_html/.htaccess.wordpress.bak` にリネームして退避する。

### Step 4: 静的サイト一式をアップロード（ターミナルで実行）

**SSH鍵を使う場合（推奨・パスワード不要）**

```bash
cd /Users/soedakei/asahigosen
pip install paramiko   # 初回のみ
python3 scripts/sftp_upload_static_site.py
```

※ プロジェクト直下の `xb300407.key` を使って SFTP 接続します。サーバーパスワードは不要です。

**FTP パスワードを使う場合**

```bash
export FTP_PASSWORD='サーバーパスワード'
python3 scripts/ftp_upload_static_site.py
```

アップロード内容：
- `index.html`、`info/`、`strength/`、`assets/` など全ファイル
- `.htaccess`（静的HTML用に上書き）

### Step 5: 動作確認

ブラウザで https://asahigousen.co.jp/ を開き、トップ・各ページが表示されることを確認する。

---

## 元に戻す場合（WordPress を再有効化）

1. FTP で `wp-config.php.bak` を `wp-config.php` に戻す
2. `public_html/.htaccess` を `public_html/.htaccess.wordpress.bak` の内容で復元
3. 静的HTMLファイル（index.html, info/, strength/ など）は必要に応じて削除

---

## ファイル一覧（Cursor 側で用意済み）

| ファイル | 説明 |
|----------|------|
| `scripts/ftp_upload_static_site.py` | 静的サイト一式を public_html にアップロード |
| `asahigousen/.htaccess` | 静的HTML用の .htaccess（index.html 優先など） |
