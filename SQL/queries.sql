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
select month from fact_sip;

SELECT
    month,
    yoy_growth_pct
FROM fact_sip
WHERE yoy_growth_pct IS NOT NULL
ORDER BY month;

-- Transactions by state
select * from fact_transactions;

select state, count(state) transactions from fact_transactions
group by state
order by transactions desc;

-- Funds with expense ratio < 1%
select * from dim_fund;

select * from dim_fund 
where expense_ratio_pct < 1
order by expense_ratio_pct asc;

-- top 5 fund houses based on their total AUM
select * from fact_aum;

select fund_house, sum(aum_crore) Total_aum_crore from fact_aum
group by fund_house
order by total_aum_crore desc 
limit 5;

-- Top 5 states with the highest total SIP investment amount.
select * from fact_transactions;

select state, sum(amount_inr) sip_investment from fact_transactions
where transaction_type = 'SIP'
group by state 
order by sip_investment DESC
limit 5;

-- Top 5 fund managers managing the highest total AUM
select d.fund_manager, sum(a.aum_crore) total_aum from dim_fund d
join fact_aum a
on d.fund_house = a.fund_house
group by d.fund_manager
order by total_aum desc
limit 5;

-- Top 5 schemes that generated the highest total transaction amount through SIP investments only.
select d.scheme_name, sum(t.amount_inr) total_transaction_amount from dim_fund d
join fact_transactions t 
on d.amfi_code = t.amfi_code
where t.transaction_type = "SIP"
group by d.scheme_name
order by total_transaction_amount DESC
limit 5;

-- Find the average 3-year return (return_3yr_pct) for each fund category, 
-- and display only those categories where the average return is greater than 15%. 
-- Sort the results from highest to lowest average return.
select category, avg(return_3yr_pct) avg_3year from fact_performance
group by category 
having avg_3year > 15 
order by avg_3year desc;