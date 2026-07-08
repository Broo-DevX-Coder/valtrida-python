# `windows/chart_popup.py`

**Role:** `ChowSharts` *(existing typo "Chow" for "Chart", kept as-is throughout the codebase, including as the registered popup class name — see `prepare.py`)* — the small configuration form popup that lets the user pick a chart type (from `base/charts.py`'s `CHARTS` registry) and its parameters (timeframe or refresh interval), then launches the corresponding chart window.

## `ChowSharts(QWidget)`

### Construction

A small fixed-size (`300x155`) form with:
- A chart-type dropdown (`self.shart_sellect["main"]`) *(existing typo "shart_sellect" for "chart_select", kept as-is)* populated from `base.charts.CHARTS` (label/key pairs).
- A parameters section (`self.time_frame`) that is **dynamically reconfigured per chart type** — either a `QComboBox` (for candlestick timeframes) or a `QSpinBox` (for order book refresh seconds), both pre-created but only one shown at a time depending on the selected chart.
- An "Add Shart" submit button, disabled until both `shart_sellect['is_correct']` and `time_frame['is_correct']` are true (see `_enable_`).
- Calls `chart.set_chart_vars(self)` for every registered chart class at construction time — this is each chart class's opportunity to attach chart-specific state to the popup instance (e.g. `SimpleCandelsChart.set_chart_vars` sets up `mainchart_items`; `OrderBook.set_chart_vars` is a no-op).

### Chart-type-specific UI ("polymorphic" popup body)

When the user selects a chart type (`on_select_chart`), the popup calls `CHARTS_CLASSES[data].reset_showchart_body(self)` — **each chart class owns the logic for how the popup's parameter section should look and behave for that chart type**, rather than `ChowSharts` having a hardcoded if/else per chart. This is the same registry-driven extensibility pattern as elsewhere in the app: adding a new chart type to `CHARTS_CLASSES`/`CHARTS` and giving it `set_chart_vars`/`reset_showchart_body`/`submit_data` static methods is enough to make it appear and work in this popup without editing `chart_popup.py` itself.

### Submission

**`on_submit()`** delegates to `CHARTS_CLASSES[self.chart_value].submit_data(self, CHARTS_CLASSES[self.chart_value])` — again, each chart class decides how to read its own parameters off the popup and instantiate itself (see `charts/candels_shart.py` / `charts/order_book.py`'s `submit_data` static methods). The resulting chart window is appended to `self.windows` and shown.

### `specific_show(coin)`

Called by `windows/main.py` when the user clicks a coin's "pen" icon — pre-fills `self.symbol_value` with that coin so the next chart created via the popup defaults to it. Note this only sets the value; it doesn't auto-select a chart type or auto-submit, so the user still needs to interact with the dropdown/button.

### Live registry watching

`_on_add_chart_class()` and `_on_add_chart()` are the popup's own analog of `windows/main.py`'s `_on_change_MW_*` watchers: they poll `CHARTS_CLASSES`/`CHARTS` every second and, if new entries appear, call `set_chart_vars` for new chart classes and add new dropdown items for new chart types — again, dormant infrastructure since nothing currently mutates these registries after startup.

### Lifecycle

**`closeEvent`** closes any windows the popup spawned and cancels its tracked async tasks (note: unlike most other window `closeEvent`s in this codebase, this one does **not** call `AsyncController.window_m(self, "delete")` — it was registered as `"add"` in `__init__` but is never explicitly removed on close, a minor inconsistency worth noting if auditing `AsyncController`'s tracked-window list for leaks).

## Related

- [`../base/charts.md`](../base/charts.md) — `CHARTS_CLASSES`, `CHARTS`.
- [`../charts/candels_shart.md`](../charts/candels_shart.md), [`../charts/order_book.md`](../charts/order_book.md) — the chart classes whose `set_chart_vars`/`reset_showchart_body`/`submit_data` static methods drive this popup's behavior.
- [`main.md`](main.md) — wraps this in an `OverlayPopup` and calls `specific_show`.
