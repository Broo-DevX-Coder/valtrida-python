# `user/window.py`

**Role:** `AuthMain` — the container widget for the "Login" popup shown from `windows/main.py` (wrapped in an `OverlayPopup`). Provides a small top tab bar to switch between "Login" and "API Register" sub-pages.

## `AUTH_OPTIONS` / `AUTH_OPTIONS_TOOLTIPS`

A small, hardcoded (not dynamically registered like `base/tool_bar.py`'s `MW_*` dicts) mapping of tab name → widget class and tooltip:

```python
AUTH_OPTIONS = {
    'Login': LoggingWidget,
    'API Register': RegisterViaBinanceAPI
}
```

Unlike the main window's tool bar or the chart popup's chart types, **this registry is not watched for runtime changes** — adding a third auth method would require editing this file directly, not just registering a new entry elsewhere.

## `AuthMain(QWidget)`

- Fixed size starts at `350x170`, but **resizes dynamically per sub-page** — `cahnge_window(name)` *(existing typo, kept as-is)* reads the target widget's own `size_` attribute (`[width, height]`, set by each widget itself: `LoggingWidget` is `[350, 125]`, `RegisterViaBinanceAPI` is `[350, 245]`) and calls `self.setFixedSize(...)`/repositions the stack accordingly, so the popup visibly grows/shrinks when switching between Login and Register.
- Builds one `QPushButton` per `AUTH_OPTIONS_TOOLTIPS` entry in a `QButtonGroup` (exclusive — only one tab checked at a time), wired to `cahnge_window` via `functools.partial`.
- Instantiates every class in `AUTH_OPTIONS` up front (both `LoggingWidget` and `RegisterViaBinanceAPI` are created immediately at `AuthMain.__init__` time, not lazily on first tab click) and adds them all to a `QStackedWidget`.
- Defaults to the "Login" tab on construction.
- `closeEvent` is a bare `event.accept()` — no cleanup of async tasks or `AsyncController` unregistration here (unlike most other windows in the app); this widget doesn't own any of its own background tasks though (`LoggingWidget`/`RegisterViaBinanceAPI` don't have persistent listeners either — their async work is one-shot `login()`/`register()` calls per button click), so there isn't currently a leak from this omission.

## Standalone run mode

The `if __name__ == "__main__":` block lets this widget be tested in isolation with its own `QApplication`/`qasync` loop and manually-started `core.listeners`/`API.listeners`.

## Related

- [`../windows/main.md`](../windows/main.md) — wraps this in an `OverlayPopup` and shows/hides it in response to `login_clicked` and `logged_in` events.
- [`widgets/login.md`](widgets/login.md), [`widgets/register_via_binance_api.md`](widgets/register_via_binance_api.md) — the two sub-pages.
- [`../styles/qss.md`](../styles/qss.md) — `QSS["BINANCE"]`, `QSS["AUTH_TOOL_BAR"]`.
