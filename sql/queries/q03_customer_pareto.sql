-- Q03 | Revenue concentration: cumulative share by customer rank
WITH c AS (
    SELECT customer_sk, SUM(line_total) AS revenue
    FROM fact_sale GROUP BY customer_sk
), cum AS (
    SELECT revenue,
           ROW_NUMBER() OVER (ORDER BY revenue DESC) AS rn,
           SUM(revenue) OVER (ORDER BY revenue DESC
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running,
           SUM(revenue) OVER () AS total,
           COUNT(*) OVER () AS n
    FROM c
)
SELECT rn AS customer_rank,
       ROUND(revenue, 0) AS revenue,
       ROUND(100.0 * running / total, 1) AS cumulative_pct_of_revenue,
       n AS total_customers
FROM cum
WHERE rn IN (1, 10, 50, 100, 500, 1000, 2000, 3000, 4000, 5000)
ORDER BY rn;