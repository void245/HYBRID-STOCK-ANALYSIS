def run_data_fetch(symbol):

    import csv
    import requests
    import os

    # ==============================
    # USER INPUT
    # ==============================
    symbol = symbol.upper()

    # ==============================
    # API DETAILS
    # ==============================
    API_KEY = YOUR_API_KEY
    URL = "https://www.alphavantage.co/query"

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY
    }

    print("Fetching daily stock data...")

    response = requests.get(URL, params=params)
    data = response.json()
    
    # ==============================
    # ERROR HANDLING
    # ==============================
    if "Time Series (Daily)" not in data:
       print("❌ Error fetching data")
       return  # Exit the function if data is not available
    #print(data)
    #exit()

    time_series = data["Time Series (Daily)"]

    # ==============================
    # SAVE TO CSV
    # ==============================
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/{symbol}_daily_prices.csv"

    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["date", "open", "high", "low", "close", "volume"])

        for date, values in time_series.items():
            writer.writerow([
             date,
                float(values["1. open"]),
                float(values["2. high"]),
                float(values["3. low"]),
                float(values["4. close"]),
                int(values["5. volume"])
            ])

    print(f"✅ Daily stock data saved to {file_path}")
