select * from fact_performance;

-- Top 5 funds by AUM
select scheme_name, aum_crore from fact_performance
order by aum_crore desc
limit 5;

-- Average NAV per month
select * from fact_nav;

select strftime('%Y-%m',date) Month, avg(nav) avg_nav from fact_nav
group by Month;

-- SIP YoY growth
select * from fact_aum;
select * from fact_transactions;

-- Transactions by state


-- Funds with expense ratio < 1%