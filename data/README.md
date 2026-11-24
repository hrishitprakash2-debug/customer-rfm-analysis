# Data provenance

| Item | Detail |
|---|---|
| Dataset | **UCI Online Retail II** |
| Source | `archive.ics.uci.edu/static/public/502/online+retail+ii.zip` |
| Contents | `online_retail_II.xlsx`, two sheets: *Year 2009-2010* (525,461 rows) and *Year 2010-2011* (541,910 rows) |
| Rows | 1,067,371 invoice lines |
| Period | 2009-12-01 → 2011-12-09 |
| Business | A real UK-based registered non-store online retailer (names anonymised by UCI) |

## Columns

`Invoice, StockCode, Description, Quantity, InvoiceDate, Price, CustomerID, Country`

- `Invoice` starting with **C** is a cancellation.
- Negative `Quantity` marks returns/adjustments.
- `Price` of 0 marks free items or data errors.
- `CustomerID` is null for guest checkouts (~15% of revenue).

## Re-download

```bash
curl -sSL -o data/raw/online_retail_ii.zip \
  "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
python -c "import zipfile;zipfile.ZipFile('data/raw/online_retail_ii.zip').extractall('data/raw')"
```

The 45 MB workbook and the 1M-row intermediate CSV are git-ignored. `data/clean/customers_rfm.csv`
and `data/clean/cohort_retention.csv` are committed so the analysis is reproducible without the download.

## Citation

Daqing Chen, Sai Liang Sain, Kun Guo (2012). *Data mining for the online retail industry: A case study
of RFM model-based customer segmentation using data mining.* Journal of Database Marketing & Customer
Strategy Management, 19(3), 197–208.
