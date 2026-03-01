import pandas as pd
import os

def detect_events_refined(symbol):
    import pandas as pd 
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    price_file = os.path.join(BASE_DIR, "data", "raw", f"{symbol}_daily_prices.csv")

    if not os.path.exists(price_file):
        return {
            "events": ["Price data not found"],
            "trend": None
        }

    df = pd.read_csv(price_file)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    df = df.sort_values("date")

    # --- Indicators ---
    df["MA20"] = df["close"].rolling(20).mean()
    df["MA200"] = df["close"].rolling(200).mean()

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    latest = df.iloc[-1]
    prev_day = df.iloc[-2]

    events = []

    # -----------------------------
    # 1️⃣ Trend Detection
    # -----------------------------
    is_uptrend = latest["close"] > latest["MA200"]
    trend = "UPTREND" if is_uptrend else "DOWNTREND"

    # -----------------------------
    # 2️⃣ Volume Spike
    # -----------------------------
    avg_volume = df["volume"].rolling(20).mean().iloc[-1]

    if latest["volume"] > 2 * avg_volume and latest["close"] > prev_day["close"]:
        events.append("⚡ Positive Volume Spike (Buying Pressure)")

    # -----------------------------
    # 3️⃣ Confirmed Breakout
    # -----------------------------
    last_30_high = df["close"].rolling(30).max().iloc[-2]

    if latest["close"] > last_30_high and is_uptrend:
        events.append("🚀 Trend-Confirmed Breakout")

    # -----------------------------
    # 4️⃣ Contextual RSI
    # -----------------------------
    if is_uptrend and latest["RSI"] < 35:
        events.append("🟢 Buy the Dip (Oversold in Uptrend)")
    elif not is_uptrend and latest["RSI"] > 65:
        events.append("🔴 Sell the Rally (Overbought in Downtrend)")

    if not events:
        events.append("No high-probability events detected")

    return {
        "events": events,
        "trend": trend
    }