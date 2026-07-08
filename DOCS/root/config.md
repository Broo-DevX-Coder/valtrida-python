# `config.py`

**Role:** Small, flat module of global runtime configuration values, imported throughout the app.

## Contents

```python
DEBUG_MODE = True   # Set to True to enable debug mode (more verbose logging)
APP_NAME = "valtrida"
VERSION = "1.0.0"

# ========= Local config in JSON in AppData (future) ==========
COLOR_MODE = 'dark'
```

- **`DEBUG_MODE`** — toggles more verbose logging. Currently hardcoded to `True`; check usages in `core/logs.py` / `core/errors.py` before assuming behavior differs between "debug" and "production" — as of this version, there's no separate build/config mechanism, this file is edited directly.
- **`APP_NAME`** — used for display/identification (e.g. window titles, log prefixes) and implicitly as the basis for the `~/.valtrida/` data directory name conceptually, though the actual directory path constants live in `base/files_folders.py` / `core/folders.py` rather than being derived from this constant at runtime.
- **`VERSION`** — the app version string, `"1.0.0"`.
- **`COLOR_MODE`** — `'dark'` or `'light'`. Read once at import time by `Styles/mods.py` and `Styles/plot_styles.py` to decide whether to rewrite stylesheet/chart colors to their light-mode equivalents (`Styles/__init__.py`'s `DARK_TO_LIGHT_COLORS`). **Changing this value requires restarting the app** — it is not a live-switchable setting.

## Note on the comment "Local config in JSON in AppData (future)"

This comment signals an intended future direction (loading config from a per-user JSON file in the app-data directory instead of this hardcoded Python module) that has **not been implemented yet**. As of this version, all values in this file are compile-time constants, not user-editable settings.

## Related

- [`../styles/mods.md`](../styles/mods.md) — consumes `COLOR_MODE`.
- [`../styles/plot_styles.md`](../styles/plot_styles.md) — consumes `COLOR_MODE` for chart theming.
