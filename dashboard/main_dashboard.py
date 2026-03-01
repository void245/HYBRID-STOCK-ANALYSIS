import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from python.event_detection import detect_events_refined


def load_json_data(folder, symbol, suffix):
    path = os.path.join("data", folder, f"{symbol}_{suffix}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


def render_dashboard():
    symbol = st.session_state.get('symbol')

    if not symbol:
        st.warning("⚠️ No stock selected. Please run analysis first.")
        return

    st.title(f"📈 Advanced Analysis Dashboard : {symbol}")

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    fund_data = load_json_data("fundamentals", symbol, "fundamentals")
    tech_data = load_json_data("processed", symbol, "technical")
    event_data = detect_events_refined(symbol)

    if not fund_data or not tech_data:
        st.error("Data files missing. Run pipeline first.")
        return

    # -----------------------------
    # FINAL DECISION LOGIC
    # -----------------------------
    final_action = "HOLD"

    if fund_data['decision'] == "BUY" and tech_data['signal'] == "BUY":
        final_action = "STRONG BUY"
    elif tech_data['signal'] == "SELL":
        final_action = "SELL"

    # -----------------------------
    # METRIC CARDS
    # -----------------------------
    st.markdown("## Decision Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Fundamental", fund_data.get("decision", "N/A"))
    col2.metric("Technical", tech_data.get("signal", "N/A"))
    col3.metric("Final Action", final_action)

    st.markdown("---")

    # -----------------------------
    # LOAD PRICE DATA
    # -----------------------------
    csv_path = f"data/raw/{symbol}_daily_prices.csv"

    if not os.path.exists(csv_path):
        st.warning("Price data missing.")
        return

    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    # Moving Average
    df["MA20"] = df["close"].rolling(20).mean()

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # -----------------------------
    # TABS
    # -----------------------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Price",
        "📉 Technical",
        "📋 Fundamentals",
        "🧠 Events"
    ])

    # =====================================================
    # TAB 1 PRICE CHART
    # =====================================================
    with tab1:
        st.subheader("Candlestick Chart + MA20")

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df['date'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ))

        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['MA20'],
            name="MA20",
            line=dict(width=2)
        ))

        fig.update_layout(
            height=500,
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # TAB 2 TECHNICAL
    # =====================================================
    with tab2:
        st.subheader("RSI Indicator")

        fig_rsi = px.line(
            df,
            x="date",
            y="RSI",
            title="RSI (Relative Strength Index)"
        )

        fig_rsi.add_hline(y=70)
        fig_rsi.add_hline(y=30)

        st.plotly_chart(fig_rsi, use_container_width=True)

        st.markdown("### Risk Reward")

        rr = tech_data.get("risk_reward")

        if rr:
            col1, col2, col3 = st.columns(3)

            col1.metric("Entry", rr["entry"])
            col2.metric("Stop Loss", rr["stop_loss"])
            col3.metric("Target", rr["target"])

            st.progress(min(rr["risk_reward"] / 5, 1.0))
            st.write(f"Risk Reward Ratio : 1 : {rr['risk_reward']}")
        else:
            st.info("Risk reward not available")

    # =====================================================
    # TAB 3 FUNDAMENTAL
    # =====================================================
    with tab3:
        st.subheader("Fundamental Metrics")

        col1, col2, col3 = st.columns(3)

        col1.metric("PE Ratio", fund_data["pe_ratio"])
        col2.metric("ROE", fund_data["roe"])
        col3.metric("Debt/Equity", fund_data["debt_equity"])

        st.markdown("### Fundamental Score")
        st.progress(fund_data["score"] / 3)

    # =====================================================
    # TAB 4 EVENTS
    # =====================================================
    with tab4:
        st.subheader("Market Events")

        st.info(f"Trend : {event_data['trend']}")

        for event in event_data["events"]:
            if "Breakout" in event or "Buy" in event:
                st.success(event)
            elif "Sell" in event:
                st.error(event)
            else:
                st.warning(event)

# import streamlit as st
# import json
# import os
# import pandas as pd
# import plotly.express as px
# from python.event_detection import detect_events_refined

# def load_json_data(folder, symbol, suffix):
#     path = os.path.join("data", folder, f"{symbol}_{suffix}.json")
#     if os.path.exists(path):
#         with open(path, "r") as f:
#             return json.load(f)
#     return None

# def render_dashboard():
#     symbol = st.session_state.get('symbol')

#     if not symbol:
#         st.warning("⚠️ No stock selected. Please go to the **Home** page and run an analysis first.")
#         return

#     st.title(f"📈 Analysis Dashboard: {symbol}")
    
#     # Load Data from Files
#     fund_data = load_json_data("fundamentals", symbol, "fundamentals")
#     tech_data = load_json_data("processed", symbol, "technical")
#     event_data = detect_events_refined(symbol)

#     if not fund_data or not tech_data:
#         st.error("Data files missing. Please run the analysis pipeline again.")
#         return

#     # --- Top Metrics Section ---
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Fundamental Rating", fund_data.get("decision", "N/A"))
#     col2.metric("Technical Signal", tech_data.get("signal", "N/A"))
    
#     # Final Action logic mirroring decision_engine.py
#     final_action = "HOLD"
#     if fund_data['decision'] == "BUY" and tech_data['signal'] == "BUY":
#         final_action = "STRONG BUY"
#     elif tech_data['signal'] == "SELL":
#         final_action = "SELL"
        
#     col3.metric("Final Action", final_action)

#     st.markdown("---")

#     # --- Charts Section ---
#     col_left, col_right = st.columns(2)

#     with col_left:
#         st.subheader("📊 Price & Technicals")
#         # Load CSV for plotting
#         csv_path = f"data/raw/{symbol}_daily_prices.csv"
#         if os.path.exists(csv_path):
#             df = pd.read_csv(csv_path)
#             fig = px.line(df, x='date', y='close', title=f"{symbol} Price History")
#             st.plotly_chart(fig, use_container_width=True)
#         else:
#             st.info("Price CSV not found for charting.")

#     with col_right:
#         st.subheader("🧠 Event Alerts")
#         st.info(f"Market Trend: **{event_data['trend']}**")
#         for event in event_data["events"]:
#             if "Breakout" in event or "Buy" in event:
#                 st.success(event)
#             elif "Sell" in event:
#                 st.error(event)
#             else:
#                 st.info(event)

#     # --- Fundamental Breakdown ---
#     st.subheader("📋 Fundamental Details")
#     st.json(fund_data)

#     if st.button("Generate Final Report"):
#         st.session_state['page'] = "Generate Report"
#          st.rerun()