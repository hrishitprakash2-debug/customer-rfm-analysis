"""05_charts.py — RFM segment value, cohort retention, concentration, trend."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent
RES, OUT = ROOT / "output" / "sql_results", ROOT / "charts"
OUT.mkdir(exist_ok=True)

ORANGE, INK, GREY, BLUE, GREEN, RED = "#FC8019", "#1A1A1A", "#8A8A8A", "#2E5AAC", "#3FA66A", "#B5452C"
plt.rcParams.update({
    "figure.facecolor": "white", "axes.facecolor": "white", "axes.edgecolor": "#DDDDDD",
    "axes.labelcolor": INK, "text.color": INK, "xtick.color": GREY, "ytick.color": GREY,
    "font.size": 10.5, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 160, "savefig.bbox": "tight", "savefig.pad_inches": 0.3,
})


def q(n):
    return pd.read_csv(RES / f"{n}.csv")


def save(fig, name, note=""):
    if note:
        fig.text(0.5, -0.03, note, ha="center", fontsize=8.5, color=GREY)
    fig.savefig(OUT / name)
    plt.close(fig)
    print("  ->", name)


# 1 — segment: customers vs revenue share --------------------------------
d = q("q02_segment_summary").sort_values("pct_revenue", ascending=True)
fig, ax = plt.subplots(figsize=(11, 5.8))
y = np.arange(len(d))
ax.barh(y - 0.2, d["pct_customers"], height=0.38, color=GREY, alpha=.85, label="% of customers")
ax.barh(y + 0.2, d["pct_revenue"], height=0.38, color=ORANGE, alpha=.95, label="% of revenue")
ax.set_yticks(y); ax.set_yticklabels(d["segment"])
ax.set_xlabel("Share (%)")
ax.set_title("25% of customers generate 69% of revenue")
ax.legend(frameon=False, loc="lower right")
for yy, (c, r) in enumerate(zip(d["pct_customers"], d["pct_revenue"])):
    ax.text(r + 1, yy + 0.2, f"{r:.0f}%", va="center", fontsize=8.5)
save(fig, "01_segment_value.png", "RFM segments · 5,878 customers · £20.5M revenue")

# 2 — cohort retention heatmap -------------------------------------------
d = q("q04_cohort_retention")
piv = d.pivot_table(index="cohort_month_index", columns="month_offset",
                    values="retention_pct").iloc[:18, :13]
# month_index = year*12 + month (month is 1-12), so shift by one before dividing
piv.index = [f"{(int(i)-1)//12}-{(int(i)-1)%12+1:02d}" for i in piv.index]
fig, ax = plt.subplots(figsize=(12, 7))
sns.heatmap(piv, annot=True, fmt=".0f", cmap="Blues", cbar_kws={"label": "% retained"},
            linewidths=.5, linecolor="white", ax=ax, annot_kws={"size": 7.5})
ax.set_xlabel("Months since first purchase")
ax.set_ylabel("Cohort (first purchase month)")
ax.set_title("Retention collapses to ~20% after month 1, then holds")
save(fig, "02_cohort_retention.png",
     "Share of each cohort still buying in month N · first 18 cohorts")

# 3 — Pareto -------------------------------------------------------------
d = q("q03_customer_pareto")
fig, ax = plt.subplots(figsize=(10, 5.4))
ax.plot(d["customer_rank"], d["cumulative_pct_of_revenue"], marker="o", color=ORANGE, lw=2.4)
for _, r in d.iterrows():
    ax.annotate(f"{r.customer_rank}: {r.cumulative_pct_of_revenue:.0f}%",
                (r.customer_rank, r.cumulative_pct_of_revenue),
                textcoords="offset points", xytext=(6, -10), fontsize=8.5)
ax.set_xscale("log")
ax.set_xlabel("Customers, ranked by revenue (log scale)")
ax.set_ylabel("Cumulative % of revenue")
ax.set_title("100 customers are half the business")
save(fig, "03_customer_pareto.png",
     "5,878 identified customers · top account alone is 15.1% of revenue")

# 4 — monthly revenue ----------------------------------------------------
d = q("q06_monthly_revenue")
fig, ax = plt.subplots(figsize=(12, 5))
ax.bar(d["month_label"], d["revenue"] / 1000, color=BLUE, alpha=.85)
ax.set_ylabel("Revenue (£ thousands)")
ax.set_title("Revenue is strongly seasonal: Q4 carries the year")
ax.tick_params(axis="x", rotation=60)
for i, v in enumerate(d["revenue"] / 1000):
    if i in (0, len(d) - 1):
        ax.text(i, v + 20, f"£{v:,.0f}k", ha="center", fontsize=8)
save(fig, "04_monthly_revenue.png", "Dec 2009 – Dec 2011, 25 months")

# 5 — RFM score grid: revenue by R×F -------------------------------------
rfm = pd.read_csv(ROOT / "data" / "clean" / "customers_rfm.csv")
grid = (rfm.pivot_table(index="r_score", columns="f_score", values="monetary", aggfunc="sum")
        .fillna(0) / 1e6)
fig, ax = plt.subplots(figsize=(8.5, 6))
sns.heatmap(grid, annot=True, fmt=".1f", cmap="Oranges", cbar_kws={"label": "Revenue (£M)"},
            linewidths=.6, linecolor="white", ax=ax)
ax.set_xlabel("Frequency score (5 = most orders)")
ax.set_ylabel("Recency score (5 = bought most recently)")
ax.set_title("Where the money sits: recent × frequent")
save(fig, "05_rfm_grid.png", "Revenue by R×F score cell, 1-5 scale")

print("\n5 charts written")
