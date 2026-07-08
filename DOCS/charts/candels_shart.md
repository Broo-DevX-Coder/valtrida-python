# `charts/candels_shart.py`

**Role:** The candlestick chart widget — a `QWebEngineView` that renders an embedded JavaScript charting library (KLineCharts), fed with historical REST data and live updates via a WebSocket kline stream. (Filename keeps the project's existing shorthand "candels_shart" — intentional, not a doc typo.)

## Embedded HTML/JS

`pp` is a large base64-encoded string containing a full HTML page with the KLineCharts library and custom draw tools bundled in, decoded and loaded via `self.setHtml(html)`. This keeps the chart's front-end self-contained (no external file dependency, no network fetch of JS at runtime) at the cost of a large embedded blob in this Python file.

## `Backend(QObject)`

A `QObject` exposed to the embedded JS page via `QWebChannel` (`self.channel.registerObject("backend", self.backend)`), letting JavaScript call back into Python. Currently exposes one `@Slot()`:

- **`mor_candales()`** *(existing typo, kept as-is)* — called from JS (presumably when the user scrolls to the edge of the chart wanting older candles). Guards against duplicate in-flight requests (`len(self.tasks) == 0`) and only proceeds if the chart has finished its initial load (`self.pa_.ready == True`), then schedules `_load_candales(te="M")` ("M" = "more") to fetch older data.

## `SimpleCandelsChart(QWebEngineView)`

### Construction

Takes `time_frame` (e.g. `"4h"`) and `symbol` (base asset, e.g. `"SOL"` — `"USDT"` is appended automatically). Sets up:
- `self.FRAME = to_milliseconds(time_frame)` — both the millisecond duration and the short label.
- The `QWebChannel`/`Backend` wiring described above.
- An `aiohttp.ClientSession` and a `uniquant` `OneSymbole` object for this symbol, both registered with `AsyncController`.
- Loads the decoded HTML, sets a custom right-click context menu (Back/Forward/Reload — standard web-view navigation, mostly vestigial since this isn't meant to navigate elsewhere), and connects `loadFinished` to `run_()`.

### Data flow

1. **`__get_klines(endt=None)`** — fetches historical candles from `/api/v3/klines` (limit 1000). On `429`/`418`/`403`, **closes the window** and reports a critical error (so a rate-limited/banned chart window doesn't sit open showing stale data). Any other non-200 status is reported as a general error and returns an empty list.
2. **`_load_candales(te="N")`** — calls `__get_klines` (either fresh, `te="N"`, or older data ending before `first_candal_time`, `te="M"`), builds a `pandas.DataFrame`, casts numeric columns, drops the last (still-forming) candle, serializes to a JS array, and calls either `chart.applyNewData(...)` (first load, also sets `self.ready = True`) or `chart.applyMoreData(...)` (subsequent "load more" calls from `Backend.mor_candales`) via `runJavaScript`.
3. **`update_price()`** — an infinite loop over `self.symbol_obj.klines_stream(self.FRAME[1])` (a live WebSocket stream from `uniquant`), scheduling `_draw_updated_candel(message)` for every update.
4. **`_draw_updated_candel(message)`** — formats the incoming kline update as a JS object literal and calls `chart.updateData({...})` via `runJavaScript`.

### Lifecycle

- **`run_(ok)`** — the `loadFinished` callback; if the page loaded successfully, kicks off `_start()` (which calls `_load_candales()` for the initial history) and `update_price()` as background tasks, then shows the window.
- **`run()`** — a bare `self.show()`, used when the widget is being run as a script (`__main__` block) rather than through the normal `loadFinished` flow.
- **`closeEvent(event)`** — schedules `close()`, unregisters from `AsyncController`, logs, and accepts the close event.
- **`close()`** (async) — closes the REST session, closes the `uniquant` symbol object, and cancels all tracked async tasks — all wrapped in a blanket `try/except: pass`.

### Static helpers used by the chart-popup UI

- **`set_chart_vars(parent)`** — initializes `SimpleCandelsChart.mainchart_items = {}` on the class (a class-level dict, shared across instances — used by the chart popup UI, see `windows/chart_popup.py`).
- **`reset_showchart_body(parent)`** *(existing typo "olugin" for "plugin" in the docstring-style comment, kept as-is)* — configures the chart-popup form (`windows/chart_popup.py`'s `ChowSharts`) to show a time-frame dropdown populated from `TIME_FRAMES_INTERVALS`, and sets `parent.spot_symbols = ALL_USDT_SYMBOLS`.
- **`submit_data(parent, chart)`** — reads the selected time frame from the popup form, instantiates `chart(symbol=..., time_frame=...)`, tracks it in `parent.windows`, and calls `.run()`.

## Standalone run mode

The `if __name__ == "__main__":` block lets this file be run directly for isolated testing — it sets up its own `QApplication`/`qasync` loop, starts `core.listeners` and `API.listeners` manually (since `prepare.py` isn't run in this mode), and shows a single chart window for the default symbol.

## Related

- [`../base/charts.md`](../base/charts.md) — registers `SimpleCandelsChart` under the `"candals_shart"` key.
- [`../windows/chart_popup.md`](../windows/chart_popup.md) — the UI that lets users configure and launch a chart via `submit_data`/`reset_showchart_body`.
- [`../base/utils.md`](../base/utils.md) — `to_milliseconds`, `TIME_FRAMES_INTERVALS`.
- [`../api/market.md`](../api/market.md) — `ALL_USDT_SYMBOLS`, `Connection_errors`.
