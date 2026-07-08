# `streams.txt`

**Role:** Authoritative, human-maintained documentation of the app's event/stream schema. Not executable code — a reference file that should be kept in sync with `core/async_controller.py` and every module that publishes or subscribes to a stream.

## Why it exists

Valtrida's core communication pattern is event-driven pub/sub (see [`../ARCHITECTURE.md`](../ARCHITECTURE.md#2-event-driven-core-queuestream)). Because events are just dicts flowing through generic channels rather than typed function calls, there's no compiler-enforced contract for what a given event's `payload` looks like. `streams.txt` fills that gap as living documentation.

## Event structure

Every event on every stream is expected to follow this shape:

```python
{
    "type": str,     # Stream category
    "event": str,    # Event name
    "source": str,   # Component that emitted the event
    "time": float,   # Timestamp
    "payload": dict  # Event payload (optional)
}
```

## The four streams

| Stream | Purpose | Example events |
|---|---|---|
| `SystemStream` | Internal system commands / UI-driven actions; app lifecycle | `login_clicked`, `coin_clicked` (payload includes `cl_type`: `pen` or `coin`), `start_of_program`, `end_of_program` |
| `UserStream` | User/session state changes | `logged_in`, `logged_out`, `user_data_changed`, `user_binance_data_changed` |
| `ErrorStream` (implemented as `ErrorsStream`) | Critical failures, potentially requiring shutdown | `connection_error`, `general_error` |
| `LogStream` (implemented as `LogsStream`) | Observability/diagnostics only — must never change system state | `log` |

Typical `"type"` values seen alongside `SystemStream` events: `live_sycle`, `window_event`, `plugin_event`. Typical `"type"` values for `UserStream`: `user_local_info`, `binance_balances`.

> Note: the file uses the names `ErrorStream` / `LogStream` in prose, while the actual code in `core/async_controller.py` names the global instances `ErrorsStream` / `LogsStream` (plural). Both names refer to the same concept — when in doubt, trust the actual exported names in `core/async_controller.py` for what to import, and use this file for the event/payload conventions.

## Design rules (from the file, worth repeating)

**Do:**
- Emit clear, well-named events.
- Keep payloads small — pass IDs, not full objects.
- Document every event name here.

**Don't:**
- Send Qt widgets/windows through streams.
- Send asyncio tasks through `SystemStream`.
- Mix unrelated responsibilities on one stream.
- Introduce undocumented event types.

## Maintenance rule

**Any change that adds, removes, or changes the shape of an event must update this file in the same commit/PR.** Treat a stream-schema change without a `streams.txt` update as incomplete.

## Related

- [`../core/async_controller.md`](../core/async_controller.md) — where these streams are actually instantiated.
- [`../ARCHITECTURE.md`](../ARCHITECTURE.md) — how streams fit into the overall design.
