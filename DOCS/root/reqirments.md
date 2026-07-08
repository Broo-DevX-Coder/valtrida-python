# `reqirments.txt`

**Role:** Python dependency list for the project. **Note the filename is `reqirments.txt`, not `requirements.txt`** — this is an existing typo in the repository, not a documentation mistake. Use the exact filename when installing dependencies or referencing it from scripts/CI.

## Contents

```
PySide2
shiboken2
qasync
pyqtgraph
numpy<2
pandas
aiohttp
websockets
pycryptodome
cryptography
janus
uniquant
```

## What each dependency is for

| Package | Used for |
|---|---|
| `PySide2` | Qt for Python — the entire UI layer |
| `shiboken2` | PySide2's binding generator runtime dependency (installed alongside PySide2) |
| `qasync` | Bridges asyncio and the Qt event loop (`index.py` uses `qasync.QEventLoop`) |
| `pyqtgraph` | Chart rendering (candlestick chart, order book) |
| `numpy<2` | Numerical operations backing chart data; pinned below 2.0 for compatibility with other libs (e.g. `pandas`/`pyqtgraph` versions in use) |
| `pandas` | Data wrangling for market/candlestick data |
| `aiohttp` | Async HTTP client, likely used for REST calls to Binance |
| `websockets` | WebSocket client, used for live market data streams from Binance |
| `pycryptodome` | Cryptographic primitives (in addition to/overlapping with `cryptography`) |
| `cryptography` | AES-GCM + PBKDF2 based local credential encryption (`user/local_cypher.py`) |
| `janus` | Thread-safe queue that works with both `threading` and `asyncio` — useful for bridging background network threads with the asyncio event loop |
| `uniquant` | Binance client library used by the `API/` layer for market/account data |

## Installing

```bash
pip install -r reqirments.txt
```

## Related

- [`../ARCHITECTURE.md`](../ARCHITECTURE.md) — how `aiohttp`/`websockets`/`uniquant` fit into the networking layer, and how `qasync`/`janus` connect background threads to the Qt/asyncio event loop.
- [`../user/local_cypher.md`](../user/local_cypher.md) — uses `cryptography` for local credential encryption.
