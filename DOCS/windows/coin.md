# `windows/coin.py`

**Role:** `OneCoin` — a per-coin detail page (`QWebEngineView`), opened when a user clicks a coin card in the Markets tab. Shows current price, 24h stats, a price history chart, and a live-updating ticker, entirely via embedded HTML/JS that talks directly to Binance's public REST and WebSocket APIs from the browser context (not routed through `API/market.py`).

## `Backend(QObject)`

Exposes one `@Slot(str)` to the embedded JS:

- **`on_pen_clicked(coin)`** — publishes a `coin_clicked` event on `SystemStream` with `cl_type: "pen"`, `headen: True` (marked as a "hidden"/low-priority system event — see `core/logs.py`'s `system_logs_listener`, which skips `headen` events unless `DEBUG_MODE` is on). `windows/main.py`'s `coin_card_clicked()` listener reacts to this by opening the chart popup pre-filled for this coin.

## The embedded page (`HTML`)

A self-contained HTML document with the coin symbol injected via a `"<Here-Coin-Symbol>"` placeholder string replacement (`HTML.replace("<Here-Coin-Symbol>", coin)`) — note this is a simple string substitution, not a templating engine, so if a coin symbol ever contained that exact placeholder text it would break; in practice Binance symbols are simple alphanumeric strings so this isn't a real risk. Styled with `Styles.css.CSS["MAIN"]`. The page:

- Fetches `/api/v3/ticker/24hr` for the current price, 24h change, high/low, volume — directly from the browser's JS context via `fetch()`, not via `aiohttp`/Python.
- Fetches `/api/v3/klines` (1h interval, last 60 candles) and renders a line chart using **Chart.js**, loaded from a CDN (`cdn.jsdelivr.net`) — this is a **different charting library** than the candlestick popup chart (`charts/candels_shart.py`, which uses KLineCharts embedded as base64). There's no shared charting code between this page and the main chart popup.
- Opens a raw WebSocket to `wss://stream.binance.com:9443/ws/{symbol}@miniTicker` for live price/volume/high/low updates, updating the DOM directly on each message.
- Loads the coin's icon from an external CDN: `cdn.jsdelivr.net/gh/vadimmalykhin/binance-icons/crypto/{coin}.svg` — this depends on that third-party GitHub-hosted icon repo remaining available and covering the given coin; if the coin isn't in that repo or the CDN is unreachable, the icon will simply fail to load (no fallback icon is set).
- A "pen" (✏) button in the header calls back into Python via `backend.on_pen_clicked(coin)`.

**Design note:** Unlike the rest of the app's networking (which is centralized through `API/market.py` with rate-limit/ban handling via `core/errors.py`), this page does its own independent `fetch`/`WebSocket` calls straight from JavaScript. This means 429/418/403 responses hit here are **not** caught by the app's critical-error pipeline — a rate limit triggered by this page's polling would just silently fail in the browser console rather than surfacing the app's "Too many requests" popup.

## `OneCoin(QWebEngineView)`

Structurally identical to `windows/tool_bar/home.py`'s `Home`/`markets.py`'s `Markets` classes: sets up a `QWebChannel` with the `Backend` object, loads the HTML, wires a Back/Forward/Reload context menu, and starts on `loadFinished`. `run()` is just `self.show()`. `closeEvent` closes any child `self.windows`, cancels `self.async_tasks`, and unregisters from `AsyncController`.

## Related

- [`main.md`](main.md) — `MainWindow.coin_card_clicked()` creates and manages `OneCoin` instances (one per coin, cached indefinitely by symbol) and reacts to the "pen" click here.
- [`../styles/css.md`](../styles/css.md) — `CSS["MAIN"]`.
- [`chart_popup.md`](chart_popup.md) — opened in response to the "pen" click published here.
