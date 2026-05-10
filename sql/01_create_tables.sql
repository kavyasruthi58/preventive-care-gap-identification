CREATE TABLE members (
    member_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE,
    gender VARCHAR(20),
    plan_type VARCHAR(50),
    risk_score DECIMAL(4,2),
    county VARCHAR(50)
);

CREATE TABLE eligibility (
    member_id INTEGER,
    coverage_start DATE,
    coverage_end DATE,
    plan_type VARCHAR(50)
);

CREATE TABLE claims (
    claim_id INTEGER PRIMARY KEY,
    member_id INTEGER,
    service_date DATE,
    cpt_code VARCHAR(20),
    icd10_code VARCHAR(20),
    provider_id INTEGER,
    paid_amount DECIMAL(10,2)
);

CREATE TABLE outreach (
    outreach_id INTEGER,
    member_id INTEGER,
    gap_type VARCHAR(100),
    outreach_date DATE,
    channel VARCHAR(50),
    status VARCHAR(50)
);