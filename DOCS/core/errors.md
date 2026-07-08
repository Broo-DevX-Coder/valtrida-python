# `core/errors.py`

**Role:** Subscribes to `ErrorsStream` and turns published error events into logged messages and, for certain critical connection errors, a blocking popup dialog followed by a full app shutdown. Also exposes the two functions (`critical_error`, `error`) that the rest of the app calls to *report* errors.

## Listeners (started by `prepare.py` via `core.listeners`)

### `critical_errors_listener()`

Subscribes to the `"connection_error"` channel on `ErrorsStream` and, for each message, matches on `message["type"]`:

- `CONNECTION_429` → logs an error and shows a popup ("Too many requests... wait 1 minute") whose OK button triggers `CRITICAL_STOP` — i.e., **the app shuts down** after the user acknowledges a 429.
- `CONNECTION_418` → same pattern, IP-ban message, 1 hour wait.
- `CONNECTION_403` → same pattern, forbidden/blocked-IP message, suggests VPN/proxy.
- `CONNECTION_0` → same pattern, "no internet connection" message.

In every case, the popup's confirm callback is `CRITICAL_STOP` (from `core/async_controller.py`) — these four conditions are treated as unrecoverable for the current session, so the app always terminates after the user dismisses the dialog, rather than attempting to continue or auto-retry.

### `errors_listener()`

Subscribes to the `"all"` channel on `ErrorsStream` (i.e., receives every error event regardless of type) and simply logs `message["payload"]["message"]` via `logging.error(...)`, with the source component included only if `DEBUG_MODE` is `True`. Wrapped in a broad `try/except: pass` so a malformed error message can't crash the listener loop itself.

## Public reporting functions

### `critical_error(ntype, source="")`

Publishes a `connection_error` event on `ErrorsStream` with `type = f"CONNECTION_{ntype}"`. Called from `API/market.py` for 429/418/403/0 conditions.

### `error(etype, source, msg, module_etype='UNKNOWN')`

The general-purpose error reporter used throughout the codebase (e.g. `API/b_accont.py`, `API/market.py`). Handles a few input shapes:

- If `etype` is not a string (e.g. an exception instance was passed directly), derives a string type name from `type(etype)` (stripped of the `<class '...'>` wrapper).
- If `etype == "UNKNOWN"` and `module_etype` isn't a string either, falls back to deriving the type name from `module_etype` instead.
- Otherwise uses `etype` as-is.
- **Special case:** if the resolved `error_type` string matches one of the fully-qualified exception names in `base.utils.NO_INTERNET_EXEPTIONS`, the event is **reclassified** as a `connection_error` with type `CONNECTION_0` — meaning a raw exception like `aiohttp.client_exceptions.ClientConnectorError` reported via `error(e, ...)` is automatically treated the same as a "no internet" condition and will trigger `critical_errors_listener`'s `CONNECTION_0` handling (popup + `CRITICAL_STOP`), not just a plain log line. This is the mechanism that connects generic exception reporting to the critical-error/shutdown path.
- Publishes the resulting event (`general_error` or `connection_error`) on `ErrorsStream` with `payload.message = msg`.

## Related

- [`async_controller.md`](async_controller.md) — `ErrorsStream`, `CRITICAL_STOP`.
- [`pop_messages.md`](pop_messages.md) — `pup_message`, used to show the blocking dialogs here.
- [`../base/utils.md`](../base/utils.md) — `NO_INTERNET_EXEPTIONS`.
- [`../api/market.md`](../api/market.md), [`../api/b_accont.md`](../api/b_accont.md) — main callers of `error`/`critical_error`.
