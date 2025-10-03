import sys
import argparse
import config
from colorama import Fore, Style, init

init(autoreset=True)

# Exchange logic
if config.EXCHANGE.lower() == "binance":
    import exchange_binance as ex
else:
    import exchange_bybit as ex

# ------------------- CLI -------------------
def run_cli():
    parser = argparse.ArgumentParser(description="Crypto Trading Bot CLI")

    parser.add_argument("--symbol", type=str, required=True, help="Trading pair, e.g., ETHUSDT")
    parser.add_argument("--side", type=str, required=True, choices=["BUY", "SELL"], help="BUY or SELL")
    parser.add_argument("--type", type=str, required=True, choices=["MARKET", "LIMIT", "STOP_LIMIT", "OCO"], help="Order type")
    parser.add_argument("--qty", type=float, required=True, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price for LIMIT / STOP_LIMIT / OCO orders")
    parser.add_argument("--stop_price", type=float, help="Stop price for STOP_LIMIT / OCO orders")
    parser.add_argument("--stop_limit_price", type=float, help="Stop limit price for OCO orders")
    parser.add_argument("--dry_run", action="store_true", help="Simulate order without sending")
    args = parser.parse_args()

    # Validate required fields for each order type
    if args.type in ["LIMIT", "STOP_LIMIT", "OCO"] and args.price is None:
        print(Fore.RED + "Error: --price is required for LIMIT, STOP_LIMIT, and OCO orders")
        return
    if args.type in ["STOP_LIMIT", "OCO"] and args.stop_price is None:
        print(Fore.RED + "Error: --stop_price is required for STOP_LIMIT and OCO orders")
        return
    if args.type == "OCO" and args.stop_limit_price is None:
        print(Fore.RED + "Error: --stop_limit_price is required for OCO orders")
        return

    side = args.side.upper()
    order = None

    # Dry run mode
    if args.dry_run:
        print(Fore.YELLOW + "Dry Run: Order not sent to exchange")
        print(vars(args))
        return

    # Execute order
    if args.type == "MARKET":
        order = ex.place_market_order(args.symbol, side, args.qty)
    elif args.type == "LIMIT":
        order = ex.place_limit_order(args.symbol, side, args.qty, args.price)
    elif args.type == "STOP_LIMIT":
        order = ex.place_stop_limit_order(args.symbol, side, args.qty, args.price, args.stop_price)
    elif args.type == "OCO":
        order = ex.place_oco_order(args.symbol, side, args.qty, args.price, args.stop_price, args.stop_limit_price)

    # ------------------- Pretty Print Result -------------------
    if order:
        if args.type == "OCO":
            if (order.get("limit_order", {}).get("retCode") == 0 and
                order.get("stop_order", {}).get("retCode") == 0):
                print(Fore.GREEN + "✅ OCO Order Placed Successfully")
                print(f"  LIMIT Order ID: {order['limit_order']['result']['orderId']}")
                print(f"  STOP-LIMIT Order ID: {order['stop_order']['result']['orderId']}")
            else:
                print(Fore.RED + "❌ OCO Order Failed")
                print(order)
        elif isinstance(order, dict) and "retCode" in order and order["retCode"] == 0:
            print(Fore.GREEN + f"✅ {args.type} Order Placed Successfully")
            print(f"Order ID: {order['result']['orderId']}")
            print(f"Symbol: {args.symbol}, Side: {side}, Qty: {args.qty}")
        else:
            print(Fore.RED + "❌ Order Failed:")
            print(order)
    else:
        print(Fore.RED + "❌ Order could not be processed")


# ------------------- UI -------------------
def run_ui():
    import ui  # Launch Streamlit UI

# ------------------- Entry -------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()  # CLI mode if any arguments passed
    else:
        run_ui()   # UI mode if no arguments passed
