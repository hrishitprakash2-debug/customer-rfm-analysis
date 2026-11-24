-- Q08 | Market performance (min 50 customers)
SELECT c.country,
       COUNT(DISTINCT c.customer_sk) AS customers,
       COUNT(DISTINCT f.invoice) AS invoices,
       ROUND(SUM(f.line_total), 0) AS revenue,
       ROUND(AVG(f.line_total), 2) AS avg_line_value
FROM fact_sale f JOIN dim_customer c ON c.customer_sk = f.customer_sk
GROUP BY c.country
HAVING COUNT(DISTINCT c.customer_sk) >= 50
ORDER BY revenue DESC
LIMIT 20;