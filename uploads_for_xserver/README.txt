画像を XServer にアップロードするためのフォルダです。

【使い方】
1. 用意済みの画像を、旧サイトと同じ構成でここに配置してください。
   例: 2021/05/logo_ag.fw_.png
      2021/05/fv.fw_-150x150.png
      2021/06/asahigousenPV.mp4
2. ターミナルで以下を実行:
   export FTP_PASSWORD='あなたのサーバーパスワード'
   python3 scripts/ftp_upload_to_xserver.py

【FTP接続情報（scripts/ftp_upload_to_xserver.py の既定値）】
ホスト: sv886.xbiz.ne.jp
ユーザー: xb300407
アップロード先: /home/xb300407/asahigousen.co.jp/public_html/wp-content/uploads
