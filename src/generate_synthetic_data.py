import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

fake = Faker()

random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

NUM_MEMBERS = 1000
NUM_CLAIMS = 6000

cpt_codes = {
    "mammogram": ["77067", "77066"],
    "colorectal": ["45378", "82274"],
    "wellness": ["G0438", "G0439"],
    "office_visit": ["99213", "99214"]
}

icd10_codes = [
    "Z12.31",
    "Z12.11",
    "Z00.00",
    "I10",
    "E11.9"
]

members = []

for i in range(1, NUM_MEMBERS + 1):

    gender = random.choice(["Female", "Male"])

    age = random.randint(30, 85)

    dob = datetime.today() - timedelta(days=age * 365)

    members.append({
        "member_id": i,
        "first_name": fake.first_name_female() if gender == "Female" else fake.first_name_male(),
        "last_name": fake.last_name(),
        "dob": dob.date(),
        "gender": gender,
        "plan_type": random.choice([
            "Medicare Advantage",
            "Employer Sponsored"
        ]),
        "risk_score": round(random.uniform(0.5, 3.5), 2),
        "county": random.choice([
            "Richmond",
            "Henrico",
            "Fairfax",
            "Arlington"
        ])
    })

members_df = pd.DataFrame(members)

eligibility = []

for _, row in members_df.iterrows():

    eligibility.append({
        "member_id": row["member_id"],
        "coverage_start": "2022-01-01",
        "coverage_end": "2025-12-31",
        "plan_type": row["plan_type"]
    })

eligibility_df = pd.DataFrame(eligibility)

claims = []

for claim_id in range(1, NUM_CLAIMS + 1):

    member = members_df.sample(1).iloc[0]

    service_type = random.choices(
        ["mammogram", "colorectal", "wellness", "office_visit"],
        weights=[0.15, 0.15, 0.20, 0.50]
    )[0]

    claims.append({
        "claim_id": claim_id,
        "member_id": member["member_id"],
        "service_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),
        "cpt_code": random.choice(
            cpt_codes[service_type]
        ),
        "icd10_code": random.choice(
            icd10_codes
        ),
        "provider_id": random.randint(1, 50),
        "paid_amount": round(
            random.uniform(75, 1500), 2
        )
    })

claims_df = pd.DataFrame(claims)

outreach_df = pd.DataFrame(columns=[
    "outreach_id",
    "member_id",
    "gap_type",
    "outreach_date",
    "channel",
    "status"
])

members_df.to_csv(
    "data/members.csv",
    index=False
)

eligibility_df.to_csv(
    "data/eligibility.csv",
    index=False
)

claims_df.to_csv(
    "data/claims.csv",
    index=False
)

outreach_df.to_csv(
    "data/outreach.csv",
    index=False
)

print("Healthcare synthetic datasets created successfully!")