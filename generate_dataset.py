import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker("en_IN")
random.seed(42)

os.makedirs("data", exist_ok=True)

departments = [
    "Sales",
    "Marketing",
    "Finance",
    "HR",
    "Operations",
    "IT",
    "Data Analytics"
]

systems = [
    "CRM System",
    "ERP System",
    "HRMS System",
    "Finance System",
    "Marketing Platform",
    "Inventory System"
]

data_owners = {
    "Sales": "Sales Head",
    "Marketing": "Marketing Head",
    "Finance": "Finance Manager",
    "HR": "HR Manager",
    "Operations": "Operations Manager",
    "IT": "IT Manager",
    "Data Analytics": "Analytics Manager"
}

data_stewards = {
    "Sales": "Sales Data Steward",
    "Marketing": "Marketing Data Steward",
    "Finance": "Finance Data Steward",
    "HR": "HR Data Steward",
    "Operations": "Operations Data Steward",
    "IT": "IT Data Steward",
    "Data Analytics": "Analytics Data Steward"
}

# 1. Data catalog
catalog = []

for table_id in range(1, 31):
    department = random.choice(departments)
    source_system = random.choice(systems)
    table_name = f"{department.lower().replace(' ', '_')}_table_{table_id}"

    catalog.append({
        "table_id": table_id,
        "table_name": table_name,
        "department": department,
        "source_system": source_system,
        "data_owner": data_owners[department],
        "data_steward": data_stewards[department],
        "record_count": random.randint(5000, 250000),
        "last_refresh_date": fake.date_between(start_date="-30d", end_date="today"),
        "data_classification": random.choice(
            ["Public", "Internal", "Confidential", "Restricted"]
        ),
        "contains_sensitive_data": random.choice(["Yes", "No"])
    })

# 2. Data quality checks
quality_checks = []

for check_id in range(1, 181):
    table = random.choice(catalog)
    total_records = table["record_count"]

    missing_records = random.randint(0, int(total_records * 0.12))
    duplicate_records = random.randint(0, int(total_records * 0.06))
    invalid_records = random.randint(0, int(total_records * 0.05))

    quality_score = round(
        max(
            0,
            100
            - ((missing_records / total_records) * 100)
            - ((duplicate_records / total_records) * 100)
            - ((invalid_records / total_records) * 100)
        ),
        2
    )

    quality_status = (
        "Excellent" if quality_score >= 95
        else "Good" if quality_score >= 85
        else "Needs Attention" if quality_score >= 70
        else "Critical"
    )

    quality_checks.append({
        "check_id": check_id,
        "table_id": table["table_id"],
        "check_date": fake.date_between(start_date="-180d", end_date="today"),
        "total_records_checked": total_records,
        "missing_records": missing_records,
        "duplicate_records": duplicate_records,
        "invalid_records": invalid_records,
        "data_quality_score": quality_score,
        "quality_status": quality_status
    })

# 3. Sensitive data fields
sensitive_fields = []

field_types = [
    ("Customer Name", "PII"),
    ("Email Address", "PII"),
    ("Phone Number", "PII"),
    ("PAN Number", "Financial"),
    ("Bank Account Number", "Financial"),
    ("Salary", "Confidential"),
    ("Employee ID", "Confidential"),
    ("Date of Birth", "PII")
]

for field_id in range(1, 121):
    table = random.choice(catalog)
    field_name, sensitivity_type = random.choice(field_types)

    sensitive_fields.append({
        "field_id": field_id,
        "table_id": table["table_id"],
        "field_name": field_name,
        "sensitivity_type": sensitivity_type,
        "encryption_status": random.choice(["Encrypted", "Not Encrypted"]),
        "access_level": random.choice(["Restricted", "Confidential", "Internal"]),
        "retention_policy_days": random.choice([365, 730, 1095, 1825, 2555]),
        "compliance_status": random.choice(["Compliant", "Review Required", "Non-Compliant"])
    })

# 4. Governance issues
governance_issues = []

issue_types = [
    "Missing Data",
    "Duplicate Data",
    "Invalid Data",
    "Sensitive Data Exposure",
    "Missing Data Owner",
    "Outdated Data",
    "Access Control Issue"
]

for issue_id in range(1, 101):
    table = random.choice(catalog)
    issue_type = random.choice(issue_types)

    governance_issues.append({
        "issue_id": issue_id,
        "table_id": table["table_id"],
        "issue_type": issue_type,
        "severity": random.choices(
            ["Low", "Medium", "High", "Critical"],
            weights=[30, 35, 25, 10]
        )[0],
        "issue_status": random.choices(
            ["Open", "In Progress", "Resolved"],
            weights=[35, 30, 35]
        )[0],
        "reported_date": fake.date_between(start_date="-120d", end_date="today"),
        "assigned_to": random.choice(list(data_stewards.values()))
    })

pd.DataFrame(catalog).to_csv("data/data_catalog.csv", index=False)
pd.DataFrame(quality_checks).to_csv("data/data_quality_checks.csv", index=False)
pd.DataFrame(sensitive_fields).to_csv("data/sensitive_data_fields.csv", index=False)
pd.DataFrame(governance_issues).to_csv("data/governance_issues.csv", index=False)

print("Data Governance and Database Analytics dataset generated successfully.")