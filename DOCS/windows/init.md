# `windows/__init__.py`

**Role:** Package entry point for `windows/`. This file is **empty** — there is no re-export surface here. Every module under `windows/` (and `windows/tool_bar/`) is imported directly by its full path elsewhere (e.g. `from .coin import OneCoin` in `windows/main.py`, `from windows.tool_bar import home` in `prepare.py`), rather than through this `__init__.py`.

## Related

- [`main.md`](main.md), [`coin.md`](coin.md), [`chart_popup.md`](chart_popup.md) — the modules in this package.
- [`tool_bar/init.md`](tool_bar/init.md) — the sibling package's (also empty) entry point.
