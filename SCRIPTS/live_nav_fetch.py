import requests 
import pandas as pd
url = "https://api.mfapi.in/mf/125497" # Storing the API URL
response = requests.get(url) # Sending request to the API
print(response.status_code) # Printing the status code

data = response.json() # Converting the response to JSON

nav_data = data['data'] # Extracting the NAV data from the JSON response

live_nav_data = pd.DataFrame(nav_data) # Converting into dataframe
print(live_nav_data.head())

live_nav_data.to_csv("DATA/RAW/hdft_top100_live_nav.csv", index=False) # Saving as a CSV file
print("Live NAV data saved successfully!")

schemes = {
    "sbi_bluechip": "119551",
    "icici_bluechip": "120503",
    "nippon_large_cap": "118632",
    "axis_bluechip": "119092",
    "kotak_bluechip": "120841"
}

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"

    response = requests.get(url)

    if response.status_code == 200:
        data =response.json()
        nav_data = data['data']
        live_nav_data = pd.DataFrame(nav_data)
        live_nav_data.to_csv(f"DATA/RAW/{name}_live_nav.csv", index=False)
        print(f"Live NAV data for {name} saved successfully!")
    else:
        print(f"Field to fetch data for {name}")

# Validate AMFI codes — confirm every code in fund_master exists in nav_history.
print("\n========== VALIDATE AMFI CODES ==========")

fund_master = pd.read_csv("DATA/RAW/01_fund_master.csv")
nav_his = pd.read_csv("DATA/RAW/02_nav_history.csv")

print(fund_master.columns)
print(nav_his.columns)

# In both tables contains the AMFI_code column.

fund_code = set(fund_master['amfi_code']) 
nav_code = set(nav_his['amfi_code'])

missing_codes = fund_code - nav_code

print(missing_codes) # There is no missing codes in the nav_history table.

print(f"fund_master codes: {len(fund_code)}")
print(f"nav_his codes: {len(nav_code)}")
print(f"missing_codes: {len(missing_codes)}")


# ============================================================
# UPDATE SQLITE WITH LIVE NAV DATA
# ============================================================

import sqlite3
from pathlib import Path

DB_PATH = Path("SQL/bluestoke_mf.db")

live_files = {
    "sbi_bluechip": "119551",
    "icici_bluechip": "120503",
    "nippon_large_cap": "118632",
    "axis_bluechip": "119092",
    "kotak_bluechip": "120841",
    "hdfc_top100": "125497"
}

con = sqlite3.connect(DB_PATH)

for fund_name, amfi_code in live_files.items():

    file_path = Path(
        f"DATA/RAW/{fund_name}_live_nav.csv"
    )

    if not file_path.exists():
        print(f"Live file not found: {file_path}")
        continue

    df = pd.read_csv(file_path)

    df["amfi_code"] = int(amfi_code)

    df = df[["amfi_code", "date", "nav"]]

    df["date"] = pd.to_datetime(
        df["date"],
        dayfirst=True
    ).dt.strftime("%Y-%m-%d")

    # Only keep dates newer than the existing database
    latest_db_date = con.execute(
        """
        SELECT MAX(date)
        FROM fact_nav
        WHERE amfi_code = ?
        """,
        (int(amfi_code),)
    ).fetchone()[0]

    if latest_db_date:
        df = df[df["date"] > latest_db_date]

    if not df.empty:

        df.to_sql(
            "fact_nav",
            con,
            if_exists="append",
            index=False
        )

        print(
            f"{fund_name}: {len(df)} new NAV rows added."
        )

    else:

        print(
            f"{fund_name}: no new NAV data."
        )

con.close()

print("\nLive NAV successfully updated in SQLite.")