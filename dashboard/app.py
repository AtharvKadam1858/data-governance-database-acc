import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "data_governance.db"

st.set_page_config(
    page_title="Data Governance Command Center",
    page_icon="🛡️",
    layout="wide"
)


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    catalog = pd.read_sql_query("SELECT * FROM data_catalog;", conn)
    quality = pd.read_sql_query("""
        SELECT
            q.*,
            c.table_name,
            c.department,
            c.source_system,
            c.data_owner,
            c.data_steward,
            c.data_classification,
            c.contains_sensitive_data
        FROM data_quality_checks q
        JOIN data_catalog c ON q.table_id = c.table_id;
    """, conn)

    sensitive = pd.read_sql_query("""
        SELECT
            s.*,
            c.table_name,
            c.department
        FROM sensitive_data_fields s
        JOIN data_catalog c ON s.table_id = c.table_id;
    """, conn)

    issues = pd.read_sql_query("""
        SELECT
            g.*,
            c.table_name,
            c.department
        FROM governance_issues g
        JOIN data_catalog c ON g.table_id = c.table_id;
    """, conn)

    conn.close()
    return catalog, quality, sensitive, issues


catalog_df, quality_df, sensitive_df, issues_df = load_data()

st.title("🛡️ Enterprise Data Governance & Database Analytics Command Center")
st.caption("Advanced dashboard for data quality, metadata governance, sensitive data monitoring, and database health analysis.")

st.sidebar.header("🔎 Filters")

department_filter = st.sidebar.multiselect(
    "Select Department",
    sorted(catalog_df["department"].unique()),
    default=sorted(catalog_df["department"].unique())
)

classification_filter = st.sidebar.multiselect(
    "Select Data Classification",
    sorted(catalog_df["data_classification"].unique()),
    default=sorted(catalog_df["data_classification"].unique())
)

quality_status_filter = st.sidebar.multiselect(
    "Select Quality Status",
    sorted(quality_df["quality_status"].unique()),
    default=sorted(quality_df["quality_status"].unique())
)

catalog_filtered = catalog_df[
    (catalog_df["department"].isin(department_filter)) &
    (catalog_df["data_classification"].isin(classification_filter))
]

quality_filtered = quality_df[
    (quality_df["department"].isin(department_filter)) &
    (quality_df["data_classification"].isin(classification_filter)) &
    (quality_df["quality_status"].isin(quality_status_filter))
]

sensitive_filtered = sensitive_df[
    sensitive_df["department"].isin(department_filter)
]

issues_filtered = issues_df[
    issues_df["department"].isin(department_filter)
]

total_tables = catalog_filtered["table_id"].nunique()
total_records = catalog_filtered["record_count"].sum()
avg_quality_score = quality_filtered["data_quality_score"].mean()
missing_records = quality_filtered["missing_records"].sum()
duplicate_records = quality_filtered["duplicate_records"].sum()
critical_issues = issues_filtered[
    (issues_filtered["severity"] == "Critical") &
    (issues_filtered["issue_status"] != "Resolved")
].shape[0]

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Tables", f"{total_tables:,}")
col2.metric("Records Monitored", f"{total_records:,}")
col3.metric("Avg Quality Score", f"{avg_quality_score:.2f}%")
col4.metric("Missing Records", f"{missing_records:,}")
col5.metric("Critical Issues", f"{critical_issues:,}")

st.divider()

col6, col7 = st.columns(2)

dept_quality = quality_filtered.groupby("department", as_index=False)["data_quality_score"].mean()

fig1 = px.bar(
    dept_quality,
    x="department",
    y="data_quality_score",
    title="Department-wise Data Quality Score"
)
col6.plotly_chart(fig1, use_container_width=True)

quality_status = quality_filtered["quality_status"].value_counts().reset_index()
quality_status.columns = ["quality_status", "count"]

fig2 = px.pie(
    quality_status,
    names="quality_status",
    values="count",
    title="Data Quality Status Distribution"
)
col7.plotly_chart(fig2, use_container_width=True)

col8, col9 = st.columns(2)

classification_data = catalog_filtered["data_classification"].value_counts().reset_index()
classification_data.columns = ["data_classification", "table_count"]

fig3 = px.bar(
    classification_data,
    x="data_classification",
    y="table_count",
    title="Data Classification by Table Count"
)
col8.plotly_chart(fig3, use_container_width=True)

sensitive_summary = sensitive_filtered["sensitivity_type"].value_counts().reset_index()
sensitive_summary.columns = ["sensitivity_type", "field_count"]

fig4 = px.pie(
    sensitive_summary,
    names="sensitivity_type",
    values="field_count",
    title="Sensitive Data Type Distribution"
)
col9.plotly_chart(fig4, use_container_width=True)

st.divider()

col10, col11 = st.columns(2)

issue_summary = issues_filtered.groupby(["severity", "issue_status"]).size().reset_index(name="issue_count")

fig5 = px.bar(
    issue_summary,
    x="severity",
    y="issue_count",
    color="issue_status",
    barmode="group",
    title="Governance Issues by Severity and Status"
)
col10.plotly_chart(fig5, use_container_width=True)

unencrypted = sensitive_filtered.groupby("encryption_status").size().reset_index(name="field_count")

fig6 = px.pie(
    unencrypted,
    names="encryption_status",
    values="field_count",
    title="Encryption Status of Sensitive Fields"
)
col11.plotly_chart(fig6, use_container_width=True)

st.divider()

st.subheader("📌 Business Insights")

if not quality_filtered.empty:
    lowest_quality_dept = dept_quality.sort_values("data_quality_score").iloc[0]
    open_issues = issues_filtered[issues_filtered["issue_status"] == "Open"].shape[0]
    non_compliant = sensitive_filtered[sensitive_filtered["compliance_status"] == "Non-Compliant"].shape[0]

    st.warning(
        f"Lowest data quality department: {lowest_quality_dept['department']} "
        f"with {lowest_quality_dept['data_quality_score']:.2f}% average score."
    )
    st.info(f"Open governance issues currently identified: {open_issues}.")
    st.error(f"Non-compliant sensitive fields identified: {non_compliant}.")

st.subheader("🗂️ Data Catalog")
st.dataframe(catalog_filtered, use_container_width=True)

st.subheader("🧾 Data Quality Monitoring Details")
st.dataframe(
    quality_filtered.sort_values("data_quality_score"),
    use_container_width=True
)

st.subheader("🔐 Sensitive Data Fields")
st.dataframe(sensitive_filtered, use_container_width=True)

st.subheader("🚨 Governance Issues")
st.dataframe(issues_filtered, use_container_width=True)

st.download_button(
    label="⬇️ Download Data Quality Report",
    data=quality_filtered.to_csv(index=False),
    file_name="data_governance_quality_report.csv",
    mime="text/csv"
)