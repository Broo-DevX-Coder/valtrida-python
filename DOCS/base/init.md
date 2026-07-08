# `base/__init__.py`

**Role:** Package entry point for `base/`. Currently re-exports only one symbol:

```python
from .user_data import UserDataGet
```

This makes `from base import UserDataGet` work anywhere in the app, rather than requiring `from base.user_data import UserDataGet`. The other `base/` submodules (`charts.py`, `tool_bar.py`, `utils.py`, `files_folders.py`) are imported directly by their full path elsewhere in the codebase (e.g. `from base.charts import CHARTS_CLASSES`, `from base.utils import QueueStream`) rather than being re-exported here.

## Related

- [`user_data.md`](user_data.md) — the module `UserDataGet` comes from.
