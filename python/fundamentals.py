def run_fundamental(symbol):   
    import requests
    import json
    import os

    #==========================================
    # USER INPUT
    #==========================================

    symbol = symbol.upper()

    #===========================================
    #API DETAILS
    #============================================

    API_KEY = "OOMSJDYHESFFOICS"
    URL = "https://www.alphavantage.co/query"

    params = {
        "function" : "OVERVIEW" ,
        "symbol" : symbol ,
        "apikey" : API_KEY
    }

    print("Fetching fundamental data....")

    response = requests.get(URL, params=params)
    data = response.json()

    if not data or "Symbol" not in data:
        print("Failed to fetch fundamental data.")
        print(data)
        exit()

    #==============================================
    # SIMPLE FUNDAMENTAL ANALYSIS
    #==============================================    

    pe_ratio = float(data.get("PERatio", 0) or 0)
    roe = float(data.get("ReturnOnEquityTTM", 0) or 0)
    debt_equity = float(data.get("DebtToEquity", 0) or 0)

    score = 0

    if pe_ratio > 0 and pe_ratio < 25 :
        score += 1 

    if roe and roe > 0.15 :
        score += 1
    if debt_equity and debt_equity < 1 :
        score += 1 


    if score >= 2 :
        decision = "BUY"
        reason = "Fundamentals strong"
    elif score == 1 :
        decision = "HOLD"
        reason = "Fundamentals mixed"
    else :
        decision = "SELL"
        reason = "Fundamentals weak"    

    #=============================================
    # SAVE RESULTS 
    #=============================================

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fund_dir = os.path.join(BASE_DIR , "data", "fundamentals")
    os.makedirs(fund_dir, exist_ok=True)  

    file_path = os.path.join(fund_dir, f"{symbol}_fundamentals.json")

    output = {
        "symbol" : symbol,
        "pe_ratio" : pe_ratio,
        "roe" : roe ,
        "debt_equity" : debt_equity ,
        "score" : score ,
        "decision" : decision
    }

    with open(file_path , "w") as f:
        json.dump(output , f , indent=4)

    print(f"Fundamental analysis completed -> {decision} ")
    print(f"saved to {file_path}")
