# Architecture Overview

Valtrida is a single-process PySide2 desktop application. This page explains the core architectural patterns that hold the codebase together, so you can navigate and extend it without re-deriving them from scratch.

## 1. Startup Flow

1. **`index.py`** is the entry point. It creates the `QApplication`, runs the bootstrap logic from `prepare.py`, and then shows the authentication window (`user/window.py`) or the main window (`windows/main.py`) depending on whether a valid local session exists.
2. **`prepare.py`** runs before any UI is shown. It ensures the local data directories exist (delegating to `core/folders.py` / `base/files_folders.py`), initializes configuration (`config.py`), and sets up the core event streams and the `AsyncController` (`core/async_controller.py`). It also references a `plugins_manager` concept that is **not actually implemented** in this repo — treat any plugin-related code paths as inert scaffolding, not a working feature.
3. **`config.py`** holds simple global runtime settings, most notably `COLOR_MODE` (`"dark"` or `"light"`), which `Styles/mods.py` reads at import time to decide whether to transform the stylesheets.

## 2. Event-Driven Core: `QueueStream`

Rather than having modules call each other's methods directly, Valtrida uses a lightweight publish/subscribe system defined in `base/utils.py`:

- **`QueueStreamChannel`** — a single named channel that holds subscriber callbacks and dispatches messages to them.
- **`QueueStream`** — a collection of channels; you publish to a channel by name and every subscriber callback registered on that channel is invoked.

On top of this primitive, `core/async_controller.py` defines **four global streams** that act as the app's nervous system:

| Stream | Purpose |
|---|---|
| `SystemStream` | System-level lifecycle events (app-wide signals, coordinated shutdown, etc.) |
| `UserStream` | User/session/account-related events (login, logout, account data updates) |
| `ErrorsStream` | Errors raised anywhere in the app are published here rather than thrown across module boundaries; `core/errors.py` subscribes and handles/logs/display them |
| `LogsStream` | Log messages are published here; `core/logs.py` subscribes and writes them out |

**`streams.txt`** at the repo root is the authoritative, human-maintained schema of what event names and payload shapes exist on these streams. When you add a new event or change a payload, update `streams.txt` in the same change — it is the single source of truth other contributors will read instead of grepping through every publisher/subscriber.

This pattern matters because it lets, e.g., a background network thread pushing new price ticks (`API/market.py`) notify a chart widget (`charts/candels_shart.py`) without either module importing the other directly — they only need to agree on a channel name and payload shape.

## 3. Avoiding Circular Imports: the `base/` Registries

Because windows need to know about charts, charts need to know about tool bar state, and the core needs to coordinate windows — a naive import graph would be circular. Valtrida avoids this with **registries** living in `base/`:

- **`base/charts.py`** — a registry that chart implementations register themselves into, so other code can look up "the chart for this context" without importing the concrete chart class/module directly.
- **`base/tool_bar.py`** — a registry for tool bar tabs/screens (`windows/tool_bar/home.py`, `markets.py`, `wallet.py`), so the main window can enumerate/mount tabs without importing each tab module in a fixed, tightly-coupled way.
- **`base/user_data.py`** — an in-memory holder for the current session's user/account data (including the placeholder `USER_OFFICIAL_ACCOUNT_INFO`, reserved for a possible future cloud/premium account concept that isn't implemented yet), so any module can read "who is logged in" without importing the auth module.

The rule of thumb: if you're about to import something from `windows/` or `charts/` into `core/` (or the reverse), check whether it should instead be mediated through one of these `base/` registries.

## 4. The `AsyncController`

`core/async_controller.py` defines an `AsyncController` responsible for tracking everything the app spins up during a session that needs coordinated cleanup:

- Open windows
- Background threads (e.g. WebSocket listener threads, polling threads)
- Scheduled/async tasks
- Open REST/HTTP sessions to Binance

Its `CRITICAL_STOP()` method is the single shutdown path: it stops tracked threads, closes tracked sessions, and closes tracked windows, so that closing the app (or a fatal error) doesn't leave orphaned network connections or threads running. New long-lived background work should register itself with the `AsyncController` rather than being spawned as an untracked `threading.Thread`.

## 5. Networking Layer (`API/`)

- **`API/market.py`** — public market data access (prices, candlesticks, order book) — does not require authentication.
- **`API/b_accont.py`** — authenticated account access (balances, orders) — requires a Binance API key/secret, supplied by the locally decrypted user credentials.

Both modules talk to Binance directly from the user's machine; there is no Valtrida-operated backend server in the loop.

## 6. Local Storage Layout

All persistent local state lives under `~/.valtrida/` (path constants centralized in `base/files_folders.py`, directory creation handled by `core/folders.py`):

```
~/.valtrida/
  data/
    users/          Per-user encrypted profile/credential files (see user/local_cypher.py)
  ASSETS/
    icons/
      ico/          .ico icon assets
      svg/          .svg icon assets
  (plugins dir reserved, unused — see Known Issues)
```

No data is written outside this directory, and no data is transmitted to any server other than Binance's own API endpoints.

## 7. Security Model

- Local accounts are protected by a password chosen by the user at registration time.
- Binance API secrets are encrypted before being written to disk using **AES-GCM**, with the encryption key derived from the user's password via **PBKDF2-HMAC-SHA256 with 200,000 iterations** (`user/local_cypher.py`).
- Decryption only happens in-memory after a successful local login; secrets are never logged (see conventions in `core/logs.py` / `core/errors.py`) and never transmitted anywhere except as part of signed requests directly to Binance.

## 8. Theming System

- **`Styles/qss.py`** — Qt Style Sheets (QSS) for native widgets, organized as named blocks (`BINANCE`, `MAIN_W_TOOL_BAR`, `POPUP_W`, `AUTH_TOOL_BAR`) applied to different windows/widgets.
- **`Styles/css.py`** — CSS used for any embedded HTML/rich-text content.
- **`Styles/icons.py`** — icons embedded as base64 strings (both `.svg` and `.ico` variants), avoiding a dependency on loose asset files at runtime for those icons.
- **`Styles/plot_styles.py`** — configures `pyqtgraph` global options and provides helper classes (`GlobalCursor`, `CandalsChart`) for consistent chart colors/labels.
- **`Styles/__init__.py`** — `DARK_TO_LIGHT_COLORS`, a single dict mapping every dark-theme color used across QSS/CSS/plot styling to its light-theme equivalent.
- **`Styles/mods.py`** — at import time, if `config.COLOR_MODE == "light"`, rewrites every dark color literal in the QSS/CSS strings to its light equivalent using `DARK_TO_LIGHT_COLORS`. This is a one-way string substitution, not a live-switchable theme — changing `COLOR_MODE` requires an app restart to take effect.

Because theming works by literal string substitution over color codes, **any new color introduced in a stylesheet must also be added to `DARK_TO_LIGHT_COLORS`** or it will not adapt to light mode.

## Known Issues

These are real, current issues in the codebase — documented here so they're not mistaken for bugs in your setup:

1. **Hardcoded absolute path** — `Styles/qss.py` (the `BINANCE` QSS block) references `/home/broo-dev/.valtrida/ASSETS/icons/svg/arrow-down.svg` for a combo box's dropdown arrow icon. This path only exists on the original author's development machine, so on any other machine the dropdown arrow icon will silently fail to load. Contrast this with the `POPUP_W` block in the same file, which uses a relative path (`./Styles/icons/arrow-down.svg`), and with `Styles/icons.py`, which already embeds an `arrow-down.svg` as base64 — either of those approaches would be more portable.
2. **Unimplemented plugin system** — `prepare.py` references a `plugins_manager`, and `core/folders.py` / `base/files_folders.py` define a `PLUGINS_DIR` and `MORE_PACKAGES` constant, but there is no plugin loader implemented anywhere in the repo. This is scaffolding for a feature that doesn't exist yet.
3. **Placeholder premium/cloud account concept** — `USER_OFFICIAL_ACCOUNT_INFO` in `base/user_data.py` suggests a future "official"/cloud-linked account tier, but nothing currently populates or reads it meaningfully.
4. **Misspelled dependency filename** — the dependencies file is named `reqirments.txt`, not `requirements.txt`. This is intentional in the sense that it's the actual filename in use — any tooling, CI, or documentation referencing dependencies must use the existing typo'd name until/unless it is deliberately renamed (with all references updated together).
5. **Miscellaneous identifier typos** — a handful of function/variable names in the codebase contain typos (e.g. `orderbook_initialyze`, `secreat`, `rigister`, `shart`, `nessary`). These are existing, in-use identifiers, not documentation errors — don't "correct" them incidentally while making unrelated changes.
