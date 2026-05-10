import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

members_path = os.path.join(BASE_DIR, "data", "members.csv")
claims_path = os.path.join(BASE_DIR, "data", "claims.csv")
gaps_path = os.path.join(BASE_DIR, "outputs", "prioritized_outreach_list.csv")

kpi_output_path = os.path.join(BASE_DIR, "outputs", "dashboard_kpis.csv")
gap_by_plan_path = os.path.join(BASE_DIR, "outputs", "gap_by_plan.csv")
gap_by_county_path = os.path.join(BASE_DIR, "outputs", "gap_by_county.csv")
gap_by_measure_path = os.path.join(BASE_DIR, "outputs", "gap_by_measure.csv")

members_df = pd.read_csv(members_path)
claims_df = pd.read_csv(claims_path)
gaps_df = pd.read_csv(gaps_path)

total_members = members_df["member_id"].nunique()
total_claims = claims_df["claim_id"].nunique()
total_open_gaps = len(gaps_df)
avg_risk_score = round(gaps_df["risk_score"].mean(), 2)

gap_rate = round((total_open_gaps / total_members) * 100, 2)

kpi_df = pd.DataFrame({
    "metric": [
        "Total Members",
        "Total Claims",
        "Total Open Care Gaps",
        "Average Risk Score",
        "Care Gap Rate (%)"
    ],
    "value": [
        total_members,
        total_claims,
        total_open_gaps,
        avg_risk_score,
        gap_rate
    ]
})

gap_by_plan = (
    gaps_df.groupby("plan_type")
    .size()
    .reset_index(name="open_gaps")
)

gap_by_county = (
    gaps_df.groupby("county")
    .size()
    .reset_index(name="open_gaps")
)

gap_by_measure = (
    gaps_df.groupby("gap_type")
    .size()
    .reset_index(name="open_gaps")
)

kpi_df.to_csv(kpi_output_path, index=False)
gap_by_plan.to_csv(gap_by_plan_path, index=False)
gap_by_county.to_csv(gap_by_county_path, index=False)
gap_by_measure.to_csv(gap_by_measure_path, index=False)

print("Dashboard KPI files created successfully!")
print("Files created in outputs folder:")
print("1. dashboard_kpis.csv")
print("2. gap_by_plan.csv")
print("3. gap_by_county.csv")
print("4. gap_by_measure.csv")