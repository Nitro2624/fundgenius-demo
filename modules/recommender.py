import pandas as pd

def load_fund_data():
    """
    Loads a dummy dataset of SBI Mutual Funds with their characteristics.
    In a real application, this would come from a database or a comprehensive internal API.
    """
    data = {
        'name': [
            "SBI Bluechip Fund", "SBI Equity Hybrid Fund", "SBI Small Cap Fund",
            "SBI contra fund", "SBI Long Term Equity Fund", "SBI Large & Midcap Fund",
            "SBI Balanced Advantage Fund", "SBI Debt Fund", "SBI Liquid Fund"
        ],
        'type': [
            "Equity - Large Cap", "Hybrid - Aggressive Hybrid", "Equity - Small Cap",
            "Equity - Contra", "ELSS", "Equity - Large & Mid Cap",
            "Hybrid - Dynamic Asset Allocation", "Debt - Short Duration", "Debt - Liquid"
        ],
        'risk_profile': [
            "Moderate", "Moderate", "High", "High", "Moderate", "High",
            "Moderate", "Low", "Conservative"
        ],
        'min_duration_years': [
            5, 3, 7, 5, 3, 5, 3, 1, 0.1
        ],
        'max_duration_years': [
            None, None, None, None, None, None, None, 3, 0.5
        ],
        'goal_suitability': [
            ["Wealth Creation", "Retirement Planning"],
            ["Wealth Creation", "Retirement Planning"],
            ["Wealth Creation", "Retirement Planning"],
            ["Wealth Creation"],
            ["Tax Saving", "Wealth Creation"],
            ["Wealth Creation", "Retirement Planning"],
            ["Wealth Creation", "Retirement Planning", "General Investment"],
            ["General Investment", "Short-term Capital Gain"],
            ["General Investment", "Short-term Capital Gain"]
        ],
        'description': [
            "Invests in large-cap companies. Suitable for stable long-term growth.",
            "Combines equity and debt for balanced growth. Good for moderate risk.",
            "Focuses on high-growth small-cap companies. High risk, high reward.",
            "Invests in undervalued stocks. High risk, potential for high returns.",
            "Tax-saving fund with equity exposure. 3-year lock-in.",
            "Diversified across large and mid-cap companies.",
            "Dynamically allocates between equity and debt based on market conditions.",
            "Invests in debt instruments with short maturity. Low risk.",
            "Highly liquid fund for very short-term parking of funds."
        ]
    }
    return pd.DataFrame(data)

# Load fund data once
FUND_DATA = load_fund_data()

def recommend_funds(risk_profile: str, duration_years: int, investment_goal: str) -> tuple:
    """
    Recommends fund categories and specific SBI Mutual Funds based on client's profile.
    This logic can be significantly expanded with more sophisticated rules or ML models.
    """
    recommended_category = "General Investment"
    suggested_funds = []

    # Map input risk to internal risk levels for filtering
    risk_mapping = {
        "Conservative": ["Conservative"],
        "Low": ["Low", "Conservative"],
        "Moderate": ["Moderate", "Low"],
        "High": ["High", "Moderate"],
        "Aggressive": ["High"]
    }
    allowed_risks = risk_mapping.get(risk_profile, ["Moderate"])

    # Filter funds based on risk, duration, and goal
    filtered_funds = FUND_DATA[
        (FUND_DATA['risk_profile'].isin(allowed_risks)) &
        (FUND_DATA['min_duration_years'] <= duration_years) &
        (FUND_DATA['goal_suitability'].apply(lambda x: investment_goal in x))
    ].copy() # Use .copy() to avoid SettingWithCopyWarning

    # Determine recommended category (simplified logic)
    if risk_profile == "High" or risk_profile == "Aggressive":
        recommended_category = "Equity - High Growth"
    elif risk_profile == "Moderate":
        recommended_category = "Hybrid - Balanced"
    else:
        recommended_category = "Debt / Hybrid - Conservative"

    # Sort and select top funds (example logic)
    if not filtered_funds.empty:
        # Example: prioritize funds with matching risk and goal.
        # In a real scenario, you'd have more complex scoring.
        filtered_funds['score'] = 0
        filtered_funds.loc[filtered_funds['risk_profile'] == risk_profile, 'score'] += 1
        filtered_funds.loc[filtered_funds['goal_suitability'].apply(lambda x: investment_goal in x), 'score'] += 1

        # Example: assign rough weights based on risk/category for allocation
        if risk_profile == "High" or risk_profile == "Aggressive":
            # For aggressive, prioritize small/mid caps and growth funds
            priority_funds = filtered_funds[
                (filtered_funds['type'].str.contains("Small Cap|Mid Cap|Contra"))
            ].sort_values(by='score', ascending=False).head(2)
            other_funds = filtered_funds[
                ~(filtered_funds['type'].str.contains("Small Cap|Mid Cap|Contra"))
            ].sort_values(by='score', ascending=False).head(1)
            selected_funds = pd.concat([priority_funds, other_funds]).drop_duplicates().head(3)

            # Assign example weights
            if "SBI Small Cap Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Small Cap Fund", 'weightage'] = 40
            if "SBI Bluechip Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Bluechip Fund", 'weightage'] = 30
            if "SBI contra fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI contra fund", 'weightage'] = 30
            # Ensure total weightage is 100% or adjust dynamically
            selected_funds['weightage'] = selected_funds['weightage'].fillna(100 / len(selected_funds)).round(0)


        elif risk_profile == "Moderate":
            # For moderate, prioritize hybrid and large/mid cap
            priority_funds = filtered_funds[
                (filtered_funds['type'].str.contains("Hybrid|Large & Mid Cap|Bluechip"))
            ].sort_values(by='score', ascending=False).head(2)
            other_funds = filtered_funds[
                ~(filtered_funds['type'].str.contains("Hybrid|Large & Mid Cap|Bluechip"))
            ].sort_values(by='score', ascending=False).head(1)
            selected_funds = pd.concat([priority_funds, other_funds]).drop_duplicates().head(3)

            if "SBI Equity Hybrid Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Equity Hybrid Fund", 'weightage'] = 40
            if "SBI Balanced Advantage Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Balanced Advantage Fund", 'weightage'] = 30
            if "SBI Bluechip Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Bluechip Fund", 'weightage'] = 30
            selected_funds['weightage'] = selected_funds['weightage'].fillna(100 / len(selected_funds)).round(0)

        else: # Low / Conservative
            # For low risk, prioritize debt and conservative hybrid
            priority_funds = filtered_funds[
                (filtered_funds['type'].str.contains("Debt|Liquid|Hybrid - Conservative"))
            ].sort_values(by='score', ascending=False).head(2)
            other_funds = filtered_funds[
                ~(filtered_funds['type'].str.contains("Debt|Liquid|Hybrid - Conservative"))
            ].sort_values(by='score', ascending=False).head(1)
            selected_funds = pd.concat([priority_funds, other_funds]).drop_duplicates().head(3)

            if "SBI Liquid Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Liquid Fund", 'weightage'] = 50
            if "SBI Debt Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Debt Fund", 'weightage'] = 30
            if "SBI Equity Hybrid Fund" in selected_funds['name'].values:
                selected_funds.loc[selected_funds['name'] == "SBI Equity Hybrid Fund", 'weightage'] = 20
            selected_funds['weightage'] = selected_funds['weightage'].fillna(100 / len(selected_funds)).round(0)

        # Convert to list of dicts with rationale
        for _, row in selected_funds.iterrows():
            suggested_funds.append({
                'name': row['name'],
                'type': row['type'],
                'weightage': row['weightage'],
                'rationale': row['description'] # Using description as rationale for now
            })

    return recommended_category, suggested_funds


def get_fund_mix(suggested_funds: list, total_amount: float) -> list:
    """
    Calculates the investment allocation based on suggested funds and total amount.
    Assumes 'weightage' is present in suggested_funds.
    """
    mix = []
    if not suggested_funds:
        return mix

    total_weightage = sum(f['weightage'] for f in suggested_funds)
    if total_weightage == 0: # Avoid division by zero if no weights assigned
        return mix

    for fund in suggested_funds:
        percentage = fund['weightage'] / total_weightage * 100
        allocated_amount = (total_amount * percentage / 100)
        mix.append({
            'fund': fund['name'],
            'amount': int(round(allocated_amount, -2)), # Round to nearest 100 for practicality
            'percentage': percentage
        })
    return mix
