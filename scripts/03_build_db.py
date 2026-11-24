"""03_build_db.py — load transactions and the RFM table into SQLite."""
from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CLEAN = ROOT / "data" / "clean"
con = sqlite3.connect(ROOT / "data" / "rfm.db")
con.execute("PRAGMA journal_mode=WAL")
con.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))

tx = pd.read_csv(CLEAN / "transactions_clean.csv", parse_dates=["InvoiceDate"])
rfm = pd.read_csv(CLEAN / "customers_rfm.csv", parse_dates=["first_purchase", "last_purchase"])

d = tx["InvoiceDate"]
dim_date = pd.DataFrame({
    "invoice_date": d.dt.strftime("%Y-%m-%d"),
    "year": d.dt.year, "month": d.dt.month,
    "month_index": d.dt.year * 12 + d.dt.month,
    "month_label": d.dt.strftime("%Y-%m"),
}).drop_duplicates("invoice_date")
dim_date.to_sql("dim_date", con, if_exists="append", index=False)

rfm[["CustomerID", "country"]].rename(columns={"CustomerID": "customer_id"}).to_sql(
    "dim_customer", con, if_exists="append", index=False)
tx[["StockCode", "Description"]].dropna(subset=["StockCode"]).drop_duplicates("StockCode").rename(
    columns={"StockCode": "stock_code", "Description": "description"}).to_sql(
    "dim_product", con, if_exists="append", index=False)

dmap = dict(con.execute("SELECT invoice_date, date_sk FROM dim_date"))
cmap = dict(con.execute("SELECT customer_id, customer_sk FROM dim_customer"))
pmap = dict(con.execute("SELECT stock_code, product_sk FROM dim_product"))

fact = pd.DataFrame({
    "invoice": tx["Invoice"].astype(str),
    "date_sk": d.dt.strftime("%Y-%m-%d").map(dmap),
    "customer_sk": tx["CustomerID"].astype("Int64").map(cmap),
    "product_sk": tx["StockCode"].astype(str).map(pmap),
    "quantity": tx["Quantity"], "price": tx["Price"], "line_total": tx["line_total"],
})
fact.to_sql("fact_sale", con, if_exists="append", index=False, chunksize=100_000)

rfm_out = pd.DataFrame({
    "customer_sk": rfm["CustomerID"].map(cmap),
    "recency_days": rfm["recency"], "frequency": rfm["frequency"], "monetary": rfm["monetary"],
    "r_score": rfm["r_score"], "f_score": rfm["f_score"], "m_score": rfm["m_score"],
    "segment": rfm["segment"], "aov": rfm["aov"], "tenure_days": rfm["tenure_days"],
    "first_purchase": rfm["first_purchase"].dt.strftime("%Y-%m-%d"),
    "last_purchase": rfm["last_purchase"].dt.strftime("%Y-%m-%d"),
}).dropna(subset=["customer_sk"])
rfm_out["customer_sk"] = rfm_out["customer_sk"].astype(int)
rfm_out.to_sql("dim_customer_rfm", con, if_exists="append", index=False)
con.commit()

counts = {t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
          for t in ["fact_sale", "dim_customer", "dim_product", "dim_date", "dim_customer_rfm"]}
orphans = con.execute("""SELECT COUNT(*) FROM fact_sale f
  LEFT JOIN dim_customer c ON c.customer_sk=f.customer_sk
  LEFT JOIN dim_date d ON d.date_sk=f.date_sk
  WHERE f.customer_sk IS NOT NULL AND (c.customer_sk IS NULL OR d.date_sk IS NULL)""").fetchone()[0]
print(counts); print("orphan FKs:", orphans)
print("reconciliation:", "PASS" if counts["fact_sale"] == len(tx) and orphans == 0 and counts["dim_customer_rfm"] == len(rfm) else "FAIL")
con.close()
