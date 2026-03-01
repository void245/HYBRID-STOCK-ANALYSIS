📈 Event-Aware Stock Market Analyzer
A Full-Stack Quantitative Analysis Dashboard & Decision Engine

🚀 Project Overview
This system is a multi-layer financial intelligence pipeline designed to simulate modern quantitative trading dashboards. It integrates Fundamental Analysis, Technical Indicators, and Real-time Event Detection into a unified Confidence Score Engine.

Unlike simple price trackers, this project uses a weighted decision matrix to provide actionable "Buy/Hold/Sell" signals backed by data confluence.

🧠 Core Intelligence Layers

1. Fundamental Analysis Engine
Evaluates long-term company health by processing :
  * Valuation : P/E Ratio vs. Historical Averages.
  * Profitibility : ROE( Return tn Equity)
  * Solvency : Debt-to-Equity ratios.
  * Signal : Generates a "Value Score" from 0-100.
    
2.Technical Analysis Engine
Detects price trends and momentum using:
* Trend: Dual Moving Average Crossover (MA20/MA200).
* Momentum: RSI (Relative Strength Index) with overbought/oversold logic.
* Volatility: Price action analysis for trend confirmation.

3. Event Detection (Algorithmic Triggers)
Identifies high-impact market anomalies:
* Volume Spikes: Detects $Z\text{-score} > 2$ volume anomalies.
* Breakouts: Identifies price movement outside 20-day resistance levels.
* Mean Reversion: "Buy-the-Dip" signals based on statistical deviations.

4. The Weighted Confidence Model
The system calculates a final conviction score using a weighted matrix:

Factor      	   Weight    	Description
Fundamentals	    40%     	Long-term structural strength.
Technicals	      30%	      Mid-term trend alignment.
Trend Consistency	20%	      Price directionality (Bull/Bear).
Event Triggers	  10%	      Short-term momentum bursts

Note: The engine includes a Divergence Penalty. If Technicals and Fundamentals provide opposite signals, the Confidence Score is automatically docked by 15% to warn the user of "Decoupled Risk."


🛠 Tech Stack & Architecture

* Language: Python 3.x
* Data Science: Pandas (Data Wrangling), NumPy (Vectorized Math).
* Visualization: Plotly (Interactive Candlestick & Gauge Charts).
* Web Framework: Streamlit (Reactive UI).
* API: Alpha Vantage (Financial Data).

Project Structure
stock-market-analyzer/
├── app.py                     # Streamlit Entry Point
├── dashboard/                 # UI Components
├── python/
│   ├── data_f.py              # API Wrapper & Caching
│   ├── fundamentals.py        # Financial Ratio Logic
│   ├── technical_analysis.py  # Indicator Calculations
│   ├── event_detection.py     # Algorithmic Triggers
│   └── decision_engine.py     # Weighted Scoring Logic
└── data/                      # Local Data Storage

▶️ Getting Started
1. Clone & Install
  Bash
      git clone https://github.com/yourusername/stock-market-analyzer.git
      cd stock-market-analyzer
      pip install -r requirements.txt

2.Configuration    
  * Get a free API Key from Alpha Vantage
  * Open python/data_f.py and replace YOUR_API_KEY.

3.Run the Dashboard
  streamlit run app.py

💡 Future Roadmap
[ ] NLP Sentiment Analysis: Integrating news headlines via FinViz.
[ ] Machine Learning: LSTM model for 5-day price forecasting.
[ ] Portfolio Backtesting: Performance simulation against the S&P 500. 

👨‍💻 Author
Purvesh Hande
Information Technology Student | Data Analytics & Python Enthusiast
