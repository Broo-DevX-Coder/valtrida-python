# `windows/tool_bar/wallet.py`

**Role:** `Wallet` — the "Wallet" tab (`QWebEngineView`), showing total balance plus a per-asset breakdown of the logged-in user's Binance spot holdings.

## `Backend(QObject)`

One `@Slot()`, identical in purpose to `Home`'s:

- **`on_login_clicked()`** — publishes `login_clicked` on `SystemStream`, triggering the Login popup.

## The embedded page (`HTML`)

Styled with `CSS["MAIN"]`. Header with login button, a total-balance card, and an empty `#pairs-list__wallet` container populated entirely from Python (see `_update_wallet` below) rather than via embedded JS fetching data itself — unlike `Home`/`Markets`/`OneCoin`, this page does **not** make its own `fetch()`/`WebSocket` calls; all data arrives via `runJavaScript` injections driven by `UserStream` events. A "Recent Trades" table with hardcoded sample rows exists but is commented out, same as in `Home`.

## `Wallet(QWebEngineView)`

- **`update_bilances(total, avilable, frozen)`** — same pattern as `Home`'s method, updates the total-balance card.
- **`_update_wallet(balances)`** — builds one HTML row per non-zero asset in the `balances` list (Binance's raw per-asset `{asset, free, locked}` entries, as returned by `API/b_accont.py`'s `get_total_balance_in_usdt`), then replaces `#pairs-list__wallet`'s innerHTML in one shot via `runJavaScript`. Notable details:
  - Assets with `free + locked == 0` are skipped entirely (no rows for zero-balance assets).
  - The displayed combined amount is rounded to 2 decimals **only if the asset is a recognized stablecoin** (`asset_name.upper() in STABLECOINS_USD`); non-stablecoin assets show the full unrounded float — so e.g. `USDT` shows as `123.45` but a small-value altcoin might render as a long unrounded decimal string. This is a deliberate (if inconsistently-applied-looking) choice: stablecoins are ~$1 so 2-decimal rounding is meaningful there, while other assets often have very small unit values where 2-decimal rounding would hide the actual quantity.
  - Each row's icon comes from `https://api.elbstream.com/logos/crypto/{asset}` (a **different** external icon source than `windows/coin.py`'s `jsdelivr`-hosted icons) — another example of icon sourcing being inconsistent/duplicated across the codebase rather than centralized.
- **`update_wallet(balances=[])`** — guards `_update_wallet` behind `self.uploaded_ok`, same pattern as `update_bilances`. Note the mutable default argument `balances=[]` — harmless here since the list is only read (iterated), never mutated, but worth flagging as a general Python anti-pattern if this method is ever changed to append to `balances`.
- **`change_bilances_listner()`** (async) — subscribes to `UserStream`'s `"user_binance_data_changed"` channel and calls both `update_bilances` and `update_wallet(data["balances_wallet"])` whenever new data arrives — this is the single feed for both the total-balance card and the per-asset list.
- **`loggin_logaout_listner()`** (async) — same shape as `Home`'s: on login, replaces the login button with "Your crypto overview" text; on logout, restores the login button and clears both the wallet list and balance card back to placeholders.

Both listeners are started in `run()`, itself wired to `loadFinished`.

## Related

- [`../main.md`](../main.md) — publishes the `user_binance_data_changed` events this page consumes.
- [`../../api/b_accont.md`](../../api/b_accont.md) — the source of the `balances` data structure rendered here.
- [`../../base/utils.md`](../../base/utils.md) — `STABLECOINS_USD`.
- [`home.md`](home.md) — near-identical login/logout listener pattern.
