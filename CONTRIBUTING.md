# Contributing to Valtrida

Thanks for your interest in contributing! This document explains how the codebase is organized, the conventions it follows, and things to be aware of before making changes.

## Getting Set Up

```bash
pip install -r reqirments.txt
python index.py
```

See [`USAGE.md`](USAGE.md) for full run instructions and [`DOCS/ARCHITECTURE.md`](DOCS/ARCHITECTURE.md) for how the pieces fit together.

## Project Structure

Read [`DOCS/README.md`](DOCS/README.md) for a full per-file index. At a high level:

- `API/` — talks to Binance (REST market data, account data).
- `base/` — shared, import-cycle-free registries and utilities used across the app.
- `core/` — cross-cutting concerns: the event streams, the async/thread/session controller, error handling, logging, and local folder setup.
- `charts/` — pyqtgraph-based chart widgets.
- `windows/` — Qt windows/screens, with `windows/tool_bar/` for the nav bar tabs.
- `user/` — authentication, local encryption of credentials, login/registration widgets.
- `Styles/` — QSS/CSS stylesheets, base64-embedded icons, and the dark→light color mapping.

## Architecture Ground Rules

Before changing core plumbing, read [`DOCS/ARCHITECTURE.md`](DOCS/ARCHITECTURE.md) in full. The two most important patterns to preserve:

1. **Event-driven communication via `QueueStream`** (`base/utils.py`, `core/async_controller.py`). Modules that need to talk to each other (e.g. a network thread pushing new price data to the UI) should publish/subscribe through the existing global streams (`SystemStream`, `UserStream`, `ErrorsStream`, `LogsStream`) rather than importing each other directly and calling methods synchronously. `streams.txt` is the authoritative schema for what event names and payloads exist — update it whenever you add or change an event.
2. **Registries in `base/` to avoid circular imports** (`base/charts.py`, `base/tool_bar.py`, `base/user_data.py`). These modules exist specifically so that windows, charts, and tool bar tabs can register themselves without `windows/`, `charts/`, and `core/` importing each other directly. If you're tempted to import a window module from inside `core/` (or vice versa), check whether a registry pattern should be used instead.

## Coding Conventions

- The codebase currently contains some existing identifier typos (e.g. `orderbook_initialyze`, `secreat`, `rigister`, `shart`, `nessary`) and one misspelled filename (`reqirments.txt` instead of `requirements.txt`). **Do not silently "fix" these** in unrelated commits — renaming a public identifier or file is a breaking change that should be its own reviewed PR, since other code and possibly external scripts may depend on the current names.
- Match the existing style within a file rather than introducing a new one (e.g. Arabic comments appear in a few style-related files — preserve them, don't remove them incidentally).
- Keep networking/blocking calls off the Qt main thread; use the existing `AsyncController` thread-tracking facilities in `core/async_controller.py` rather than spawning untracked `threading.Thread` instances, so they are properly joined/stopped on shutdown.

## Known Issues / Things to Be Careful With

- **Hardcoded absolute path**: `Styles/qss.py` references `/home/broo-dev/.valtrida/ASSETS/icons/svg/arrow-down.svg` for a dropdown arrow icon. This only resolves on the original author's machine. If you're fixing this, prefer resolving the path via `base/files_folders.py` (which already exposes `ASSETS_ICONS_SVG`) or embedding the icon as base64 like the rest of `Styles/icons.py` does.
- **Unused plugin scaffolding**: `prepare.py` references a `plugins_manager` concept and `core/folders.py` / `base/files_folders.py` define a `PLUGINS_DIR` / `MORE_PACKAGES`, but there is no actual plugin loader implemented yet. Don't assume a plugin system exists at runtime.
- **`USER_OFFICIAL_ACCOUNT_INFO`** (`base/user_data.py`) hints at future premium/cloud-account features that aren't built out — treat it as a placeholder, not a working feature.
- **Filename typo**: `reqirments.txt` is the actual, in-use filename. Renaming it to `requirements.txt` would be a reasonable improvement but must update every reference to it (docs, CI, README) in the same change.

## Security Notes

- User passwords/secrets are never stored in plaintext. `user/local_cypher.py` encrypts Binance API secrets with AES-GCM using a key derived via PBKDF2-HMAC-SHA256 (200,000 iterations) from the user's local password. Any change to this flow should preserve or upgrade (never downgrade) these parameters, and should include a migration path for existing encrypted files.
- Never log API keys/secrets or decrypted credentials — check `core/logs.py` and `core/errors.py` usage sites if you add new logging around auth code.

## Submitting Changes

1. Keep changes focused — one concern per change (e.g. don't mix a typo rename with a feature).
2. If you add a new event to the stream system, update `streams.txt`.
3. If you add a new source file, add a corresponding page under `DOCS/` (mirroring the existing structure) and link it from `DOCS/README.md`.
4. Manually verify the app still launches (`python index.py`) and the screens you touched still render and function, since there is no automated UI test suite currently in the project.
