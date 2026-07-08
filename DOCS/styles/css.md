# `Styles/css.py`

**Role:** `CSS["MAIN"]` — the single shared CSS stylesheet string injected into every embedded `QWebEngineView` HTML page in the app (Home, Markets, Wallet, OneCoin). Written once here and reused everywhere, rather than each page defining its own styles.

## Structure

A plain triple-quoted CSS string (not a CSS-in-JS framework, no preprocessing/minification), organized by comment-delimited sections matching the different pages/components it's shared across:

- **Base Styles / Scrollbar** — dark background (`#0d0f1a`) with a subtle dotted radial-gradient texture, custom WebKit scrollbar styling (relevant since `QWebEngineView` is Chromium-based and does respect `::-webkit-scrollbar` rules).
- **Header / Container / Card** — the generic page-header and card layout used across Home/Wallet/Markets/OneCoin.
- **Trade Header / Status / Trade Info / Profit-Loss / Table** — styling for elements that appear only in the currently-commented-out "Open Orders"/"Recent Trades" sections of `Home`/`Wallet` (see those files' docs) — so a fair amount of this stylesheet is currently dead CSS with no rendered element to apply to, kept in anticipation of that markup being un-commented later.
- **Buttons / Pairs List / Pair Cell** — the wallet asset-list styling (`.pairs-list`, `.pair`, `.available`/`.frozen` color classes) consumed by `windows/tool_bar/wallet.py`.
- **Market CSS** (`.search-bar`, `.coins-grid`, `.coin-card`, `.pen`) — the Markets tab's coin grid, consumed by `windows/tool_bar/markets.py`.
- **Coin Header / Pen Button / Login Button** — used by `windows/coin.py`'s `OneCoin` page and the login-button markup shared by `Home`/`Wallet`.

## Notable choices

- All colors here are dark-theme hardcoded hex literals; every one of them **must** have a matching entry in `Styles/__init__.py`'s `DARK_TO_LIGHT_COLORS` for light mode to render correctly (see [`init.md`](init.md)) — `Styles/mods.py` performs a raw string substitution over this entire blob when `COLOR_MODE == "light"`.
- The brand accent green `#4aa96c` (scrollbar thumb, header `h2`, profit text, buttons) is the same accent used throughout `Styles/qss.py`'s Qt widget styling — the two files aren't shared/derived from a single source of truth for that color (it's independently hardcoded in both), so keeping them visually consistent is a manual responsibility if the palette is ever revised.

## Related

- [`init.md`](init.md) — `DARK_TO_LIGHT_COLORS`, the light-mode conversion table this stylesheet depends on.
- [`mods.md`](mods.md) — applies `change_to_light_mode` to `CSS["MAIN"]` at import time when `COLOR_MODE == "light"`.
- [`../windows/tool_bar/home.md`](../windows/tool_bar/home.md), [`../windows/tool_bar/markets.md`](../windows/tool_bar/markets.md), [`../windows/tool_bar/wallet.md`](../windows/tool_bar/wallet.md), [`../windows/coin.md`](../windows/coin.md) — the pages that embed this stylesheet.
