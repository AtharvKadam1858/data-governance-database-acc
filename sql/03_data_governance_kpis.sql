SELECT
    COUNT(DISTINCT c.table_id) AS total_tables,
    SUM(c.record_count) AS total_records_monitored,
    ROUND(AVG(q.data_quality_score), 2) AS average_data_quality_score,
    SUM(q.missing_records) AS total_missing_records,
    SUM(q.duplicate_records) AS total_duplicate_records,
    SUM(q.invalid_records) AS total_invalid_records
FROM data_catalog c
JOIN data_quality_checks q ON c.table_id = q.table_id;

SELECT
    c.department,
    COUNT(DISTINCT c.table_id) AS total_tables,
    ROUND(AVG(q.data_quality_score), 2) AS governance_score,
    COUNT(DISTINCT c.data_owner) AS data_owners,
    COUNT(DISTINCT c.data_steward) AS data_stewards
FROM data_catalog c
JOIN data_quality_checks q ON c.table_id = q.table_id
GROUP BY c.department
ORDER BY governance_score ASC;