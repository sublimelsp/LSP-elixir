import hashlib
import os
import shutil
import sublime

from LSP.plugin.core import logging
from LSP.plugin import AbstractPlugin
from sublime_lib import ActivityIndicator
from urllib.request import urlretrieve
from zipfile import ZipFile

SERVER_URL = "https://github.com/elixir-lsp/elixir-ls/releases/download/v0.6.0/elixir-ls.zip"
SERVER_HASH = "2784cf0964ec0723b46ab51edc81f84914b4fd5f6687a00822edd12bb1be6c71"
SERVER_VERSION = "0.6.0"

IS_WINDOWS = sublime.platform() == "windows"

DEAFULT_SETTINGS = {
    'env': {},
    'experimental_capabilities': {},
    'languages': [],
    'initializationOptions': {},
    'settings': {},
}


def log_debug(msg):
    logging.debug("lsp-elixir: {}".format(msg))


def is_elixir_installed():
    return shutil.which('elixir') is not None


def get_cache_path():
    cache_path = os.path.join(sublime.cache_path(), __package__)
    os.makedirs(cache_path, exist_ok=True)
    return cache_path


def get_server_dir(version):
    return os.path.join(get_cache_path(), "server", version)


def get_server_exec():
    """Returns path to the server executable (it may not exist)."""
    exe = "language_server.bat" if IS_WINDOWS else "language_server.sh"
    return os.path.join(get_server_dir(SERVER_VERSION), exe)


def is_valid_hash(path, expected):
    with open(path, "rb") as f:
        calculated = hashlib.sha256(f.read()).hexdigest()
        return calculated == expected


def unpack_server(zip_file):
    if not is_valid_hash(zip_file, SERVER_HASH):
        log_debug("Invalid hash, aborting")
        return

    target_dir = get_server_dir(SERVER_VERSION)
    os.makedirs(target_dir, exist_ok=True)
    log_debug("Unpacking server to: {}".format(target_dir))

    with ZipFile(zip_file, "r") as f:
        f.extractall(target_dir)

    # ZipFile removes permissions, make server executable
    if not IS_WINDOWS:
        os.chmod(os.path.join(target_dir, "language_server.sh"), 0o755)
        os.chmod(os.path.join(target_dir, "launch.sh"), 0o755)

    log_debug("Server installed")


def download_server():
    log_debug("Downloading server from {}".format(SERVER_URL))
    target = sublime.active_window()
    label = "Downloading Elixir language server binary"

    with ActivityIndicator(target, label):
        try:
            tmp_file, _ = urlretrieve(SERVER_URL)
            unpack_server(tmp_file)
            os.unlink(tmp_file)
        except Exception as ex:
            log_debug("Failed downloading server: {}".format(ex))


def delete_server():
    target_dir = get_server_dir(SERVER_VERSION)
    log_debug("Deleting server from {}".format(target_dir))
    shutil.rmtree(target_dir, ignore_errors=True)


def is_server_downloaded():
    return os.path.exists(get_server_exec())


class LspElixirPlugin(AbstractPlugin):
    @classmethod
    def name(cls):
        return "elixir"

    @classmethod
    def configuration(cls):
        config = {
            "enabled": True,
            "command": [get_server_exec()],
        }
        config.update(DEAFULT_SETTINGS)

        user_configs, file_path = super().configuration()
        for key, value in config.items():
            if not user_configs.has(key):
                user_configs.set(key, value)

        return user_configs, file_path

    @classmethod
    def needs_update_or_installation(cls):
        return not is_server_downloaded()

    @classmethod
    def install_or_update(cls):
        download_server()

    def on_pre_server_command(self, command, done):
        if command['command'].startswith('editor.action'):
            logging.debug("lsp-elixir: intercepted command {}".format(command))
            done()
            return True
        return False


def plugin_unloaded():
    """Called when the plugin is disabled or removed."""
    if is_server_downloaded():
        delete_server()
