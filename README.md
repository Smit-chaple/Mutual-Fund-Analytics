# Mutual Fund Analytics — Bluestock Fintech Capstone

## Overview
End-to-end mutual fund analytics project covering ETL, SQLite, EDA, performance/risk analytics, advanced analytics, Streamlit dashboard, live NAV updates, weekly reporting and scheduled automation.

## Architecture
Extract → Transform → Load → Analyse → Visualise → Report → Automated Email

## Main Components
- `DATA/RAW/` — raw and live data
- `DATA/PROCESSED/` — processed data
- `SQL/bluestoke_mf.db` — SQLite database
- `SCRIPTS/data_ingestion.py` — extraction
- `SCRIPTS/data_cleaning.py` — transformation
- `SCRIPTS/load_database.py` — database loading
- `SCRIPTS/run_pipeline.py` — master ETL runner
- `SCRIPTS/weekly_email_report.py` — weekly report/email
- `APP/app.py` — Streamlit dashboard
- `Performance_Analytics.ipynb` — performance analytics
- `Advanced_Analytics.ipynb` — advanced analytics
- `REPORTS/` — generated reports

## Dashboard
1. Industry Overview
2. Fund Performance
3. Investor Analytics
4. SIP & Market Trends

## Database Tables
`dim_fund`, `fact_nav`, `fact_aum`, `fact_performance`, `fact_transactions`, `fact_sip`

## Run Dashboard
```powershell
streamlit run APP/app.py
```

## Run ETL
```powershell
python SCRIPTS/run_pipeline.py
```

## Security
Do not commit API keys, `.env` files or credentials. Keep private configuration outside GitHub.

## Final Deliverables
ETL pipeline, SQLite database, EDA, performance analytics, advanced analytics, dashboard, automated reporting, final PDF report and presentation.
