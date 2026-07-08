# `core/pop_messages.py`

**Role:** A single reusable helper, `pup_message(...)`, for showing a modal `QMessageBox` styled with the app's popup stylesheet, optionally running a callback when the user clicks OK.

## `pup_message(title, text, function, type_="info")`

```python
pup_message(
    title="Error",
    text="An error occurred while processing your request.",
    function=handle_error,
    type_="error"
)
```

1. Creates a `QMessageBox`, sets its title and text.
2. Maps `type_` to a `QMessageBox` icon: `"error"` → `Critical`, `"warning"` → `Warning`, anything else (including the default `"info"`) → `Information`.
3. Applies `Styles.qss.QSS["POPUP_W"]` as the box's stylesheet, so error/warning/info popups match the app's dark (or light) theme instead of using the OS-default message box look.
4. Shows the box modally with `msg.exec_()` (blocks the calling thread/coroutine until dismissed — this is a real modal dialog, not a toast/notification).
5. If the user clicks OK **and** `function` is callable, calls `function()` with no arguments.

## Notable caller: `core/errors.py`

`critical_errors_listener()` in `core/errors.py` calls `pup_message(..., CRITICAL_STOP, "error")` for critical connection errors — meaning `CRITICAL_STOP()` (full app shutdown) only actually runs **after** the user clicks OK on the popup, not immediately when the error is detected. This is a deliberate UX choice: the user always gets to see *why* the app is about to close before it closes.

## Related

- [`../styles/qss.md`](../styles/qss.md) — the `POPUP_W` stylesheet applied here.
- [`errors.md`](errors.md) — the primary caller.
