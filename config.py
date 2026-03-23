"""
EVM Balance Checker — Configuration
====================================
Все настройки softa собраны здесь. Networks.py трогать не нужно.
"""

from decimal import Decimal

# ─────────────────────────────────────────────────────────────────────────────
# NETWORK MODE
# ─────────────────────────────────────────────────────────────────────────────
# Управляет тем, какие сети попадают в меню и в режим All Networks.
#
#   "all"       — основные сети + тестовые  (режим 1)
#   "mainnet"   — только основные сети      (режим 2, по умолчанию)
#   "testnet"   — только тестовые сети      (режим 3)
#
NETWORK_MODE = "mainnet"

# ─────────────────────────────────────────────────────────────────────────────
# CONCURRENCY
# ─────────────────────────────────────────────────────────────────────────────
# Максимальное число одновременных запросов при работе с прокси.
MAX_CONCURRENT = 20

# Минимальное число одновременных запросов без прокси.
MIN_CONCURRENT = 3

# ─────────────────────────────────────────────────────────────────────────────
# RPC FAILOVER
# ─────────────────────────────────────────────────────────────────────────────
# Количество попыток на одну RPC перед переключением на следующую.
RETRY_PER_RPC = 2

# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
# Балансы ниже этого значения отображаются как "~ 0", а нулевые — скрываются.
MIN_VALUE_TO_DISPLAY = 0.00001

# ─────────────────────────────────────────────────────────────────────────────
# PRICE FETCHING
# ─────────────────────────────────────────────────────────────────────────────
# False — используется первая биржа, вернувшая цену (быстрее).
# True  — опрашиваются все биржи параллельно, считается средняя цена;
#         если разброс между min и max превышает PRICE_DIVERGENCE_THRESHOLD,
#         выводится предупреждение с ценами по каждой бирже.
COMPARE_PRICES = True

# Порог расхождения цен между биржами (только при COMPARE_PRICES = True).
# Значение 0.02 соответствует 2%.
PRICE_DIVERGENCE_THRESHOLD = "0.02"

# ─────────────────────────────────────────────────────────────────────────────
# PRICE SOURCES
# ─────────────────────────────────────────────────────────────────────────────
# Цепочка бирж для получения цены нативного токена.
# Порядок важен: при COMPARE_PRICES = False используется первая ответившая.
# Чтобы отключить биржу — закомментируй или удали её блок.
# {symbol} подставляется автоматически (например ETH, BNB, AVAX).
#
PRICE_SOURCES = [
    {
        "name": "Binance",
        "url":   "https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT",
        "parse": lambda data: Decimal(data["price"]),
    },
    {
        "name": "Bybit",
        "url":   "https://api.bybit.com/v5/market/tickers?category=spot&symbol={symbol}USDT",
        "parse": lambda data: Decimal(data["result"]["list"][0]["lastPrice"]),
    },
    {
        "name": "OKX",
        "url":   "https://www.okx.com/api/v5/market/ticker?instId={symbol}-USDT",
        "parse": lambda data: Decimal(data["data"][0]["last"]),
    },
    {
        "name": "KuCoin",
        "url":   "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT",
        "parse": lambda data: Decimal(data["data"]["price"]),
    },
    {
        "name": "Bitget",
        "url":   "https://api.bitget.com/api/v2/spot/market/tickers?symbol={symbol}USDT",
        "parse": lambda data: Decimal(data["data"][0]["lastPr"]),
    },
    {
        "name": "Gate.io",
        "url":   "https://api.gateio.ws/api/v4/spot/tickers?currency_pair={symbol}_USDT",
        "parse": lambda data: Decimal(data[0]["last"]),
    },
]
