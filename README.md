# trading-bot
Crypto Trading Bot

A Python-based crypto trading bot supporting Binance Futures Testnet (USDT-M) and Bybit Testnet.
Place MARKET, LIMIT, STOP-LIMIT, and OCO orders via CLI or Streamlit UI, with logging, error handling, and dry-run mode for testing.

Features

✅ Place MARKET and LIMIT orders

✅ Place STOP-LIMIT and OCO orders

✅ Support for BUY and SELL sides

✅ Command-Line Interface (CLI) for fast execution

✅ Streamlit UI for interactive order placement

✅ Dry Run Mode: simulate orders without sending to the exchange

✅ Logs all orders and errors

✅ Works with both Binance and Bybit testnets

Requirements

Python 3.10+

pip packages:

pip install python-binance bybit streamlit colorama


Testnet API keys for Binance or Bybit

File Structure
trading-bot/
│
├─ main.py             # Entry point: CLI or UI
├─ cli.py              # CLI implementation (optional)
├─ exchange_binance.py # Binance testnet order functions
├─ exchange_bybit.py   # Bybit testnet order functions
├─ ui.py               # Streamlit UI
├─ config.py           # API keys and exchange selection
├─ logger.py           # Logging functions
└─ utils.py            # Utility functions (e.g., logging)

CLI Usage

MARKET Order

python main.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01


Output Example

✅ MARKET Order Placed Successfully
Order ID: abc123
Symbol: BTCUSDT, Side: BUY, Qty: 0.01


LIMIT Order

python main.py --symbol BTCUSDT --side SELL --type LIMIT --qty 0.01 --price 32000


Output Example

✅ LIMIT Order Placed Successfully
Order ID: def456
Symbol: BTCUSDT, Side: SELL, Qty: 0.01


STOP-LIMIT Order

python main.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --qty 0.01 --price 31550 --stop_price 31500


Possible Output

❌ Order could not be processed
Error from exchange: triggerPrice must be > lastPrice


OCO Order

python main.py --symbol BTCUSDT --side SELL --type OCO --qty 0.01 --price 32000 --stop_price 29000 --stop_limit_price 28500


Output Example

✅ OCO Order Placed Successfully
  LIMIT Order ID: ghi789
  STOP-LIMIT Order ID: jkl012


Dry Run Mode

python main.py --symbol BTCUSDT --side BUY --type MARKET --qty 0.01 --dry_run


Output Example

Dry Run: Order not sent
{'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'qty': 0.01}

Streamlit UI

Run:

python main.py


UI Features

Dropdown for available symbols

Side selection: BUY / SELL

Order type selection: MARKET, LIMIT, STOP-LIMIT, OCO

Input fields for quantity, price, stop price, stop-limit price

Dry Run option

Displays success or error messages clearly

Example UI Screenshots

Place Order Panel


Successful Order Result


Error Display Example
