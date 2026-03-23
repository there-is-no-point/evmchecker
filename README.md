# EVM Balance Checker (Fork)

> Fork of [mikke555/evm-checker](https://github.com/mikke555/evm-checker) with extended functionality.

Balance checker for Ethereum and EVM-compatible chains. Uses async and Multicall3 for efficiency — all token balances fetched in a single RPC request per wallet. Results are displayed in a table and exported to a file of your choice.

Proxy usage is recommended for better performance.

---

## What's new in this fork ✨

Compared to the original:

| Feature | Original | Fork |
|---|---|---|
| Launch modes | Single chain only | Single chain + All Networks |
| Network filter | — | Mainnet / Testnet / All |
| Price sources | Binance only | Binance → Bybit → OKX → KuCoin → Bitget → Gate.io |
| Price mode | — | Fast (first) or Compare (average with divergence warning) |
| RPC failover | Random pick, N retries | Random start, sequential fallback per RPC |
| Output formats | CSV only | CSV / Excel (.xlsx) / JSON |
| All Networks: progress | — | Overall progress bar across chains |
| All Networks: empty chains | Saved anyway | Skipped automatically |
| All Networks: summary | — | Summary table at the end |
| All Networks: single file | — | One Excel/JSON file with all networks |
| Empty addresses.txt | Crashes with IndexError | Clear error message |
| Configuration | config.py (mixed) | config.py (settings) + networks.py (chains) |

---

## Features ✨

- **Two launch modes** — check a single chain or all chains at once
- **Network mode filter** — mainnet only, testnet only, or both
- **Output format choice** — CSV, Excel (.xlsx with one sheet per network), or JSON
- Checks multiple addresses simultaneously
- Batches all balance calls into a single RPC request via Multicall3
- **Multi-RPC failover** — random start, sequential fallback if an RPC fails
- **Price chain** — Binance → Bybit → OKX → KuCoin → Bitget → Gate.io with fast or compare mode
- Supports any EVM chain with Multicall3 deployed
- Supports ERC-20 token balances
- Proxy support for rate limiting
- Timestamped output filenames

---

## Installation 🚀

1. **Clone the repository**
```bash
git clone https://github.com/your-username/evm-checker.git
cd evm-checker
```

2. **Setup virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

3. **Install dependencies**

Requires **Python 3.12+**.
```bash
pip install -r requirements.txt
```

4. **Setup input files**
   - Add wallet addresses to `addresses.txt` (one per line)
   - *(Optional)* Add HTTP proxies to `proxies.txt` (format: `username:password@ip:port`)

---

## Usage 🎯

```bash
python main.py
```

Two prompts appear on startup:

```
? Select chain (type to search): [ All Networks ]
? Select output format: CSV
```

### Single chain mode
Select any chain from the list. The checker fetches balances for all addresses in `addresses.txt`, prints a table in the terminal, and saves the result file to `results/`.

### All Networks mode
Select `[ All Networks ]`. The checker iterates through every chain visible under the current `NETWORK_MODE`:

- Shows an **overall progress bar** across all chains
- **Skips chains** where all balances are zero — no clutter, no empty files
- Prints a per-network table for each non-empty chain
- Prints a **summary table** at the end: address / network / native balance / USD
- Saves results: one Excel file with sheets per network, one JSON file, or separate CSVs per network

```
results/
  all_networks-21_03_2026_14_30_00.xlsx   ← Excel (one sheet per network)
  all_networks-21_03_2026_14_30_00.json   ← JSON (all networks in one file)
  ethereum-21_03_2026_14_30_00.csv        ← CSV (one file per network)
  base-21_03_2026_14_30_05.csv
  ...
```

---

## Network Mode 🌐

Controlled by `NETWORK_MODE` in `config.py`. Filters which chains appear in the menu and in All Networks mode.

| Value | Description |
|---|---|
| `"mainnet"` | Mainnets only *(default)* |
| `"testnet"` | Testnets only |
| `"all"` | Both mainnets and testnets |

```python
# config.py
NETWORK_MODE = "mainnet"
```

Testnets are marked with `"testnet": True` in `networks.py`. All other chains are treated as mainnets.

---

## Output Formats 📄

Selected interactively at each run.

| Format | Single chain | All Networks |
|---|---|---|
| CSV | One file | One file per network |
| Excel (.xlsx) | One file | One file, one sheet per network |
| JSON | One file | One file, all networks combined |

---

## Price Sources 💱

USD value for the native token is fetched from a chain of 6 exchanges:

```
Binance → Bybit → OKX → KuCoin → Bitget → Gate.io
```

Configured in `PRICE_SOURCES` inside `config.py` — reorder, add, or remove exchanges there.

### Two modes — controlled by `COMPARE_PRICES` in `config.py`

**`COMPARE_PRICES = False`** *(default — faster)*
Exchanges are queried in order. The first valid price is used immediately.

**`COMPARE_PRICES = True`** *(slower — all exchanges in parallel)*
All exchanges are queried simultaneously. The **average price** is used.
If the spread exceeds `PRICE_DIVERGENCE_THRESHOLD` (default: **2%**), a warning is printed with a per-exchange breakdown:
```
⚠ Price divergence for ETH: 2.41% (threshold: 2%)
  Binance    $3100.00
  Bybit      $3174.20
  OKX        $3098.50
  Average    $3124.23
```

---

## Multi-RPC Failover ⚡

Each chain in `networks.py` can have multiple RPC endpoints. The checker picks the **first RPC randomly**, then falls back through the rest in order:

1. A random RPC is picked as the starting point
2. It is attempted up to `RETRY_PER_RPC` times (default: **2**)
3. If all attempts fail → prints `RPC failed (...), switching to next...`
4. If all RPCs exhausted → returns zero balances for that address

---

## Adding a Custom Chain ⚙️

Open `networks.py` and add a new entry. Add `"testnet": True` for testnets.

```python
"mychain": {
    "rpc": [
        "https://rpc.mychain.io",
        "https://mychain.public-rpc.com",
    ],
    "symbol": "ETH",
    "tokens": {
        "USDC": "0xContractAddressHere",
        "USDT": "0xContractAddressHere",
    },
    "multicall": DEFAULT_MULTICALL,
    # "testnet": True,
},
```

| Field | Source |
|---|---|
| `rpc` | [chainlist.org](https://chainlist.org) or Alchemy / BlastAPI / QuickNode |
| `symbol` | Native token ticker — must have a `{symbol}USDT` pair on at least one exchange in `PRICE_SOURCES` |
| Token addresses | Chain block explorer (Etherscan, Basescan, etc.) |
| `multicall` | [multicall3.com/deployments](https://www.multicall3.com/deployments) |

---

## File Structure 📁

```
evm-checker/
├── main.py          — main script (launch modes, balance fetching, output)
├── config.py        — all settings: network mode, concurrency, price sources
├── networks.py      — chain definitions: RPCs, token addresses, Multicall3
├── addresses.txt    — wallet addresses to check (one per line)
├── proxies.txt      — HTTP proxies, optional (format: user:pass@ip:port)
├── requirements.txt — Python dependencies
├── abi/
│   ├── erc20.json       — ERC-20 ABI (balanceOf, decimals)
│   └── multicall.json   — Multicall3 ABI
└── results/         — output files (auto-created on first run)
```

---

## Configuration Reference

All settings in `config.py`. `main.py` and `networks.py` do not need to be edited for normal use.

| Parameter | Default | Description |
|---|---|---|
| `NETWORK_MODE` | `"mainnet"` | Which chains to show: `"mainnet"`, `"testnet"`, or `"all"` |
| `MAX_CONCURRENT` | `20` | Max parallel requests when proxies are provided |
| `MIN_CONCURRENT` | `3` | Max parallel requests without proxies |
| `RETRY_PER_RPC` | `2` | Attempts per RPC before switching to the next |
| `MIN_VALUE_TO_DISPLAY` | `0.00001` | Amounts below this show as `~ 0` |
| `COMPARE_PRICES` | `False` | `True` — average from all exchanges; `False` — first valid price |
| `PRICE_DIVERGENCE_THRESHOLD` | `"0.02"` | Max spread between exchange prices before warning |
| `PRICE_SOURCES` | 6 exchanges | Ordered list of exchanges with URLs and response parsers |

---

---

# EVM Balance Checker (Форк)

> Форк [mikke555/evm-checker](https://github.com/mikke555/evm-checker) с расширенной функциональностью.

Чекер балансов для Ethereum и EVM-совместимых сетей. Использует асинхронность и Multicall3 — все балансы токенов запрашиваются за один RPC-запрос на кошелёк. Результаты выводятся в таблицу и сохраняются в файл выбранного формата.

Использование прокси рекомендуется для повышения скорости.

---

## Что нового в форке ✨

По сравнению с оригиналом:

| Функция | Оригинал | Форк |
|---|---|---|
| Режимы запуска | Только одна сеть | Одна сеть + All Networks |
| Фильтр сетей | — | Mainnet / Testnet / All |
| Источники цен | Только Binance | Binance → Bybit → OKX → KuCoin → Bitget → Gate.io |
| Режим цен | — | Быстрый (первая) или Сравнение (средняя + предупреждение) |
| RPC Failover | Случайный выбор, N попыток | Случайный старт, последовательный fallback |
| Форматы вывода | Только CSV | CSV / Excel (.xlsx) / JSON |
| All Networks: прогресс | — | Общий прогресс-бар по сетям |
| All Networks: пустые сети | Сохраняются | Пропускаются автоматически |
| All Networks: сводка | — | Сводная таблица в конце |
| All Networks: один файл | — | Один Excel/JSON для всех сетей |
| Пустой addresses.txt | Падает с IndexError | Понятное сообщение об ошибке |
| Конфигурация | config.py (всё вместе) | config.py (настройки) + networks.py (сети) |

---

## Возможности ✨

- **Два режима запуска** — одна сеть или все сети сразу
- **Фильтр режима сетей** — только мейннеты, только тестнеты или все
- **Выбор формата вывода** — CSV, Excel (.xlsx с листами по сетям) или JSON
- Одновременная проверка множества адресов
- Пакетные запросы через Multicall3 — один RPC-запрос на кошелёк
- **Multi-RPC Failover** — случайный старт, последовательный переход при сбое
- **Цепочка бирж** — Binance → Bybit → OKX → KuCoin → Bitget → Gate.io, быстрый или режим сравнения
- Поддержка любой EVM-сети с Multicall3
- Поддержка ERC-20 токенов
- Поддержка прокси
- Временные метки в именах файлов

---

## Установка 🚀

1. **Клонировать репозиторий**
```bash
git clone https://github.com/your-username/evm-checker.git
cd evm-checker
```

2. **Создать виртуальное окружение**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

3. **Установить зависимости**

Требуется **Python 3.12+**.
```bash
pip install -r requirements.txt
```

4. **Настроить входные файлы**
   - Добавить адреса кошельков в `addresses.txt` (по одному на строку)
   - *(Опционально)* Добавить HTTP-прокси в `proxies.txt` (формат: `username:password@ip:port`)

---

## Использование 🎯

```bash
python main.py
```

При запуске появятся два вопроса:

```
? Select chain (type to search): [ All Networks ]
? Select output format: CSV
```

### Режим одной сети
Выбери любую сеть из списка. Чекер получит балансы всех адресов из `addresses.txt`, выведет таблицу в терминал и сохранит файл в `results/`.

### Режим All Networks
Выбери `[ All Networks ]`. Чекер пройдёт по всем сетям в рамках текущего `NETWORK_MODE`:

- Показывает **общий прогресс-бар** по сетям
- **Пропускает сети** где все балансы нулевые
- Выводит таблицу по каждой непустой сети
- Выводит **сводную таблицу** в конце: адрес / сеть / нативный баланс / USD
- Сохраняет: один Excel-файл с листами, один JSON, или отдельные CSV

```
results/
  all_networks-21_03_2026_14_30_00.xlsx   ← Excel (лист на каждую сеть)
  all_networks-21_03_2026_14_30_00.json   ← JSON (все сети в одном файле)
  ethereum-21_03_2026_14_30_00.csv        ← CSV (отдельный файл на сеть)
  base-21_03_2026_14_30_05.csv
  ...
```

---

## Режим сетей 🌐

Управляется параметром `NETWORK_MODE` в `config.py`.

| Значение | Описание |
|---|---|
| `"mainnet"` | Только мейннеты *(по умолчанию)* |
| `"testnet"` | Только тестнеты |
| `"all"` | Мейннеты и тестнеты вместе |

Тестовые сети помечены флагом `"testnet": True` в `networks.py`.

---

## Форматы вывода 📄

Выбираются интерактивно при каждом запуске.

| Формат | Одна сеть | All Networks |
|---|---|---|
| CSV | Один файл | Отдельный файл на каждую сеть |
| Excel (.xlsx) | Один файл | Один файл, лист на каждую сеть |
| JSON | Один файл | Один файл, все сети внутри |

---

## Источники цен 💱

USD-стоимость запрашивается у цепочки из 6 бирж:

```
Binance → Bybit → OKX → KuCoin → Bitget → Gate.io
```

Список с URL задан в `PRICE_SOURCES` в `config.py` — там можно менять порядок, добавлять и убирать биржи.

**`COMPARE_PRICES = False`** *(по умолчанию)* — первая ответившая биржа.

**`COMPARE_PRICES = True`** — все биржи параллельно, средняя цена. При разбросе > `PRICE_DIVERGENCE_THRESHOLD` (2%) выводится предупреждение с ценами по каждой бирже.

---

## Multi-RPC Failover ⚡

Для каждой сети в `networks.py` можно указать несколько RPC. Первая выбирается случайно, остальные — fallback по порядку. Попыток на одну RPC: `RETRY_PER_RPC` (по умолчанию **2**).

---

## Добавление своей сети ⚙️

Открой `networks.py`, добавь блок в словарь `config`. Для тестнетов добавь `"testnet": True`.

```python
"mychain": {
    "rpc": ["https://rpc.mychain.io", "https://mychain.public-rpc.com"],
    "symbol": "ETH",
    "tokens": {
        "USDC": "0xАдресКонтракта",
    },
    "multicall": DEFAULT_MULTICALL,
    # "testnet": True,
},
```

---

## Структура файлов 📁

```
evm-checker/
├── main.py          — основной скрипт
├── config.py        — все настройки
├── networks.py      — конфиги сетей
├── addresses.txt    — адреса кошельков
├── proxies.txt      — HTTP-прокси (опционально)
├── requirements.txt — зависимости Python
├── abi/
│   ├── erc20.json
│   └── multicall.json
└── results/         — файлы с результатами
```

---

## Справочник параметров

| Параметр | По умолчанию | Описание |
|---|---|---|
| `NETWORK_MODE` | `"mainnet"` | Фильтр сетей: `"mainnet"`, `"testnet"` или `"all"` |
| `MAX_CONCURRENT` | `20` | Макс. параллельных запросов с прокси |
| `MIN_CONCURRENT` | `3` | Макс. параллельных запросов без прокси |
| `RETRY_PER_RPC` | `2` | Попыток на один RPC перед переключением |
| `MIN_VALUE_TO_DISPLAY` | `0.00001` | Суммы ниже этого показываются как `~ 0` |
| `COMPARE_PRICES` | `False` | Режим получения цены |
| `PRICE_DIVERGENCE_THRESHOLD` | `"0.02"` | Порог расхождения цен между биржами |
| `PRICE_SOURCES` | 6 бирж | Список бирж с URL и парсерами |
