# Enterprise Data Governance & Database Analytics Command Center

An advanced data governance dashboard built using SQL, SQLite, Python, Pandas, Plotly, and Streamlit.

## Project Overview

This project monitors database health, data quality, sensitive data fields, governance issues, data classification, and data ownership through an interactive command center dashboard.

## Key Features

- Data catalog monitoring
- Data quality scorecard
- Missing, duplicate, and invalid record analysis
- Department-wise governance score
- Sensitive data classification
- Encryption status monitoring
- Compliance issue tracking
- Data owner and data steward mapping
- Governance issue severity analysis
- Downloadable data quality report

## Technologies Used

- SQL
- SQLite
- Python
- Pandas
- Plotly
- Streamlit
- Faker

## How to Run Locally

```bash
pip install -r requirements.txt
python generate_dataset.py
python create_database.py
streamlit run dashboard/app.py