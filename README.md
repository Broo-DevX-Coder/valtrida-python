# Valtrida

Valtrida is a local-first desktop application for trading and monitoring markets on **Binance**, built with **Python** and **PySide2 (Qt for Python)**.

It runs entirely on your own machine: your Binance API keys are encrypted and stored locally, market data streams over WebSocket/REST directly from Binance, and no data is sent to any third-party server operated by this project.

## Features

- **Live market data** — real-time order book and candlestick charts per trading pair, powered by `pyqtgraph`.
- **Wallet overview** — view your Binance spot balances, available/frozen amounts, and a simple portfolio breakdown.
- **Markets browser** — search and browse tradable pairs, open per-coin detail windows.
- **Local, encrypted accounts** — each user profile is protected with a password; API secrets are encrypted at rest with AES-GCM (PBKDF2-derived key, 200,000 iterations, SHA-256).
- **Dark & light themes** — a single source-of-truth color palette drives both QSS (Qt widget styling) and CSS (used in embedded HTML/QtWebEngine views).
- **Event-driven core** — a small pub/sub messaging system (`QueueStream`) decouples networking, UI, error handling, and logging.

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | PySide2 (Qt for Python) |
| Charts | pyqtgraph |
| Exchange | Binance REST + WebSocket API (via `python-binance` / `uniquant`, see `reqirments.txt`) |
| Concurrency | Python `threading`, custom async/task controller |
| Local storage | Flat encrypted files under `~/.valtrida/` |
| Crypto | `cryptography` (AES-GCM, PBKDF2-HMAC-SHA256) |

## Project Layout

```
streams.txt           Authoritative reference for the internal event/stream schema
Program/              The folder that contain all program files and folders bellow

index.py             Application entry point
prepare.py            Bootstrap: folders, config, plugins, pre-flight checks
config.py             Global runtime configuration (color mode, etc.)
API/                  Binance REST/market data access layer
base/                 Shared registries and utilities (charts, tool bar, user data, files/folders)
core/                 Application core: async controller, error handling, logging, folder setup
charts/               Chart widgets (candlestick chart, order book)
windows/              Qt windows/screens, including windows/tool_bar/ for the navigation bar
user/                 Authentication, local encryption, login/registration UI
Styles/               QSS/CSS stylesheets, icons, light/dark theme mapping
```

## Documentation

Full developer documentation — one page per source file, plus architecture notes — lives in [`DOCS/`](DOCS/README.md).

- [`DOCS/README.md`](DOCS/README.md) — documentation index
- [`DOCS/ARCHITECTURE.md`](DOCS/ARCHITECTURE.md) — how the app fits together (streams, registries, controller, storage layout)
- [`USAGE.md`](USAGE.md) — running the app and day-to-day usage
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to contribute, code conventions, known quirks

## Quick Start

```bash
pip install -r reqirments.txt   # note: filename is "reqirments.txt" (existing typo in the repo)
cd Program
python index.py
```

See [`USAGE.md`](USAGE.md) for full setup instructions, including creating your first local account and connecting a Binance API key.

## Status & Known Issues

This is a personal/hobby project, not a commercial product. See [`DOCS/ARCHITECTURE.md`](DOCS/ARCHITECTURE.md#known-issues) for a list of known rough edges (e.g. a hardcoded local file path in `Styles/qss.py`, unused plugin scaffolding).

## License

No license file is currently included in this repository. Treat the code as "all rights reserved" by the author unless a `LICENSE` file is added.
