import sublime

from lsp_utils import GenericClientHandler, ServerResourceInterface
from LSP.plugin.core.typing import Optional

from .server_zip_resource import ServerZipResource

SERVER_URL = "https://github.com/elixir-lsp/elixir-ls/releases/download/v0.9.0/elixir-ls.zip"
SERVER_HASH = "aa3c990363a35d3673f11a2f098d902bdab97aecc0980b7de3bf84330b5254f3"
SERVER_VERSION = "0.9.0"

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
                                             asset_hash=SERVER_HASH,
                                             executables=SERVER_EXECUTABLES)
        return cls.__server
