# Valtrida Developer Documentation

This folder contains one documentation page per source file in the project, plus a high-level architecture overview. It is meant to reflect the **current state of the code**, not the original design intent — quirks and known issues are called out explicitly rather than hidden.

Start here:

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — how the pieces fit together: the event stream system, registries, the async controller, and local storage layout. Read this first.

Then browse by area:

## Root

- [`root/index.md`](root/index.md) — `index.py`, the application entry point
- [`root/prepare.md`](root/prepare.md) — `prepare.py`, startup/bootstrap logic
- [`root/config.md`](root/config.md) — `config.py`, global runtime configuration
- [`root/streams.md`](root/streams.md) — `streams.txt`, the event/stream schema reference
- [`root/reqirments.md`](root/reqirments.md) — `reqirments.txt`, dependencies

## `API/` — Binance access layer

- [`api/init.md`](api/init.md) — `API/__init__.py`
- [`api/market.md`](api/market.md) — `API/market.py`, public market data
- [`api/b_accont.md`](api/b_accont.md) — `API/b_accont.py`, authenticated account access

## `base/` — shared registries & utilities

- [`base/charts.md`](base/charts.md) — `base/charts.py`, chart-type registry
- [`base/tool_bar.md`](base/tool_bar.md) — `base/tool_bar.py`, tool bar tab registry
- [`base/user_data.md`](base/user_data.md) — `base/user_data.py`, in-memory user/session data
- [`base/utils.md`](base/utils.md) — `base/utils.py`, `QueueStream`/`QueueStreamChannel` pub/sub primitives
- [`base/files_folders.md`](base/files_folders.md) — `base/files_folders.py`, path constants
- [`base/init.md`](base/init.md) — `base/__init__.py`

## `core/` — application core

- [`core/async_controller.md`](core/async_controller.md) — `core/async_controller.py`, global streams + `AsyncController`
- [`core/errors.md`](core/errors.md) — `core/errors.py`, error stream consumers/handling
- [`core/folders.md`](core/folders.md) — `core/folders.py`, local data directory setup
- [`core/logs.md`](core/logs.md) — `core/logs.py`, logging stream consumer
- [`core/pop_messages.md`](core/pop_messages.md) — `core/pop_messages.py`, user-facing popup notifications
- [`core/init.md`](core/init.md) — `core/__init__.py`

## `charts/` — chart widgets

- [`charts/candels_shart.md`](charts/candels_shart.md) — `charts/candels_shart.py`, candlestick chart widget
- [`charts/order_book.md`](charts/order_book.md) — `charts/order_book.py`, order book widget
- [`charts/init.md`](charts/init.md) — `charts/__init__.py` (empty)

## `windows/` — screens

- [`windows/main.md`](windows/main.md) — `windows/main.py`, main application window
- [`windows/coin.md`](windows/coin.md) — `windows/coin.py`, per-coin detail window
- [`windows/chart_popup.md`](windows/chart_popup.md) — `windows/chart_popup.py`, standalone chart popup window
- [`windows/init.md`](windows/init.md) — `windows/__init__.py` (empty)
- [`windows/tool_bar/home.md`](windows/tool_bar/home.md) — `windows/tool_bar/home.py`
- [`windows/tool_bar/markets.md`](windows/tool_bar/markets.md) — `windows/tool_bar/markets.py`
- [`windows/tool_bar/wallet.md`](windows/tool_bar/wallet.md) — `windows/tool_bar/wallet.py`
- [`windows/tool_bar/init.md`](windows/tool_bar/init.md) — `windows/tool_bar/__init__.py` (empty)

## `user/` — authentication & local security

- [`user/local_cypher.md`](user/local_cypher.md) — `user/local_cypher.py`, AES-GCM/PBKDF2 encryption of credentials
- [`user/window.md`](user/window.md) — `user/window.py`, authentication window
- [`user/widgets/login.md`](user/widgets/login.md) — `user/widgets/login.py`
- [`user/widgets/register_via_binance_api.md`](user/widgets/register_via_binance_api.md) — `user/widgets/register_via_binance_api.py`
- [`user/init.md`](user/init.md) — `user/__init__.py` (empty)

## `Styles/` — theming

- [`styles/css.md`](styles/css.md) — `Styles/css.py`, CSS used in embedded HTML views
- [`styles/qss.md`](styles/qss.md) — `Styles/qss.py`, Qt widget stylesheets (QSS)
- [`styles/icons.md`](styles/icons.md) — `Styles/icons.py`, base64-embedded icon assets
- [`styles/mods.md`](styles/mods.md) — `Styles/mods.py`, dark→light stylesheet transformation
- [`styles/plot_styles.md`](styles/plot_styles.md) — `Styles/plot_styles.py`, pyqtgraph chart theming
- [`styles/init.md`](styles/init.md) — `Styles/__init__.py`, dark→light color map

## Root-level guides

- [`../README.md`](../README.md) — project overview
- [`../USAGE.md`](../USAGE.md) — running and using the app
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — contribution guidelines and conventions
