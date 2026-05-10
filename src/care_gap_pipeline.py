import pandas as pd
import os

# -----------------------------
# PROJECT PATH SETUP
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

members_path = os.path.join(BASE_DIR, "data", "members.csv")
claims_path = os.path.join(BASE_DIR, "data", "claims.csv")

output_gap_path = os.path.join(BASE_DIR, "outputs", "prioritized_outreach_list.csv")
output_summary_path = os.path.join(BASE_DIR, "outputs", "care_gap_summary.csv")

# -----------------------------
# LOAD DATASETS
# -----------------------------

members_df = pd.read_csv(members_path)
claims_df = pd.read_csv(claims_path)

# -----------------------------
# DATE CONVERSION
# -----------------------------

members_df["dob"] = pd.to_datetime(members_df["dob"])
claims_df["service_date"] = pd.to_datetime(claims_df["service_date"])

today = pd.Timestamp.today()

# -----------------------------
# CALCULATE MEMBER AGE
# -----------------------------

members_df["age"] = (today - members_df["dob"]).dt.days // 365

# -----------------------------
# BREAST CANCER SCREENING GAP
# Female, age 50-74, no mammogram in last 2 years
# -----------------------------

female_members = members_df[
    (members_df["gender"] == "Female") &
    (members_df["age"].between(50, 74))
]

mammogram_claims = claims_df[
    claims_df["cpt_code"].isin(["77067", "77066"])
]

recent_mammograms = mammogram_claims[
    mammogram_claims["service_date"] >= today - pd.DateOffset(years=2)
]

members_with_mammo = recent_mammograms["member_id"].unique()

breast_gap = female_members[
    ~female_members["member_id"].isin(members_with_mammo)
].copy()

breast_gap["gap_type"] = "Breast Cancer Screening"

# -----------------------------
# COLORECTAL SCREENING GAP
# Age 45-75, no colorectal screening in last 5 years
# -----------------------------

eligible_colorectal = members_df[
    members_df["age"].between(45, 75)
]

colorectal_claims = claims_df[
    claims_df["cpt_code"].isin(["45378", "82274"])
]

recent_colorectal = colorectal_claims[
    colorectal_claims["service_date"] >= today - pd.DateOffset(years=5)
]

members_with_colorectal = recent_colorectal["member_id"].unique()

colorectal_gap = eligible_colorectal[
    ~eligible_colorectal["member_id"].isin(members_with_colorectal)
].copy()

colorectal_gap["gap_type"] = "Colorectal Screening"

# -----------------------------
# ANNUAL WELLNESS VISIT GAP
# Age 65+, no wellness visit in current year
# -----------------------------

eligible_wellness = members_df[
    members_df["age"] >= 65
]

wellness_claims = claims_df[
    claims_df["cpt_code"].isin(["G0438", "G0439"])
]

current_year = today.year

recent_wellness = wellness_claims[
    wellness_claims["service_date"].dt.year == current_year
]

members_with_wellness = recent_wellness["member_id"].unique()

wellness_gap = eligible_wellness[
    ~eligible_wellness["member_id"].isin(members_with_wellness)
].copy()

wellness_gap["gap_type"] = "Annual Wellness Visit"

# -----------------------------
# COMBINE ALL CARE GAPS
# -----------------------------

all_gaps = pd.concat(
    [breast_gap, colorectal_gap, wellness_gap],
    ignore_index=True
)

# -----------------------------
# PRIORITIZE OUTREACH LIST
# Higher risk members come first
# -----------------------------

all_gaps = all_gaps.sort_values(
    by="risk_score",
    ascending=False
)

# -----------------------------
# SAVE OUTPUT FILES
# -----------------------------

all_gaps.to_csv(output_gap_path, index=False)

gap_summary = (
    all_gaps["gap_type"]
    .value_counts()
    .reset_index()
)

gap_summary.columns = ["gap_type", "member_count"]

gap_summary.to_csv(output_summary_path, index=False)

# -----------------------------
# PRINT RESULTS
# -----------------------------

print("\nCare Gap Pipeline Completed Successfully!")

print("\nOutput files created:")
print("1. outputs/prioritized_outreach_list.csv")
print("2. outputs/care_gap_summary.csv")

print("\nTop 10 High Priority Members:")

print(
    all_gaps[
        [
            "member_id",
            "first_name",
            "last_name",
            "age",
            "gender",
            "plan_type",
            "gap_type",
            "risk_score",
            "county"
        ]
    ].head(10)
)