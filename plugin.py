import sublime

from lsp_utils import GenericClientHandler, ServerResourceInterface
from LSP.plugin.core.typing import Optional

from .server_zip_resource import ServerZipResource

SERVER_URL = "https://github.com/elixir-lsp/elixir-ls/releases/download/v0.6.4/elixir-ls-1.11.zip"
SERVER_HASH = "30df49d0c7c12717814a3b03d4b8064197820a10beac138ad6d63d28f5295a4f"
SERVER_VERSION = "0.6.4"

SERVER_EXECUTABLES = ["language_server.sh", "launch.sh"]
BINARY_PATH = "language_server.bat" if sublime.platform() == 'windows' else "language_server.sh"


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
            cls.__server = ServerZipResource(cls.storage_path(),
                                             cls.package_name,
                                             BINARY_PATH,
                                             SERVER_URL,
                                             SERVER_VERSION,
                                             executables=SERVER_EXECUTABLES)
        return cls.__server
