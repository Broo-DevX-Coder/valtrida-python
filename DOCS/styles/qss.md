# `Styles/qss.py`

**Role:** `QSS` — a dict of four named Qt stylesheet strings (`"BINANCE"`, `"MAIN_W_TOOL_BAR"`, `"POPUP_W"`, `"AUTH_TOOL_BAR"`), each applied via `setStyleSheet(...)` to different native Qt widget trees across the app (as opposed to `Styles/css.py`, which styles the embedded web-view HTML pages).

## `QSS["BINANCE"]`

The main app-wide Qt widget theme — a dark Binance-inspired palette applied broadly (`AuthMain`, `LoggingWidget`, `RegisterViaBinanceAPI`, `OverlayPopup`, chart windows, order book windows, etc.). Styles `QWidget`, `QPushButton` (including special `#buyButton`/`#sellButton` object-name variants), `QLineEdit`, `QLabel`, `QComboBox`, `QTabWidget`/`QTabBar`, `QScrollBar`, `QTableWidget`/`QHeaderView`, and `QListWidget`.

**Known issue:** the `QComboBox::down-arrow` rule references an **absolute local filesystem path** — `url(/home/broo-dev/.valtrida/ASSETS/icons/svg/arrow-down.svg)` — which is almost certainly a developer's own machine path baked in by accident. This means the combo-box dropdown arrow icon will fail to load (rendering with Qt's default arrow instead, or no arrow, depending on Qt version) on any machine other than that original developer's, including this deployment. This is flagged as a **known issue** in [`../ARCHITECTURE.md`](../ARCHITECTURE.md) as well. Contrast with `QSS["POPUP_W"]`'s equivalent rule, which correctly uses a relative path (`url(./Styles/icons/arrow-down.svg)`).

## `QSS["MAIN_W_TOOL_BAR"]`

Styles the bottom navigation tool bar in `windows/main.py`'s `MainWindow` — a rounded gray bar (`#7a7a7a`) with transparent buttons that highlight yellow (`#FCD535`/`#F0B90B`, Binance's brand yellow) on hover/press/checked state, plus a matching `QToolTip` style.

## `QSS["POPUP_W"]`

A stylesheet scoped entirely under `QWidget#popupWindow` (i.e. it only applies to a widget with that specific `objectName`) — styles buttons (including buy/sell variants in Binance's green/red, `#0ECB81`/`#F6465D`), line edits, combo boxes, and scrollbars for a popup context. **Note:** grepping the rest of the codebase, no widget currently sets `objectName("popupWindow")` — this stylesheet's selector scope means it is **not currently applied to anything** (the actual popups, `OverlayPopup`/`AuthMain`, use `QSS["BINANCE"]` instead). This looks like leftover/planned styling for a popup pattern that was superseded by `OverlayPopup`'s current unscoped-`QSS["BINANCE"]` approach.

## `QSS["AUTH_TOOL_BAR"]`

Scoped under `QWidget#options_bar` — styles the Login/API-Register tab-switcher buttons in `user/window.py`'s `AuthMain` (which does set `self.options_bar.setObjectName("options_bar")`, so this one **is** actively used, unlike `POPUP_W`).

## Related

- [`init.md`](init.md) — `DARK_TO_LIGHT_COLORS`.
- [`mods.md`](mods.md) — converts all four of these strings to light mode when `COLOR_MODE == "light"`.
- [`../ARCHITECTURE.md`](../ARCHITECTURE.md) — Known Issues section, absolute-path arrow icon.
- [`../windows/main.md`](../windows/main.md), [`../user/window.md`](../user/window.md) — primary consumers.
