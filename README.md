# LSP-elixir

Elixir support for Sublime Text's LSP plugin provided through
[ElixirLS](https://github.com/elixir-lsp/elixir-ls/).

Requires **Elixir 1.12.0+** and **OTP 22+**. A good way of installing these is
using the [ASDF package manager](https://github.com/asdf-vm/asdf) with the
[asdf-elixir plugin](https://github.com/asdf-vm/asdf-elixir). On Windows,
[Scoop](https://scoop.sh/) is a solid option. `scoop install elixir` or 
`scoop install elixir@1.14.1-otp-25`.

## Installation

Install the following packages in Sublime Text:

* [Elixir](https://packagecontrol.io/packages/Elixir) or [Elixir Sublime Syntax](https://packagecontrol.io/packages/ElixirSyntax) - Elixir syntax support
* [LSP](https://packagecontrol.io/packages/LSP) - Base LSP package
* [LSP-elixir](https://packagecontrol.io/packages/LSP-elixir) - This plugin

## Configuration

Defaults can be edited by selecting `Preferences: LSP-elixir Settings` from the
command palette.

### Format on save

To format your code on save add the following setting to your syntax-specific settings (Elixir in this case) and/or project files:

```json
{
  "lsp_format_on_save": true
}
```

## Upgrade to latest version

For developers! To upgrade this library to use the latest version of elixir-ls,
run:

```
./scripts/update.py
```

This will update the server info in `plugin.py` to match the latest [release of
elixir-ls](https://github.com/elixir-lsp/elixir-ls/releases).
