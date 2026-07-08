# `base/tool_bar.py`

**Role:** Registry for the main window's navigation tool bar — both the "stacked" (tab-like) screens and the separate popup windows — plus the button-label mappings used to build the tool bar UI.

## Contents

```python
MW_STACKED_WINDOWS = {
    #"Home":Home,
    #"Trades":Trades(),
    #"Wallet":Wallet,
}

MW_WINDOW_STAKED_BUTTONS = {
    "home": "Home",
    "markets": "Markets",
    "wallet": "Wallet"
}

MW_POPUP_WIDOWS_BUTTONS = {
    #"charts":"Charts",
}

MW_POPUP_WIDOWS = {}
```

- **`MW_STACKED_WINDOWS`** — key is the screen's display name (e.g. `"Home"`), value is the window/widget **class** to instantiate for it. Populated by `prepare.py`:
  ```python
  tool_bar.MW_STACKED_WINDOWS["Home"] = home.Home
  tool_bar.MW_STACKED_WINDOWS["Wallet"] = wallet.Wallet
  tool_bar.MW_STACKED_WINDOWS["Markets"] = markets.Markets
  ```
  `windows/main.py` reads this to build its `QStackedWidget` of tabs. The commented-out `"Trades":Trades()` line hints that a "Trades" tab was previously planned/removed or is still pending — as of this version, there is no `Trades` tab implemented.
- **`MW_WINDOW_STAKED_BUTTONS`** *(existing typo "STAKED" for "STACKED", kept as-is)* — a lowercase-key-to-display-name map (`"home" → "Home"`), likely used to wire up tool bar button object names/icons to the corresponding entry in `MW_STACKED_WINDOWS`.
- **`MW_POPUP_WIDOWS_BUTTONS`** *(existing typo "WIDOWS" for "WINDOWS", kept as-is)* — analogous button-label map for popup windows; currently empty (only a commented example).
- **`MW_POPUP_WIDOWS`** — key is the popup's display name, value is a dict `{"m": <class>, "ft?": <bool>}` where `"m"` is the window class and `"ft?"` presumably means "first time?" (whether this is the first time the popup is being opened, likely used to decide whether to run one-time setup). Populated by `prepare.py`:
  ```python
  tool_bar.MW_POPUP_WIDOWS["Charts"] = {"m": ChowSharts, "ft?": True}
  tool_bar.MW_POPUP_WIDOWS["Login"] = {"m": AuthMain, "ft?": True}
  ```

## Why this exists

Same rationale as `base/charts.py`: `windows/main.py` needs to know about every tab/popup window class, but those window modules must not need to import `windows/main.py` back. Routing registration through this module (populated once from `prepare.py`) breaks that potential cycle.

## Related

- [`../root/prepare.md`](../root/prepare.md) — populates all four dicts here.
- [`../windows/main.md`](../windows/main.md) — primary consumer, builds the nav tool bar from these registries.
- [`../windows/tool_bar/home.md`](../windows/tool_bar/home.md), [`markets.md`](../windows/tool_bar/markets.md), [`wallet.md`](../windows/tool_bar/wallet.md) — the classes registered into `MW_STACKED_WINDOWS`.
- [`../windows/chart_popup.md`](../windows/chart_popup.md), [`../user/window.md`](../user/window.md) — the classes registered into `MW_POPUP_WIDOWS`.
