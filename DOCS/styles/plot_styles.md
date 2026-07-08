# `Styles/plot_styles.py`

**Role:** Theming for `pyqtgraph`-based charts (as opposed to the KLineCharts/Chart.js web-based charts elsewhere in the app) — sets global `pyqtgraph` config options and provides helper classes for styling chart cursor labels and candlestick colors. Note: as of the code read this session, no chart file under `charts/` currently imports from this module (both `SimpleCandelsChart` and `OrderBook` render entirely via `QWebEngineView`/JS, not `pyqtgraph`) — this appears to be either legacy code from an earlier `pyqtgraph`-based charting approach, or infrastructure prepared for a not-yet-built native chart widget.

## `COL(x)` lambda

```python
COL = lambda x: DARK_TO_LIGHT_COLORS[x] if x in DARK_TO_LIGHT_COLORS.keys() and COLOR_MODE == "light" else x
```

A **per-call, lazy** light-mode color lookup — unlike `Styles/mods.py`'s approach (which rewrites stylesheet strings once at import time), this module re-checks `COLOR_MODE` and looks up the replacement color **every time `COL(...)` is called**. Functionally equivalent for a static `COLOR_MODE` (set once from config at startup and not changed at runtime), but architecturally distinct — this is the only place in the styling system that does the light-mode substitution as a live function call rather than a one-time string rewrite.

## `binance_charts_theme()`

Called immediately at module import time (not gated behind a function call from elsewhere) — sets `pyqtgraph`'s global `background`/`foreground`/`antialias` config options via `pg.setConfigOption(...)`. Because `pyqtgraph` config options are global/module-level state, importing this file anywhere has the side effect of setting these options for **any** `pyqtgraph` widget created afterward in the process, not just ones explicitly tied to this module.

## `GlobalCursor`

A namespace class (not instantiated — methods take `widget` as an explicit first parameter rather than `self`) for styling `pyqtgraph` text/label items used as chart cursors:
- **`set_label_pos2(widget, value_v, value_diciamles=2)`** *(existing typo "diciamles" for "decimals", kept as-is)* — sets a small rounded HTML label showing a single value.
- **`set_label_pos(widget, date_str, value_n, value_v, value_diciamles=2, auther=None)`** *(existing typo "auther", likely meant as an "author"/extra-label parameter, kept as-is)* — a richer label showing a date and a named value, with an optional extra `auther` string appended.

## `CandalsChart`

Another namespace class:
- **`set_candals_color()`** *(existing typo "candals" for "candles", kept as-is)* — returns Binance-style candle colors (`#0ECB81` up / `#F6465D` down) as a dict — note the inline Arabic comments describing these as "blue/purple" (`أزرق صاعد` / `بنفسجي هابط`) don't match the actual green/red hex values used, an internal comment inconsistency (harmless, cosmetic).
- **`set_price_label(widget, price, up=True, price_diciamles=2)`** — styles a floating price label matching the up/down candle color.

## Related

- [`init.md`](init.md) — `DARK_TO_LIGHT_COLORS`.
- [`mods.md`](mods.md) — the alternate, import-time light-mode conversion approach used for QSS/CSS.
- [`../root/config.md`](../root/config.md) — `COLOR_MODE`.
