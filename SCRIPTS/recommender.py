import pandas as pd

# Load data
fund_scorecard = pd.read_csv("data/processed/fund_scorecard.csv")

# Ask user for risk appetite
risk_appetite = input("Enter risk appetite (Low / Moderate / High): ").strip().title()

# Validate input
if risk_appetite not in ["Low", "Moderate", "High"]:
    print("Invalid risk appetite. Please enter Low, Moderate, or High.")

else:
    # Filter funds by risk grade
    recommendations = (
        fund_scorecard[
            fund_scorecard["risk_grade"] == risk_appetite].sort_values("sharpe_ratio", ascending=False).head(3)
    )

    print("\nTop 3 Recommended Funds")
    print("=" * 70)

    print(
        recommendations[
            [
                "scheme_name",
                "risk_grade",
                "sharpe_ratio",
                "CAGR_3Y",
                "fund_score"
            ]
        ].to_string(index=False)
    )