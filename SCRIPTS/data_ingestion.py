import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# 01_fund_master.csv
print("\n========== FUND MASTER ==========")

fund_master = pd.read_csv("DATA/RAW/01_fund_master.csv")
print("\nFirst 5 Rows")
print(fund_master.head(5))

print("\nShape of Fund Master")
print(fund_master.shape) # There is 15 Columns and 40 Rows

print("\nInformation about Fund Master")
print(fund_master.info()) # There is no null values are present in this table 

print("\nDescription of Fund Master")
print(fund_master.describe())

# 02_nav_history.csv
print("\n========== NAV HISTORY ==========")
nav_his = pd.read_csv("DATA/RAW/02_nav_history.csv")

print("\nFirst 5 Rows")
print(nav_his.head(5))

print("\nShape of NAV History")
print(nav_his.shape) # There is 3 Column nd 46000 Rows

print("\nData Types of NAV History")
print(nav_his.dtypes)

print("\nInformation about NAV History")
print(nav_his.info())

print("\nDescription of NAV History")
print(nav_his.describe())

# 03_aum_by_fund_house
print("\n========== AUM BY FUND HOUSE ==========")
aum_fund_house = pd.read_csv("DATA/RAW/03_aum_by_fund_house.csv")

print("\nFirst 5 Rows")
print(aum_fund_house.head(5))

print("\nShape of AUM by Fund House")
print(aum_fund_house.shape)

print("\nData Types of AUM by Fund House")
print(aum_fund_house.dtypes)

print("\nInformation about AUM by Fund House")
print(aum_fund_house.info())

print("\nDescription of AUM by Fund House")
print(aum_fund_house.describe())

# 04_monthly_sip_inflows
print("\n========== MONTHLY SIP INFLOWS ==========")
m_sip_inflows = pd.read_csv("DATA/RAW/04_monthly_sip_inflows.csv")

print("\nFirst 5 Rows")
print(m_sip_inflows.head(5))

print("\nShape of Monthly SIP Inflows")
print(m_sip_inflows.shape)

print("\nData Types of Monthly SIP Inflows")
print(m_sip_inflows.dtypes)

print("\nInformation about Monthly SIP Inflows")
print(m_sip_inflows.info())

print("\nDescription of Monthly SIP Inflows")
print(m_sip_inflows.describe())

# 05_category_inflows
print("\n========== CATEGORY INFLOWS ==========")
cat_inflows = pd.read_csv("DATA/RAW/05_category_inflows.csv")

print("\nFirst 5 Rows")
print(cat_inflows.head(5))

print("\nShape of Category Inflows")
print(cat_inflows.shape)

print("\nData Types of Category Inflows")
print(cat_inflows.dtypes)

print("\nInformation about Category Inflows")
print(cat_inflows.info())

print("\nDescription of Category Inflows")
print(cat_inflows.describe())

# 06_industry_folio_counts
print("\n========== INDUSTRY FOLIO COUNTS ==========")
ind_folio_count = pd.read_csv("DATA/RAW/06_industry_folio_count.csv")

print("\nFirst 5 Rows")
print(ind_folio_count.head(5))

print("\nShape of Industry Folio Counts")
print(ind_folio_count.shape)

print("\nData Types of Industry Folio Counts")
print(ind_folio_count.dtypes)

print("\nInformation about Industry Folio Counts")
print(ind_folio_count.info())

print("\nDescription of Industry Folio Counts")
print(ind_folio_count.describe())

# 07_scheme_performance
print("\n========== SCHEME PERFORMANCE ==========")
scheme_perf = pd.read_csv("DATA/RAW/07_scheme_performance.csv")

print("\nFirst 5 Rows")
print(scheme_perf.head(5))

print("\nShape of Scheme Performance")
print(scheme_perf.shape)

print("\nData Types of Scheme Performance")
print(scheme_perf.dtypes)

print("\nInformation about Scheme Performance")
print(scheme_perf.info())

print("\nDescription of Scheme Performance")
print(scheme_perf.describe())

# 08_investor_transactions
print("\n========== INVESTOR TRANSACTIONS ==========")
investor_trans = pd.read_csv("DATA/RAW/08_investor_transactions.csv")

print("\nFirst 5 Rows")
print(investor_trans.head(5))

print("\nShape of Investor Transactions")
print(investor_trans.shape)

print("\nData Types of Investor Transactions")
print(investor_trans.dtypes)

print("\nInformation about Investor Transactions")
print(investor_trans.info())

print("\nDescription of Investor Transactions")
print(investor_trans.describe())

#09_portfolio_holdings
print("\n========== PORTFOLIO HOLDINGS ==========")
portfolio_holding = pd.read_csv("DATA/RAW/09_portfolio_holdings.csv")

print("\nFirst 5 Rows")
print(portfolio_holding.head(5))

print("\nShape of Portfolio Holdings")
print(portfolio_holding.shape)

print("\nData Types of Portfolio Holdings")
print(portfolio_holding.dtypes)

print("\nInformation about Portfolio Holdings")
print(portfolio_holding.info())

print("\nDescription of Portfolio Holdings")
print(portfolio_holding.describe())

#10_benchmark_indices
print("\n========== BENCHMARK INDICES ==========")
b_mark_indice = pd.read_csv("DATA/RAW/10_benchmark_indices.csv")

print("\nFirst 5 Rows")
print(b_mark_indice.head(5))

print("\nShape of Benchmark Indices")
print(b_mark_indice.shape)

print("\nData Types of Benchmark Indices")
print(b_mark_indice.dtypes)

print("\nInformation about Benchmark Indices")
print(b_mark_indice.info())

print("\nDescription of Benchmark Indices")
print(b_mark_indice.describe())

# Explore Master Fund Data
print("\n========== EXPLORE FUND MASTER ==========")
print(fund_master.head(5))

# Unique Fund Houses
print(fund_master['fund_house'].unique())

# Unique Categories
print(fund_master['category'].unique())

# Unique Sub_Categories
print(fund_master['sub_category'].unique())

# Unique Risk_grades
print(fund_master['risk_category'].unique())








