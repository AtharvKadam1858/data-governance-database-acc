-- Critical and high governance issues
SELECT
    c.table_name,
    c.department,
    g.issue_type,
    g.severity,
    g.issue_status,
    g.reported_date,
    g.assigned_to
FROM governance_issues g
JOIN data_catalog c ON g.table_id = c.table_id
WHERE g.severity IN ('High', 'Critical')
  AND g.issue_status != 'Resolved'
ORDER BY
    CASE g.severity
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
    END,
    g.reported_date DESC;

-- Issue summary by department
SELECT
    c.department,
    COUNT(*) AS total_issues,
    SUM(CASE WHEN g.severity = 'Critical' THEN 1 ELSE 0 END) AS critical_issues,
    SUM(CASE WHEN g.issue_status = 'Open' THEN 1 ELSE 0 END) AS open_issues
FROM governance_issues g
JOIN data_catalog c ON g.table_id = c.table_id
GROUP BY c.department
ORDER BY critical_issues DESC, open_issues DESC;

-- Data classification summary
SELECT
    data_classification,
    COUNT(*) AS total_tables,
    SUM(record_count) AS total_records
FROM data_catalog
GROUP BY data_classification
ORDER BY total_records DESC;