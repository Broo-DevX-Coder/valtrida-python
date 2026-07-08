# `base/charts.py`

**Role:** A tiny registry mapping a chart's key name to its implementation class, letting other modules request a chart type by string key instead of importing the concrete chart class directly (avoiding circular imports between `windows/`, `charts/`, and `base/`).

## Contents

```python
CHARTS_CLASSES = {
    #"candals_shart":SimpleCandelsChart,
    #"order_book":OrderBook
}

CHARTS = [
    ("Candals Shart", "candals_shart"),
    ("Order Book ", "order_book"),
]
```

- **`CHARTS_CLASSES`** — starts empty (the commented-out lines are just documentation of intent/shape). It is populated at runtime by `prepare.py`:
  ```python
  charts.CHARTS_CLASSES["candals_shart"] = candels_shart.SimpleCandelsChart
  charts.CHARTS_CLASSES["order_book"] = order_book.OrderBook
  ```
  Any code that needs to instantiate a chart by key (e.g. `windows/coin.py`, `windows/chart_popup.py`) looks it up here rather than importing `charts.candels_shart` / `charts.order_book` directly.
- **`CHARTS`** — a list of `(display_label, key)` tuples used to populate any UI element that lets the user pick a chart type (e.g. a dropdown in a chart popup), where `key` is looked up in `CHARTS_CLASSES` to get the actual class.

## Why this exists

Without this indirection, a window module that wants to show a chart would need to `import charts.candels_shart`, and if `charts.candels_shart` ever needed to import something from `windows/` (e.g. to access shared window state), that would create a circular import. By routing everything through this registry (populated once, early, from `prepare.py`), `windows/` and `charts/` never need to import each other.

## Related

- [`../root/prepare.md`](../root/prepare.md) — where `CHARTS_CLASSES` is actually populated.
- [`../charts/candels_shart.md`](../charts/candels_shart.md), [`../charts/order_book.md`](../charts/order_book.md) — the classes registered here.
