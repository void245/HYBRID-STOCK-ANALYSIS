import streamlit as st


def render_sidebar():

    st.sidebar.title("📊 Hybrid Stock AI")

    symbol = st.session_state.get("symbol")

    if symbol:
        st.sidebar.success(f"Active : {symbol}")
    else:
        st.sidebar.warning("No Stock Selected")

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        ["Home", "Dashboard", "Generate Report"]
    )

    st.sidebar.markdown("---")

    st.sidebar.caption("Fundamental + Technical + Event Intelligence")

    return page

# import streamlit as st

# def render_sidebar():
#     st.sidebar.title("📊 Stock Analyzer")

#     # Display current active symbol if it exists
#     current_symbol = st.session_state.get('symbol', "None")
#     st.sidebar.write(f"**Active Ticker:** :green[{current_symbol}]")

#     page = st.sidebar.radio(
#         "Navigation",
#         ["Home", "Dashboard", "Generate Report"]
#     )

#     st.sidebar.markdown("---")
#     st.sidebar.info("Hybrid Stock Analysis System\n\nFundamental + Technical + Event")

#     return page