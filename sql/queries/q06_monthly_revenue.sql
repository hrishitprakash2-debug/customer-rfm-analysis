-- Q06 | Monthly revenue, invoices and AOV (window functions for growth)
WITH m AS (
    SELECT d.month_index, d.month_label,
           SUM(f.line_total) AS revenue,
           COUNT(DISTINCT f.invoice) AS invoices,
           COUNT(DISTINCT f.customer_sk) AS customers
    FROM fact_sale f JOIN dim_date d ON d.date_sk = f.date_sk
    GROUP BY d.month_index, d.month_label
)
SELECT month_index, month_label,
       ROUND(revenue, 0) AS revenue,
       invoices, customers,
       ROUND(revenue / invoices, 2) AS aov,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month_index))
             / LAG(revenue) OVER (ORDER BY month_index), 1) AS mom_growth_pct,
       ROUND(100.0 * SUM(revenue) OVER (ORDER BY month_index)
             / SUM(revenue) OVER (), 1) AS cumulative_revenue_pct
FROM m
ORDER BY month_index;