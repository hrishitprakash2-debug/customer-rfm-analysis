"""07_recalc_excel.py — recalc in Excel and diff every headline cell against pandas."""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "output" / "Customer_RFM_Summary.xlsx"
try:
    import win32com.client as win32
except ImportError:
    sys.exit("pywin32 missing")

xl = win32.DispatchEx("Excel.Application"); xl.Visible = False; xl.DisplayAlerts = False
try:
    wb = xl.Workbooks.Open(str(XLSX.resolve())); xl.CalculateFullRebuild(); wb.Save()
    wb.Close(SaveChanges=True); print("Excel recalculation: done")
finally:
    xl.Quit()

rfm = pd.read_csv(ROOT / "data" / "clean" / "customers_rfm.csv")
exp = {
    "customers": len(rfm),
    "revenue": round(rfm.monetary.sum(), 2),
    "avg_ltv": round(rfm.monetary.mean(), 2),
    "avg_orders": round(rfm.frequency.mean(), 4),
    "repeat_rate": round((rfm.frequency > 1).mean(), 6),
    "dormant_share": round((rfm.recency > 180).mean(), 6),
}
ws = load_workbook(XLSX, data_only=True)["Summary"]
got = {"customers": ws["B6"].value, "revenue": ws["D6"].value, "avg_ltv": ws["F6"].value,
       "avg_orders": ws["H6"].value, "repeat_rate": ws["J6"].value, "dormant_share": ws["L6"].value}
seg_row = {ws.cell(row=r, column=2).value: r for r in range(10, 25)}
champ = rfm[rfm.segment == "Champions"]
exp["champion_revenue_share"] = round(champ.monetary.sum() / rfm.monetary.sum(), 6)
got["champion_revenue_share"] = ws.cell(row=seg_row["Champions"], column=6).value

print(f"\n{'metric':<26}{'Excel':>16}{'pandas':>16}{'match':>9}")
print("-" * 68)
bad = []
for k, v in exp.items():
    g = got.get(k)
    ok = g is not None and abs(float(g) - v) <= max(0.01, abs(v) * 0.005)
    if not ok: bad.append(k)
    print(f"{k:<26}{str(round(float(g),4) if isinstance(g,float) else g):>16}"
          f"{str(round(v,4) if isinstance(v,float) else v):>16}{'OK' if ok else 'MISMATCH':>9}")
print("\n" + ("ALL CHECKS PASS — workbook matches pandas" if not bad else f"MISMATCHES: {bad}"))
