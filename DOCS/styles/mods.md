# `Styles/mods.py`

**Role:** The light/dark theming switch. On import, if `config.COLOR_MODE == "light"`, rewrites every stylesheet string in `Styles.qss.QSS` and `Styles.css.CSS` in place, converting their dark-mode hex colors to light-mode equivalents.

## `change_to_light_mode(content)`

Iterates every `(dark, light)` pair in `Styles/__init__.py`'s `DARK_TO_LIGHT_COLORS` dict and does a plain `content.replace(dark, light)` for each — a full-text substring substitution, not a CSS/QSS parser. Order of iteration doesn't matter for the current color set (no dark literal is itself a substring of another dark literal in a way that would cause double-replacement issues), but this is a fragile assumption that would need re-checking if new colors are ever added to the table.

## Module-level execution

```python
if COLOR_MODE == "light":
    from .qss import QSS
    from .css import CSS

    QSS["BINANCE"] = change_to_light_mode(QSS["BINANCE"])
    QSS["MAIN_W_TOOL_BAR"] = change_to_light_mode(QSS["MAIN_W_TOOL_BAR"])
    QSS["POPUP_W"] = change_to_light_mode(QSS["POPUP_W"])
    QSS["AUTH_TOOL_BAR"] = change_to_light_mode(QSS["AUTH_TOOL_BAR"])
    CSS["MAIN"] = change_to_light_mode(CSS["MAIN"])
```

This runs **once**, at import time — meaning **`Styles/mods.py` must be imported before any consumer reads `QSS`/`CSS`**, or those consumers will get the still-dark-mode strings. In practice this works because `prepare.py`'s import ordering ensures `Styles.mods` is imported early during app startup (see [`../root/prepare.md`](../root/prepare.md)), before any window classes are constructed. `Styles.plot_styles` (the `pyqtgraph` theme) is **not** touched by this module — it does its own independent light-mode check inline via the `COL(...)` lambda (see [`plot_styles.md`](plot_styles.md)) rather than being converted here, so there are two separate/parallel mechanisms for dark→light conversion in this codebase depending on which stylesheet system is involved (raw QSS/CSS string tables here, vs. a live lookup-per-call in `plot_styles.py`).

## Related

- [`init.md`](init.md) — `DARK_TO_LIGHT_COLORS`.
- [`qss.md`](qss.md), [`css.md`](css.md) — the stylesheets mutated by this module.
- [`plot_styles.md`](plot_styles.md) — the separate, non-`mods.py`-based light-mode mechanism for chart theming.
- [`../root/config.md`](../root/config.md) — `COLOR_MODE`.
- [`../root/prepare.md`](../root/prepare.md) — import ordering that makes this module's side effect take hold before it's needed.
