from binance.client import Client
import config
from utils import log
import time

# Initialize Binance client
client = Client(config.API_KEY, config.API_SECRET, testnet=True)
client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

# ------------------- MARKET order -------------------
def place_market_order(symbol, side, quantity):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        log(f"Binance MARKET Order: {order}")
        return order
    except Exception as e:
        log(f"Error placing MARKET order: {e}")
        return {"error": str(e)}

# ------------------- LIMIT order -------------------
def place_limit_order(symbol, side, quantity, price):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price)
        )
        log(f"Binance LIMIT Order: {order}")
        return order
    except Exception as e:
        log(f"Error placing LIMIT order: {e}")
        return {"error": str(e)}

# ------------------- STOP-LIMIT order -------------------
def place_stop_limit_order(symbol, side, quantity, price, stop_price):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="STOP_MARKET",   # Correct Futures type
            stopPrice=str(stop_price),
            quantity=quantity
        )
        log(f"Binance STOP-LIMIT (STOP_MARKET) Order: {order}")
        return order
    except Exception as e:
        log(f"Error placing STOP-LIMIT order: {e}")
        return {"error": str(e)}

# ------------------- OCO order (simulated for Futures) -------------------
def place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price):
    try:
        log("Simulating OCO on Binance Futures: placing LIMIT and STOP_MARKET orders linked manually")
        
        # Place LIMIT order
        limit_order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=str(price)
        )
        log(f"OCO LIMIT Order: {limit_order}")
        
        # Place STOP_MARKET order
        stop_order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type="STOP_MARKET",
            stopPrice=str(stop_price),
            quantity=quantity
        )
        log(f"OCO STOP-LIMIT (STOP_MARKET) Order: {stop_order}")
        
        # Return both orders together
        return {
            "limit_order": limit_order,
            "stop_order": stop_order
        }
        
    except Exception as e:
        log(f"Error placing OCO order: {e}")
        return {"error": str(e)}
