from python.data_f import run_data_fetch
from python.fundamentals import run_fundamental
from python.technical_analysis import run_technical
from python.decision_engine import run_decision_engine

def run_full_pipeline(symbol):
    print(f"🚀Starting pipeline for : {symbol}")

    run_data_fetch(symbol)
    run_fundamental(symbol)
    run_technical(symbol)
    run_decision_engine(symbol)

    print("✅ Pipeline completed successfully!")