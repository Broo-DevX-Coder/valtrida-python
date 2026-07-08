# `Styles/__init__.py`

**Role:** Defines `DARK_TO_LIGHT_COLORS` — the single source-of-truth color-substitution table used to convert every dark-themed stylesheet in the app into a light-mode equivalent via simple string replacement.

## `DARK_TO_LIGHT_COLORS`

A flat `dict` mapping every dark-theme hex color literal used anywhere in `Styles/qss.py`, `Styles/css.py`, and `Styles/plot_styles.py` to a corresponding light-theme hex color, grouped by comment into categories: Main Backgrounds, Popup/Secondary Backgrounds, Borders, Text Colors, Secondary Text, Brand Accent Colors, Status Colors, Table Alternates, Misc, Markets Cards, and Body background image.

**How it's consumed:** `Styles/mods.py`'s `change_to_light_mode(content)` does a straightforward `content.replace(dark, light)` for every key in this dict, over the full text of a QSS/CSS string. This means:
- **Every color used in dark mode must have an entry here**, or it will simply stay dark-colored when `COLOR_MODE == "light"` — there's no fallback/computed conversion (e.g. no HSL-based auto-lightening), it's a fully manual, hardcoded 1:1 mapping. Adding a new hardcoded color literal to any stylesheet file without also adding it here will silently break light-mode theming for that specific color, with no error or warning.
- Because it's a plain substring replacement (not a CSS-aware parser), colors are matched purely by their hex string — a color used in two different semantic contexts (e.g. `#EAECEF` used for both text and possibly a border somewhere) always maps to the exact same light-mode replacement everywhere it appears, with no way to give it different meanings in different contexts. This works for the current stylesheets but would need re-thinking if a future style ever needed context-sensitive color mapping (i.e. the same dark literal needing two different light replacements depending on where it's used).
- Order doesn't matter for correctness (no overlapping substrings among the current color literals), but this file must be re-audited any time a new stylesheet color is introduced elsewhere in `Styles/`.

## Related

- [`mods.md`](mods.md) — `change_to_light_mode`, the sole consumer of this dict.
- [`qss.md`](qss.md), [`css.md`](css.md), [`plot_styles.md`](plot_styles.md) — the stylesheets whose dark-mode literals this dict must cover.
- [`../root/config.md`](../root/config.md) — `COLOR_MODE`, the setting that decides whether this conversion runs at all.
