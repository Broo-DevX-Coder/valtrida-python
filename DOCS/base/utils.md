# `base/utils.py`

**Role:** Grab-bag of app-wide constants, small helper functions, and the two pub/sub primitives (`QueueStream`, `QueueStreamChannel`) that the entire event-driven architecture is built on. Imported from many places; has no dependency on the rest of the app (no circular-import risk).

## Constants

- **`TIME_FRAMES_INTERVALS`** — the list of chart interval strings the app supports (`"1m"` through `"1M"`), used to populate timeframe selectors for candlestick charts.
- **`qt_color_names`** — the full list of CSS/Qt named colors, likely used for validating or offering color choices somewhere in the UI.
- **`STABLECOINS_USD`** — a large list of USD-pegged stablecoin tickers (`USDT`, `USDC`, `BUSD`, `DAI`, etc., with Arabic-language inline comments describing each). Used by `API/market.py` to determine a symbol's quote asset. Note there are a few duplicate entries in the list (e.g. `MUSD`, `HUSD`, `SEURO` each appear twice) — harmless since it's used for membership checks, but worth knowing if you're editing it.
- **`NO_INTERNET_EXEPTIONS`** *(existing typo, kept as-is)* — a list of fully-qualified exception class name strings (e.g. `"aiohttp.client_exceptions.ClientConnectorError"`, `"builtins.OSError"`) that represent "no internet / connection lost" conditions, presumably matched by name elsewhere (e.g. in error handling) to distinguish real API errors from local connectivity problems.

## Functions

- **`uuid_gen(pref=None, sufx=None, rotations=4)`** — generates a pseudo-UUID string made of `rotations` groups of 5 random alphanumeric characters joined by `-`, optionally prefixed with `pref--` and suffixed with `--sufx`. Used throughout `API/market.py` to tag ownership of a symbol's order book/trade stream (not a cryptographically secure UUID — just a unique-enough tag for coordination, not for security).
- **`DATE`** — a lambda converting a millisecond timestamp to a `"YYYY-MM-DD HH:MM:SS"` string.
- **`to_milliseconds(frame: str)`** — parses a timeframe string like `"15min"` or `"1h"` into `(milliseconds, short_label)` using a regex match against a unit table (`ms`, `s`, `min`/`m`, `h`, `d`, `w`, `M`). Raises `ValueError` if the string doesn't match the expected pattern.

## Classes

### `TimeAxis(pg.AxisItem)`

A `pyqtgraph` custom axis that overrides `tickStrings()` to render millisecond-timestamp tick values as human-readable dates (via `DATE`), falling back to an empty string for any value that fails to convert. Used by the candlestick chart's x-axis.

### `QueueStream`

The simplest pub/sub primitive in the app:
- `subscribe()` — creates a new `asyncio.Queue`, registers it in `self.subscribes`, and returns it to the caller.
- `unsuscribe(sub)` *(existing typo, kept as-is)* — removes a previously-returned queue from the subscriber list.
- `put(msg)` (async) — delivers `msg` to **every** current subscriber queue concurrently via `asyncio.gather`.
- `send(msg)` — a fire-and-forget, non-async wrapper that schedules `put(msg)` as an asyncio task. This is the method most publishers actually call (e.g. `SystemStream.send({...})` in `prepare.py`).

Every subscriber gets every message — there's no per-channel filtering at this level. This is the primitive used directly by, e.g., `Connection_errors` in `API/market.py`.

### `QueueStreamChannel`

A channel-aware extension of the same idea, used for the four global app streams in `core/async_controller.py`:
- `subscribes` is a dict keyed by channel name, always containing an `'all'` bucket.
- `subscribe(channel)` — creates a bounded `asyncio.Queue(maxsize=100)` (note: bounded, unlike plain `QueueStream` — a slow/stuck subscriber could eventually cause `put()` to block if the queue fills, since `put` isn't using `put_nowait`) tied to a specific channel, creating the channel's subscriber list if needed.
- `unsuscribe(sub, channel)` — removes a subscriber from a channel; if that was the last subscriber, the channel entry is deleted entirely.
- `put(msg)` (async) — delivers `msg` to subscribers of the channel named by `msg["event"]` **and** to every subscriber of the special `'all'` channel. This is why `msg["event"]` (not `msg["type"]`) is the dispatch key — subscribers that want a specific event name subscribe to that name as a "channel"; subscribers that want everything subscribe to `'all'`.
- `send(msg)` — same fire-and-forget pattern as `QueueStream.send`.

## Related

- [`../core/async_controller.md`](../core/async_controller.md) — instantiates `QueueStreamChannel` for the four global streams and documents the event schema more fully (see also `streams.txt`).
- [`../api/market.md`](../api/market.md) — uses `QueueStream`, `STABLECOINS_USD`, `uuid_gen` directly.
- [`../charts/candels_shart.md`](../charts/candels_shart.md) — uses `TimeAxis`, `to_milliseconds`.
