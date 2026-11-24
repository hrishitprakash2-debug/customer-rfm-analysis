-- Q10 | Revenue at stake in the at-risk segments
SELECT segment,
       COUNT(*) AS customers,
       ROUND(SUM(monetary), 0) AS lifetime_revenue,
       ROUND(AVG(recency_days), 0) AS avg_days_since_last,
       ROUND(AVG(frequency), 1) AS avg_orders,
       ROUND(SUM(CASE WHEN recency_days > 180 THEN monetary ELSE 0 END), 0) AS revenue_dormant_180d
FROM dim_customer_rfm
GROUP BY segment
ORDER BY revenue_dormant_180d DESC;