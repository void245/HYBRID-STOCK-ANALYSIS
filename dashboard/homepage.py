import streamlit as st
from python.pipeline_runner import run_full_pipeline


def render_homepage():

    st.title("📊 Event-Aware Hybrid Stock Analyzer")

    st.markdown("""
    This system combines:
    - Fundamental Analysis  
    - Technical Indicators  
    - Event-Driven Signals  
    """)

    st.markdown("---")

    center = st.columns([1,2,1])

    with center[1]:

        symbol = st.text_input(
            "Enter Stock Symbol",
            placeholder="Example: AAPL / NVDA / TSLA",
            value=st.session_state.get('symbol', "")
        )

        analyze = st.button("Run Full Analysis")

        if analyze and symbol:

            symbol = symbol.upper().strip()
            st.session_state['symbol'] = symbol

            with st.spinner("Running Hybrid Pipeline..."):
                try:
                    run_full_pipeline(symbol)
                    st.success("Analysis Completed")

                    st.session_state["auto_nav"] = True
                    st.rerun()

                except Exception as e:
                    st.error(e)

    # AUTO NAVIGATION
    if st.session_state.get("auto_nav"):
        st.session_state["auto_nav"] = False
        st.session_state["page"] = "Dashboard"

# import streamlit as st
# from python.pipeline_runner import run_full_pipeline

# def render_homepage():
#     st.title("📊 Event-Aware Hybrid Stock Analyzer")

#     st.markdown("""
#         Welcome to the Event-Aware Hybrid Stock Analyzer!
#         This system combines Fundamental, Technical, and Event-based logic.
#     """)
    
#     st.markdown("---")

#     col1, col2 = st.columns([3, 1])

#     with col1:
#         # Use session_state to persist the symbol across pages
#         symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, NVDA):", 
#                                value=st.session_state.get('symbol', ""))

#     with col2:
#         st.write("##") # Alignment spacer
#         analyze = st.button("Analyze")

#     if analyze and symbol:
#         symbol = symbol.upper().strip()
#         st.session_state['symbol'] = symbol # Save to session
        
#         with st.spinner(f"Running full pipeline for {symbol}..."):
#             try:
#                 run_full_pipeline(symbol)
#                 st.success(f"Analysis for {symbol} is complete! Go to Dashboard.")
#             except Exception as e:
#                 st.error(f"Pipeline Error: {e}")