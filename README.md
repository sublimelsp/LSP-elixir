# LSP-elixir

Elixir support for Sublime Text's LSP plugin provided through
[ElixirLS](https://github.com/elixir-lsp/elixir-ls/).

Requires **Elixir 1.10.0+** and **OTP 22+**. A good way of installing these is
using the [ASDF package manager](https://github.com/asdf-vm/asdf) with the
[asdf-elixir plugin](https://github.com/asdf-vm/asdf-elixir).

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
