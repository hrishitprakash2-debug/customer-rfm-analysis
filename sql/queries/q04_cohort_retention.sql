-- Q04 | Monthly cohort retention matrix (SQL does the whole calculation)
WITH first_m AS (
    SELECT f.customer_sk, MIN(d.month_index) AS cohort_index
    FROM fact_sale f JOIN dim_date d ON d.date_sk = f.date_sk
    GROUP BY f.customer_sk
),
activity AS (
    SELECT DISTINCT f.customer_sk, d.month_index
    FROM fact_sale f JOIN dim_date d ON d.date_sk = f.date_sk
),
offsets AS (
    SELECT fm.cohort_index, a.customer_sk, a.month_index - fm.cohort_index AS month_offset
    FROM activity a JOIN first_m fm ON fm.customer_sk = a.customer_sk
),
sizes AS (
    SELECT cohort_index, COUNT(*) AS cohort_size FROM first_m GROUP BY cohort_index
)
SELECT o.cohort_index AS cohort_month_index,
       o.month_offset,
       COUNT(DISTINCT o.customer_sk) AS active_customers,
       s.cohort_size,
       ROUND(100.0 * COUNT(DISTINCT o.customer_sk) / s.cohort_size, 1) AS retention_pct
FROM offsets o JOIN sizes s ON s.cohort_index = o.cohort_index
WHERE o.month_offset <= 12
GROUP BY o.cohort_index, o.month_offset, s.cohort_size
ORDER BY o.cohort_index, o.month_offset;