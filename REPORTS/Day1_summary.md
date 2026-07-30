# Day 1 Summary – Data Ingestion

## Tasks Completed

* Created the project folder structure for organizing raw data, processed data, scripts, reports, SQL files, and dashboards.
* Loaded the provided CSV datasets using Pandas and verified their structure using `.head()`, `.shape`, `.dtypes`, and `.info()`.
* Fetched live NAV data from the MFAPI and stored it in the `DATA/RAW` folder.
* Explored the `fund_master` dataset to understand the available fund houses, categories, sub-categories, and risk grades.
* Validated the relationship between the `fund_master` and `nav_history` datasets using the `amfi_code` column.

## Data Quality Summary

* The `fund_master` dataset contains **10 unique fund houses** and **40 mutual fund schemes**.
* The `nav_history` dataset is linked to the `fund_master` dataset through the **amfi_code** field and stores the historical **Net Asset Value (NAV)** with the corresponding dates.
* Data validation confirmed that **all AMFI scheme codes in `fund_master` are present in `nav_history`**.
* No missing AMFI codes were found during the validation process.
* The datasets were successfully loaded and are ready for the next stage of data cleaning and exploratory data analysis.
  