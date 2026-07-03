import sqlite3
import pandas as pd

DATABASE_PATH = "database/data_governance.db"

query = """
SELECT
    table_name,
    department,
    source_system,
    data_owner,
    record_count,
    data_classification,
    contains_sensitive_data
FROM data_catalog
LIMIT 10;
"""

try:
    conn = sqlite3.connect(DATABASE_PATH)
    df = pd.read_sql_query(query, conn)

    print(df)
    print(f"\nTotal Rows Returned: {len(df)}")

    conn.close()

except Exception as e:
    print("Error:", e)