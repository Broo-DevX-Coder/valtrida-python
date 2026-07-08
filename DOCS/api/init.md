# `API/__init__.py`

**Role:** Package entry point for `API/` — re-exports the pieces `prepare.py` and other modules need, and declares this package's listener list.

## Contents

```python
from .market import redirect_connection_errors
from .market import SINGLE_API

listeners = [redirect_connection_errors]
CHOISED_SYMBOLS_CLASS = SINGLE_API
```

- **`listeners`** — a list of async callables that `prepare.py` schedules as asyncio tasks at startup (see [`../root/prepare.md`](../root/prepare.md)). For `API/`, this currently contains only `redirect_connection_errors`, which forwards critical connection errors from the market-data layer into the app-wide error handling pipeline (see [`market.md`](market.md)).
- **`CHOISED_SYMBOLS_CLASS`** — an alias for `market.SINGLE_API`, the main class other modules use to subscribe to live data (order book, trades) for a given coin. The name ("chosen symbols class") signals this is the currently-selected implementation for per-symbol data access — if the app ever supports multiple market-data backends, this is the seam where that selection would happen.

## Related

- [`market.md`](market.md) — defines everything re-exported here.
- [`../root/prepare.md`](../root/prepare.md) — consumes `listeners`.
