import pandas as pd
import numpy as np
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

gaps_path = os.path.join(BASE_DIR, "outputs", "prioritized_outreach_list.csv")

outreach_output_path = os.path.join(BASE_DIR, "outputs", "outreach_effectiveness.csv")
final_outreach_path = os.path.join(BASE_DIR, "outputs", "final_outreach_priority_list.csv")

gaps_df = pd.read_csv(gaps_path)

random.seed(42)
np.random.seed(42)

channels = ["Phone", "Email", "SMS", "Mail"]

gaps_df["recommended_channel"] = np.where(
    gaps_df["risk_score"] >= 2.8,
    "Phone",
    np.where(
        gaps_df["risk_score"] >= 2.0,
        "SMS",
        "Email"
    )
)

gaps_df["priority_level"] = np.where(
    gaps_df["risk_score"] >= 2.8,
    "High",
    np.where(
        gaps_df["risk_score"] >= 2.0,
        "Medium",
        "Low"
    )
)

gaps_df["outreach_status"] = np.random.choice(
    ["Completed", "Pending", "Unable to Reach"],
    size=len(gaps_df),
    p=[0.55, 0.30, 0.15]
)

gaps_df["gap_closed"] = np.where(
    gaps_df["outreach_status"] == "Completed",
    np.random.choice(["Yes", "No"], size=len(gaps_df), p=[0.65, 0.35]),
    "No"
)

outreach_summary = (
    gaps_df.groupby(["recommended_channel", "outreach_status", "gap_closed"])
    .size()
    .reset_index(name="member_count")
)

gaps_df.to_csv(final_outreach_path, index=False)
outreach_summary.to_csv(outreach_output_path, index=False)

print("Outreach optimization files created successfully!")
print("1. outputs/final_outreach_priority_list.csv")
print("2. outputs/outreach_effectiveness.csv")