import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///SQL/bluestoke_mf.db")

fund = pd.read_csv("DATA/PROCESSED/01_fund_master.csv")
fund.to_sql(
    name = "dim_fund",
    con = engine,
    if_exists = "replace",
    index = False
)
print("dim_fund table created successfully in the database.")

nav_his = pd.read_csv("DATA/PROCESSED/02_nav_history.csv")
nav_his.to_sql(
    name = "fact_nav",
    con =  engine,
    if_exists = "replace",
    index = False
    )
print("fact_nav table created successfully in the database.")

aum_fund_house = pd.read_csv("DATA/PROCESSED/03_aum_by_fund_house.csv")
aum_fund_house.to_sql(
    name = "fact_aum",
    con = engine,
    if_exists = "replace",
    index = False
)
print("fact_aum table created successfully in the database.")

scheme = pd.read_csv("DATA/PROCESSED/07_scheme_performance.csv")
scheme.to_sql(
    name = "fact_performance",
    con = engine,
    if_exists = "replace",
    index = False
)
print("fact_performance table created successfully in the database.")

investor = pd.read_csv("DATA/PROCESSED/08_investor_transactions.csv")
investor.to_sql(
    name = "fact_transactions",
    con = engine,
    if_exists = "replace",
    index = False
)
print("fact_transactions table created successfully in the database.","\n")

mon_sip = pd.read_csv("DATA/PROCESSED/04_monthly_sip_inflows.csv")
mon_sip.to_sql(
    name = "fact_sip",
    con = engine,
    if_exists = "replace",
    index = False
)

# Verification 
from sqlalchemy import text 

def verify_count(engine, table_name, dataframe):
    with engine.connect() as conn:
        db_count = conn.execute(
            text(f"select count(*) from {table_name}")
        ).scalar()

    print(f"Data_Frame Rows: {dataframe.shape[0]}")
    print(f"DataBase Rows: {db_count}")

    if dataframe.shape[0]==db_count:
        print("Verification Passed")
    else:
        print("Verification Failed")

print(verify_count(engine,"dim_fund", fund),"\n")
print(verify_count(engine,"fact_aum", aum_fund_house),"\n")
print(verify_count(engine,"fact_nav", nav_his),"\n")
print(verify_count(engine,"fact_performance", scheme),"\n")
print(verify_count(engine,"fact_transactions", investor),"\n")
print(verify_count(engine,"fact_sip", mon_sip),"\n")