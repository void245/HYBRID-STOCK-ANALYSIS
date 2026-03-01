import streamlit as st
from dashboard.sidebar import render_sidebar
from dashboard.homepage import render_homepage
from dashboard.main_dashboard import render_dashboard

# Standard Streamlit Setup
st.set_page_config(
    page_title="Event-Aware Stock Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"

)
st.markdown("""
<style>
.block-container{
    padding-top:2rem;
}
</style>
""", unsafe_allow_html=True)


# 1. Sidebar Navigation 
# This returns the string value of the selected radio button
page = render_sidebar()

# 2. Page Routing
if page == "Home":
    render_homepage()

elif page == "Dashboard":
    render_dashboard()

elif page == "Generate Report":
    st.title("📄 Investment Report Generator")
    symbol = st.session_state.get('symbol')
    
    if symbol:
        st.write(f"Generating comprehensive report for **{symbol}**...")
        # We will plug the report logic here next
        st.button("Download PDF Report (Coming Soon)")
    else:
        st.warning("Please analyze a stock on the Home page first.")

else:
    # Fallback for other menu items like 'Data Fetcher' etc.
    st.title(page)
    st.info("This module is currently being integrated.")