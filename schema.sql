CREATE TABLE patents_priority (
    patent_id TEXT PRIMARY KEY,
    priority_claim_sequence INT,
    priority_claim_kind TEXT,
    foreign_application_id TEXT,
    filing_date DATE,
    foreign_country_filed TEXT
);

CREATE TABLE patents_orgs (
    patent_id TEXT PRIMARY KEY,
    gi_organization_id TEXT,
    fedagency_name TEXT,
    level_one TEXT,
    level_two TEXT,
    level_three TEXT
);