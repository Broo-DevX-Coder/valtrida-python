# `charts/__init__.py`

**Role:** Package entry point for `charts/`. This file is **empty** — `SimpleCandelsChart` and `OrderBook` are imported directly from their own modules (e.g. `from charts.candels_shart import SimpleCandelsChart` in `base/charts.py`, where they're registered into the `CHARTS_CLASSES`/`CHARTS` dicts), not re-exported here.

## Related

- [`candels_shart.md`](candels_shart.md), [`order_book.md`](order_book.md) — the modules in this package.
- [`../base/charts.md`](../base/charts.md) — the registry that imports and exposes these chart classes to the rest of the app.
