SELECT
    c.table_name,
    c.department,
    q.check_date,
    q.total_records_checked,
    q.missing_records,
    q.duplicate_records,
    q.invalid_records,
    q.data_quality_score,
    q.quality_status
FROM data_quality_checks q
JOIN data_catalog c ON q.table_id = c.table_id
ORDER BY q.data_quality_score ASC;

SELECT
    c.department,
    ROUND(AVG(q.data_quality_score), 2) AS average_quality_score,
    SUM(q.missing_records) AS total_missing_records,
    SUM(q.duplicate_records) AS total_duplicate_records,
    SUM(q.invalid_records) AS total_invalid_records
FROM data_quality_checks q
JOIN data_catalog c ON q.table_id = c.table_id
GROUP BY c.department
ORDER BY average_quality_score ASC;