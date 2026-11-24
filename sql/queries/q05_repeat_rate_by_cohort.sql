-- Q05 | Repeat-purchase rate per cohort (share buying more than once)
WITH first_m AS (
    SELECT f.customer_sk, MIN(d.month_index) AS cohort_index
    FROM fact_sale f JOIN dim_date d ON d.date_sk = f.date_sk
    GROUP BY f.customer_sk
),
freq AS (
    SELECT customer_sk, COUNT(DISTINCT invoice) AS invoices
    FROM fact_sale GROUP BY customer_sk
)
SELECT fm.cohort_index AS cohort_month_index,
       COUNT(*) AS cohort_size,
       SUM(CASE WHEN fq.invoices > 1 THEN 1 ELSE 0 END) AS repeaters,
       ROUND(100.0 * SUM(CASE WHEN fq.invoices > 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS repeat_pct,
       ROUND(AVG(fq.invoices), 2) AS avg_invoices
FROM first_m fm JOIN freq fq ON fq.customer_sk = fm.customer_sk
GROUP BY fm.cohort_index
ORDER BY fm.cohort_index;