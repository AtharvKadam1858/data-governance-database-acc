CREATE TABLE data_catalog (
    table_id INTEGER PRIMARY KEY,
    table_name TEXT,
    department TEXT,
    source_system TEXT,
    data_owner TEXT,
    data_steward TEXT,
    record_count INTEGER,
    last_refresh_date DATE,
    data_classification TEXT,
    contains_sensitive_data TEXT
);

CREATE TABLE data_quality_checks (
    check_id INTEGER PRIMARY KEY,
    table_id INTEGER,
    check_date DATE,
    total_records_checked INTEGER,
    missing_records INTEGER,
    duplicate_records INTEGER,
    invalid_records INTEGER,
    data_quality_score REAL,
    quality_status TEXT,
    FOREIGN KEY (table_id) REFERENCES data_catalog(table_id)
);

CREATE TABLE sensitive_data_fields (
    field_id INTEGER PRIMARY KEY,
    table_id INTEGER,
    field_name TEXT,
    sensitivity_type TEXT,
    encryption_status TEXT,
    access_level TEXT,
    retention_policy_days INTEGER,
    compliance_status TEXT,
    FOREIGN KEY (table_id) REFERENCES data_catalog(table_id)
);

CREATE TABLE governance_issues (
    issue_id INTEGER PRIMARY KEY,
    table_id INTEGER,
    issue_type TEXT,
    severity TEXT,
    issue_status TEXT,
    reported_date DATE,
    assigned_to TEXT,
    FOREIGN KEY (table_id) REFERENCES data_catalog(table_id)
);