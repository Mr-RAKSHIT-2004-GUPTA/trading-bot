import streamlit as st
import pandas as pd
import config

# Exchange logic
if config.EXCHANGE.lower() == "binance":
    import exchange_binance as ex
    AVAILABLE_SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT"]
else:
    import exchange_bybit as ex
    AVAILABLE_SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT"]

st.title("📈 Crypto Trading Bot UI")
st.write("Place MARKET, LIMIT, STOP-LIMIT, or OCO orders interactively.")

# ------------------- User Inputs -------------------
symbol = st.selectbox("Trading Pair", AVAILABLE_SYMBOLS)
side = st.selectbox("Side", ["BUY", "SELL"])
order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "STOP_LIMIT", "OCO"])
qty = st.number_input("Quantity", min_value=0.0001, value=0.01, step=0.0001)

price = st.number_input("Price (for LIMIT/STOP_LIMIT/OCO)", value=0.0)
stop_price = st.number_input("Stop Price (for STOP_LIMIT/OCO)", value=0.0)
stop_limit_price = st.number_input("Stop-Limit Price (for OCO)", value=0.0)

dry_run = st.checkbox("Dry Run (Simulate without sending)")

# ------------------- Place Order -------------------
if st.button("Place Order"):

    # ------------------- Validation -------------------
    if order_type in ["LIMIT", "STOP_LIMIT", "OCO"] and price <= 0:
        st.error("Price must be > 0 for LIMIT, STOP_LIMIT, OCO orders")
    elif order_type in ["STOP_LIMIT", "OCO"] and stop_price <= 0:
        st.error("Stop price must be > 0 for STOP_LIMIT and OCO orders")
    elif order_type == "OCO" and stop_limit_price <= 0:
        st.error("Stop-limit price must be > 0 for OCO orders")
    else:
        order = None

        # ------------------- Dry Run -------------------
        if dry_run:
            st.warning("Dry Run: Order not sent")
            st.json({
                "Symbol": symbol,
                "Side": side,
                "Type": order_type,
                "Quantity": qty,
                "Price": price,
                "Stop Price": stop_price,
                "Stop-Limit Price": stop_limit_price
            })
        else:
            # ------------------- Execute -------------------
            if order_type == "MARKET":
                order = ex.place_market_order(symbol, side, qty)
            elif order_type == "LIMIT":
                order = ex.place_limit_order(symbol, side, qty, price)
            elif order_type == "STOP_LIMIT":
                order = ex.place_stop_limit_order(symbol, side, qty, price, stop_price)
            elif order_type == "OCO":
                order = ex.place_oco_order(symbol, side, qty, price, stop_price, stop_limit_price)

            # ------------------- Display Results -------------------
            if order:
                if isinstance(order, dict) and "error" not in order:
                    st.success(f"{order_type} order placed successfully!")

                    # MARKET / LIMIT / STOP-LIMIT
                    if order_type != "OCO":
                        df = pd.DataFrame({
                            "Field": ["Order ID", "Symbol", "Side", "Quantity"],
                            "Value": [str(order.get('orderId') or order['result'].get('orderId')),
                                      str(symbol), str(side), str(qty)]
                        })
                        st.subheader("Order Details")
                        st.table(df)

                    # OCO Orders
                    else:
                        df = pd.DataFrame({
                            "Field": ["LIMIT Order ID", "STOP-LIMIT Order ID", "Symbol", "Side", "Quantity"],
                            "Value": [
                                str(order['limit_order']['result']['orderId']),
                                str(order['stop_order']['result']['orderId']),
                                str(symbol), str(side), str(qty)
                            ]
                        })
                        st.subheader("OCO Orders Details")
                        st.table(df)

                else:
                    # ------------------- Error Case -------------------
                    st.error("❌ Order failed!")
                    st.subheader("Error Details")
                    if isinstance(order, dict):
                        for key, value in order.items():
                            st.write(f"**{key}:** {value}")
                    else:
                        st.write(order)
            else:
                st.error("❌ Order could not be processed")
