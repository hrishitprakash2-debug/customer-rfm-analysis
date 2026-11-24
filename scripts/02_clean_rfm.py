"""
02_clean_rfm.py — Online Retail II -> clean transactions, RFM table, cohort matrix.

Every exclusion is counted, because "unknown customer" and "cancellation" are
different populations and lumping them together destroys both analyses:
  * a cancelled invoice is a reversed order, not a purchase
  * a NULL Customer ID is a guest checkout, so it cannot enter an RFM model
Nothing is imputed — customers without an ID are simply out of scope for RFM.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW, CLEAN = ROOT / "data" / "raw" / "transactions.csv", ROOT / "data" / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW, encoding="utf-8", low_memory=False)
rows_in = len(df)
log: dict = {"source": "UCI Online Retail II (real UK online retailer, 2009-2011)",
             "rows_in": rows_in}

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df["Invoice"] = df["Invoice"].astype(str).str.strip()
df["is_cancellation"] = df["Invoice"].str.upper().str.startswith("C")

drops = {}
drops["unparseable_invoice_date"] = int(df["InvoiceDate"].isna().sum())
df = df[df["InvoiceDate"].notna()]

drops["cancelled_invoices"] = int(df["is_cancellation"].sum())
df = df[~df["is_cancellation"]]

drops["non_positive_quantity"] = int((df["Quantity"] <= 0).sum())
df = df[df["Quantity"] > 0]

drops["non_positive_price"] = int((df["Price"] <= 0).sum())
df = df[df["Price"] > 0]

drops["duplicate_rows"] = int(df.duplicated().sum())
df = df.drop_duplicates()

drops["missing_customer_id"] = int(df["CustomerID"].isna().sum())
customers_df = df[df["CustomerID"].notna()].copy()

df["line_total"] = df["Quantity"] * df["Price"]
customers_df["line_total"] = customers_df["Quantity"] * customers_df["Price"]
df["month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

customers_df["CustomerID"] = customers_df["CustomerID"].astype(int)
snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# ------------------------------------------------------------------ RFM
g = customers_df.groupby("CustomerID")
rfm = pd.DataFrame({
    "last_purchase": g["InvoiceDate"].max(),
    "first_purchase": g["InvoiceDate"].min(),
    "frequency": g["Invoice"].nunique(),
    "monetary": g["line_total"].sum(),
    "items": g["Quantity"].sum(),
    "country": g["Country"].first(),
})
rfm["recency"] = (snapshot - rfm["last_purchase"]).dt.days


def score(series: pd.Series, higher_is_better: bool) -> pd.Series:
    """Quintile score 1-5 where 5 is always the desirable end.

    rank() is ascending, so rank 1 is the *smallest* value. Labels are then
    reversed for recency (small is good) and kept for frequency/monetary
    (large is good). Ties are broken by rank so qcut never fails on equal edges.
    """
    r = series.rank(method="first", ascending=True)
    labels = [1, 2, 3, 4, 5] if higher_is_better else [5, 4, 3, 2, 1]
    return pd.qcut(r, 5, labels=labels).astype(int)


rfm["r_score"] = score(rfm["recency"], higher_is_better=False)
rfm["f_score"] = score(rfm["frequency"], higher_is_better=True)
rfm["m_score"] = score(rfm["monetary"], higher_is_better=True)


def segment(r: int, f: int, m: int) -> str:
    if r >= 4 and f >= 4:
        return "Champions"
    if r >= 3 and f >= 3:
        return "Loyal"
    if r >= 4 and f <= 2:
        return "New / Promising"
    if r == 3 and f <= 2:
        return "Needs Attention"
    if r <= 2 and m >= 4:
        return "At Risk (high value)"
    if r <= 2 and f >= 3:
        return "Can't Lose"
    return "Hibernating"


rfm["segment"] = [segment(r, f, m) for r, f, m in
                  zip(rfm.r_score, rfm.f_score, rfm.m_score)]
rfm["aov"] = rfm["monetary"] / rfm["frequency"]
rfm["tenure_days"] = (rfm["last_purchase"] - rfm["first_purchase"]).dt.days
rfm = rfm.reset_index()

# ------------------------------------------------------- cohort retention
cust_month = customers_df.assign(month=customers_df["InvoiceDate"].dt.to_period("M"))
cohort = cust_month.groupby("CustomerID")["month"].min().rename("cohort_month")
act = cust_month[["CustomerID", "month"]].drop_duplicates().merge(
    cohort, on="CustomerID")
act["offset"] = (act["month"].astype("period[M]") - act["cohort_month"].astype("period[M]")).apply(lambda x: x.n)
size = cohort.value_counts().sort_index()
matrix = (act.groupby(["cohort_month", "offset"])["CustomerID"].nunique()
          .unstack(fill_value=0).sort_index())
retention = matrix.div(size, axis=0).mul(100).round(1)
retention.index = retention.index.astype(str)

# ------------------------------------------------------------- outputs
keep = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price",
        "CustomerID", "Country", "line_total", "month"]
df[keep].to_csv(CLEAN / "transactions_clean.csv", index=False, encoding="utf-8")
rfm.to_csv(CLEAN / "customers_rfm.csv", index=False, encoding="utf-8")
retention.to_csv(CLEAN / "cohort_retention.csv", encoding="utf-8")

log.update({
    "drops": drops,
    "rows_out_transactions": int(len(df)),
    "rows_out_customer_transactions": int(len(customers_df)),
    "customers": int(rfm.shape[0]),
    "snapshot_date": str(snapshot.date()),
    "period": [str(df.InvoiceDate.min().date()), str(df.InvoiceDate.max().date())],
    "revenue_total": round(float(df.line_total.sum()), 2),
    "revenue_identified_customers": round(float(customers_df.line_total.sum()), 2),
    "guest_revenue_pct": round(float(df[df.CustomerID.isna()].line_total.sum()
                                     / df.line_total.sum() * 100), 2),
    "repeat_customer_pct": round(float((rfm.frequency > 1).mean() * 100), 1),
    "one_time_customers": int((rfm.frequency == 1).sum()),
})
checks = {
    "rows_out_equals_rows_in_minus_drops": len(df) == rows_in - sum(drops.values()) + drops["missing_customer_id"],
    "no_negative_line_totals": bool((df.line_total > 0).all()),
    "rfm_customer_count_positive": rfm.shape[0] > 0,
    "rfm_scores_within_1_5": bool(rfm[["r_score", "f_score", "m_score"]].stack().between(1, 5).all()),
    "cohort_matrix_pct_within_0_100": bool((retention.stack() <= 100.01).all()),
}
log["integrity_checks"] = checks
log["integrity_passed"] = all(checks.values())
(CLEAN / "data_quality.json").write_text(json.dumps(log, indent=2), encoding="utf-8")

print(f"transactions: {rows_in:,} -> {len(df):,}")
print("drops:", drops)
print(f"customers: {len(rfm):,} | revenue: {log['revenue_total']:,.0f} | guest revenue: {log['guest_revenue_pct']}%")
print("integrity:", "PASS" if log["integrity_passed"] else "FAIL", checks)
print(rfm.groupby("segment").agg(customers=("CustomerID", "count"),
                                 revenue=("monetary", "sum")).sort_values("revenue", ascending=False))
