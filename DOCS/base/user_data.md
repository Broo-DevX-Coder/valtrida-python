# `base/user_data.py`

**Role:** In-memory holder for the currently logged-in user's data (local account info, Binance credentials, and a reserved "official account" concept), plus setter functions and a `UserDataGet` accessor class. This is one of the `base/` registries that lets any module read "who is logged in" without importing the auth module directly.

## Data dicts

```python
USER_LOCAL_INFO = {"name": '', "id": '', "auths_tokens": []}
USER_BINANCE_INFO = {"api_key": '', "api_secret": '', "user_id": '', "account_type": 'SPOT'}
USER_OFFICIAL_ACCOUNT_INFO = {"email": '', "name": '', "token": ''}
```

- **`USER_LOCAL_INFO`** — the current local account's display name, local ID, and any auth tokens.
- **`USER_BINANCE_INFO`** — the decrypted Binance API key/secret for the current session, the associated user ID, and account type (currently always `'SPOT'` — no futures/margin support implied here).
- **`USER_OFFICIAL_ACCOUNT_INFO`** — **currently unused placeholder** for a possible future "official"/cloud-linked account concept (email, name, token). Nothing in the rest of the codebase populates this meaningfully as of this version — treat it as reserved, not a working feature.

All three are **module-level mutable dicts acting as process-wide singletons** — there is no per-window/per-thread isolation. Since this is a single-user desktop app (one logged-in user per running process), this is a reasonable simplification, but it does mean these values must be reset/cleared explicitly on logout rather than relying on object lifecycle.

## Setter functions

- `set_user_local_info(name, id)`
- `set_user_binance_info(api_key, api_secret, user_id, account_type)`
- `set_user_official_account_info(email, name, token)`
- `set_auth_tokens(auths_tokens)`

Each mutates the corresponding dict in place (not replacing the dict object, so any code holding a reference to e.g. `USER_BINANCE_INFO` will see updates without re-fetching it).

## `UserDataGet`

A static-method-only class providing read access:

```python
UserDataGet.get_user_local_info()
UserDataGet.get_user_binance_info()
UserDataGet.get_user_official_account_info()
```

Each simply returns the corresponding module-level dict (by reference, not a copy — callers should treat the returned dict as read-only unless they intend to mutate shared state).

## Security note

`USER_BINANCE_INFO["api_secret"]` holds the **decrypted** API secret in plaintext, in memory, for the duration of the session. This is necessary to sign outgoing Binance requests (see `API/b_accont.py`), but means any code with access to this module can read the secret — be deliberate about what gets logged or displayed, since a log statement that happens to print this dict would leak the secret. See `user/local_cypher.py` for how the secret is protected at rest.

## Related

- [`../user/local_cypher.md`](../user/local_cypher.md) — decrypts credentials from disk into this module at login time.
- [`../api/b_accont.md`](../api/b_accont.md) — consumes `api_key`/`api_secret` from `USER_BINANCE_INFO`.
- [`init.md`](init.md) — `base/__init__.py` re-exports `UserDataGet`.
