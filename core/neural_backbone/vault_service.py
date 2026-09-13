import os
import json
import threading
from pathlib import Path

class VaultService:
    def __init__(self):
        self._locks = {}
        self._global_lock = threading.Lock()

    def _get_lock(self, file_path: str) -> threading.Lock:
        with self._global_lock:
            if file_path not in self._locks:
                self._locks[file_path] = threading.Lock()
            return self._locks[file_path]

    def read_json(self, file_path: str, default=None):
        if default is None:
            default = []
        if not os.path.exists(file_path):
            return default
        lock = self._get_lock(file_path)
        with lock:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[VaultService] Error reading {file_path}: {e}")
                return default

    def write_json(self, file_path: str, data) -> bool:
        lock = self._get_lock(file_path)
        with lock:
            try:
                os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
                temp_file = f"{file_path}.tmp"
                with open(temp_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                if os.path.exists(file_path):
                    os.replace(temp_file, file_path)
                else:
                    os.rename(temp_file, file_path)
                return True
            except Exception as e:
                print(f"[VaultService] Error writing {file_path}: {e}")
                return False

vault_service = VaultService()
