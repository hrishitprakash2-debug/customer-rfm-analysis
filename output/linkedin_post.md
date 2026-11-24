# LinkedIn post — Customer RFM & retention (findings-first)

## Post (copy-paste, plain text)

1,007,913 transactions. 5,878 customers. One quarter of them generate 69% of the revenue.

I ran RFM segmentation and cohort retention on two years of real orders from a UK online retailer. Four things stood out:

- 1,473 "Champions" (25% of customers) produce £12.0M of £17.4M revenue. Their average lifetime value is £8,135.
- The top 100 customers are 46.9% of revenue. The single largest account is 15.1% — one account, one-sixth of the business.
- 725 customers who used to buy have gone quiet for 180+ days, holding £1.9M of historical revenue.
- Retention collapses in the first month: median month-1 retention is 20.5%, and cohorts barely decay after that. The leak is month one, not year two.

My recommendation: the win-back pool is worth more than new acquisition. Reactivating 10% of those 2,351 dormant customers at their historical average order value is roughly £224K — more than 440 new customers at the current average lifetime value.

How I built it:
SQL — SQLite star schema and 10 queries, including a full cohort retention matrix computed in SQL
Python — pandas for cleaning and RFM quintiles, matplotlib and seaborn for the heatmaps
Excel — customer-level workbook where every summary figure is a live formula, verified against pandas (7/7)

Caveat: this retailer is wholesale-heavy, so the absolute values are far above consumer benchmarks. The structure — concentration and the month-1 drop-off — is what transfers.

Code is on my GitHub (link in the first comment). Final-year BBA student, looking for data analyst internships — happy to hear where this analysis is weak.

#DataAnalytics #SQL #Python #Excel #CustomerAnalytics #RFM #DataAnalyst

## First comment

Repo (queries, charts, workbook): https://github.com/hrishitprakash2-debug/customer-rfm-analysis

Data: UCI Online Retail II. 1,067,371 raw rows in, 1,007,913 analysed after dropping cancellations, returns, zero-price lines and duplicates — counts are in data_quality.json.
