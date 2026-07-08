# `API/market.py`

**Role:** Public (unauthenticated) Binance market data access — symbol discovery, live order book, and live trades, exposed per-coin through the `SINGLE_API` class. This is the busiest, most stateful module in the networking layer.

## Module-level state

- **`ALL_SYMBOLS` / `ALL_USDT_SYMBOLS` / `ALL_COINS`** — module-level lists intended to hold the full universe of symbols/coins discovered from Binance. (As of this version, populated elsewhere/on demand rather than eagerly at import time.)
- **`PLATFORMS_OBJS`** — a small registry mapping a platform name (currently only `"Binance"`) to the `uniquant` classes used for public symbol data (`Binance.Public.PublicSymbols`, `Binance.Public.OneSymbole`). This indirection is what would let a second exchange be added later without changing `SINGLE_API`'s logic.
- **`SYMBOLS_DATA`** — the central live-state dictionary, keyed as `SYMBOLS_DATA[platform][symbol]`, holding per-symbol status flags (`OB`/`TRADES` open or closed), an `operations_queue` (a FIFO-like list of UUIDs used to serialize which task "owns" starting a symbol's stream — see below), the underlying `uniquant` `OneSymbole` object, an `errors_stream`/`trades_stream` `QueueStream`, and the current order book snapshot (`asks`/`bids`).
- **`Connection_errors`** — a dedicated `QueueStream` that critical connection errors are published to; `redirect_connection_errors()` (below) is the sole subscriber and forwards them into the app-wide error stream.

## `redirect_connection_errors()`

An infinite loop (registered in `API/__init__.py`'s `listeners`, started by `prepare.py`) that subscribes to `Connection_errors` and, for each message:
- If the error type is one of `CONNECTION_429`, `CONNECTION_418`, `CONNECTION_403`, or `CONNECTION_0`, calls `critical_error(...)` — these correspond to Binance rate-limiting (429), IP ban (418), forbidden (403), and connection-failure (0) conditions, all serious enough to warrant a critical/blocking error.
- Otherwise, calls the regular `error(...)` for anything else.

## `SINGLE_API` class

Represents "give me live order book + trade data for one coin" and manages the underlying per-symbol subscriptions.

### Construction (`__init__`)

Takes a `coin` (base asset, e.g. `"BTC"`) and a `platform_name` (default `"Binance"`). Registers itself with `AsyncController.window_m(self, event="add")` so it's tracked for cleanup, and ensures `SYMBOLS_DATA[platform_name]` exists.

### `get_symbols()` (static)

Fetches `/api/v3/exchangeInfo` from Binance directly via `aiohttp`, filters for symbols that are spot-tradable and end in `USDT`, and returns that list. Handles 429/418/403 as critical errors and other non-200 statuses / exceptions as regular errors.

### `initialize()`

Appends `"USDT"` to `self.coin` (so `"BTC"` becomes `"BTCUSDT"`), opens a persistent `aiohttp.ClientSession` (registered with `AsyncController.rest_m`), determines the quote asset by checking which entry in `STABLECOINS_USD` (from `base/utils.py`) is a substring of the symbol, and creates the `SYMBOLS_DATA[platform][symbol]` entry (status closed for both `OB` and `TRADES`, a fresh `uniquant` `OneSymbole` instance, empty order book, and a fresh `trades_stream`).

### Order book pipeline

- **`orderbook_initialyze(limit=5000)`** *(note: existing typo, not a doc error)* — waits until `self.symbole_data["are_symboles_ready"]` is true, then schedules `_one_symbol_orderbook_stream(s, limit)` for every symbol as an asyncio task.
- **`_one_symbol_orderbook_stream(symbol, limit)`** — the actual per-symbol worker. Generates a UUID and appends it to that symbol's `operations_queue["OB"]`, then loops: if the symbol's `OB` status is `"closed"` **and** this UUID is at the front of the queue (i.e., it's this instance's turn), it claims the symbol (marks `OB` open, removes itself from the queue, adds itself to `adopted_symbols["OB"]`), starts the underlying `uniquant` `OneSymbole` object, registers its window/REST session with `AsyncController`, and then iterates `s_obj.orderbook_stream(limit=limit)`, writing each update into `SYMBOLS_DATA[...]["orderbook"]`. On any exception, it reverts the symbol to `"closed"`, re-queues its UUID, and continues retrying. This UUID-queue pattern is essentially **a fairness/ownership lock**: multiple `SINGLE_API` instances (e.g. multiple open coin windows) can request the same symbol's order book, but only one at a time actually opens the underlying WebSocket connection to Binance, and ownership is handed off in FIFO order when the current owner fails or closes.
- **`recv_orderbook(t=1)`** — waits at least `max(t, 1.5)` seconds, then aggregates the current order book across all of this instance's needed symbols (summing quantities at matching price levels) and returns a combined `{"connections", "symbols", "asks", "bids"}` dict.

### Trades pipeline

Mirrors the order book pipeline structurally:
- **`trades_initialyze()`** — subscribes to `self.trades_queue`, schedules `_one_symbol_trades_stream(s)` and `_one_symbol_trade_redirect(s)` per symbol, returns the subscription handle.
- **`_one_symbol_trades_stream(symbol)`** — same UUID-queue ownership pattern as the order book version, but for the `TRADES` status/queue, iterating `s_obj.trades_stream()` and publishing each trade to the shared `SYMBOLS_DATA[...]["trades_stream"]`.
- **`_one_symbol_trade_redirect(symbol)`** — subscribes to that shared per-symbol `trades_stream` and forwards every message into this instance's own `self.trades_queue`, so multiple `SINGLE_API` instances watching the same symbol each get their own copy of every trade.
- **`recv_trade(trades_sub)`** — awaits and returns the next trade from a given subscription.

### Cleanup

- **`_cancel_adoption()`** — for every symbol this instance currently "owns" (in `adopted_symbols`), marks it closed and removes any of this instance's UUIDs from the operations queues, freeing the symbol up for another instance to claim.
- **`close()`** — calls `_cancel_adoption()`, closes the REST session, cancels all tracked `async_tasks`, and unregisters itself from `AsyncController`.

## Why the ownership/queue pattern exists

Binance WebSocket connections are a limited resource (both practically and per Binance's own rate limits). If two `windows/coin.py` instances for the same coin were each allowed to open their own WebSocket connection to the same symbol, that would double the connection count for no benefit. Instead, exactly one `SINGLE_API` instance "owns" the live stream per symbol at a time, and all other interested instances receive the data via the shared `trades_stream`/`orderbook` state instead of opening their own connection.

## Related

- [`../base/utils.md`](../base/utils.md) — `QueueStream`, `STABLECOINS_USD`, `uuid_gen`.
- [`../core/async_controller.md`](../core/async_controller.md) — `AsyncController.window_m` / `.rest_m`, `critical_error`, `error`, `log`.
- [`../charts/order_book.md`](../charts/order_book.md), [`../charts/candels_shart.md`](../charts/candels_shart.md) — consumers of this data.
- [`b_accont.md`](b_accont.md) — the authenticated counterpart to this module.
