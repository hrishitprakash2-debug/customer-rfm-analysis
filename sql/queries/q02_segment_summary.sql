-- Q02 | RFM segment value: customers, revenue, share
SELECT segment,
       COUNT(*) AS customers,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM dim_customer_rfm), 1) AS pct_customers,
       ROUND(SUM(monetary), 0) AS revenue,
       ROUND(100.0 * SUM(monetary) / (SELECT SUM(monetary) FROM dim_customer_rfm), 1) AS pct_revenue,
       ROUND(AVG(recency_days), 0) AS avg_recency_days,
       ROUND(AVG(frequency), 1) AS avg_frequency,
       ROUND(AVG(monetary), 0) AS avg_monetary,
       ROUND(AVG(aov), 0) AS avg_order_value
FROM dim_customer_rfm
GROUP BY segment
ORDER BY revenue DESC;