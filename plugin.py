import sublime

from lsp_utils import GenericClientHandler, ServerResourceInterface
from LSP.plugin.core.typing import Optional

from .server_zip_resource import ServerZipResource

SERVER_VERSION = "0.25.0"
SERVER_URL = "https://github.com/elixir-lsp/elixir-ls/releases/download/v0.25.0/elixir-ls-v0.25.0.zip"
SERVER_SHA256 = "08ab46b78a2cc6b5a8af10c1f64fc45440b7521ebdaf08a5af2437b54ccce5a4"

SERVER_EXECUTABLES = ["language_server.sh", "launch.sh"]
BINARY_PATH = (
    "language_server.bat" if sublime.platform() == "windows" else "language_server.sh"
)


def plugin_loaded() -> None:
    LspElixirPlugin.setup()


def plugin_unloaded() -> None:
    LspElixirPlugin.cleanup()


class LspElixirPlugin(GenericClientHandler):
    package_name = __package__
    __server = None

    @classmethod
    def get_displayed_name(cls) -> str:
        return "lsp-elixir"

    @classmethod
    def manages_server(cls) -> bool:
        return True

    @classmethod
    def get_server(cls) -> Optional[ServerResourceInterface]:
        if not cls.__server:
            cls.__server = ServerZipResource(
                cls.storage_path(),
                cls.package_name,
                BINARY_PATH,
                SERVER_URL,
                SERVER_VERSION,
                asset_hash=SERVER_SHA256,
                executables=SERVER_EXECUTABLES,
            )
        return cls.__server
