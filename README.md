# Rust Server Toolkit

A Codex plugin for Facepunch Rust server administrators: server setup, Oxide/Carbon C# plugin repair, and JSON configuration workflows.

**0.1.0-alpha.2 — early alpha.** Includes three Codex skills and a read-only JSON checker. See the [Docker validation report](docs/DOCKER-VALIDATION.md) for tested behavior and limitations.

## Features

| Skill | Purpose |
| --- | --- |
| `rust-server-setup` | Set up, update, and diagnose servers on Linux, Windows, Docker, or hosting panels |
| `rust-plugin-repair` | Investigate compiler errors, load failures, and hook exceptions; prepare source fixes |
| `rust-plugin-config` | Identify settings from source, prepare changes, validate JSON, and plan deployment |

This is a skills-based plugin that guides Codex through administration tasks. It does not include a dedicated RCON client, management daemon, or automatic C# build environment. Actual operations require shell/file access and, where applicable, SSH or hosting-panel access. The JSON helper requires Python 3.10+ and no third-party packages.

## Installation

Add this repository as a Codex marketplace:

```sh
codex plugin marketplace add miyagawayuu/rust-server-toolkit
codex plugin add rust-server-toolkit@personal
```

The catalog currently uses the scaffold's default identifier, `personal`. If another marketplace already uses that identifier, inspect the sources shown by Codex before proceeding; do not overwrite an unrelated catalog.

For local development, register the repository root:

```sh
codex plugin marketplace add /absolute/path/to/rust-server-toolkit
codex plugin add rust-server-toolkit@personal
```

After installation, start a new task and select the plugin. Availability depends on your Codex version and organization policy.

## Example prompts

- "Set up Rust with Carbon on my Ubuntu VPS. Start by preparing the startup configuration."
- "Review this C# plugin and log, then fix the Oxide compilation error."
- "Use this plugin's source to prepare a configuration change that doubles gathering rates."

You can prepare changes without a live server connection by providing the configuration and plugin source or documentation. Remove passwords, tokens, and private webhook URLs from shared logs.

## JSON validation

Run from the repository root:

```sh
python plugins/rust-server-toolkit/skills/rust-plugin-config/scripts/config_check.py check Plugin.json
python plugins/rust-server-toolkit/skills/rust-plugin-config/scripts/config_check.py diff original.json candidate.json
python -m unittest discover -s tests -v
python scripts/package.py
```

The checker never changes its input files and omits values from diff output. Key names may still contain private information. Valid JSON does not establish compatibility with a plugin's configuration schema.

## Development and distribution

- [Release notes and release process](docs/RELEASE.md)
- [Evaluation scenarios](docs/EVALUATION.md)
- [Docker tests](tests/docker/README.md)
- [Privacy](PRIVACY.md)
- License: MIT. Third-party Rust plugins and server binaries are not bundled.

This is an independent project, not an official Facepunch, Oxide, Carbon, or OpenAI product.
