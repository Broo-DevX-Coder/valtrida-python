# `user/widgets/register_via_binance_api.py`

**Role:** `RegisterViaBinanceAPI` — the "API Register" tab of `AuthMain`. Lets a new user save a local account by providing a Binance API key/secret plus a local username and password, so they can later log back in via `LoggingWidget` without re-entering their Binance keys.

## Form

Five `QLineEdit`s (username, API key, API secret, password, password confirmation — both password fields use `QLineEdit.Password` echo mode), manually positioned, plus a "Register" submit button. The button is enabled only once **every** field is non-empty **and** the two password fields match (`rigister_texts_slot` *(existing typo, kept as-is)* recomputes `password_confirmed` whenever either password field changes, then gates the button on `all(self.items["true_v"].values())`).

## `register()` (async, triggered by the submit button)

1. Disables the submit button.
2. If `self.items["status"] == "reset_accont"` *(existing typo, kept as-is)*: deletes any existing `.enc` file for the entered username first — this is a **reset/overwrite path**, though nothing in the currently-read codebase actually sets `self.items["status"]` to `"reset_accont"` (it's always initialized to `"normal"` and never reassigned elsewhere in this file); this looks like unfinished/planned functionality for a future "reset account" flow rather than something reachable from the current UI.
3. Calls `get_account_info(API_key, API_secret)` to validate the entered Binance credentials against the live API **before** saving anything locally.
4. Validates, in order: password length (`>= 8` chars, else "Password Error"), username format (`is_valid_string` — must match `[A-Za-z0-9_]+` only, else "UserName Error"), then the Binance API validation result (`"INVALID_API_KEY"` vs. any other failure, mirroring `LoggingWidget.login`'s two error messages).
5. On success: generates a random 8-digit `us_id` (`random.randint(10_000_000, 99_999_999)` — **not** cryptographically unique; this is a locally-generated identifier, not the actual Binance UID, though it's stored alongside `auther.UID` which *is* the real Binance UID from `get_account_info`), builds the credentials dict, and calls `CipherUserData().save_new_local_user(password, data)`.
   - If saving succeeded: shows a success popup; on dismissal, calls `register_success(data)`.
   - If saving failed (username already has a saved `.enc` file): shows a "Repeated user name" error.

## `register_success(data)`

Same pattern as `LoggingWidget.login_success` — writes credentials into `base/user_data.py`'s in-memory globals and publishes `logged_in` on `UserStream`, immediately logging the newly-registered user in without requiring a separate login step.

## Related

- [`../local_cypher.md`](../local_cypher.md) — `CipherUserData.save_new_local_user`.
- [`../../api/b_accont.md`](../../api/b_accont.md) — `get_account_info`.
- [`../../core/pop_messages.md`](../../core/pop_messages.md) — `pup_message`.
- [`../../base/files_folders.md`](../../base/files_folders.md) — `USERS_FILE`.
- [`login.md`](login.md) — the sibling "Login" tab, sharing the same verification/success pattern.
