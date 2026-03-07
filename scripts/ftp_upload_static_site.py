#!/usr/bin/env python3
"""
静的HTMLサイト一式を XServer の public_html にアップロードする。
WordPress 無効化後、静的ページを表示するためのアップロード用。

使用例:
  export FTP_PASSWORD='サーバーパスワード'
  python3 scripts/ftp_upload_static_site.py
"""
import os
import sys
from ftplib import FTP

FTP_HOST = os.environ.get("FTP_HOST", "sv886.xbiz.ne.jp")
FTP_USER = os.environ.get("FTP_USER", "xb300407")
FTP_PASSWORD = os.environ.get("FTP_PASSWORD", "")
REMOTE_BASE = "/home/xb300407/asahigousen.co.jp/public_html"
LOCAL_SITE = os.path.join(os.path.dirname(__file__), "..", "asahigousen")


def upload_dir(ftp: FTP, local_path: str) -> None:
    """現在のFTPカレントディレクトリに、ローカルディレクトリを再帰的にアップロード。"""
    for name in sorted(os.listdir(local_path)):
        if name.startswith(".") and name != ".htaccess":
            continue
        local_full = os.path.join(local_path, name)
        if os.path.isdir(local_full):
            try:
                ftp.mkd(name)
            except Exception:
                pass
            ftp.cwd(name)
            upload_dir(ftp, local_full)
            ftp.cwd("..")
        else:
            with open(local_full, "rb") as f:
                ftp.storbinary(f"STOR {name}", f)
            print(f"  ↑ {name}")


def main():
    if not os.path.isdir(LOCAL_SITE):
        print(f"ローカルサイトが見つかりません: {LOCAL_SITE}")
        sys.exit(1)
    if not FTP_PASSWORD:
        print("環境変数 FTP_PASSWORD を設定してください。")
        print("例: export FTP_PASSWORD='サーバーパスワード'")
        sys.exit(1)

    print(f"接続: {FTP_HOST} (ユーザー: {FTP_USER})")
    print(f"アップロード元: {LOCAL_SITE}")
    print(f"アップロード先: {REMOTE_BASE}")
    print()

    try:
        ftp = FTP(FTP_HOST, timeout=60)
        ftp.login(FTP_USER, FTP_PASSWORD)
        # public_html まで移動
        for part in REMOTE_BASE.strip("/").split("/"):
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
        upload_dir(ftp, LOCAL_SITE)
        ftp.quit()
        print("\n✅ 静的サイトのアップロード完了")
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
