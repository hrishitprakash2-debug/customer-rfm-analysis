-- Q07 | Win-back list: high-value customers who have gone quiet
SELECT c.customer_id, c.country, r.segment, r.recency_days, r.frequency,
       ROUND(r.monetary, 0) AS lifetime_revenue,
       r.r_score, r.f_score, r.m_score
FROM dim_customer_rfm r JOIN dim_customer c ON c.customer_sk = r.customer_sk
WHERE r.recency_days > 180 AND r.m_score >= 4
ORDER BY r.monetary DESC
LIMIT 25;