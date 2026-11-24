# Query results

## q01_kpi_overview

Q01 | Headline KPIs

|   sale_lines |   invoices |   customers |     revenue |   avg_order_value |   repeat_customer_pct |
|-------------:|-----------:|------------:|------------:|------------------:|----------------------:|
|  1.00791e+06 |      40077 |        5878 | 2.04763e+07 |            510.92 |                  72.4 |

## q02_segment_summary

Q02 | RFM segment value: customers, revenue, share

| segment              |   customers |   pct_customers |          revenue |   pct_revenue |   avg_recency_days |   avg_frequency |   avg_monetary |   avg_order_value |
|:---------------------|------------:|----------------:|-----------------:|--------------:|-------------------:|----------------:|---------------:|------------------:|
| Champions            |        1473 |            25.1 |      1.19834e+07 |          69   |                 20 |            15.7 |           8135 |               413 |
| Loyal                |        1229 |            20.9 |      2.54996e+06 |          14.7 |                 78 |             5.4 |           2075 |               369 |
| At Risk (high value) |         395 |             6.7 |      1.43009e+06 |           8.2 |                366 |             6.2 |           3620 |               814 |
| Hibernating          |        1463 |            24.9 | 475957           |           2.7 |                460 |             1.2 |            325 |               266 |
| New / Promising      |         441 |             7.5 | 391838           |           2.3 |                 28 |             1.5 |            889 |               536 |
| Can't Lose           |         493 |             8.4 | 339778           |           2   |                378 |             3.5 |            689 |               209 |
| Needs Attention      |         384 |             6.5 | 203761           |           1.2 |                106 |             1.4 |            531 |               395 |

## q03_customer_pareto

Q03 | Revenue concentration: cumulative share by customer rank

|   customer_rank |          revenue |   cumulative_pct_of_revenue |   total_customers |
|----------------:|-----------------:|----------------------------:|------------------:|
|               1 |      3.10146e+06 |                        15.1 |              5879 |
|              10 | 147143           |                        28.1 |              5879 |
|              50 |  34095           |                        40.7 |              5879 |
|             100 |  20204           |                        46.9 |              5879 |
|             500 |   6221           |                        66.9 |              5879 |
|            1000 |   3424           |                        78   |              5879 |
|            2000 |   1551           |                        89.2 |              5879 |
|            3000 |    835           |                        94.8 |              5879 |
|            4000 |    439           |                        97.8 |              5879 |
|            5000 |    215           |                        99.4 |              5879 |

## q04_cohort_retention

Q04 | Monthly cohort retention matrix (SQL does the whole calculation)

|   cohort_month_index |   month_offset |   active_customers |   cohort_size |   retention_pct |
|---------------------:|---------------:|-------------------:|--------------:|----------------:|
|                24120 |              0 |                955 |           956 |            99.9 |
|                24120 |              1 |                337 |           956 |            35.3 |
|                24120 |              2 |                319 |           956 |            33.4 |
|                24120 |              3 |                406 |           956 |            42.5 |
|                24120 |              4 |                363 |           956 |            38   |
|                24120 |              5 |                343 |           956 |            35.9 |
|                24120 |              6 |                360 |           956 |            37.7 |
|                24120 |              7 |                327 |           956 |            34.2 |
|                24120 |              8 |                321 |           956 |            33.6 |
|                24120 |              9 |                346 |           956 |            36.2 |

## q05_repeat_rate_by_cohort

Q05 | Repeat-purchase rate per cohort (share buying more than once)

|   cohort_month_index |   cohort_size |   repeaters |   repeat_pct |   avg_invoices |
|---------------------:|--------------:|------------:|-------------:|---------------:|
|                24120 |           955 |         871 |         91.2 |          16.08 |
|                24121 |           383 |         336 |         87.7 |           8.23 |
|                24122 |           374 |         315 |         84.2 |           6.72 |
|                24123 |           443 |         364 |         82.2 |           6.52 |
|                24124 |           294 |         231 |         78.6 |           5.14 |
|                24125 |           254 |         199 |         78.3 |           4.43 |
|                24126 |           270 |         205 |         75.9 |           4.49 |
|                24127 |           186 |         140 |         75.3 |           5.16 |
|                24128 |           162 |         117 |         72.2 |           4.6  |
|                24129 |           243 |         171 |         70.4 |           4.13 |

## q06_monthly_revenue

Q06 | Monthly revenue, invoices and AOV (window functions for growth)

|   month_index | month_label   |   revenue |   invoices |   customers |    aov |   mom_growth_pct |   cumulative_revenue_pct |
|--------------:|:--------------|----------:|-----------:|------------:|-------:|-----------------:|-------------------------:|
|         24120 | 2009-12       |    822484 |       1682 |         955 | 488.99 |            nan   |                      4   |
|         24121 | 2010-01       |    651155 |       1105 |         720 | 589.28 |            -20.8 |                      7.2 |
|         24122 | 2010-02       |    551505 |       1201 |         772 | 459.2  |            -15.3 |                      9.9 |
|         24123 | 2010-03       |    830915 |       1681 |        1057 | 494.3  |             50.7 |                     13.9 |
|         24124 | 2010-04       |    678875 |       1462 |         942 | 464.35 |            -18.3 |                     17.3 |
|         24125 | 2010-05       |    657706 |       1500 |         966 | 438.47 |             -3.1 |                     20.5 |
|         24126 | 2010-06       |    749537 |       1645 |        1041 | 455.65 |             14   |                     24.1 |
|         24127 | 2010-07       |    648810 |       1529 |         928 | 424.34 |            -13.4 |                     27.3 |
|         24128 | 2010-08       |    695252 |       1425 |         911 | 487.9  |              7.2 |                     30.7 |
|         24129 | 2010-09       |    921697 |       1839 |        1145 | 501.19 |             32.6 |                     35.2 |

## q07_winback_list

Q07 | Win-back list: high-value customers who have gone quiet

|   customer_id | country        | segment              |   recency_days |   frequency |   lifetime_revenue |   r_score |   f_score |   m_score |
|--------------:|:---------------|:---------------------|---------------:|------------:|-------------------:|----------:|----------:|----------:|
|         12346 | United Kingdom | At Risk (high value) |            326 |          12 |              77556 |         2 |         5 |         5 |
|         16754 | United Kingdom | At Risk (high value) |            372 |          29 |              65500 |         2 |         5 |         5 |
|         13093 | United Kingdom | At Risk (high value) |            276 |          55 |              54144 |         2 |         5 |         5 |
|         17850 | United Kingdom | At Risk (high value) |            372 |         155 |              51209 |         2 |         5 |         5 |
|         15749 | United Kingdom | At Risk (high value) |            235 |           3 |              44534 |         2 |         3 |         5 |
|         15098 | United Kingdom | Loyal                |            182 |           3 |              39917 |         3 |         3 |         5 |
|         13902 | Denmark        | At Risk (high value) |            632 |           5 |              34095 |         1 |         4 |         5 |
|         12482 | Sweden         | At Risk (high value) |            576 |          29 |              23691 |         1 |         5 |         5 |
|         14063 | United Kingdom | At Risk (high value) |            438 |           9 |              22710 |         1 |         5 |         5 |
|         15808 | United Kingdom | At Risk (high value) |            306 |          21 |              17180 |         2 |         5 |         5 |

## q08_country_performance

Q08 | Market performance (min 50 customers)

| country        |   customers |   invoices |          revenue |   avg_line_value |
|:---------------|------------:|-----------:|-----------------:|-----------------:|
| United Kingdom |        5349 |      33539 |      1.43885e+07 |            20.54 |
| Germany        |         107 |        790 | 425940           |            25.85 |
| France         |          93 |        610 | 347091           |            25.85 |

## q09_order_value_bands

Q09 | Order value distribution, and how many orders are one-offs

| order_band   |   orders |   pct_orders |          revenue |   pct_revenue |
|:-------------|---------:|-------------:|-----------------:|--------------:|
| £1k+         |     3599 |          9   |      9.39882e+06 |          45.9 |
| £250-500     |    13277 |         33.1 |      4.68634e+06 |          22.9 |
| £500-1k      |     6234 |         15.6 |      4.26018e+06 |          20.8 |
| £100-250     |    11146 |         27.8 |      1.88771e+06 |           9.2 |
| £50-100      |     2247 |          5.6 | 171287           |           0.8 |
| <£50         |     3574 |          8.9 |  71918           |           0.4 |

## q10_segment_at_risk_value

Q10 | Revenue at stake in the at-risk segments

| segment              |   customers |   lifetime_revenue |   avg_days_since_last |   avg_orders |   revenue_dormant_180d |
|:---------------------|------------:|-------------------:|----------------------:|-------------:|-----------------------:|
| At Risk (high value) |         395 |        1.43009e+06 |                   366 |          6.2 |            1.43009e+06 |
| Hibernating          |        1463 |   475957           |                   460 |          1.2 |       475957           |
| Can't Lose           |         493 |   339778           |                   378 |          3.5 |       339778           |
| Loyal                |        1229 |        2.54996e+06 |                    78 |          5.4 |        87200           |
| Needs Attention      |         384 |   203761           |                   106 |          1.4 |         3462           |
| New / Promising      |         441 |   391838           |                    28 |          1.5 |            0           |
| Champions            |        1473 |        1.19834e+07 |                    20 |         15.7 |            0           |
