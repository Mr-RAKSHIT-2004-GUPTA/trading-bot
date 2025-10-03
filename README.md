# Crypto Trading Bot

A Python-based crypto trading bot supporting **Binance Futures Testnet (USDT-M)** and **Bybit Testnet**.  
Place **MARKET, LIMIT, STOP-LIMIT, and OCO orders** via **CLI or Streamlit UI**, with logging, error handling, and dry-run mode for testing.

---

## Features

- ✅ Place **MARKET** and **LIMIT** orders  
- ✅ Place **STOP-LIMIT** and **OCO** orders  
- ✅ Support for **BUY** and **SELL** sides  
- ✅ **Command-Line Interface (CLI)** for fast execution  
- ✅ **Streamlit UI** for interactive order placement  
- ✅ **Dry Run Mode**: simulate orders without sending to the exchange  
- ✅ Logs all orders and errors  
- ✅ Works with both **Binance** and **Bybit** testnets  

---

## Requirements

- Python 3.10+  
- pip packages:

```bash
pip install python-binance bybit streamlit colorama

---

## File Structure

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
