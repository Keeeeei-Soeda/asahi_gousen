# WordPress 再構築 — 手動作業ガイド

2nd_recovery.md の Step 3・5・6 を管理画面で行うための手順と、抽出済みテキストの参照先です。

---

## 抽出済みコンテンツ（Step 2 完了分）

以下のテキストは `wp_content_extract/` に保存済みです。固定ページ作成時にコピー＆ペーストして利用してください。

| ファイル | ページ名 | WPスラッグ |
|----------|----------|------------|
| index.txt | トップページ | （フロントページに設定） |
| info.txt | お知らせ一覧 | （投稿一覧のため固定ページではない） |
| archives_1271.txt | お知らせ詳細（例） | （投稿として作成） |
| strength.txt | 当社の強み | `strength` |
| service.txt | 当社のものづくり | `service` |
| business_area.txt | 展開分野 | `business_area` |
| machine.txt | 設備紹介 | `machine` |
| aboutus.txt | 会社案内 | `aboutus` |
| message.txt | メッセージ | `message` |
| contact.txt | お問い合わせ | `contact` |
| privacy-policy.txt | プライバシーポリシー | `privacy-policy` |

---

## Step 3: 固定ページの作成

1. **固定ページ → 新規追加**
2. **タイトル**を入力（例: 当社の強み）
3. **スラッグ**を設定（例: `strength`）  
   - 一覧: strength, service, business_area, machine, aboutus, message, contact, privacy-policy
4. **「Elementorで編集」**をクリック
5. `wp_content_extract/【スラッグ】.txt` を開き、本文をコピーして Elementor のテキストブロックに貼り付け
6. 画像はメディアライブラリから挿入（Step 4 でアップロード済みのものを使用）
7. **公開**をクリック

※ トップページは「設定 → 表示設定」で「ホームページの表示」を「固定ページ」にし、作成したトップ用ページを指定してください。

---

## Step 4: 画像のアップロード（FTP で行う場合）

1. 用意済み画像を `uploads_for_xserver/` に配置  
   - 旧サイトと同じ構成（例: `2021/05/logo_ag.fw_.png`）
2. ターミナルで実行:
   ```bash
   export FTP_PASSWORD='あなたのサーバーパスワード'
   python3 scripts/ftp_upload_to_xserver.py
   ```
3. または WP 管理画面 → メディア → 新規追加 で個別アップロード

---

## Step 5: ナビゲーションメニュー

1. **外観 → メニュー**
2. メニュー名を入力（例: メインメニュー）→ メニューを作成
3. 左側から固定ページを「メニューに追加」
4. 並び順を次のように調整:

   - ホーム → /
   - お知らせ → /info
   - 当社の強み → /strength
   - 当社のものづくり → /service
   - 展開分野 → /business_area
   - 設備紹介 → /machine
   - 会社案内 → /aboutus
   - メッセージ → /message
   - お問い合わせ → /contact

5. 「メニューを保存」
6. **表示場所**で「メインメニュー」等にチェック → 保存

---

## Step 6: お問い合わせフォーム（Contact Form 7）

1. **プラグイン → 新規追加** → 「Contact Form 7」で検索 → インストール・有効化
2. **お問い合わせ → 新規追加** でフォームを作成
3. 生成された **ショートコード**（例: `[contact-form-7 id="123" title="お問い合わせ"]`）をコピー
4. **固定ページ「お問い合わせ」**を Elementor で編集し、ショートコードブロックを追加して貼り付け
5. 保存・公開

---

## Step 7: 動作確認チェックリスト

- [ ] トップページが正常に表示される
- [ ] 全11ページが存在し URL でアクセスできる
- [ ] ナビゲーションメニューが機能する
- [ ] 画像が全ページで表示される
- [ ] お問い合わせフォームが送信できる
- [ ] スマートフォン表示が崩れていない
- [ ] プライバシーポリシーページが存在する
