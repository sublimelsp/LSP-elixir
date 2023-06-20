import sublime

from lsp_utils import GenericClientHandler, ServerResourceInterface
from LSP.plugin.core.typing import Optional

from .server_zip_resource import ServerZipResource

SERVER_VERSION = "0.15.0"
SERVER_URL = "https://github.com/elixir-lsp/elixir-ls/releases/download/v0.15.0/elixir-ls-v0.15.0.zip"
SERVER_SHA256 = "d388294c509c4e1fee023aa3723f241d453858910b28670c81fbd337f91d1ba9"

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
