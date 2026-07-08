# `Styles/icons.py`

**Role:** Holds every app icon (SVG for tool bar buttons, ICO for window icons) as base64-encoded string literals, keyed by filename, in the module-level `svg_icons` and `ico_icons` dicts.

## `svg_icons`

Maps filenames (`"charts.svg"`, `"home.svg"`, `"profile.svg"`, `"markets.svg"`, `"trade.svg"`, `"trades.svg"`, `"wallet.svg"`, `"arrow-down.svg"`) to base64-encoded SVG source. These correspond to the tool bar icon keys referenced in `base/tool_bar.py`'s `MW_WINDOW_STAKED_BUTTONS`/`MW_POPUP_WIDOWS_BUTTONS` dicts (e.g. `{"home": "Home", "markets": "Markets", ...}` — `windows/main.py` builds each button's icon path as `os.path.join(ASSETS_ICONS_SVG, f"{icon}.svg")`).

## `ico_icons`

Maps filenames (e.g. `"charts.ico"`) to base64-encoded `.ico` binary data — used for window icons (`main.ico`, `charts.ico`, etc.) via `QIcon(os.path.join(ASSETS_ICONS_ICO, "...ico"))` calls throughout `windows/`, `user/window.py`, `windows/chart_popup.py`.

**Notable:** one of the sampled `.ico` entries in this file's base64 payload contains embedded C2PA/JUMBF metadata (content-provenance metadata used by tools like Adobe/OpenAI image generators to record "this was AI-generated" attribution) baked into the icon's raw bytes — visible as `c2pa.claim`/`ChatGPT`/`org.cai.c2pa_rs` strings inside the decoded binary. This doesn't affect the icon's function (it displays normally as an image), but is worth knowing if licensing/provenance of the app's icon assets is ever audited — at least one icon was generated via an AI image tool with that metadata intact.

## Relationship to `base/files_folders.py`

This module imports `ASSETS_ICONS_ICO`/`ASSETS_ICONS_SVG` (the on-disk paths where these icons are expected to live) but — based on this file's own content — doesn't appear to itself decode-and-write these base64 blobs into files at those paths within this file; that write-out step (if it exists) happens elsewhere in the startup sequence (see `prepare.py`/`base/files_folders.py`), with this module serving as the **embedded source of truth** for icon bytes so the app can regenerate its assets folder even if it's deleted, without needing to ship separate binary icon files alongside the Python source.

## Related

- [`../base/files_folders.md`](../base/files_folders.md) — `ASSETS_ICONS_ICO`, `ASSETS_ICONS_SVG`, and the logic that materializes these assets to disk.
- [`../base/tool_bar.md`](../base/tool_bar.md) — the icon-key registries consumed by `windows/main.py` when building tool bar buttons.
