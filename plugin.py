from __future__ import annotations

from functools import partial
from pathlib import Path

import sublime
from LSP.plugin import LspPlugin, OnPreStartContext
from lsp_utils import InstallDirectory, download_and_extract_github_asset
from typing_extensions import override

SERVER_VERSION = "0.31.1"
SERVER_REPO = "elixir-lsp/elixir-ls"
SERVER_TAG = f"v{SERVER_VERSION}"
SERVER_ASSET = f"elixir-ls-v{SERVER_VERSION}.zip"
SERVER_SHA256 = "bac08322ea3698157eb2373bb5b65e38c15df9dd41e1c06f142f874367fa472f"

SERVER_EXECUTABLES = ["language_server.sh", "launch.sh"]
BINARY_PATH = (
    "language_server.bat" if sublime.platform() == "windows" else "language_server.sh"
)


def plugin_loaded() -> None:
    LspElixirPlugin.register()


def plugin_unloaded() -> None:
    LspElixirPlugin.unregister()


class LspElixirPlugin(LspPlugin):
    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        server_path = context.configuration.root_settings.get("server_path")
        if not server_path or server_path == "auto":
            server_path = str(cls.install_server() / BINARY_PATH)
        context.variables["server_path"] = server_path

    @classmethod
    def install_server(cls) -> Path:
        install_dir = InstallDirectory(
            cls.plugin_storage_path,
            "server",
            SERVER_VERSION,
            legacy_dirs=[cls.plugin_storage_path / "server"],
        )
        return install_dir.install(
            partial(
                download_and_extract_github_asset,
                SERVER_REPO,
                SERVER_TAG,
                SERVER_ASSET,
                executables=SERVER_EXECUTABLES,
                sha256=SERVER_SHA256,
            )
        )
