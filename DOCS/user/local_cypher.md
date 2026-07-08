# `user/local_cypher.py`

**Role:** `CipherUserData` — encrypts and decrypts each local user's saved credentials (Binance API key/secret, username) to/from `.enc` files on disk, so the app never stores API keys in plaintext. This is what backs both "remember me"-style local login (`user/widgets/login.py`) and account registration (`user/widgets/register_via_binance_api.py`).

## Encryption scheme

Uses AES-GCM (`AES.MODE_GCM`) with a password-derived key:

- **`new_register_ciphering(password, data)`** — generates a random 16-byte salt, derives a 32-byte key from the password via `PBKDF2` (200,000 iterations, SHA-256 — a deliberately slow KDF to resist brute-force on a stolen `.enc` file), base64-encodes the JSON-serialized `data` dict, then AES-GCM encrypts it. Returns the concatenation `salt + nonce + tag + ciphertext` as raw bytes — this single blob is everything needed to later decrypt the data given the correct password, with no separate metadata file. On any exception, returns `False` rather than raising.
- **`decrypt_register_data(password, token)`** — reverses the above: slices the salt/nonce/tag/ciphertext back out of the blob (fixed 16/16/16-byte prefix lengths), re-derives the key with the same PBKDF2 parameters, and calls `decrypt_and_verify` — which will raise `ValueError` (caught, returns `False`) if the password is wrong or the file was tampered with, since GCM's authentication tag check fails first.

## File storage

- **`save_new_local_user(password, data)`** — writes to `{USERS_FILE}/{data['user_name']}.enc`. Refuses to overwrite an existing file for that username (returns `False` if the file already exists) — so registering with a username that's already used on this device silently fails at this layer (the caller, `RegisterViaBinanceAPI.register`, surfaces this as a "Repeated user name" error popup).
- **`get_local_user(password, un)`** — reads `{USERS_FILE}/{un}.enc`, attempts to decrypt with the given password. Returns `(True, data_dict)` on success, `(False, "incorrect_info")` if decryption failed (wrong password or corrupted file — these two cases are indistinguishable from this method's perspective), or `(False, "user_not_found")` if no `.enc` file exists for that username.

## Security notes

- The per-user encryption key is derived solely from the user's chosen local password — there's no OS-level keychain integration, so the strength of the stored API-secret's protection is entirely dependent on the local password's strength (the UI enforces only an 8-character minimum, see `RegisterViaBinanceAPI.register`).
- `.enc` files are portable but **not** transferable between installations without also knowing the password — losing the password means losing access to the saved account (there is no recovery path; the user would need to re-register via `RegisterViaBinanceAPI`, which also requires re-entering their real Binance API key/secret).

## Related

- [`window.md`](window.md) — hosts the Login/Register widgets that call into this file.
- [`widgets/login.md`](widgets/login.md), [`widgets/register_via_binance_api.md`](widgets/register_via_binance_api.md) — callers of `get_local_user`/`save_new_local_user`.
- [`../base/files_folders.md`](../base/files_folders.md) — `USERS_FILE`, the directory these `.enc` files live in.
