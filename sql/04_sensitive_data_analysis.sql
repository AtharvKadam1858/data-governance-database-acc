SELECT
    c.table_name,
    c.department,
    s.field_name,
    s.sensitivity_type,
    s.encryption_status,
    s.access_level,
    s.compliance_status
FROM sensitive_data_fields s
JOIN data_catalog c ON s.table_id = c.table_id
ORDER BY s.compliance_status, s.encryption_status;

SELECT
    s.sensitivity_type,
    COUNT(*) AS sensitive_field_count,
    SUM(CASE WHEN s.encryption_status = 'Not Encrypted' THEN 1 ELSE 0 END) AS unencrypted_fields,
    SUM(CASE WHEN s.compliance_status = 'Non-Compliant' THEN 1 ELSE 0 END) AS non_compliant_fields
FROM sensitive_data_fields s
GROUP BY s.sensitivity_type
ORDER BY sensitive_field_count DESC;