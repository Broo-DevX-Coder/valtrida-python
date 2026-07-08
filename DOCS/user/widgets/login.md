# `user/widgets/login.py`

**Role:** `LoggingWidget` *(existing typo "Logging" for "Login" in the class name, kept as-is)* — the Login tab of `AuthMain`. Lets a returning user unlock their previously-saved local credentials with a username + password.

> Note: `user/widgets/` has no `__init__.py` — it's an implicit namespace package (Python 3 supports importing from a directory without `__init__.py`), which works fine here since it's imported as `from .widgets.login import LoggingWidget` and never needs package-level re-exports.

## `LoggingWidget(QWidget)`

### Form

Two `QLineEdit`s (username, password — password uses `QLineEdit.Password` echo mode) and a "Login" submit button, all manually positioned (no layout manager). The submit button starts disabled and is only enabled once **both** fields are non-empty/non-whitespace (`login_texts_slot`, connected to both fields' `textChanged` signals, tracks each field's validity in `self.items["true_v"]` and enables the button via `all(...)`).

### `login()` (async, triggered by the submit button)

1. Disables the submit button (prevents double-submission while the async flow runs).
2. Calls `CipherUserData().get_local_user(password, username)` to decrypt the locally saved `.enc` file for that username.
3. **If decryption succeeded** (`data[0] == True`): calls `API.b_accont.get_account_info(api_key, api_secret)` to **verify the saved credentials are still valid against Binance** (a saved API key could have been revoked/rotated since it was saved) — this means every login re-validates against the live API, it doesn't just trust the locally decrypted data.
   - If that check fails with `"INVALID_API_KEY"`: shows an error popup explaining the key is invalid/lacks permissions, and re-enables the button (`self.ena`) when dismissed.
   - If it fails for any other reason: shows a generic "API Secreat Error" popup.
   - If it succeeds: shows a success popup; on dismissal, calls `login_success(data[1])`.
4. **If decryption failed** with `"incorrect_info"`: shows a "wrong password" warning.
5. **If decryption failed** with `"user_not_found"`: shows a "user not found" warning.

In all failure branches, `self.ena` (re-enables the submit button) is passed as the popup's dismissal callback — so the button stays disabled until the user acknowledges the error message, preventing rapid repeated login attempts.

### `login_success(data)`

Writes the decrypted credentials into the in-memory `base/user_data.py` globals via `set_user_binance_info`/`set_user_local_info`, then publishes `logged_in` on `UserStream` — this is the event `windows/main.py`'s `loggin_logaout_listner` and every tab's own login/logout listeners are waiting for.

## Standalone run mode

Same pattern as other files: an `if __name__ == "__main__":` block for isolated testing with a manually-driven `qasync` loop.

## Related

- [`../local_cypher.md`](../local_cypher.md) — `CipherUserData.get_local_user`.
- [`../../api/b_accont.md`](../../api/b_accont.md) — `get_account_info`.
- [`../../core/pop_messages.md`](../../core/pop_messages.md) — `pup_message`.
- [`../../base/user_data.md`](../../base/user_data.md) — `set_user_binance_info`, `set_user_local_info`.
- [`../window.md`](../window.md) — hosts this widget as the "Login" tab.
- [`register_via_binance_api.md`](register_via_binance_api.md) — the sibling "API Register" tab, sharing the same success/verification pattern.
