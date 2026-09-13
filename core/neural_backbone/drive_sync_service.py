# ☁️ GENESIS Drive Sync Service | Cloud Run ✕ Google Drive 永続同期サービス
import os
import sys
import json
import time
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class DriveSyncService:
    """
    Cloud RunコンテナがScale to 0（インスタンス数0）で停止しても、
    作業成果物や差分が消失しないよう、Google Driveとの間で
    起動時ダウンロード＆更新時アップロードを管理する永続化サービス。
    """
    def __init__(self):
        self.local_root = ROOT_DIR
        self.drive_mount = os.environ.get("GOOGLE_DRIVE_MOUNT", r"g:\マイドライブ\GENESIS_ROOT")
        self.is_cloud_run = bool(os.environ.get("K_SERVICE") or os.environ.get("CLOUD_RUN_JOB"))

    def sync_to_drive(self, relative_path: str) -> bool:
        """ローカルで変更されたファイルをGoogle Driveストレージへ同期保存"""
        src = self.local_root / relative_path
        if not src.exists():
            return False

        # If on local machine where drive_mount is the same directory, no copy needed
        if os.path.abspath(str(self.local_root)) == os.path.abspath(self.drive_mount):
            return True

        dst = Path(self.drive_mount) / relative_path
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_file():
                shutil.copy2(src, dst)
            elif src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"[DriveSync] Synced {relative_path} -> Google Drive")
            return True
        except Exception as e:
            print(f"[DriveSync] Error syncing {relative_path}: {e}", file=sys.stderr)
            return False

    def sync_from_drive(self, relative_path: str) -> bool:
        """Google Drive上の最新データをローカルコンテナへ同期展開"""
        src = Path(self.drive_mount) / relative_path
        if not src.exists():
            return False

        if os.path.abspath(str(self.local_root)) == os.path.abspath(self.drive_mount):
            return True

        dst = self.local_root / relative_path
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src.is_file():
                shutil.copy2(src, dst)
            elif src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"[DriveSync] Pulled {relative_path} <- Google Drive")
            return True
        except Exception as e:
            print(f"[DriveSync] Error pulling {relative_path}: {e}", file=sys.stderr)
            return False

drive_sync_service = DriveSyncService()
