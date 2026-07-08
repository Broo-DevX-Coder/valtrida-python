# `windows/main.py`

**Role:** Defines `MainWindow` — the app's top-level `QMainWindow` — plus `OverlayPopup`, the generic "modal-over-the-main-window" wrapper used for popup windows (Login, Charts). This is the busiest UI orchestration file: it builds the nav tool bar from `base/tool_bar.py`'s registries, wires up the login/logout and coin-click event flows, and polls Binance balances once logged in.

## `OverlayPopup(QWidget)`

A frameless, translucent-background widget that sits on top of `MainWindow`, centering an arbitrary `content_widget` and drawing a semi-transparent black backdrop (`QColor(0,0,0,180)`) behind it via a custom `paintEvent`. Every entry in `MW_POPUP_WIDOWS` gets wrapped in one of these (see `MainWindow.__init__`). Provides:
- `center_content()` — repositions the content widget in the middle of the overlay.
- `resizeEvent` — keeps the overlay covering the full parent window and re-centers content on resize.
- `run()` / `specific_show(*args, **kwargs)` — delegate to the wrapped content widget's own `run()`/`specific_show()` methods (e.g. `ChowSharts.specific_show(coin=...)`).

Note the `close_btn` created in `__init__` is positioned using the *tool bar's* button-count geometry formula (`(len(MW_WINDOW_STAKED_BUTTONS)+len(MW_POPUP_WIDOWS_BUTTONS))*62`), which looks like a copy-paste artifact from the tool bar sizing logic rather than something meaningful for a single "Close" button's width — cosmetic, but worth knowing if the popup's close button appears oddly sized/positioned when the tool bar has many buttons.

## `MainWindow(QMainWindow)`

### Construction

- Sets a minimum size of `1100x800`, a dynamic window title via `self.set_window_t` (includes the local username once logged in), and the app icon from `ASSETS_ICONS_ICO/main.ico`.
- Snapshots the four `base/tool_bar.py` registries (`MW_STACKED_WINDOWS`, `MW_POPUP_WIDOWS`, `MW_WINDOW_STAKED_BUTTONS`, `MW_POPUP_WIDOWS_BUTTONS`) into `self.FIRST_*` copies — used later to detect **runtime additions** to these registries (see "Live registry watching" below).
- Builds `self.stack` (`QStackedWidget`) by instantiating every class in `MW_STACKED_WINDOWS` and adding it as a page; builds `self.popup_windows` by instantiating every class in `MW_POPUP_WIDOWS` and wrapping each in an `OverlayPopup`.
- Builds the bottom tool bar (`self.tool_bar`) from `MW_WINDOW_STAKED_BUTTONS` and `MW_POPUP_WIDOWS_BUTTONS`: one `QPushButton` per entry, using an SVG icon from `ASSETS_ICONS_SVG/{key}.svg`, wired to `cahnge_window` (stacked tabs) or `hide_show_popup_window` (popups) respectively via `functools.partial`.
- The "Home" tab button starts checked by default.

### Tab/popup switching

- **`cahnge_window(w)`** *(existing typo "cahnge" for "change", kept as-is)* — updates the window title, switches `self.stack`'s current widget, and updates which tool bar button is checked.
- **`hide_show_popup_window(t)`** — the first time a given popup is shown (`self.popup_windows[t]["ft?"]` is `True`), calls its `run()` once (lazy first-time init) before flipping `"ft?"` to `False`; every time, shows the popup and unchecks its tool bar button (so popup buttons act like triggers, not persistent toggles).

### Balance polling — `update_user_data_on_ui()` (async)

Runs continuously for the lifetime of the window (started in `run()`). While `self.logged_in` is `False`, just sleeps 10s in a loop doing nothing. Once logged in:
1. Fetches `get_total_balance_in_usdt(...)` using the current session's credentials.
2. Pushes `user_local_info`/`user_data_changed` onto `UserStream` unconditionally (updates the Home tab's user info even if the balance fetch fails).
3. If the balance fetch succeeded, rounds totals to 2 decimals and pushes `binance_balances`/`user_binance_data_changed` onto `UserStream` — this is what `Home` and `Wallet` tabs listen for to update their displayed balances.
4. If the balance fetch failed (`balances == False`), sleeps 5s and retries the whole loop iteration (skipping the normal 10s sleep) rather than giving up.
5. Otherwise sleeps 10s before polling again — **this is the sole heartbeat balance refresh interval for the entire app**; there's no push-based balance stream from Binance, only this poll.

### Event listeners started by `run()`

`run()` starts seven background tasks (all tracked via `AsyncController.async_m`) and calls `self.show()`:

- **`loggin_logaout_listner()`** *(existing typo, kept as-is)* — the central login/logout state machine. Subscribes to both `UserStream`'s `"logged_in"` and `"logged_out"` channels; while `self.logged_in == False`, waits only on the `"logged_in"` channel (ignoring logout events, since you can't log out while not logged in), and vice versa. On login: hides the Login popup, waits 1s (presumably to let credential state settle before polling), and starts `update_user_data_on_ui()` as a tracked task. On logout: cancels that task if it's still running.
- **`coin_card_clicked()`** — subscribes to `SystemStream`'s `"coin_clicked"` channel (published by `windows/tool_bar/markets.py` and `windows/coin.py`'s `Backend` classes). For `cl_type == "coin"`: opens (or switches to, if already open) a dedicated `OneCoin` stacked page named `f"{coin}_COIN"` — **coin pages are created lazily and never removed**, so navigating to many different coins over a session will accumulate stacked widgets indefinitely (a minor memory-growth known issue, not catastrophic since each `OneCoin` is fairly lightweight, but worth noting). For `cl_type == "pen"`: shows the Charts popup pre-filled for that coin via `specific_show(coin=coin)`.
- **`login_button_clicked()`** — subscribes to `SystemStream`'s `"login_clicked"` channel (published from the Home/Wallet tabs' login buttons) and shows the Login popup.
- **`_on_change_MW_STACKED_WINDOWS()`, `_on_change_MW_POPUP_WIDOWS()`, `_on_change_MW_WINDOW_STAKED_BUTTONS()`, `_on_change_MW_POPUP_WIDOWS_BUTTONS()`** — see "Live registry watching" below.

### Live registry watching

Each of the four `_on_change_*` coroutines polls its corresponding `base/tool_bar.py` dict **every second**, comparing it against the snapshot taken at `MainWindow.__init__` time. If new keys have appeared (e.g. a hypothetical plugin registering a new tab at runtime after the window was already built), the relevant tab/popup/button is instantiated and added on the fly, and the snapshot is updated. **This only handles additions, not removals or replacements** — if an existing key's value changes or a key is deleted from the registry, these watchers will not detect or react to that. As of this version, nothing in the codebase actually adds entries to these registries after `prepare.py` runs at startup, so this machinery is effectively dormant infrastructure for a future plugin system, not something exercised in normal use.

### Shutdown

**`closeEvent`** closes every window in `self.windows` (currently only ever populated with popup window entries — see `__init__`), cancels tracked async tasks, unregisters from `AsyncController`, publishes an `end_of_program` event on `SystemStream`, and calls `sys.exit()` — closing the main window terminates the entire process, not just that window.

## Related

- [`../base/tool_bar.md`](../base/tool_bar.md) — the four registries this file consumes and watches.
- [`../base/user_data.md`](../base/user_data.md) — `USER_LOCAL_INFO`, `USER_BINANCE_INFO`.
- [`../api/b_accont.md`](../api/b_accont.md) — `get_total_balance_in_usdt`.
- [`coin.md`](coin.md) — `OneCoin`, opened from `coin_card_clicked`.
- [`../user/window.md`](../user/window.md) — `AuthMain`, one of the popups wrapped in `OverlayPopup`.
- [`chart_popup.md`](chart_popup.md) — `ChowSharts`, the other popup.
- [`tool_bar/home.md`](tool_bar/home.md), [`tool_bar/markets.md`](tool_bar/markets.md), [`tool_bar/wallet.md`](tool_bar/wallet.md) — the stacked tab classes.
