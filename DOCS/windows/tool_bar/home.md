# `windows/tool_bar/home.py`

**Role:** `Home` — the "Home" tab (`QWebEngineView`) shown by default in the main window's stacked navigation. Displays the logged-in user's name/UID/account type and total balance; shows a "Login" button when logged out.

## `Backend(QObject)`

One `@Slot()`:

- **`on_login_clicked()`** — publishes a `login_clicked` event on `SystemStream`. `windows/main.py`'s `login_button_clicked()` listener reacts by showing the Login popup (`AuthMain`).

## The embedded page (`HTML`)

Styled with `Styles.css.CSS["MAIN"]`. Shows a header with user name/UID/account-type placeholders and a login button, plus a "Total Balance" card. A large block of the page — Profit & Loss, Open Orders, and Recent Trades cards, including a hardcoded sample row (`ETH/USDT`, `BTC/USDT`) — is present but **entirely commented out** (`<!-- ... -->`). This is aspirational/placeholder UI for features not yet wired up to real data; don't assume Open Orders / Recent Trades / PnL are functional anywhere in the app based on this markup existing in the source.

## `Home(QWebEngineView)`

Same `QWebChannel`/`Backend` setup pattern as `windows/coin.py`/`windows/tool_bar/markets.py`. Notable methods:

- **`update_bilances(total, avilable, frozen)`** *(existing typo "bilances"/"avilable", kept as-is)* — injects the given values into the balance card via `runJavaScript`, but only if `self.uploaded_ok` (i.e. the page has finished its initial load) — calls made before load-finish are silently no-ops rather than queued.
- **`update_user_info(name, uid, type_)`** — same pattern, for the header user-info fields.
- **`loggin_logaout_listner()`** (async) — the same "wait on whichever of `logged_in`/`logged_out` is currently relevant" pattern as `windows/main.py`'s listener of the same name (see [`../main.md`](../main.md)). On login, replaces the login-button area with plain text `"Home Page"`; on logout, restores the login button and resets balances/user info to placeholder dashes.
- **`change_bilances_listner()`** (async) — subscribes to `UserStream`'s `"user_binance_data_changed"` channel (published by `MainWindow.update_user_data_on_ui`) and calls `update_bilances` with the fresh totals whenever a new balance snapshot arrives.

Both listeners are started from `run()`, which is itself triggered via the `loadFinished` signal (not called externally) — so `Home`'s listeners only start once the embedded page has actually loaded.

## Related

- [`../main.md`](../main.md) — subscribes to this file's `login_clicked` events; publishes the `user_binance_data_changed` events this file listens for.
- [`../../styles/css.md`](../../styles/css.md) — `CSS["MAIN"]`.
- [`../../base/tool_bar.md`](../../base/tool_bar.md) — registers this class under the `"Home"` key.
