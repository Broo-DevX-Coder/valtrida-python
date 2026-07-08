# `windows/tool_bar/markets.py`

**Role:** `Markets` — the "Markets" tab (`QWebEngineView`), showing a searchable grid of every USDT trading pair on Binance with live prices, and entry points to open a coin's detail page or its chart popup.

## `Backend(QObject)`

Two `@Slot(str)` methods:

- **`on_coin_clicked(coin)`** — publishes `coin_clicked` on `SystemStream` with `cl_type: "coin"`. `windows/main.py`'s `coin_card_clicked()` opens (or switches to) that coin's `OneCoin` page.
- **`on_pen_clicked(coin)`** — publishes `coin_clicked` with `cl_type: "pen"`. Opens the Charts popup pre-filled for that coin.

Both events are marked `headen: True` (low-priority for the system log listener — see `core/logs.py`).

## The embedded page (`HTML`)

Entirely self-sufficient JS, styled with `CSS["MAIN"]`:

- **`load_symbols()`** — fetches `/api/v3/exchangeInfo`, filters for `USDT`-suffixed symbols, builds `coin_list`, then calls `render_coins()`.
- **`render_coins(filter="")`** — rebuilds the coin grid, filtering by substring match against the search box. Each card has a coin name/price and a "pen" (✏) icon; clicking the card body calls `coin_clicked(coin)`, clicking the pen calls `pen_clicked(coin)` (with `e.stopPropagation()` so it doesn't also trigger the card click).
- **`start_ws()`** — opens `wss://stream.binance.com:9443/ws/!miniTicker@arr`, Binance's **all-market mini-ticker stream** (every symbol, all at once), and updates each visible coin card's price live as ticks arrive.
- The search input re-renders the grid on every keystroke (no debounce) — filtering is purely client-side against the already-fetched `coin_list`, not a new API call per keystroke.

**Design note (same caveat as `windows/coin.py`):** this page's networking is independent JS `fetch`/`WebSocket` calls, entirely outside `API/market.py`'s connection management and `core/errors.py`'s rate-limit handling. The `!miniTicker@arr` firehose stream in particular is a fairly heavy subscription (every symbol on Binance, continuously) — if Binance ever rate-limits or drops this connection, there is no reconnect logic in this JS and no visibility into it from the app's error pipeline; the market grid would simply stop updating until the tab/page is reloaded.

## `Markets(QWebEngineView)`

Structurally identical to `Home`/`OneCoin` — `QWebChannel` setup, HTML load, Back/Forward/Reload context menu, `run()` = `self.show()`. No Python-side listeners on `UserStream`/`SystemStream` in this file (unlike `Home`/`Wallet`) — all its interactivity flows outward via the `Backend` slots, not inward via stream subscriptions.

## Related

- [`../main.md`](../main.md) — reacts to `coin_clicked` events published from here.
- [`../coin.md`](../coin.md) — the page opened for `cl_type == "coin"`.
- [`../chart_popup.md`](../chart_popup.md) — the popup opened for `cl_type == "pen"`.
- [`../../styles/css.md`](../../styles/css.md) — `CSS["MAIN"]`.
