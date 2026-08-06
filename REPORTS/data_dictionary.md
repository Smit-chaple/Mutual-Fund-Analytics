# Data Dictionary

## Project: Mutual Fund Analytics
**Author:** Smit Chaple  
**Description:** This document describes the datasets, columns, data types, business definitions, and source files used in the Mutual Fund Analytics project.

---

# 1. Fund Master

**Source:** DATA/RAW/01_fund_master.csv

Column Name              Data Type          Business Definition

amfi_code                Integer            Unique AMFI code identifying each mutual fund scheme.
fund_house               Text               Name of the Asset Management Company (AMC).
scheme_name              Text               Official name of the mutual fund scheme.
category                 Text               Primary investment category of the mutual fund.
sub_category             Text               Detailed classification of the mutual fund.
plan                     Text               Indicates whether the scheme is Direct or Regular.
launch_date              Date               Date on which the mutual fund scheme was launched.
benchmark                Text               Benchmark index used to evaluate scheme performance.
expense_ratio_pct        Decimal            Annual management fee charged by the fund.
exit_load_pct            Decimal            Exit fee charged when units are redeemed before the specified period.
min_sip_amount           Integer            Minimum amount required to start a SIP.
min_lumpsum_amount       Integer            Minimum amount required for one-time investment.
fund_manager             Text               Name of the fund manager responsible for the scheme.
risk_category            Text               Risk classification assigned to the scheme.
sebi_category_code       Text               SEBI classification code for the scheme.



## Dataset Name

NAV History

Source File

DATA/RAW/02_nav_history.csv


Column Name              Data Type          Business Definition

amfi_code                Integer            Unique mutual fund scheme identifier.
date                     Date               Date on which NAV was recorded.
nav                      Decimal            Net Asset Value per unit for the scheme.



## Dataset Name

AUM by Fund House

Source File

DATA/RAW/03_aum_by_fund_house.csv


Column Name              Data Type          Business Definition

date                     Date               Reporting date for AUM values.
fund_house               Text               Name of the Asset Management Company.
aum_lakh_crore           Decimal            Total Assets Under Management expressed in lakh crore.
aum_crore                Integer            Total Assets Under Management expressed in crore.
num_schemes              Integer            Total number of mutual fund schemes managed by the fund house.



## Dataset Name

Monthly SIP Inflows

Source File

DATA/RAW/04_monthly_sip_inflows.csv


Column Name                Data Type          Business Definition

month                      Date               Reporting month.
sip_inflow_crore           Integer            Total SIP inflow during the month (in crore).
active_sip_accounts_crore  Decimal            Number of active SIP accounts (in crore).
new_sip_accounts_lakh      Decimal            Number of new SIP accounts opened (in lakh).
sip_aum_lakh_crore         Decimal            SIP Assets Under Management (in lakh crore).
yoy_growth_pct             Decimal            Year-over-Year percentage growth in SIP inflows.



## Dataset Name

Category Inflows

Source File

DATA/RAW/05_category_inflows.csv


Column Name              Data Type          Business Definition

month                    Date               Reporting month.
category                 Text               Mutual fund category.
net_inflow_crore         Decimal            Net inflow recorded for the category during the month (in crore).



## Dataset Name

Industry Folio Count

Source File

DATA/RAW/06_industry_folio_count.csv


Column Name              Data Type          Business Definition

month                    Date               Reporting month.
total_folios_crore       Decimal            Total investor folios across the mutual fund industry.
equity_folios_crore      Decimal            Number of equity fund folios.
debt_folios_crore        Decimal            Number of debt fund folios.
hybrid_folios_crore      Decimal            Number of hybrid fund folios.
others_folios_crore      Decimal            Number of folios belonging to other categories.



## Dataset Name

Scheme Performance

Source File

DATA/RAW/07_scheme_performance.csv


Column Name             Data Type          Business Definition

amfi_code                Integer            Unique mutual fund scheme identifier.
scheme_name              Text               Official scheme name.
fund_house               Text               Name of the Asset Management Company.
category                 Text               Mutual fund category.
plan                     Text               Direct or Regular plan.
return_1yr_pct           Decimal            One-year annualized return percentage.
return_3yr_pct           Decimal            Three-year annualized return percentage.
return_5yr_pct           Decimal            Five-year annualized return percentage.
benchmark_3yr_pct        Decimal            Three-year benchmark return percentage.
alpha                    Decimal            Risk-adjusted excess return over benchmark.
beta                     Decimal            Measure of volatility relative to benchmark.
sharpe_ratio             Decimal            Risk-adjusted performance metric.
sortino_ratio            Decimal            Downside risk-adjusted performance metric.
std_dev_ann_pct          Decimal            Annualized standard deviation of returns.
max_drawdown_pct         Decimal            Maximum observed portfolio loss from peak.
aum_crore                Integer            Assets Under Management in crore.
expense_ratio_pct        Decimal            Annual expense ratio charged by the scheme.
morningstar_rating       Integer            Morningstar star rating.
risk_grade               Text               Overall investment risk classification.



## Dataset Name

Investor Transactions

Source File

DATA/RAW/08_investor_transactions.csv


Column Name            Data Type          Business Definition

transaction_id          Integer            Unique transaction identifier.
amfi_code               Integer            Mutual fund scheme identifier.
investor_id             Integer            Unique investor identifier.
transaction_date        Date               Date of investment transaction.
transaction_type        Text               Type of transaction (SIP, Lumpsum, Redemption).
amount_inr              Decimal            Transaction amount in Indian Rupees.
units                   Decimal            Number of units purchased or redeemed.
state                   Text               Investor's state.
city_tier               Text               Investor location category (T30/B30).
age_group               Text               Investor age category.
gender                  Text               Investor gender.
kyc_status              Text               Investor KYC verification status.



## Dataset Name

Portfolio Holdings

Source File

DATA/RAW/09_portfolio_holdings.csv


Column Name             Data Type          Business Definition

amfi_code                Integer            Mutual fund scheme identifier.
stock_symbol             Text               Stock ticker symbol.
stock_name               Text               Name of the company.
sector                   Text               Industry sector of the company.
weight_pct               Decimal            Portfolio allocation percentage.
market_value_cr          Decimal            Market value of holdings in crore.
current_price_inr        Decimal            Current market price of the stock.
portfolio_date           Date               Portfolio reporting date.



## Dataset Name

Benchmark Indices

Source File

DATA/RAW/10_benchmark_indices.csv


Column Name             Data Type          Business Definition

date                     Date               Trading date.
index_name               Text               Name of the benchmark index.
close_value              Decimal            Closing value of the benchmark index.