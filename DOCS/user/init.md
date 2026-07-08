# `user/__init__.py`

**Role:** Package entry point for `user/`. This file is **empty** — `window.py`, `local_cypher.py`, and the `widgets/` sub-package are all imported directly by full path wherever needed (e.g. `from user.local_cypher import CipherUserData`), not re-exported here.

## Related

- [`window.md`](window.md), [`local_cypher.md`](local_cypher.md) — the modules in this package.
- [`widgets/login.md`](widgets/login.md), [`widgets/register_via_binance_api.md`](widgets/register_via_binance_api.md) — the sub-package's modules (note: `user/widgets/` itself has no `__init__.py` at all, unlike this package).
