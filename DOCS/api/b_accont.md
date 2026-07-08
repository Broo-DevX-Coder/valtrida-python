# `API/b_accont.py`

**Role:** Authenticated Binance account access — signed REST calls to fetch account balances and compute a total portfolio value in USDT. (Filename keeps the project's existing shorthand/typo style — "b_accont" — left as-is.)

## `create_signature(params, secret)`

Builds Binance's required HMAC-SHA256 request signature: joins `params` into a `key=value&key=value...` query string (in dict insertion order) and signs it with the API secret using `hmac.new(..., hashlib.sha256).hexdigest()`. This mirrors Binance's documented signing scheme exactly — do not reorder params after computing the signature, or the signature will no longer match.

## `get_account_info(api_key, api_secret, session=None)`

Calls Binance's `/api/v3/account` endpoint (`GET`, signed):

1. Builds params with a fresh `timestamp` (current time in ms) and appends the HMAC signature.
2. Sends the request with `X-MBX-APIKEY: <api_key>` header.
3. Optionally reuses a caller-provided `aiohttp.ClientSession` (closing it only if this function opened it itself — the `close_session` flag pattern is used consistently across this module so long-lived sessions from `AsyncController`/`SINGLE_API` are never closed prematurely).
4. Response handling:
   - `200` → returns `(True, response_json)`, unless the body indicates a Binance-level error.
   - `400` → returns `(False, "SECREAT_KEY_ERROR")` *(existing typo, not a doc error — the actual returned string literal is `"SECREAT_KEY_ERROR"`)* — the secret doesn't match the given API key.
   - `401` → returns `(False, "INVALID_API_KEY")`.
   - anything else → returns `(False, "UNKNON_ERROR")` *(existing typo, kept as-is)*, and reports a `CONNECTION_{status}` error.
   - any exception → returns `(False, "CONNECTION_ERROR")`.

All error paths call the module's `error_()` helper, which wraps `core.error(...)` with this module's name as the source (see [`../core/errors.md`](../core/errors.md)).

## `get_prices(session=None)`

Calls Binance's public `/api/v3/ticker/price` endpoint (unsigned — this is public data, doesn't need `api_key`) and returns a `{symbol: price}` dict for every symbol Binance returns. Returns `False` on any non-200 response or exception.

## `get_total_balance_in_usdt(api_key, api_secret, session=None)`

Combines the two functions above to compute a portfolio total:

1. Calls `get_account_info` — bails out returning `False` if it fails.
2. Calls `get_prices` — bails out returning `False` if it fails.
3. For every non-zero balance entry:
   - If the asset **is** `USDT`, adds it directly to `total_usdt`/`free_amount`/`locked_amount`.
   - Otherwise, looks up `{asset}USDT` in the prices map and converts `free`/`locked`/total amounts to USDT at that rate.
   - If no direct `{asset}USDT` pair exists (e.g. an asset only tradable against BTC or another quote), that asset is **silently excluded** from the total — this is a known limitation, not a bug: the portfolio total may undercount assets without a direct USDT pair.
4. Returns `(total_usdt, free_amount, locked_amount, balances)` — the last element being the raw balances list from Binance, useful for rendering a per-asset breakdown (see `windows/tool_bar/wallet.py`).

## Related

- [`../user/local_cypher.md`](../user/local_cypher.md) — where the `api_key`/`api_secret` passed into these functions come from (decrypted locally after login).
- [`../windows/tool_bar/wallet.md`](../windows/tool_bar/wallet.md) — primary consumer of `get_total_balance_in_usdt`.
- [`market.md`](market.md) — the unauthenticated counterpart to this module.
