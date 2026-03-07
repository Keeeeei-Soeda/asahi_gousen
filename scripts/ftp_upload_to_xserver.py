#!/usr/bin/env python3
"""
2nd_recovery.md Step 4: 用意済み画像を XServer FTP にアップロードする。
環境変数 FTP_PASSWORD にサーバーパスワードを設定して実行してください。

使用例:
  export FTP_PASSWORD='your_server_password'
  python3 scripts/ftp_upload_to_xserver.py

またはアップロード元ディレクトリを指定:
  python3 scripts/ftp_upload_to_xserver.py path/to/local/uploads
"""
import os
import sys
from ftplib import FTP

# XServer FTP（FTPソフト設定で確認した値）
FTP_HOST = os.environ.get("FTP_HOST", "sv886.xbiz.ne.jp")
FTP_USER = os.environ.get("FTP_USER", "xb300407")
# パスワードは環境変数で渡す（サーバーパスワードと同じ）
FTP_PASSWORD = os.environ.get("FTP_PASSWORD", "")
# リモートのアップロード先（WordPress の uploads ディレクトリ）
REMOTE_UPLOADS = "/home/xb300407/asahigousen.co.jp/public_html/wp-content/uploads"

# デフォルトのローカルアップロード元
DEFAULT_LOCAL_DIR = os.path.join(
    os.path.dirname(__file__), "..", "uploads_for_xserver"
)


def upload_dir(ftp: FTP, local_path: str) -> None:
    """現在のFTPカレントディレクトリに、ローカルディレクトリを再帰的にアップロード。"""
    for name in os.listdir(local_path):
        local_full = os.path.join(local_path, name)
        if os.path.isdir(local_full):
            try:
                ftp.mkd(name)
            except Exception:
                pass  # 既に存在する場合
            ftp.cwd(name)
            upload_dir(ftp, local_full)
            ftp.cwd("..")
        else:
            with open(local_full, "rb") as f:
                ftp.storbinary(f"STOR {name}", f)
            print(f"  ↑ {name}")


def main():
    local_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOCAL_DIR
    if not os.path.isdir(local_dir):
        print(f"ローカルディレクトリがありません: {local_dir}")
        print("用意済み画像をこのディレクトリに配置してから再実行してください。")
        print("例: 2021/05/logo_ag.fw_.png など、旧サイトの wp-content/uploads と同じ構成で配置")
        sys.exit(1)
    if not FTP_PASSWORD:
        print("環境変数 FTP_PASSWORD を設定してください。")
        print("例: export FTP_PASSWORD='your_server_password'")
        sys.exit(1)

    print(f"接続: {FTP_HOST} (ユーザー: {FTP_USER})")
    print(f"アップロード元: {local_dir}")
    print(f"アップロード先: {REMOTE_UPLOADS}")
    print()

    try:
        ftp = FTP(FTP_HOST, timeout=30)
        ftp.login(FTP_USER, FTP_PASSWORD)
        # リモートの wp-content/uploads まで移動（無ければ作成）
        for part in REMOTE_UPLOADS.strip("/").split("/"):
            if not part:
                continue
            try:
                ftp.cwd(part)
            except Exception:
                try:
                    ftp.mkd(part)
                    ftp.cwd(part)
                except Exception:
                    pass
        upload_dir(ftp, local_dir)
        ftp.quit()
        print("\n✅ アップロード完了")
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
