#!/usr/bin/env python3
"""
Upgrade plugin.py server info to the latest release of elixir-ls as seen here:
https://github.com/elixir-lsp/elixir-ls/releases
"""

import hashlib
import json
import os
import re
import urllib.request


def main():
    current_version = get_current_release_version()
    release = fetch_latest_release()
    latest_version = release["tag_name"].lstrip("v")

    print(f"Current version: {current_version}")
    print(f"Latest version: {latest_version}")

    if current_version == latest_version:
        print("✓ Using the latest version")
        return

    print("Update? [Y/n]")
    if input().strip().lower() not in ["", "y"]:
        print("Aborted.")
        return

    update_version(latest_version, release)

    with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
        print(f"version={latest_version}", file=gh_output)

    print(f"\n✓ Updated to {latest_version}")


def update_version(version, release):
    url = get_download_url(release)
    hash = calculate_hash(url)

    print(f"SERVER_VERSION = {version}")
    print(f"SERVER_URL = {url}")
    print(f"SERVER_SHA256 = {hash}")

    with open("plugin.py") as f:
        content = f.read()

    content = re.sub(r"^SERVER_VERSION.+", f'SERVER_VERSION = "{version}"', content, 0, re.MULTILINE)
    content = re.sub(r"^SERVER_URL.+", f'SERVER_URL = "{url}"', content, 0, re.MULTILINE)
    content = re.sub(r"^SERVER_SHA256.+", f'SERVER_SHA256 = "{hash}"', content, 0, re.MULTILINE)

    with open("plugin.py", "w") as f:
        f.write(content)


def get_download_url(release):
    for asset in release["assets"]:
        if asset["name"] == "elixir-ls.zip":
            return asset["browser_download_url"]
    raise Exception("Asset url not found")


def get_current_release_version():
    with open("plugin.py") as f:
        content = f.read()
        m = re.search(r'SERVER_VERSION = "([0-9.]+)"', content)
        if not m:
            raise Exception("Cannot find current version in plugin.py")
        return m.group(1)


def calculate_hash(url):
    response = http_get(url)
    hash_object = hashlib.sha256(response)
    return hash_object.hexdigest()


def fetch_latest_release():
    response = http_get("https://api.github.com/repos/elixir-lsp/elixir-ls/releases")
    releases = json.loads(response)

    for release in releases:
        if not release["draft"] and not release["prerelease"]:
            return release

    raise Exception("No release found")


def http_get(url):
    print(f"<-- GET {url}")
    with urllib.request.urlopen(url) as response:
        if response.status != 200:
            raise Exception(f"Failed loading data, got HTTP {response.status}")
        return response.read()


if __name__ == "__main__":
    main()
