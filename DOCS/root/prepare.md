# `prepare.py`

**Role:** Startup bootstrap — wires together streams, listeners, chart classes, tool bar tabs, and popup windows before the UI is shown. Imported once, for its side effects, from `index.py`.

## What it does, in order

### 1. Environment variables (before any Qt/QtWebEngine import)

```python
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--no-sandbox --disable-gpu --disable-software-rasterizer"
os.environ["QTWEBENGINE_DISABLE_SANDBOX"] = "1"
os.environ["PYQTGRAPH_QT_LIB"] = "PySide2"
```

- Disables the Chromium sandbox and GPU rasterization for the embedded `QtWebEngine` view — common workarounds for running QtWebEngine inside containerized/sandboxed or headless-ish environments (like this one) where the default sandbox/GPU path fails to initialize.
- Explicitly tells `pyqtgraph` to use `PySide2` as its Qt binding, since pyqtgraph can auto-detect the wrong binding if multiple Qt bindings are installed.

### 2. Imports with side effects

Imports `Styles` (`mods`, `icons`), `core`, `base`, `API`, `core.folders`, `base.charts`, `base.tool_bar`, `charts.candels_shart`, `charts.order_book`, and the three `windows.tool_bar` tab modules (`home`, `wallet`, `markets`), plus `core.SystemStream`.

### 3. Start all module-level listeners

```python
listners_objs = [core, API]
for obj in listners_objs:
    for i in obj.listeners:
        asyncio.create_task(i())
```

Both the `core` and `API` packages expose a `listeners` list (of async callables) via their `__init__.py`. Each one is scheduled as an asyncio task here. This is the mechanism by which, e.g., the error/log stream consumers (`core/errors.py`, `core/logs.py`) and market-data listeners (`API/market.py`) actually start running — simply importing those modules is not enough; they must register their listener coroutine in their package's `listeners` list for `prepare.py` to start it.

### 4. Register chart classes

```python
charts.CHARTS_CLASSES["candals_shart"] = candels_shart.SimpleCandelsChart
charts.CHARTS_CLASSES["order_book"] = order_book.OrderBook
```

Populates the registry in `base/charts.py` (see [`../base/charts.md`](../base/charts.md)) so other code can look up chart widget classes by key instead of importing them directly.

### 5. Register tool bar tabs

```python
tool_bar.MW_STACKED_WINDOWS["Home"] = home.Home
tool_bar.MW_STACKED_WINDOWS["Wallet"] = wallet.Wallet
tool_bar.MW_STACKED_WINDOWS["Markets"] = markets.Markets
```

Populates the registry in `base/tool_bar.py` (see [`../base/tool_bar.md`](../base/tool_bar.md)) that `windows/main.py` uses to build the stacked-widget navigation.

### 6. Register popup windows

```python
tool_bar.MW_POPUP_WIDOWS["Charts"] = {"m": ChowSharts, "ft?": True}
tool_bar.MW_POPUP_WIDOWS["Login"] = {"m": AuthMain, "ft?": True}
```

Registers `windows.chart_popup.ChowSharts` and `user.window.AuthMain` as popup windows, each with a `"ft?"` (first-time?) flag alongside the class reference.

### 7. Announce program start

```python
SystemStream.send({
    "type": "live_sycle",
    "event": "start_of_program",
    "source": "prepare",
    "payload": {"event": "The program Started"}
})
```

Publishes a `start_of_program` event on `SystemStream` so any subscriber (e.g. logging) can react to app startup. See `streams.txt` for the full event schema.

## Known scaffolding referenced but not implemented

The project goal/scratchpad convention calls out a `plugins_manager` concept expected around this bootstrap step; as of this version of `prepare.py`, there is no plugin loading code present — only the directory constants (`PLUGINS_DIR`, `MORE_PACKAGES`) exist in `base/files_folders.py` / `core/folders.py`. Don't assume plugins are actually loaded at startup.

## Related

- [`../core/async_controller.md`](../core/async_controller.md) — defines `SystemStream` and the other global streams.
- [`../base/charts.md`](../base/charts.md), [`../base/tool_bar.md`](../base/tool_bar.md) — the registries populated here.
- [`../windows/tool_bar/home.md`](../windows/tool_bar/home.md), [`markets.md`](../windows/tool_bar/markets.md), [`wallet.md`](../windows/tool_bar/wallet.md) — the tab classes registered here.
