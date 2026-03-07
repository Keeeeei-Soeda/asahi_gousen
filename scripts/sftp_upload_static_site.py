#!/usr/bin/env python3
"""
静的HTMLサイト一式を XServer に SFTP（SSH鍵認証）でアップロードする。
xb300407.key などの秘密鍵を使って、パスワード不要でアップロード可能。

使用例:
  python3 scripts/sftp_upload_static_site.py

環境変数（任意）:
  SSH_KEY_PATH  秘密鍵のパス（デフォルト: プロジェクト直下の xb300407.key）
  SSH_HOST      ホスト名（デフォルト: sv886.xbiz.ne.jp）
  SSH_PORT      SSHポート（デフォルト: 10022、XServer標準）
"""
import os
import sys

try:
    import paramiko
except ImportError:
    print("paramiko がインストールされていません。")
    print("  pip install paramiko")
    sys.exit(1)

SSH_HOST = os.environ.get("SSH_HOST", "sv886.xbiz.ne.jp")
SSH_PORT = int(os.environ.get("SSH_PORT", "10022"))
SSH_USER = os.environ.get("SSH_USER", "xb300407")
REMOTE_BASE = "/home/xb300407/asahigousen.co.jp/public_html"
LOCAL_SITE = os.path.join(os.path.dirname(__file__), "..", "asahigousen")
DEFAULT_KEY = os.path.join(os.path.dirname(__file__), "..", "xb300407.key")


def upload_dir(sftp, local_path: str, remote_path: str) -> None:
    """ローカルディレクトリを再帰的にアップロード。"""
    for name in sorted(os.listdir(local_path)):
        if name.startswith(".") and name != ".htaccess":
            continue
        local_full = os.path.join(local_path, name)
        remote_full = f"{remote_path.rstrip('/')}/{name}"
        if os.path.isdir(local_full):
            try:
                sftp.stat(remote_full)
            except FileNotFoundError:
                sftp.mkdir(remote_full)
            upload_dir(sftp, local_full, remote_full)
        else:
            sftp.put(local_full, remote_full)
            print(f"  ↑ {remote_full}")


def main():
    key_path = os.environ.get("SSH_KEY_PATH", DEFAULT_KEY)
    if not os.path.isfile(key_path):
        print(f"秘密鍵が見つかりません: {key_path}")
        print("SSH_KEY_PATH でパスを指定するか、プロジェクト直下に xb300407.key を配置してください。")
        sys.exit(1)
    if not os.path.isdir(LOCAL_SITE):
        print(f"ローカルサイトが見つかりません: {LOCAL_SITE}")
        sys.exit(1)

    print(f"接続: {SSH_HOST}:{SSH_PORT} (ユーザー: {SSH_USER})")
    print(f"秘密鍵: {key_path}")
    print(f"アップロード元: {LOCAL_SITE}")
    print(f"アップロード先: {REMOTE_BASE}")
    print()

    try:
        key = paramiko.RSAKey.from_private_key_file(key_path)
        transport = paramiko.Transport((SSH_HOST, SSH_PORT))
        transport.connect(username=SSH_USER, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # public_html を基準に、asahigousen の中身をアップロード
        # 既存の public_html 直下に index.html, assets/, info/ 等を配置
        for name in sorted(os.listdir(LOCAL_SITE)):
            if name.startswith(".") and name != ".htaccess":
                continue
            local_full = os.path.join(LOCAL_SITE, name)
            remote_full = f"{REMOTE_BASE}/{name}"
            if os.path.isdir(local_full):
                try:
                    sftp.stat(remote_full)
                except FileNotFoundError:
                    sftp.mkdir(remote_full)
                upload_dir(sftp, local_full, remote_full)
            else:
                sftp.put(local_full, remote_full)
                print(f"  ↑ {remote_full}")

        sftp.close()
        transport.close()
        print("\n✅ 静的サイトのアップロード完了")
    except paramiko.ssh_exception.SSHException as e:
        print(f"\n❌ SSHエラー: {e}")
        print("  - サーバーパネルで SSH が有効か確認してください")
        print("  - ポート 10022 で接続できるか確認してください")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
