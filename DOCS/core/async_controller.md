# `core/async_controller.py`

**Role:** Defines the four global event streams that drive the app's event-driven architecture, plus `AsyncController` — the process-wide registry of everything (windows, threads, REST sessions, async functions/loops) that needs coordinated cleanup — and `CRITICAL_STOP()`, the single emergency-shutdown entry point.

## The four global streams

```python
ErrorsStream = QueueStreamChannel()
UserStream = QueueStreamChannel()
LogsStream = QueueStreamChannel()
SystemStream = QueueStreamChannel()
```

These are singletons (module-level instances), each a `QueueStreamChannel` (see [`../base/utils.md`](../base/utils.md)). Every event published to any of them is expected to follow the schema documented in `streams.txt`:

```python
{"type": str, "event": str, "source": str, "time": float, "payload": dict}
```

- **`SystemStream`** — system/UI-driven events and lifecycle events (`start_of_program`, `end_of_program`, `login_clicked`, `coin_clicked`, etc).
- **`UserStream`** — user/session/account state changes (`logged_in`, `logged_out`, `user_data_changed`, `user_binance_data_changed`).
- **`ErrorsStream`** — errors, consumed by `core/errors.py`'s two listeners.
- **`LogsStream`** — log messages, consumed by `core/logs.py`'s listeners.

See [`../root/streams.md`](../root/streams.md) for the fuller schema reference.

## Tracking lists

```python
ALL_ASYNC_FUNCTIONS = []
ALL_QT_WINDOWS = []
ALL_REST_SESSIONS = []
ALL_THREADS = []
ALL_ASYNC_LOOPS = []
```

Plain module-level lists — the actual storage behind `AsyncController`'s registration methods.

## `AsyncController`

A class used purely as a namespace for static-style management functions (note: none of these are decorated `@staticmethod`, they're called as `AsyncController.window_m(...)` — this works in Python because the first parameter is just treated as a positional arg, not `self`, since the class is never instantiated). Four resource types, each with an add/delete toggle via an `event` parameter:

- **`window_m(window, event="add")`** — track/untrack a Qt window in `ALL_QT_WINDOWS`.
- **`loop_m(loop, event="add")`** — track/untrack an asyncio event loop in `ALL_ASYNC_LOOPS`.
- **`rest_m(session, event="add")`** — track/untrack an `aiohttp.ClientSession` in `ALL_REST_SESSIONS`.
- **`async_m(func, event="add")`** — track/untrack an async task/function in `ALL_ASYNC_FUNCTIONS`.
- **`thread_m(thread, event="add")`** — track/untrack a `threading.Thread` in `ALL_THREADS`.

Every add is deduplicated (`if ... not in ...`) and every delete is safe against items that were never added. This is the mechanism referenced throughout `API/market.py` (`AsyncController.window_m(self, event="add")`, `AsyncController.rest_m(self.rest_session, event="add")`, etc.) — any module that opens a long-lived resource is expected to register it here so it can be torn down centrally.

## `CRITICAL_STOP()`

The single, synchronous, best-effort shutdown path:

1. Gets the current event loop.
2. Closes every tracked Qt window (`loop.run_until_complete(asyncio.gather(...))`), swallowing any exception per-window so one broken window doesn't block the rest.
3. Cancels every tracked async function/task (best-effort, swallowing exceptions).
4. Joins every tracked thread with a 1-second timeout each (best-effort — a thread that doesn't stop within 1s is not force-killed, just left; not a hard guarantee of full cleanup).
5. Stops every tracked async loop via `call_soon_threadsafe(loop.stop)`.
6. Closes every tracked REST session (`aiohttp.ClientSession.close()`), again via `run_until_complete`.
7. Calls `sys.exit(1)` — always exits with status code `1`, even on a "clean" critical stop; this is intentional, since `CRITICAL_STOP` is only ever invoked in response to a critical error condition (see `core/errors.py`), not on a normal user-initiated close.

Every step is wrapped in a bare `try/except: pass` — this function is designed to make a best effort at cleanup even if individual resources are already in a bad state, prioritizing "the process actually exits" over "every resource is cleanly released."

## Related

- [`../base/utils.md`](../base/utils.md) — `QueueStreamChannel`, the primitive these streams are built on.
- [`../root/streams.md`](../root/streams.md) — the authoritative event schema documentation.
- [`errors.md`](errors.md) — calls `CRITICAL_STOP` in response to certain connection errors.
- [`init.md`](init.md) — re-exports these streams and `AsyncController` for the rest of the app.
