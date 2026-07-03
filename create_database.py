import os
import sqlite3
import pandas as pd

os.makedirs("database", exist_ok=True)

DB_PATH = "database/data_governance.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("DROP TABLE IF EXISTS governance_issues;")
cursor.execute("DROP TABLE IF EXISTS sensitive_data_fields;")
cursor.execute("DROP TABLE IF EXISTS data_quality_checks;")
cursor.execute("DROP TABLE IF EXISTS data_catalog;")

cursor.execute("""
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
""")

cursor.execute("""
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
""")

cursor.execute("""
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
""")

cursor.execute("""
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
""")

csv_files = {
    "data_catalog": "data/data_catalog.csv",
    "data_quality_checks": "data/data_quality_checks.csv",
    "sensitive_data_fields": "data/sensitive_data_fields.csv",
    "governance_issues": "data/governance_issues.csv"
}

for table, file_path in csv_files.items():
    df = pd.read_csv(file_path)
    df.to_sql(table, conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Data Governance SQLite database created successfully.")