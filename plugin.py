import hashlib
import json
import os
import shutil
import sublime

from LSP.plugin.core import logging
from LSP.plugin.core.handlers import LanguageHandler
from LSP.plugin.core.settings import read_client_config
from sublime_lib import ActivityIndicator
from threading import Thread
from urllib.request import urlretrieve
from zipfile import ZipFile
from collections import namedtuple

Server = namedtuple("Server", ["url", "hash", "version"])

IS_WINDOWS = sublime.platform() == "windows"


# Keys to read and their fallbacks.
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
    server = get_server_info()
    exe = "language_server.bat" if IS_WINDOWS else "language_server.sh"
    return os.path.join(get_server_dir(server.version), exe)


def is_valid_hash(path, expected):
    with open(path, "rb") as f:
        calculated = hashlib.sha256(f.read()).hexdigest()
        return calculated == expected


def unpack_server(zip_file, target_dir):
    log_debug("Unpacking server to: {}".format(target_dir))
    os.makedirs(target_dir, exist_ok=True)

    with ZipFile(zip_file, "r") as f:
        f.extractall(target_dir)

    # ZipFile removes permissions, make server executable
    if not IS_WINDOWS:
        os.chmod(os.path.join(target_dir, "language_server.sh"), 0o755)
        os.chmod(os.path.join(target_dir, "launch.sh"), 0o755)

    log_debug("Server downloaded.")


def download_server():
    server = get_server_info()
    target_dir = get_server_dir(server.version)
    log_debug("Downloading server from {}".format(server.url))

    def _done(tmp_file):
        if is_valid_hash(tmp_file, server.hash):
            log_debug("Server hash is valid")
            unpack_server(tmp_file, target_dir)
        else:
            log_debug("Invalid hash, aborting")

        os.unlink(tmp_file)

    def _download():
        target = sublime.active_window()
        label = "Downloading Elixir language server binary"
        with ActivityIndicator(target, label):
            tmp_file, _ = urlretrieve(server.url)
            _done(tmp_file)

    thread = Thread(target=_download)
    thread.start()


def delete_server():
    server = get_server_info()
    target_dir = get_server_dir(server.version)
    log_debug("Deleting server from {}".format(server.url))
    shutil.rmtree(target_dir, ignore_errors=True)


def get_server_info():
    """Load server data from server.json"""
    filename = "Packages/{}/server.json".format(__package__)
    server = json.loads(sublime.load_resource(filename))
    return Server(server["url"], server["sha256"], server["version"])


def is_server_downloaded():
    return os.path.exists(get_server_exec())


class LspElixirPlugin(LanguageHandler):
    @property
    def name(self):
        return __package__.lower()

    @property
    def config(self):
        config = {
            "enabled": True,
            "command": [get_server_exec()],
        }

        filename = '{}.sublime-settings'.format(__package__)
        settings = sublime.load_settings(filename)
        for key, default in DEAFULT_SETTINGS.items():
            config[key] = settings.get(key, default)

        return read_client_config(self.name, config)

    def on_start(self, window) -> bool:
        if not is_elixir_installed():
            sublime.status_message(
                "Please install Elixir for LSP-elixir plugin to work.")
            return False

        if not is_server_downloaded():
            sublime.status_message(
                "Elixir Language Server not yet downloaded.")
            return False

        return True


def plugin_loaded():
    if not is_server_downloaded():
        download_server()


def plugin_unloaded():
    """Called when the plugin is disabled or removed."""
    if is_server_downloaded():
        delete_server()
