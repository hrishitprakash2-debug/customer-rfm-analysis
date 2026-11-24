-- Q01 | Headline KPIs
SELECT COUNT(*) AS sale_lines,
       COUNT(DISTINCT invoice) AS invoices,
       COUNT(DISTINCT customer_sk) AS customers,
       ROUND(SUM(line_total), 0) AS revenue,
       ROUND(SUM(line_total) / COUNT(DISTINCT invoice), 2) AS avg_order_value,
       (SELECT ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM dim_customer_rfm), 1)
          FROM dim_customer_rfm WHERE frequency > 1) AS repeat_customer_pct
FROM fact_sale;