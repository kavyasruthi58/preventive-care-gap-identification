-- Breast Cancer Screening Gap
SELECT
    m.member_id,
    m.first_name,
    m.last_name,
    m.gender,
    m.plan_type,
    m.risk_score,
    m.county,
    'Breast Cancer Screening' AS gap_type
FROM members m
LEFT JOIN claims c
    ON m.member_id = c.member_id
    AND c.cpt_code IN ('77067', '77066')
    AND c.service_date >= CURRENT_DATE - INTERVAL '2 years'
WHERE m.gender = 'Female'
  AND EXTRACT(YEAR FROM AGE(CURRENT_DATE, m.dob)) BETWEEN 50 AND 74
  AND c.member_id IS NULL;


-- Colorectal Screening Gap
SELECT
    m.member_id,
    m.first_name,
    m.last_name,
    m.gender,
    m.plan_type,
    m.risk_score,
    m.county,
    'Colorectal Screening' AS gap_type
FROM members m
LEFT JOIN claims c
    ON m.member_id = c.member_id
    AND c.cpt_code IN ('45378', '82274')
    AND c.service_date >= CURRENT_DATE - INTERVAL '5 years'
WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, m.dob)) BETWEEN 45 AND 75
  AND c.member_id IS NULL;


-- Annual Wellness Visit Gap
SELECT
    m.member_id,
    m.first_name,
    m.last_name,
    m.gender,
    m.plan_type,
    m.risk_score,
    m.county,
    'Annual Wellness Visit' AS gap_type
FROM members m
LEFT JOIN claims c
    ON m.member_id = c.member_id
    AND c.cpt_code IN ('G0438', 'G0439')
    AND EXTRACT(YEAR FROM c.service_date) = EXTRACT(YEAR FROM CURRENT_DATE)
WHERE EXTRACT(YEAR FROM AGE(CURRENT_DATE, m.dob)) >= 65
  AND c.member_id IS NULL;