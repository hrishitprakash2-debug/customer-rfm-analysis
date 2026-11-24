-- Q09 | Order value distribution, and how many orders are one-offs
WITH o AS (
    SELECT invoice, customer_sk, SUM(line_total) AS order_value
    FROM fact_sale GROUP BY invoice, customer_sk
)
SELECT CASE WHEN order_value < 50 THEN '<£50'
            WHEN order_value < 100 THEN '£50-100'
            WHEN order_value < 250 THEN '£100-250'
            WHEN order_value < 500 THEN '£250-500'
            WHEN order_value < 1000 THEN '£500-1k'
            ELSE '£1k+' END AS order_band,
       COUNT(*) AS orders,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM o), 1) AS pct_orders,
       ROUND(SUM(order_value), 0) AS revenue,
       ROUND(100.0 * SUM(order_value) / (SELECT SUM(order_value) FROM o), 1) AS pct_revenue
FROM o
GROUP BY order_band
ORDER BY revenue DESC;