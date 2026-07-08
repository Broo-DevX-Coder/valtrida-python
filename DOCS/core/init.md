# `core/__init__.py`

**Role:** Package entry point for `core/` — re-exports the public surface of the streams, controller, logging, and error-reporting functions, and assembles this package's `listeners` list consumed by `prepare.py`.

## Contents

```python
from .async_controller import LogsStream, SystemStream, UserStream, ErrorsStream
from .async_controller import AsyncController
from .logs import log
from .errors import critical_error, error

from .errors import errors_listener, critical_errors_listener
from .logs import logs_listener, system_logs_listener
listeners = [errors_listener, logs_listener, critical_errors_listener, system_logs_listener]
```

- Re-exports the four global streams and `AsyncController`, so other modules can `from core import SystemStream, AsyncController` etc. instead of reaching into `core.async_controller` directly.
- Re-exports `log`, `critical_error`, `error` — the three functions used throughout the app to report activity/errors.
- Assembles **`listeners`**: the four background coroutines (`errors_listener`, `logs_listener`, `critical_errors_listener`, `system_logs_listener`) that must run continuously for the whole error/logging pipeline to function. `prepare.py` schedules every entry in this list as an asyncio task at startup — if a new listener is added to `core/errors.py` or `core/logs.py`, it must also be added to this `listeners` list, or it will simply never run despite being defined.

## Related

- [`async_controller.md`](async_controller.md), [`errors.md`](errors.md), [`logs.md`](logs.md) — the modules whose symbols are re-exported here.
- [`../root/prepare.md`](../root/prepare.md) — consumes `core.listeners`.
