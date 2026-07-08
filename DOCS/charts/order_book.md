# `charts/order_book.py`

**Role:** The order book widget — shown as two separate side-by-side windows (bids and asks), each a live-updating table, driven by `API/market.py`'s `SINGLE_API` (accessed here through the `CHOISED_SYMBOLS_CLASS` alias from `API/__init__.py`).

## `OrderBookSideWindow(QWidget)`

Represents **one side** (either `"bids"` or `"asks"`) of the order book as its own top-level window.

- Styled with `Styles.qss.QSS["BINANCE"]` plus an inline stylesheet override for the table (`background-color: black`, etc. — note this is a small deviation from the shared theme, hardcoded here rather than pulled from `Styles/qss.py`/`Styles/__init__.py`, meaning it will **not** be automatically converted to a light-theme color if `COLOR_MODE` is `"light"`).
- A 3-column `QTableWidget`: Price, Quantity (in the base asset), Quantity (in USD, computed as `price * qty`).
- **`update_side(levels)`** — takes a list of `(price, qty)` tuples, sorts them (ascending for asks — lowest ask first; descending for bids — highest bid first, matching how Binance's own UI orders each side), and repopulates the table via `_set_row`.
- **`_set_row(row, price, qty, cum, color)`** — formats price to `PRICE_DECIMALS` places and quantity/total to 4 decimal places; colors the price cell red (asks) or lime (bids).
- **`closeEvent`** — emits a `closed` Qt signal (so the parent `OrderBook` can react — see `_on_child_closed` below), unregisters from `AsyncController`, then calls the base class's `closeEvent`.

## `OrderBook`

The coordinating object — not a `QWidget` itself, but a plain Python object that owns and manages the pair of `OrderBookSideWindow` instances plus the polling task that feeds them.

### Construction

Takes `time_frame` (seconds between order book refreshes, default `1`) and `symbol` (default `"SOLUSDT"`). Sets `self.TIME_MS = time_frame * 1000`, creates a `CHOISED_SYMBOLS_CLASS(self.SYMBOL)` instance (currently `API.market.SINGLE_API`, see [`../api/market.md`](../api/market.md)), opens a 20-second-timeout `aiohttp.ClientSession`, and registers itself with `AsyncController`.

### `_polling_update()` (async)

The core loop: initializes the symbol object, starts its order book stream (`orderbook_initialyze`), then loops forever calling `recv_orderbook(self.TIME_MS/1000)` and pushing the resulting `bids`/`asks` into whichever `OrderBookSideWindow` instances are currently open (matched by `win.side`).

### Lifecycle

- **`run()`** — creates the two `OrderBookSideWindow` instances (bids and asks), connects each one's `closed` signal to `_on_child_closed`, tracks them in `self.opened_windows`, starts `_polling_update()` as a background task, and shows both windows.
- **`_on_child_closed(win)`** — removes the closed window from `opened_windows`; if that was the last one open, schedules `close_async()` — i.e., **closing both order book side windows automatically tears down the underlying network subscription**, rather than leaving it running in the background.
- **`close_async()`** (async) — the real cleanup path: guarded against re-entrance via `self._closing`, cancels all tracked async tasks, closes the REST session, and force-closes any windows still open.
- **`close()`** — a synchronous convenience wrapper that schedules `close_async()` as a task (or, if there's no running event loop — `RuntimeError`/`RuntimeWarning` — falls back to `loop.run_until_complete(...)`), and also directly closes any still-open side windows.
- **`colse_session()`** *(existing typo, kept as-is)* — a small unused-looking helper that just closes `self.rest_session`; note `close_async()` closes the session inline rather than calling this method, so this method currently has no callers in this file (dead code, but harmless).

### Static helpers used by the chart-popup UI

Mirrors the pattern in `charts/candels_shart.py`:
- **`reset_showchart_body(parent)`** — configures the chart-popup form to show a numeric "seconds" input instead of a dropdown (order book refresh interval, not a candle timeframe), and validates that a nonzero value has been entered (`parent.time_frame['is_correct']`).
- **`submit_data(parent, chart)`** — same pattern as the candlestick chart's version: reads the numeric time frame, instantiates `chart(symbol=..., time_frame=...)`, tracks and runs it.
- **`set_chart_vars(parent)`** — a no-op placeholder (present for interface symmetry with `SimpleCandelsChart.set_chart_vars`, which does have setup work to do).

## Standalone run mode

Like `candels_shart.py`, has an `if __name__ == "__main__":` block for running this widget in isolation with its own `QApplication`/`qasync` loop — though note it does **not** start `core.listeners`/`API.listeners` here (unlike `candels_shart.py`'s standalone block), so error/log stream consumers won't be running if this file is executed directly on its own.

## Related

- [`../api/market.md`](../api/market.md) — `SINGLE_API` (aliased as `CHOISED_SYMBOLS_CLASS`), the data source for this widget.
- [`../base/charts.md`](../base/charts.md) — registers `OrderBook` under the `"order_book"` key.
- [`../styles/qss.md`](../styles/qss.md) — `QSS["BINANCE"]`.
