def run_technical(symbol):   
    import pandas as pd
    import os
    import json 

    #==========================================
    # USER INPUT
    #==========================================

    symbol = symbol.upper()

    #===========================================
    # LOAD PRICE DATA
    #===========================================

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    price_file = os.path.join(BASE_DIR, "data", "raw", f"{symbol}_daily_prices.csv")

    if not os.path.exists(price_file):
        print("Price data not found . Run data_fetcher.py first.")
        exit()

    df = pd.read_csv(price_file)
    df["close"] = df["close"].astype(float)

    #sort by date
    df = df.sort_values("date")

    #===========================================
    # MOVING AVERAGES 
    #===========================================

    df["MA20"] = df["close"].rolling(window=20).mean()

    #===========================================
    #RSI CALCULATION
    #===========================================

    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss 
    df["RSI"] = 100 - (100 / (1 + rs))

    #===========================================
    #Risk Reward Ratio
    #===========================================
    def calculate_risk_reward(df):
        """
        Calculate Risk-Reward using 20-day support/resistance
        """

        latest_price = df["close"].iloc[-1]

        support = df["close"].rolling(20).min().iloc[-1]
        resistance = df["close"].rolling(20).max().iloc[-1]

        risk = latest_price - support
        reward = resistance - latest_price

        if risk <= 0:
            return None

        rr_ratio = reward / risk

        return {
            "entry": round(latest_price, 2),
            "stop_loss": round(support, 2),
            "target": round(resistance, 2),
            "risk_reward": round(rr_ratio, 2)
        }

    rr_data = calculate_risk_reward(df)
    #===========================================
    # DECISION LOGIC
    #===========================================

    latest = df.iloc[-1]

    signal = "HOLD"

    if latest["close"] > latest["MA20"] and latest["RSI"] < 70 :
        signal = "BUY"
    elif latest["close"] < latest["MA20"] and latest["RSI"] > 30 :
        signal = "SELL"

    #=============================================
    # #SAVE RESULTS
    #=============================================

    tech_dir = os.path.join(BASE_DIR , "data", "processed")
    os.makedirs(tech_dir , exist_ok=True)

    output = {
        "symbol" : symbol,
        "close_price" : round(latest["close"], 2),
        "MA20" : round(latest["MA20"], 2),
        "RSI" : round(latest["RSI"], 2),
        "signal" : signal,
        "risk_reward" : rr_data
    }

    file_path = os.path.join(tech_dir, f"{symbol}_technical.json")

    with open(file_path, "w")as f:
        json.dump(output, f, indent=4)

    print(f"Technical analysis signal : {signal}")
    print(f"saved to {file_path}")


