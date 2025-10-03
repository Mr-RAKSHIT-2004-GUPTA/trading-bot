from pybit.unified_trading import HTTP
import config
from utils import log
import time

# Initialize Bybit client
session = HTTP(testnet=True, api_key=config.API_KEY, api_secret=config.API_SECRET)

def place_market_order(symbol, side, quantity):
    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side.capitalize(),
            orderType="Market",
            qty=quantity
        )
        log(f"Bybit MARKET Order: {order}")
        return order
    except Exception as e:
        log(f"Error placing MARKET order: {e}")
        return None

def place_limit_order(symbol, side, quantity, price):
    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side.capitalize(),
            orderType="Limit",
            qty=quantity,
            price=price,
            timeInForce="GTC"
        )
        log(f"Bybit LIMIT Order: {order}")
        return order
    except Exception as e:
        log(f"Error placing LIMIT order: {e}")
        return None

def place_stop_limit_order(symbol, side, quantity, price, stop_price):
    try:
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side.capitalize(),
            orderType="Limit",
            qty=quantity,
            price=price,
            triggerPrice=stop_price,
            triggerDirection=1 if side.upper()=="BUY" else 2,
            timeInForce="GTC"
        )
        log(f"Bybit STOP-LIMIT Order: {order}")
        return order
    except Exception as e:
        log(f"Error placing STOP-LIMIT order: {e}")
        return None

# ✅ Full OCO Simulation
def place_oco_order(symbol, side, quantity, limit_price, stop_price, stop_limit_price):
    """
    Simulate OCO for Bybit:
    1️⃣ Place a LIMIT order at limit_price (take profit)
    2️⃣ Place a STOP-LIMIT order at stop_price/stop_limit_price (stop loss)
    3️⃣ Returns both orders
    """
    log(f"Placing Bybit OCO simulation: LIMIT={limit_price}, STOP-LIMIT={stop_price}/{stop_limit_price}")
    
    # Place LIMIT (take profit) order
    limit_order = place_limit_order(symbol, side, quantity, limit_price)
    
    # Place STOP-LIMIT (stop loss) order
    stop_order = place_stop_limit_order(symbol, side, quantity, stop_limit_price, stop_price)
    
    # Optional: Monitoring/cancellation loop can be added here if one executes
    log("Bybit OCO simulation completed. Monitor manually or implement auto-cancel for one order if desired.")
    
    return {"limit_order": limit_order, "stop_order": stop_order}
