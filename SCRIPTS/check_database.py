import sqlite3

db_path = "SQL/bluestoke_mf.db"

con = sqlite3.connect(db_path)

print("\n========== QUERY 1: FUND COUNT ==========\n")

result = con.execute("""
    SELECT COUNT(*)
    FROM dim_fund
""").fetchone()[0]

print("Total funds:", result)


print("\n========== QUERY 2: FUND HOUSES ==========\n")

result = con.execute("""
    SELECT fund_house, COUNT(*) AS scheme_count
    FROM dim_fund
    GROUP BY fund_house
    ORDER BY scheme_count DESC
""").fetchall()

for row in result:
    print(row)


print("\n========== QUERY 3: NAV RECORDS ==========\n")

result = con.execute("""
    SELECT COUNT(*)
    FROM fact_nav
""").fetchone()[0]

print("Total NAV records:", result)


print("\n========== QUERY 4: TRANSACTION SUMMARY ==========\n")

result = con.execute("""
    SELECT
        transaction_type,
        COUNT(*) AS transactions,
        SUM(amount_inr) AS total_amount
    FROM fact_transactions
    GROUP BY transaction_type
    ORDER BY total_amount DESC
""").fetchall()

for row in result:
    print(row)


# ============================================================
# CHECK SUSPICIOUS FUND MASTER RECORDS
# ============================================================

print("\n========== SUSPICIOUS FUND MASTER RECORDS ==========\n")

result = con.execute("""
    SELECT *
    FROM dim_fund
    WHERE fund_house IS NULL
       OR fund_house = '10'
""").fetchall()

for row in result:
    print(row)


# ============================================================
# CLOSE DATABASE
# ============================================================

con.close()

