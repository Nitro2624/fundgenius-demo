
# FundGenius: Internal AI-Powered Mutual Fund Assistant
# Streamlit App Code (MVP Version)

import streamlit as st
import pandas as pd

# Title and Description
st.set_page_config(page_title="FundGenius - SBI MF Assistant", layout="centered")
st.title("💸 FundGenius - Internal Mutual Fund Assistant")
st.markdown("""
This AI-powered tool helps SBI MF employees recommend suitable funds based on client profiles.
""")

# Input Section
st.header("📝 Client Profile")
age = st.slider("Client Age:", 18, 80, 30)
risk = st.selectbox("Risk Appetite:", ["Low", "Moderate", "High"])
goal = st.selectbox("Financial Goal:", ["Retirement", "Wealth Creation", "Education", "Tax Saving", "General Investment"])
duration = st.slider("Investment Duration (in years):", 1, 30, 5)

# Fund Mapping Logic
funds_data = {
    "Debt & Liquid Funds": [
        "SBI Liquid Fund",
        "SBI Magnum Ultra Short Duration Fund",
        "SBI Magnum Low Duration Fund"
    ],
    "Hybrid Funds": [
        "SBI Equity Hybrid Fund",
        "SBI Balanced Advantage Fund",
        "SBI Conservative Hybrid Fund"
    ],
    "Equity Funds": [
        "SBI Bluechip Fund",
        "SBI Small Cap Fund",
        "SBI Focused Equity Fund",
        "SBI Contra Fund",
        "SBI Large & Midcap Fund"
    ]
}

# Recommendation Engine
def recommend_funds(risk, duration):
    if risk == "Low" and duration <= 1:
        return "Debt & Liquid Funds"
    elif risk == "Moderate" and duration <= 3:
        return "Hybrid Funds"
    elif risk == "High" and duration > 3:
        return "Equity Funds"
    else:
        return "Hybrid Funds" if duration <= 3 else "Equity Funds"

# Button and Result
if st.button("🔍 Get Fund Recommendations"):
    category = recommend_funds(risk, duration)
    st.subheader(f"Recommended Fund Category: {category}")
    st.success("Suggested Funds:")
    for fund in funds_data[category]:
        st.markdown(f"- {fund}")

# Footer
st.markdown("---")
st.caption("Developed by Nitro2624 | Powered by Streamlit")
