def run_data_fetch(symbol):
    import requests
    import csv
    import os

    #=========================================
    # USER INPUT
    #=========================================
    symbol = symbol.upper()

    #=========================================
    # API DETAILS
    #=========================================

    API_KEY = "OOMSJDYHESFFOICS"
    URL = "https://www.alphavantage.co/query"

    #=========================================

    params ={
        "function" : "TIME_SERIES_INTRADAY" ,
        "symbol" : symbol ,
        "interval": "5min",          # 👈 IMPORTANT CHANGE
        "outputsize": "compact", 
        "apikey" : API_KEY
    }

    #=========================================
    # FETCH DATA
    #=========================================

    response = requests.get(URL , params=params)
    data = response.json()

    if "Time Series (1min)" not in data:
        print("Error fetching data . API limit or invalid symbol.")
        print(data)
        exit()
    time_series = data["Time Series (1min)"]

    #=========================================
    # SAVE TO CSV
    #=========================================

    os.makedirs("data/raw" , exist_ok=True)
    file_path = f"data/raw/{symbol}_live_prices.csv"

    with open(file_path , "w", newline="")as file:
        writer = csv.writer(file)
        writer.writerow(["time", "open", "high", "low", "close", "volume"])

        for time, values in time_series.items():
            writer.writerow([
                time,
                float(values["1. open"]),
                float(values["2. high"]),
                float(values["3. low"]),
                float(values["4. close"]),
                int(values["5. volume"])
            ])

    print(f"Live data saved to {file_path}")