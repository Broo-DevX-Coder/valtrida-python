# `core/folders.py`

**Role:** Ensures every local application directory referenced in `base/files_folders.py` actually exists on disk, and adds the "more packages" directory to `sys.path`. Runs entirely at **import time** (no functions to call — importing this module *is* the setup).

## What it does

```python
from base.files_folders import *

os.makedirs(APP_DATA, exist_ok=True)
os.makedirs(os.path.join(APP_DATA, 'data', "users"), exist_ok=True)
os.makedirs(PLUGINS_DIR, exist_ok=True)
os.makedirs(MORE_PACKAGES, exist_ok=True)

os.makedirs(ASSETS, exist_ok=True)
os.makedirs(ASSETS_HTML, exist_ok=True)
os.makedirs(ASSETS_CSS, exist_ok=True)
os.makedirs(ASSETS_QSS, exist_ok=True)
os.makedirs(ASSETS_ICONS, exist_ok=True)
os.makedirs(ASSETS_ICONS_SVG, exist_ok=True)
os.makedirs(ASSETS_ICONS_ICO, exist_ok=True)

sys.path.append(MORE_PACKAGES)
```

- Creates `~/.valtrida/`, `~/.valtrida/data/users/`, `~/.valtrida/Plugins/`, `~/.valtrida/Packages/`, and the full `~/.valtrida/ASSETS/...` tree, all with `exist_ok=True` so re-running is a no-op on subsequent launches.
- Appends `MORE_PACKAGES` (`~/.valtrida/Packages`) to `sys.path`, meaning any Python package dropped into that directory becomes importable by the app — this is the (currently unused) hook for the not-yet-implemented plugin/extension system referenced in `prepare.py`.
- Note the `os.path.join(APP_DATA, 'data', "users")` call duplicates what `base.files_folders.USERS_FILE` already computes — it works correctly since both resolve to the same path, but if that path ever changes in `base/files_folders.py`, this line should be updated to use `USERS_FILE` directly rather than re-deriving it.

## Related

- [`../base/files_folders.md`](../base/files_folders.md) — defines every path constant used here.
- [`../root/prepare.md`](../root/prepare.md) — imports `core`, which imports `core.folders` (see `core/__init__.py` if it imports `folders` — otherwise this module is triggered wherever `from core import folders` appears, e.g. in `prepare.py`).
