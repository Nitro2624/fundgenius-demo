import streamlit as st
import pandas as pd
from modules.recommender import recommend_funds, get_fund_mix
from modules.amfi_data import get_latest_navs_for_sbi
from modules.manager_notes import get_fund_manager_notes
from modules.market_data_api import get_live_market_indices, get_stock_data

st.set_page_config(page_title="FundGenius - SBI MF Assistant", layout="wide")

st.title("💼 FundGenius - AI Mutual Fund Assistant (Internal)")
st.caption("For SBI Mutual Fund Employee Use Only")
st.markdown("---")

# --- Sidebar: Client Input & Filters ---
st.sidebar.header("📋 Client Profile & Filters")
age = st.sidebar.slider("Client Age", 18, 80, 30, help="Age of the client.")
risk = st.sidebar.selectbox("Risk Profile", ["Conservative", "Low", "Moderate", "High", "Aggressive"], index=2, help="Client's willingness to take investment risk.")
goal = st.sidebar.selectbox("Investment Goal", ["Retirement Planning", "Wealth Creation", "Child's Education", "Tax Saving", "General Investment", "Short-term Capital Gain"], help="Primary objective of the investment.")
duration = st.sidebar.slider("Investment Duration (Years)", 1, 30, 5, help="Expected investment horizon in years.")
amount = st.sidebar.number_input("Investment Amount (INR)", 1000, 100000000, 100000, step=1000, help="Total amount client intends to invest.")
st.sidebar.markdown("---")
st.sidebar.info("Adjust client parameters to get tailored recommendations and insights.")


# --- Main Content Area ---

# 1. Fund Recommendation
st.header("🎯 Fund Recommendation")
st.markdown("Based on the client's profile, here are the suggested fund categories and specific SBI Mutual Fund schemes.")
try:
    recommended_category, suggested_funds = recommend_funds(risk, duration, goal)
    st.success(f"**Recommended Category:** {recommended_category}")
    st.subheader("Suggested SBI Mutual Fund Schemes:")
    if suggested_funds:
        for fund in suggested_funds:
            st.markdown(f"- **{fund['name']}** - _{fund['type']}_ [Recommended Allocation: {fund['weightage']}%]")
            st.write(f"  * _Rationale: {fund['rationale']}_")
    else:
        st.warning("No specific funds could be recommended based on the current criteria. Please adjust inputs or contact a senior advisor.")
except Exception as e:
    st.error(f"Error generating fund recommendations: {e}")
    st.info("Ensure the `recommender.py` module is correctly configured and has a comprehensive fund database.")
st.markdown("---")

# 2. Suggested Fund Mix
st.header("🔄 Suggested Fund Mix & Allocation")
st.markdown("Here's a proposed allocation of the client's investment amount across the recommended funds.")
try:
    if suggested_funds: # Only show mix if funds were recommended
        mix_data = get_fund_mix(suggested_funds, amount)
        st.subheader("Investment Allocation Breakdown:")
        total_allocated = 0
        for item in mix_data:
            st.markdown(f"- ₹**{item['amount']:,}** (`{item['percentage']:.2f}%`) → **{item['fund']}**")
            total_allocated += item['amount']
        st.markdown(f"**Total Allocated Amount:** ₹{total_allocated:,}")
        if total_allocated != amount:
            st.warning(f"Note: Total allocated amount (₹{total_allocated:,}) differs from the input amount (₹{amount:,}). This might be due to rounding).")
    else:
        st.info("Please generate fund recommendations first to see a fund mix.")
except Exception as e:
    st.error(f"Error generating fund mix: {e}")
    st.info("Check the `get_fund_mix` function in `recommender.py`.")
st.markdown("---")

# 3. Fund Manager Insights
st.header("🧠 Fund Manager Insights & Commentary")
st.markdown("Stay updated with the latest commentary and outlook from our expert fund managers.")
try:
    notes = get_fund_manager_notes()
    if notes:
        for i, line in enumerate(notes):
            st.info(f"🔹 **Insight {i+1}:** {line}")
    else:
        st.info("No recent fund manager insights available. Check back later.")
except Exception as e:
    st.error(f"Error fetching fund manager notes: {e}")
    st.info("Ensure the `manager_notes.py` module can access its data source.")
st.markdown("---")

# 4. Live NAVs (SBI Mutual Funds)
st.header("📈 SBI Mutual Fund NAVs (Live)")
st.markdown("Access the latest Net Asset Values (NAVs) for SBI Mutual Fund schemes. Data typically updated daily after market close.")
try:
    # This function should fetch actual NAVs from AMFI or a reliable API
    navs_df = get_latest_navs_for_sbi()
    if not navs_df.empty:
        st.dataframe(navs_df, use_container_width=True, height=300)
        st.caption(f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')} (Data source for NAVs: AMFI or authorized API)")
    else:
        st.warning("Could not fetch latest SBI Mutual Fund NAVs. Data might be unavailable or API limit reached.")
except Exception as e:
    st.error(f"Error fetching live NAVs: {e}")
    st.info("Verify your internet connection and the `get_latest_navs_for_sbi` function in `amfi_data.py`.")
st.markdown("---")

# 5. General Market Data (Optional, but highly functional)
st.header("📊 General Market Overview")
st.markdown("Quick glance at key Indian market indices and selected stock performance.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Major Indices")
    try:
        indices_data = get_live_market_indices()
        if not indices_data.empty:
            st.dataframe(indices_data, use_container_width=True, hide_index=True)
            st.caption("Source: Live Market Data API (e.g., Broker API)")
        else:
            st.info("Could not fetch live index data.")
    except Exception as e:
        st.error(f"Error fetching live index data: {e}")
        st.info("Check `get_live_market_indices` in `market_data_api.py`.")

with col2:
    st.subheader("Key SBI Stock Performance")
    # This is a placeholder for specific stock data related to SBI or its holdings
    sbi_stock_ticker = "SBIN.NS" # Example for NSE: SBI
    try:
        stock_info = get_stock_data(sbi_stock_ticker)
        if stock_info:
            st.write(f"**{stock_info.get('symbol', 'N/A')}** - {stock_info.get('name', 'N/A')}")
            st.write(f"Current Price: ₹**{stock_info.get('current_price', 'N/A'):,.2f}**")
            st.write(f"Change: {'+' if stock_info.get('change', 0) >= 0 else ''}{stock_info.get('change', 'N/A'):,.2f} ({stock_info.get('percent_change', 'N/A'):.2f}%)")
            st.write(f"Open: ₹{stock_info.get('open', 'N/A'):,.2f} | High: ₹{stock_info.get('high', 'N/A'):,.2f} | Low: ₹₹{stock_info.get('low', 'N/A'):,.2f}")
            st.caption("Source: Live Market Data API (e.g., Broker API)")
        else:
            st.info(f"Could not fetch data for {sbi_stock_ticker}.")
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        st.info("Check `get_stock_data` in `market_data_api.py`.")
st.markdown("---")

# --- Footer ---
st.markdown("---")
st.caption("Developed by Nitro2624 for Internal SBI Mutual Fund Use. All recommendations are AI-generated and should be reviewed by a human advisor.")
st.caption("Disclaimer: This tool provides AI-driven insights and is for internal training and informational purposes only. It does not constitute financial advice or an offer to buy/sell securities. Consult a qualified financial advisor for actual investment decisions.")
