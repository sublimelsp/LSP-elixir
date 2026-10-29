#!/usr/bin/env python3
"""
Update SERVER_SHA256 in plugin.py to the hash of the elixir-ls release that SERVER_VERSION
points to. Renovate updates SERVER_VERSION, and the update-hash workflow runs this script on its
pull requests.
"""

from __future__ import annotations

import hashlib
import re
import urllib.request

SERVER_URL = (
    "https://github.com/elixir-lsp/elixir-ls/releases/download/v{version}/elixir-ls-v{version}.zip"
)


def main():
    with open("plugin.py") as f:
        content = f.read()

    version = get_value(content, "SERVER_VERSION")
    current_hash = get_value(content, "SERVER_SHA256")
    latest_hash = calculate_hash(SERVER_URL.format(version=version))

    print(f"SERVER_VERSION = {version}")
    print(f"SERVER_SHA256 = {latest_hash}")

    if current_hash == latest_hash:
        print("✓ The hash is up to date")
        return

    content = re.sub(
        r"^SERVER_SHA256 = .+",
        f'SERVER_SHA256 = "{latest_hash}"',
        content,
        flags=re.MULTILINE,
    )

    with open("plugin.py", "w") as f:
        f.write(content)

    print("✓ Updated the hash")


def get_value(content, name):
    m = re.search(rf'^{name} = "([^"]+)"', content, flags=re.MULTILINE)
    if not m:
        raise Exception(f"Cannot find {name} in plugin.py")
    return m.group(1)


def calculate_hash(url):
    print(f"<-- GET {url}")
    with urllib.request.urlopen(url) as response:
        return hashlib.sha256(response.read()).hexdigest()


if __name__ == "__main__":
    main()
