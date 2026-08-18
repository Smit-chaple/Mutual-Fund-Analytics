import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# Nav_history

clean_his = pd.read_csv("DATA/RAW/02_nav_history.csv")
print(clean_his.head(10),"\n")

print(clean_his.shape,"\n")

print(clean_his.info(),"\n")

print(clean_his.describe(),"\n")

clean_his['date'] =pd.to_datetime(clean_his['date'], format='%Y-%m-%d')

print("info()","\n")
clean_his.info()

clean_his = clean_his.sort_values(by=['amfi_code', 'date'], ascending=True)

if clean_his["nav"].isnull().any():
    raise ValueError("NAV contains missing values")

if (clean_his["nav"] <= 0).any():
    raise ValueError("NAV contains zero or negative values")

#I checked for missing NAV values. Since no missing values were found, forward-filling was not required

clean_his.to_csv("DATA/PROCESSED/02_nav_history.csv", index=False)

# investor_transactions
investor_trans = pd.read_csv("DATA/RAW/08_investor_transactions.csv")

print(investor_trans.head(10),"\n")

print(f"Shape of investor_trans: {investor_trans.shape}","\n")

print("Checking for column Name: ",investor_trans.columns,"\n")

investor_trans.info()

print(investor_trans.describe(),"\n")

print("Checking for missing values:","\n", investor_trans.isnull().sum(),"\n")

print("Transaction Type values:", investor_trans['transaction_type'].unique(),"\n")
print("KYC Status values:", investor_trans['kyc_status'].unique(),"\n")

print("Negative Amount values:","\n", investor_trans["amount_inr"] <= 0,"\n")

print("Duplicate values:", "\n", investor_trans[["investor_id", "amfi_code", "transaction_type", "transaction_date"]].duplicated().sum(),"\n")

investor_trans['transaction_date'] = pd.to_datetime(investor_trans["transaction_date"], format= "%Y-%m-%d")

investor_trans.to_csv("DATA/PROCESSED/08_investor_transactions.csv", index=False)
# There is no correction is required in this File. The data is clean and ready for analysis.

# scheme_performance
scheme_perf = pd.read_csv("DATA/RAW/07_scheme_performance.csv")

print(scheme_perf.head(10),"\n")

print(f"Shape of Scheme_performance: {scheme_perf.shape}","\n")

scheme_perf.info(),"\n"

print(scheme_perf.describe(),"\n")

print("Column Names: ", scheme_perf.columns,"\n")

print("Checking for missing values:","\n", scheme_perf.isnull().sum(),"\n")

return_cols =[
    'return_1yr_pct',
    'return_3yr_pct',
    'return_5yr_pct',
    'benchmark_3yr_pct',
]

print(scheme_perf[return_cols].dtypes,"\n")

for col in return_cols:

    Q1 = scheme_perf[col].quantile(0.25)
    Q3 = scheme_perf[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    anomalies = scheme_perf[
        (scheme_perf[col] < lower) |
        (scheme_perf[col] > upper)
    ]

    print(f"\n{col}")
    print("Lower limit:", lower)
    print("Upper limit:", upper)
    print("Potential anomalies:", len(anomalies))

col = 'benchmark_3yr_pct'

Q1 = scheme_perf[col].quantile(0.25)
Q3 = scheme_perf[col].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

anomalies = scheme_perf[
    (scheme_perf[col] < lower) |
    (scheme_perf[col] > upper)
]

print(anomalies[
    ['amfi_code',
     'scheme_name',
     'category',
     'fund_house',
     'return_3yr_pct',
     'benchmark_3yr_pct']
])


print("Duplicate Values:","\n", scheme_perf[["amfi_code", "scheme_name"]].duplicated().sum(),"\n")

print(f"Expense Ratio values: {scheme_perf['expense_ratio_pct'].between(0.1, 2.5).sum()}","\n")

print(f"Out of expense_ratio_pct range: {((scheme_perf['expense_ratio_pct'] < 0.1) | (scheme_perf['expense_ratio_pct'] > 2.5)).sum()}","\n")

scheme_perf.to_csv("DATA/PROCESSED/07_scheme_performance.csv", index = False)

# fund master
fund = pd.read_csv("DATA/RAW/01_fund_master.csv")
print(fund.head(10),"\n")

print(f"Shape of fund: {fund.shape}","\n")
fund.info()
print(fund.describe(),"\n")
print("Column Names: ", fund.columns,"\n")
print("Checking for missing values:","\n", fund.isnull().sum(),"\n")
print("Duplicate Values:","\n", fund[["amfi_code", "scheme_name"]].duplicated().sum(),"\n")

# Remove completely empty rows
fund.dropna(how="all", inplace=True)

# Remove rows where essential fund information is missing
fund.dropna(
    subset=["amfi_code", "scheme_name", "fund_house"],
    inplace=True
)

fund["launch_date"] = pd.to_datetime(fund["launch_date"], format="%d-%m-%Y")
fund.to_csv("DATA/PROCESSED/01_fund_master.csv", index=False)

# aum by fund house
aum_fund_house = pd.read_csv("DATA/RAW/03_aum_by_fund_house.csv")
print("AUM by Fund House: ",aum_fund_house.head(10),"\n")

print(f"Shape of aum_fund_house: {aum_fund_house.shape}","\n")
aum_fund_house.info()
print(aum_fund_house.describe(),"\n")
print("Column Names: ", aum_fund_house.columns,"\n")
print("Checking for missing values:","\n", aum_fund_house.isnull().sum(),"\n")
print("Duplicate Values:","\n", aum_fund_house[["date","fund_house"]].duplicated().sum(),"\n")

aum_fund_house["date"] =pd.to_datetime(aum_fund_house["date"], format = "%d-%m-%Y")
aum_fund_house.to_csv("DATA/PROCESSED/03_aum_by_fund_house.csv", index=False)

# Monthly Sip Inflows
mon_sip = pd.read_csv("DATA/RAW/04_monthly_sip_inflows.csv")
print(mon_sip.head(10),"\n")

print("Shape of monthly_sip_inflows: ",mon_sip.shape,"\n")
mon_sip.info()
print(mon_sip.describe(),"\n")
print("Column Name: ",mon_sip.columns,"\n")
print("Checking for missing values: ",mon_sip.isnull().sum())

print(mon_sip[mon_sip['yoy_growth_pct'].isnull()][
    ['month', 'yoy_growth_pct']
],"\n")
# yoy_growth_pct contains 12 missing values corresponding to the first 12 months of the dataset, 
# where prior-year monthly data is unavailable. These values were retained as null.

# print(mon_sip[mon_sip["new_sip_accounts_lakh"] == 46],"\n")

mon_sip["month"] = pd.to_datetime(mon_sip["month"], format="%Y-%m")
mon_sip.to_csv("DATA/PROCESSED/04_monthly_sip_inflows.csv", index=False)
print("Shape: ",mon_sip.head(),"\n")

# category inflows 
cat_inflow = pd.read_csv("DATA/RAW/05_category_inflows.csv")
print(cat_inflow.head(10),"\n")

print("Shape of category_inflows: ",cat_inflow.shape,"\n")
cat_inflow.info()
print(cat_inflow.describe(),"\n")
print("Columns Name: ",cat_inflow.columns,"\n")
print("Checking for missing values: ","\n",cat_inflow.isnull().sum(),"\n")
print("Duplicate Values: ","\n",cat_inflow[["month", "category"]].duplicated().sum(),"\n")

cat_inflow["month"] = pd.to_datetime(cat_inflow["month"], format = "%Y-%m")
cat_inflow.to_csv("DATA/PROCESSED/05_category_inflows.csv", index = False)

# Industry folio count
ind_folio = pd.read_csv("DATA/RAW/06_industry_folio_count.csv")
print(ind_folio.head(10),"\n")

print("Shape of industry_folio_count: ",ind_folio.shape,"\n")
ind_folio.info()
print(ind_folio.describe(),"\n")
print("Column Names: ",ind_folio.columns,"\n")
print("Checking for missing values: ","\n",ind_folio.isnull().sum(),"\n")

ind_folio["calculated_total"] = (
    ind_folio["equity_folios_crore"]
    + ind_folio["debt_folios_crore"]
    + ind_folio["hybrid_folios_crore"]
    + ind_folio["others_folios_crore"]
)

ind_folio["difference"] = (
    ind_folio["total_folios_crore"]
    - ind_folio["calculated_total"]
)

print(ind_folio[
    ["month", "total_folios_crore", "calculated_total", "difference"]
])

ind_folio.drop(
    columns=["calculated_total", "difference"],
    inplace=True
)

ind_folio["month"] = pd.to_datetime(ind_folio["month"], format = "%Y-%m")
ind_folio.to_csv("DATA/PROCESSED/06_industry_folio_count.csv", index=False)

# Portfolio Holding
port_holding = pd.read_csv("DATA/RAW/09_portfolio_holdings.csv")
print(port_holding.head(10),"\n")

print("Shape of portfolio_holdings: ",port_holding.shape,"\n")
port_holding.info()
print(port_holding.describe(),"\n")
print("Column Names: ",port_holding.columns,"\n")
print("Checking for missing values: ","\n",port_holding.isnull().sum(),"\n")
print("Duplicated Values: ","\n",port_holding[["amfi_code", "stock_symbol", "portfolio_date"]].duplicated().sum(),"\n")
print((port_holding['weight_pct'] > 0).sum(),"\n")
port_holding["portfolio_date"] = pd.to_datetime(port_holding["portfolio_date"], format = "%d-%m-%Y")
port_holding.to_csv("DATA/PROCESSED/09_portfolio_holdings.csv", index = False)

# Benchmark_indices
bench_indice = pd.read_csv("DATA/RAW/10_benchmark_indices.csv")
print(bench_indice.head(10), "\n")

print("Shape of benchmark_indices: ", bench_indice.shape, "\n")
bench_indice.info()
print(bench_indice.describe(), "\n")
print("Column Names: ", bench_indice.columns, "\n")
print("Checking for missing values: ", "\n", bench_indice.isnull().sum(), "\n")
print((bench_indice["close_value"] < 0).sum(),"\n")
print("Duplicate Values: ", "\n", bench_indice[["index_name", "date"]].duplicated().sum(), "\n")

bench_indice["date"] = pd.to_datetime(bench_indice["date"], format = "%d-%m-%Y")
bench_indice.to_csv("DATA/PROCESSED/10_benchmark_indices.csv", index = False)