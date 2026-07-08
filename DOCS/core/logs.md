# `core/logs.py`

**Role:** Configures Python's `logging` module for the whole app (console + rotating-by-run log file) and subscribes to `LogsStream`/`SystemStream` to turn published events into actual log output. Also exposes the `log()` function used throughout the codebase to publish log events.

## Setup performed at import time

- Sets `PYQTGRAPH_QT_LIB=PySide2` again (already set in `prepare.py` — harmless redundancy, but a sign this module is meant to be robust to being imported in isolation/before `prepare.py`).
- Computes `LOGS_FILE = ~/.valtrida/logs/` and creates it if missing.
- Calls `logging.basicConfig(...)` with:
  - Level `DEBUG` if `config.DEBUG_MODE` else `INFO`.
  - Two handlers: a `FileHandler` writing to a **new timestamped file per run** (`YYYY-MM-DD_HH-MM-SS.log`, mode `"w"`), and a `RichHandler` (from the `rich` library) for nicely formatted console output. Because each run gets its own file (never appended to, never rotated/deleted), **log files accumulate indefinitely** in `~/.valtrida/logs/` — there is no cleanup mechanism, so long-running installs should periodically clear old logs manually.
  - Format: `"%(asctime)s [%(levelname)s] -> %(message)s"`.
- Silences (`CRITICAL` level only) the loggers for `websockets`, `asyncio`, `qasync`, `socket`, `pyside2`, and `uniquant`, so their internal chatter doesn't clutter the app's own log output.
- A few `warnings.filterwarnings(...)` calls exist but are **commented out** — they're a documented option for silencing specific noisy warnings (destroyed pending tasks, duplicate pyqtgraph items, un-awaited coroutines) if they become a nuisance, not currently active.

## Listeners (started by `prepare.py` via `core.listeners`)

### `logs_listener()`

Subscribes to the `"all"` channel on `LogsStream`. For each message, reads `type`, `payload["content"]`, and (if `DEBUG_MODE`) `source`, then routes to `logging.debug/warning/info` based on `type`. Note: messages of type `"debug"` or `"warning"` are **only actually logged if `DEBUG_MODE` is `True`** — with `DEBUG_MODE = False`, debug/warning-level app log events are silently dropped by this listener (though `info`-typed messages always go through).

### `system_logs_listener()`

Subscribes to the `"all"` channel on `SystemStream` and logs every system event at `INFO` level, deriving the message content from either `message["event"]` or `message["payload"]["event"]` if present. Supports a `payload["headen"]` flag *(existing typo for "hidden", kept as-is)* — if truthy, the event is treated as a "hidden"/low-priority event and is **skipped entirely unless `DEBUG_MODE` is `True`**. This is how `SystemStream` can carry high-frequency/noisy UI events without flooding the log file in normal (non-debug) use.

## `log(ltype, content, source="")`

The function other modules call to publish a log event (mirrors `core.errors.error`'s role for the error stream):

```python
asyncio.create_task(LogsStream.put({
    "type": ltype, "event": "log", "source": source,
    "time": datetime.now().timestamp(),
    "payload": {"content": content}
}))
```

Note this uses `LogsStream.put(...)` wrapped in `asyncio.create_task` directly, rather than `LogsStream.send(...)` (which does the same thing internally) — functionally equivalent, just a slightly different call style than `error()`/`critical_error()` use in `core/errors.py`.

## Related

- [`async_controller.md`](async_controller.md) — `LogsStream`, `SystemStream`.
- [`../root/streams.md`](../root/streams.md) — the `log` event's documented shape.
- Nearly every module in `API/` calls `log(...)` (often via a small per-module `log_()` wrapper) to report debug-level activity.
