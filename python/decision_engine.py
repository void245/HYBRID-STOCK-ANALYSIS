def run_decision_engine(symbol):

    import json
    import os
    from python.event_detection import detect_events_refined   # 👈 ADD THIS

    #===================================
    # USER INPUT
    #===================================

    symbol = symbol.upper()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    fund_file = os.path.join(BASE_DIR , "data", "fundamentals", f"{symbol}_fundamentals.json")
    tech_file = os.path.join(BASE_DIR , "data", "processed", f"{symbol}_technical.json")

    if not os.path.exists(fund_file) or not os.path.exists(tech_file):
        print("Required analysis files are missing.")
        exit()

    #===================================
    # LOAD DATA
    #===================================

    with open(fund_file) as f:
        fundamentals = json.load(f)

    with open(tech_file) as f:
        technicals = json.load(f)

    fund_decision = fundamentals["decision"]
    tech_signal = technicals["signal"]
    rr_data = technicals.get("risk_reward", None)


    #====================================
    # GET EVENT + TREND DATA
    #====================================

    event_data = detect_events_refined(symbol)
    events = event_data["events"]
    trend = event_data["trend"]

    #====================================
    # ADVANCED HYBRID LOGIC
    #====================================

    final_decision = "HOLD"

    # 🚀 STRONG BUY
    if (
        fund_decision == "BUY"
        and tech_signal == "BUY"
        and trend == "UPTREND"
        and any("Breakout" in e or "Buy the Dip" in e for e in events)
    ):
        final_decision = "🚀 STRONG BUY"

    # 🔴 STRONG SELL
    elif (
        tech_signal == "SELL"
        and trend == "DOWNTREND"
        and any("Sell the Rally" in e for e in events)
    ):
        final_decision = "🔴 STRONG SELL"

    # 📈 LONG TERM BUY
    elif fund_decision == "BUY" and trend == "UPTREND":
        final_decision = "📈 LONG TERM BUY"

    # ⚪ HOLD
    else:
        final_decision = "⚪ HOLD"

    #====================================
    # RISK REWARD FILTER (NEW)
    #====================================

    if rr_data:
        rr_ratio = rr_data["risk_reward"]

        # If risk-reward is poor → downgrade decision
        if rr_ratio < 1 and final_decision != "⚪ HOLD":
            final_decision = "⚪ HOLD (Poor Risk-Reward)"    

    #====================================
    # CONFIDENCE SCORE LOGIC 
    #====================================
    def calculate_confidence_score(fund_decision, tech_signal, trend, events):
        """
        Calculates a 0–100 confidence score using weighted multi-factor logic.
        """

        # -----------------------------
        # Safety handling
        # -----------------------------
        fund = fund_decision.upper()
        tech = tech_signal.upper()
        trend = trend.upper()
        events = events or []

        confidence = 0

        # -----------------------------
        # WEIGHTS
        # -----------------------------
        FUND_WEIGHT = 40
        TECH_WEIGHT = 30
        TREND_WEIGHT = 20
        EVENT_WEIGHT = 10

        # -----------------------------
        # Fundamental scoring
        # -----------------------------
        if fund == "BUY" or fund == "SELL":
            confidence += FUND_WEIGHT
        elif fund == "HOLD":
            confidence += FUND_WEIGHT * 0.4   # Neutral strength

        # -----------------------------
        # Technical scoring
        # -----------------------------
        if tech == "BUY" or tech == "SELL":
             confidence += TECH_WEIGHT
        elif tech == "HOLD":
            confidence += TECH_WEIGHT * 0.4

        # -----------------------------
        # Trend scoring
        # -----------------------------
        if trend in ["UPTREND", "DOWN", "DOWNTREND"]:
            confidence += TREND_WEIGHT
        elif trend == "SIDEWAYS":
            confidence += TREND_WEIGHT * 0.4

        # -----------------------------
        # Event scoring
        # -----------------------------
        event_score = 0

        for e in events:
            e = e.lower()

            if "breakout" in e:
                event_score += 6
            elif "volume" in e:
                event_score += 3
            elif "dip" in e or "rally" in e:
                event_score += 5

        event_score = min(event_score, EVENT_WEIGHT)
        confidence += event_score

        # -----------------------------
        # Opposite Signal Penalty
        # -----------------------------
        if (fund == "BUY" and tech == "SELL") or (fund == "SELL" and tech == "BUY"):
            confidence *= 0.5   # Strong penalty

        # -----------------------------
        # Confluence Bonus
        # -----------------------------
        trend_direction = None

        if trend in ["UPTREND", "UP"]:
            trend_direction = "BUY"
        elif trend in ["DOWNTREND", "DOWN"]:
            trend_direction = "SELL"

        if fund == tech and fund == trend_direction and fund in ["BUY", "SELL"]:
            confidence += 10

        # -----------------------------
        # Final formatting
        # -----------------------------
        confidence = min(confidence, 100)

        return round(confidence)

    confidence = calculate_confidence_score(
        fund_decision,
        tech_signal,
        trend,
        events
    )
    import plotly.graph_objects as go

    def create_confidence_gauge(score, ticker, final_decision):
        """
        Create a professional dark-theme gauge chart for stock confidence.

        Parameters:
        score (int/float): Confidence score (0–100)
        ticker (str): Stock symbol (e.g., AAPL)
        final_decision (str): Final trading decision (e.g., STRONG BUY)

         Returns:
        fig: Plotly Figure object
        """
    

        # Safety clamp
        score = max(0, min(100, score))

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            number={'suffix': "%"},
            title={
                'text': f"{ticker} Confidence Score",
                'font': {'size': 24, 'color': "white"}
            },
            gauge={
                'axis': {
                    'range': [0, 100],
                    'tickcolor': "white"
                },

                 # Needle color
                'bar': {'color': "#00FFAA"},

                # Color sectors
                'steps': [
                    {'range': [0, 40], 'color': "#FF4C4C"},   # Red
                    {'range': [40, 70], 'color': "#FFD84C"},  # Yellow
                    {'range': [70, 100], 'color': "#00CC66"}  # Green
                ],

                 # Outer border styling
                'borderwidth': 2,
                'bordercolor': "white"
            }
        ))

        # Dark professional layout
        fig.update_layout(
            paper_bgcolor="black",
            plot_bgcolor="black",
            font={'color': "white"},
            margin=dict(l=20, r=20, t=60, b=60),

            # Annotation for final decision
            annotations=[
                dict(
                    text=f"Final Decision: <b>{final_decision}</b>",
                    x=0.5,
                    y=0.05,
                    showarrow=False,
                    font=dict(size=18, color="white")
                )
            ]
        )

        return fig

    #====================================
    # OUTPUT RESULT
    #====================================

    print("\nFINAL DECISION REPORT")
    print("-----------------------")
    print(f"Stock: {symbol}")
    print(f"Fundamental Decision: {fund_decision}")
    print(f"Technical Signal: {tech_signal}")
    print(f"Trend: {trend}")
    print(f"Confidence Score: {confidence}%")
    #====================================
    # RISK REWARD OUTPUT
    #====================================

    if rr_data:
        print("\nRISK-REWARD ANALYSIS")
        print("-----------------------")
        print(f"Entry Price : {rr_data['entry']}")
        print(f"Stop Loss   : {rr_data['stop_loss']}")
        print(f"Target      : {rr_data['target']}")
        print(f"Risk-Reward : 1 : {rr_data['risk_reward']}")

    #====================================
    # EVENTS OUTPUT
    #====================================    
    print("\nDetected Events:")
    for e in events:
        print("-", e)

    print("\nFINAL DECISION:", final_decision)


