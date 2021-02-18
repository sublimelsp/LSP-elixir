import hashlib
import os
import sublime

from zipfile import ZipFile
from urllib.request import urlretrieve

from lsp_utils import ServerResourceInterface, ServerStatus
from sublime_lib import ActivityIndicator
from LSP.plugin.core.typing import List

__all__ = ['ServerZipResource']


class ServerZipResource(ServerResourceInterface):
    def __init__(self,
                 storage_path: str,
                 package_name: str,
                 binary_path: str,
                 asset_url: str,
                 asset_version: str,
                 *,
                 asset_hash: str = None,
                 executables: List[str] = []) -> None:
        self._storage_path = storage_path
        self._package_name = package_name
        self._binary_path = binary_path
        self._url = asset_url
        self._version = asset_version
        self._status = ServerStatus.UNINITIALIZED

        self._hash = asset_hash
        self._executables = executables

    def get_server_dir(self) -> str:
        return os.path.join(self._storage_path, self._package_name, "server", self._version)

    def get_server_exec(self) -> str:
        return os.path.join(self.get_server_dir(), self._binary_path)

    def is_server_downloaded(self):
        return os.path.exists(self.get_server_exec())

    def is_valid_hash(self, path, expected) -> bool:
        if not self._hash:
            return True

        with open(path, "rb") as f:
            calculated = hashlib.sha256(f.read()).hexdigest()
            return calculated == expected

    def unpack_server(self, zip_file) -> None:
        if not self.is_valid_hash(zip_file, self._hash):
            return

        target_dir = self.get_server_dir()
        os.makedirs(target_dir, exist_ok=True)

        with ZipFile(zip_file, "r") as f:
            f.extractall(target_dir)

        # ZipFile removes permissions, make server executable
        if self._executables and not sublime.platform() == 'windows':
            for executable in self._executables:
                os.chmod(os.path.join(target_dir, executable), 0o755)

    def download_server(self) -> None:
        target = sublime.active_window()
        label = "Downloading zip file..."

        with ActivityIndicator(target, label):
            tmp_file, _ = urlretrieve(self._url)
            self.unpack_server(tmp_file)
            os.unlink(tmp_file)

    # ServerResourceInterface

    def get_status(self) -> int:
        return self._status

    def needs_installation(self) -> bool:
        if self.is_server_downloaded():
            self._status = ServerStatus.READY
            return False
        return True

    def install_or_update(self) -> None:
        self.download_server()
        self._status = ServerStatus.READY

    @property
    def binary_path(self) -> str:
        return self.get_server_exec()
