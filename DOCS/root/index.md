# `index.py`

**Role:** Application entry point.

## What it does

1. Sets `Qt.AA_ShareOpenGLContexts` on the `QCoreApplication` **before** anything else is created — required for `QtWebEngine` to share OpenGL contexts correctly with the rest of the Qt UI.
2. Initializes `QtWebEngine` (used for any embedded HTML/CSS content, see `Styles/css.py`).
3. Creates the `QApplication`.
4. Creates a `qasync.QEventLoop` wrapping the Qt event loop and installs it as the asyncio event loop via `asyncio.set_event_loop(loop)`. This is what allows the rest of the app (streams, listeners, network code) to use native `async`/`await` while still running inside the Qt event loop, rather than needing a separate thread for asyncio.
5. Defines `async def main()`, which:
   - Imports `prepare` (triggering all bootstrap/registration side effects — see [`prepare.md`](prepare.md)).
   - Imports and instantiates `windows.main.MainWindow`, then calls `.run()` on it to show the main window.
   - Enters an effectively infinite `await asyncio.sleep(1000)` loop just to keep the coroutine (and therefore the event loop) alive.
6. Under `if __name__ == "__main__":`, runs `loop.run_until_complete(main())`, catching `RuntimeError` and `KeyboardInterrupt` so that closing the app or hitting Ctrl+C doesn't produce an ugly traceback.

## Why it's structured this way

The strict ordering (set attribute → init QtWebEngine → create QApplication → create event loop) matters because PySide2/QtWebEngine are sensitive to initialization order; doing these out of order is a common source of crashes in PySide2 + QtWebEngine apps. Don't reorder these steps without testing carefully.

## Related

- [`prepare.md`](prepare.md) — everything that happens as a side effect of `import prepare` inside `main()`.
- [`../windows/main.md`](../windows/main.md) — the `MainWindow` class instantiated here.
