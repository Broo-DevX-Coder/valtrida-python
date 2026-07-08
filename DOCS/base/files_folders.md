# `base/files_folders.py`

**Role:** Central definition of every filesystem path the app reads from or writes to, all derived from a single application-data root directory. Keeping every path in one module means there's exactly one place to look when auditing what Valtrida touches on disk.

## Contents

```python
APP_DATA = os.path.join(Path.home(), f".{APP_NAME}")   # e.g. ~/.valtrida
USERS_FILE = os.path.join(APP_DATA, 'data', "users")
PLUGINS_DIR = os.path.join(APP_DATA, "Plugins")
TEMP_FILE = tempfile.mkdtemp()
MORE_PACKAGES = os.path.join(APP_DATA, "Packages")

ASSETS = os.path.join(APP_DATA, "ASSETS")
ASSETS_HTML = os.path.join(APP_DATA, "ASSETS", "html")
ASSETS_CSS = os.path.join(APP_DATA, "ASSETS", "css")
ASSETS_QSS = os.path.join(APP_DATA, "ASSETS", "qss")
ASSETS_ICONS = os.path.join(APP_DATA, "ASSETS", "icons")
ASSETS_ICONS_SVG = os.path.join(APP_DATA, "ASSETS", "icons", "svg")
ASSETS_ICONS_ICO = os.path.join(APP_DATA, "ASSETS", "icons", "ico")
```

- **`APP_DATA`** — `~/.{APP_NAME}`, i.e. `~/.valtrida` given `config.APP_NAME = "valtrida"`. This is the root of all persistent local state.
- **`USERS_FILE`** — `~/.valtrida/data/users`, where per-user encrypted profile files live (see `user/local_cypher.py`).
- **`PLUGINS_DIR`** — `~/.valtrida/Plugins`. **Reserved for a plugin system that is not implemented yet** (see `prepare.py`'s reference to a non-existent `plugins_manager`).
- **`TEMP_FILE`** — a fresh temp directory created via `tempfile.mkdtemp()` **every time this module is imported**. Since Python caches module imports, this effectively means one temp directory per process run, not per use — but note it is **never cleaned up** by this module; nothing here calls `shutil.rmtree` on it. If the app is used to write scratch files into `TEMP_FILE`, those directories will accumulate in the OS temp folder across runs unless the OS or another mechanism cleans them.
- **`MORE_PACKAGES`** — `~/.valtrida/Packages`. Reserved, alongside `PLUGINS_DIR`, for the unimplemented plugin/extension concept.
- **`ASSETS*`** — a family of paths for HTML, CSS, QSS, and icon assets under `~/.valtrida/ASSETS/`. Note that `Styles/icons.py` imports `ASSETS_ICONS_ICO`/`ASSETS_ICONS_SVG` from this module but primarily uses **base64-embedded** icons rather than reading files from these paths — these constants exist as the "on-disk" counterpart/fallback location, not necessarily the primary source at runtime for every icon.

## Note on the hardcoded path bug elsewhere

`Styles/qss.py` contains a **hardcoded absolute path** (`/home/broo-dev/.valtrida/ASSETS/icons/svg/arrow-down.svg`) instead of using `ASSETS_ICONS_SVG` from this module. That is a bug in `Styles/qss.py`, not in this file — this module's job (deriving all paths from `Path.home()` so they're portable) is done correctly; it's just not being used consistently everywhere. See [`../styles/qss.md`](../styles/qss.md) and [`../ARCHITECTURE.md`](../ARCHITECTURE.md#known-issues).

## Related

- [`../core/folders.md`](../core/folders.md) — creates these directories on disk at startup.
- [`../user/local_cypher.md`](../user/local_cypher.md) — writes encrypted user files under `USERS_FILE`.
- [`../styles/icons.md`](../styles/icons.md), [`../styles/qss.md`](../styles/qss.md) — consume the `ASSETS_ICONS_*` constants.
