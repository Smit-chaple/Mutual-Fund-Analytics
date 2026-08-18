import os
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import resend
from dotenv import load_dotenv


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "SQL" / "bluestoke_mf.db"
REPORT_PATH = PROJECT_ROOT / "REPORTS" / "weekly_report.html"
RECIPIENTS_PATH = PROJECT_ROOT / "CONFIG" / "recipients.csv"


# ============================================================
# LOAD DATA
# ============================================================

con = sqlite3.connect(DB_PATH)

fund = pd.read_sql("""
    SELECT *
    FROM dim_fund
    WHERE scheme_name IS NOT NULL
""", con)

sip = pd.read_sql("""
    SELECT *
    FROM fact_sip
    ORDER BY month
""", con)

transactions = pd.read_sql("""
    SELECT transaction_type, amount_inr
    FROM fact_transactions
""", con)

nav = pd.read_sql("""
    SELECT amfi_code, date, nav
    FROM fact_nav
""", con)

con.close()


# ============================================================
# BASIC KPIs
# ============================================================

total_funds = len(fund)

total_transactions = len(transactions)

generated_time = datetime.now().strftime("%d-%m-%Y %H:%M")


# ============================================================
# LATEST AVAILABLE SIP DATA
# ============================================================

latest_sip = sip.iloc[-1]

latest_sip_month = latest_sip["month"]

sip_inflow = latest_sip["sip_inflow_crore"]

active_sip_accounts = latest_sip["active_sip_accounts_crore"]

new_sip_accounts = latest_sip["new_sip_accounts_lakh"]

sip_aum = latest_sip["sip_aum_lakh_crore"]


# ============================================================
# LIVE NAV DATA
# ============================================================

nav["date"] = pd.to_datetime(nav["date"])

latest_nav_date = nav["date"].max()

latest_nav = nav[
    nav["date"] == latest_nav_date
].copy()


# ============================================================
# SELECTED LIVE FUNDS
# ============================================================

live_funds = {
    119551: "SBI Bluechip Fund",
    120503: "ICICI Prudential Bluechip Fund",
    118632: "Nippon India Large Cap Fund",
    119092: "Axis Bluechip Fund",
    120841: "Kotak Bluechip Fund",
    125497: "HDFC Top 100 Fund"
}


latest_nav["fund_name"] = latest_nav["amfi_code"].map(
    live_funds
)

latest_nav = latest_nav[
    latest_nav["fund_name"].notna()
].copy()


# ============================================================
# LIVE NAV SUMMARY
# ============================================================

live_nav_rows = ""

for _, row in latest_nav.iterrows():

    live_nav_rows += f"""
    <tr>
        <td style="padding:8px 0;">
            {row["fund_name"]}
        </td>

        <td style="padding:8px 0;text-align:right;">
            ₹{row["nav"]:,.2f}
        </td>
    </tr>
    """


# ============================================================
# INTERACTIVE CHART — SIP INFLOW
# ============================================================

fig_sip = px.line(
    sip,
    x="month",
    y="sip_inflow_crore",
    markers=True,
    title="Monthly SIP Inflow"
)

fig_sip.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(
        l=70,
        r=40,
        t=90,
        b=80
    ),
    xaxis_title="Month",
    yaxis_title="SIP Inflow (₹ Cr)",
    hovermode="x unified"
)


# ============================================================
# INTERACTIVE CHART — TRANSACTION DISTRIBUTION
# ============================================================

transaction_count = (
    transactions
    .groupby("transaction_type")
    .size()
    .reset_index(name="count")
)

fig_transaction = px.pie(
    transaction_count,
    names="transaction_type",
    values="count",
    hole=0.45,
    title="Transaction Distribution"
)

fig_transaction.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(
        l=40,
        r=40,
        t=90,
        b=40
    )
)


# ============================================================
# INTERACTIVE CHART — TRANSACTION AMOUNT
# ============================================================

transaction_amount = (
    transactions
    .groupby("transaction_type")["amount_inr"]
    .sum()
    .reset_index()
)

fig_amount = px.bar(
    transaction_amount,
    x="transaction_type",
    y="amount_inr",
    text_auto=".2s",
    title="Transaction Amount by Type"
)

fig_amount.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(
        l=90,
        r=40,
        t=90,
        b=90
    ),
    xaxis_title="Transaction Type",
    yaxis_title="Amount (₹)"
)


# ============================================================
# CONVERT CHARTS TO HTML
# ============================================================

sip_chart = fig_sip.to_html(
    full_html=False,
    include_plotlyjs="cdn",
    config={"responsive": True}
)

transaction_chart = fig_transaction.to_html(
    full_html=False,
    include_plotlyjs=False,
    config={"responsive": True}
)

amount_chart = fig_amount.to_html(
    full_html=False,
    include_plotlyjs=False,
    config={"responsive": True}
)


# ============================================================
# INTERACTIVE HTML REPORT
# ============================================================

html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Mutual Fund Analytics Report</title>

<style>

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f9;
    color: #1f2937;
}}

.header {{
    background: #111827;
    color: white;
    padding: 35px 50px;
}}

.header h1 {{
    margin: 0;
    font-size: 34px;
}}

.header p {{
    color: #d1d5db;
}}

.container {{
    max-width: 1500px;
    margin: auto;
    padding: 35px 45px;
}}

.kpis {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}}

.card {{
    background: white;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}}

.card-title {{
    color: #6b7280;
    font-size: 14px;
    margin-bottom: 8px;
}}

.card-value {{
    font-size: 30px;
    font-weight: bold;
}}

.section {{
    background: white;
    padding: 25px;
    margin-bottom: 25px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}}

.section h2 {{
    margin-top: 0;
}}

.chart-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
}}

.snapshot-table {{
    width: 100%;
    border-collapse: collapse;
}}

.snapshot-table td {{
    padding: 14px;
    border-bottom: 1px solid #e5e7eb;
}}

.snapshot-table td:first-child {{
    font-weight: bold;
    width: 40%;
}}

.footer {{
    text-align: center;
    color: #6b7280;
    padding: 35px;
}}

@media(max-width: 1000px) {{

    .kpis {{
        grid-template-columns: 1fr 1fr;
    }}

    .chart-grid {{
        grid-template-columns: 1fr;
    }}

}}

@media(max-width: 600px) {{

    .container {{
        padding: 20px;
    }}

    .kpis {{
        grid-template-columns: 1fr;
    }}

    .header {{
        padding: 25px;
    }}

    .header h1 {{
        font-size: 26px;
    }}

}}

</style>

</head>

<body>

<div class="header">

<h1>📊 Mutual Fund Analytics</h1>

<p>Interactive Weekly Performance Report</p>

<p>Generated: {generated_time}</p>

</div>


<div class="container">


<div class="kpis">

<div class="card">
<div class="card-title">Total Funds</div>
<div class="card-value">{total_funds}</div>
</div>

<div class="card">
<div class="card-title">Latest SIP Inflow</div>
<div class="card-value">₹{sip_inflow:,.0f} Cr</div>
</div>

<div class="card">
<div class="card-title">SIP AUM</div>
<div class="card-value">₹{sip_aum:,.2f} Lakh Cr</div>
</div>

<div class="card">
<div class="card-title">Total Transactions</div>
<div class="card-value">{total_transactions:,}</div>
</div>

</div>


<div class="section">

<h2>📈 SIP Inflow Trend</h2>

{sip_chart}

</div>


<div class="chart-grid">

<div class="section">

<h2>🥧 Transaction Distribution</h2>

{transaction_chart}

</div>


<div class="section">

<h2>💰 Transaction Amount</h2>

{amount_chart}

</div>

</div>


<div class="section">

<h2>📋 Latest SIP Snapshot</h2>

<table class="snapshot-table">

<tr>
<td>Month</td>
<td>{latest_sip_month}</td>
</tr>

<tr>
<td>SIP Inflow</td>
<td>₹{sip_inflow:,.2f} Cr</td>
</tr>

<tr>
<td>Active SIP Accounts</td>
<td>{active_sip_accounts:.2f} Cr</td>
</tr>

<tr>
<td>New SIP Accounts</td>
<td>{new_sip_accounts:.2f} Lakh</td>
</tr>

<tr>
<td>SIP AUM</td>
<td>₹{sip_aum:,.2f} Lakh Cr</td>
</tr>

</table>

</div>


</div>


<div class="footer">

<b>Mutual Fund Analytics Project</b>

<br>

ETL → SQLite → Analytics → Dashboard → Automated Reporting

</div>

</body>

</html>
"""


# ============================================================
# SAVE INTERACTIVE REPORT
# ============================================================

REPORT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

REPORT_PATH.write_text(
    html,
    encoding="utf-8"
)

print("Interactive HTML report generated successfully.")
print(f"Report: {REPORT_PATH}")


# ============================================================
# LOAD RESEND API KEY
# ============================================================

load_dotenv()

api_key = os.getenv("RESEND_API_KEY")

if not api_key:

    raise RuntimeError(
        "RESEND_API_KEY not found in .env"
    )

resend.api_key = api_key


# ============================================================
# LOAD RECIPIENTS
# ============================================================

if not RECIPIENTS_PATH.exists():

    raise FileNotFoundError(
        f"Recipients file not found: {RECIPIENTS_PATH}"
    )


recipients_df = pd.read_csv(
    RECIPIENTS_PATH
)

recipient_emails = (
    recipients_df["email"]
    .dropna()
    .astype(str)
    .str.strip()
    .tolist()
)

if not recipient_emails:

    raise ValueError(
        "No email recipients found in recipients.csv"
    )


# ============================================================
# EMAIL SUMMARY
# ============================================================

email_html = f"""
<!DOCTYPE html>

<html>

<body style="
    margin:0;
    padding:20px;
    background:#f4f6f9;
    font-family:Arial,sans-serif;
">

<div style="
    max-width:650px;
    margin:auto;
    background:white;
    padding:30px;
    border-radius:14px;
">

<h2 style="
    margin:0;
    color:#111827;
">

📊 Mutual Fund Analytics

</h2>

<p style="
    margin-top:6px;
    color:#6b7280;
">

Daily Market & Portfolio Snapshot

</p>

<p style="
    color:#6b7280;
    font-size:13px;
">

Generated: {generated_time}

</p>


<hr>


<h3>🔴 Live NAV Snapshot</h3>

<p style="
    color:#6b7280;
    font-size:13px;
">

Latest available live NAV date:
<b>{latest_nav_date.strftime("%d-%m-%Y")}</b>

</p>


<table style="
    width:100%;
    border-collapse:collapse;
">

<tr>

<td style="
    padding:8px 0;
    border-bottom:1px solid #eeeeee;
">

<b>Fund</b>

</td>

<td style="
    padding:8px 0;
    border-bottom:1px solid #eeeeee;
    text-align:right;
">

<b>Latest NAV</b>

</td>

</tr>

{live_nav_rows}

</table>


<hr>


<h3>🟡 Latest Available SIP Data</h3>

<p style="
    color:#6b7280;
    font-size:13px;
">

SIP data is monthly, so this section shows the
latest available month: <b>{latest_sip_month}</b>

</p>


<table style="
    width:100%;
    border-collapse:collapse;
">

<tr>

<td style="padding:8px 0;">
<b>SIP Inflow</b>
</td>

<td style="
    padding:8px 0;
    text-align:right;
">

₹{sip_inflow:,.2f} Cr

</td>

</tr>


<tr>

<td style="padding:8px 0;">
<b>Active SIP Accounts</b>
</td>

<td style="
    padding:8px 0;
    text-align:right;
">

{active_sip_accounts:.2f} Cr

</td>

</tr>


<tr>

<td style="padding:8px 0;">
<b>New SIP Accounts</b>
</td>

<td style="
    padding:8px 0;
    text-align:right;
">

{new_sip_accounts:.2f} Lakh

</td>

</tr>


<tr>

<td style="padding:8px 0;">
<b>SIP AUM</b>
</td>

<td style="
    padding:8px 0;
    text-align:right;
">

₹{sip_aum:,.2f} Lakh Cr

</td>

</tr>

</table>


<hr>






<hr>


<p style="
    color:#6b7280;
    font-size:13px;
    line-height:1.6;
">



<p style="
    margin-bottom:0;
    color:#6b7280;
    font-size:13px;
">

<b>Mutual Fund Analytics Project</b>

<br>

ETL → SQLite → Analytics → Dashboard → Reporting

</p>

</div>

</body>

</html>
"""


# ============================================================
# SEND EMAIL
# ============================================================

resend.Emails.send({

    "from": "onboarding@resend.dev",

    "to": recipient_emails,

    "subject": (
        f"Mutual Fund Analytics — "
        f"{latest_nav_date.strftime('%d-%m-%Y')}"
    ),

    "html": email_html

})


# ============================================================
# FINAL MESSAGE
# ============================================================

print()
print("==========================================")
print("WEEKLY REPORT COMPLETED")
print("==========================================")

print("Interactive report:")
print(REPORT_PATH)

print()

print("Summary email sent successfully.")

print("Latest NAV date:")
print(latest_nav_date.strftime("%Y-%m-%d"))

print()

print("SIP data month:")
print(latest_sip_month)

print()

print("Recipients:")

for email in recipient_emails:
    print(f" - {email}")

print("==========================================")