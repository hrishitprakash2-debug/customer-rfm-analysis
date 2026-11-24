"""06_build_excel.py — RFM summary workbook; every figure a live formula."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.formatting.rule import DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
rfm = pd.read_csv(ROOT / "data" / "clean" / "customers_rfm.csv")
dq = json.loads((ROOT / "data" / "clean" / "data_quality.json").read_text(encoding="utf-8"))

HDR_F, HDR_B = Font(size=10, bold=True, color="FFFFFF"), PatternFill("solid", fgColor="FC8019")
THIN = Side(style="thin", color="DDDDDD")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

wb = Workbook()
wsd = wb.active
wsd.title = "Customers"
cols = ["CustomerID", "segment", "recency", "frequency", "monetary",
        "r_score", "f_score", "m_score", "aov", "country"]
wsd.append(cols)
for row in rfm[cols].itertuples(index=False):
    wsd.append([None if pd.isna(v) else v for v in row])
N = len(rfm) + 1
for c in range(1, len(cols) + 1):
    wsd.cell(row=1, column=c).font, wsd.cell(row=1, column=c).fill = HDR_F, HDR_B
wsd.freeze_panes = "A2"
wsd.auto_filter.ref = f"A1:J{N}"
D = {n: f"Customers!${get_column_letter(i)}$2:${get_column_letter(i)}${N}"
     for i, n in enumerate(cols, start=1)}

ws = wb.create_sheet("Summary", 0)
ws.sheet_view.showGridLines = False
ws["B2"] = "Customer base — RFM and retention"
ws["B2"].font = Font(size=19, bold=True, color="1A1A1A")
ws["B3"] = (f"{int(dq['customers']):,} identified customers · {int(dq['rows_out_customer_transactions']):,} "
            f"lines · £{dq['revenue_total']:,.0f} net revenue · {dq['period'][0]} to {dq['period'][1]}")
ws["B3"].font = Font(size=9.5, color="666666")

kpis = [
    ("CUSTOMERS", f"=COUNTA({D['CustomerID']})", "#,##0"),
    ("REVENUE", f"=SUM({D['monetary']})", '"£"#,##0'),
    ("AVG LIFETIME VALUE", f"=AVERAGE({D['monetary']})", '"£"#,##0'),
    ("AVG ORDERS", f"=AVERAGE({D['frequency']})", "0.0"),
    ("REPEAT RATE", f'=COUNTIF({D["frequency"]},">1")/COUNTA({D["CustomerID"]})', "0.0%"),
    ("DORMANT 180d+", f'=COUNTIF({D["recency"]},">180")/COUNTA({D["CustomerID"]})', "0.0%"),
]
c = 2
for label, f, fmt in kpis:
    ws.cell(row=5, column=c, value=label).font = Font(size=8.5, color="666666")
    cell = ws.cell(row=6, column=c, value=f)
    cell.font, cell.number_format = Font(size=15, bold=True, color="FC8019"), fmt
    ws.merge_cells(start_row=5, start_column=c, end_row=5, end_column=c + 1)
    ws.merge_cells(start_row=6, start_column=c, end_row=6, end_column=c + 1)
    c += 2
for i in range(2, 14):
    ws.column_dimensions[get_column_letter(i)].width = 15

ws["B8"] = "Segment value — customers vs revenue"
ws["B8"].font = Font(size=12, bold=True)
heads = ["Segment", "Customers", "% of customers", "Revenue", "% of revenue",
         "Avg recency (days)", "Avg orders", "Avg lifetime value"]
for i, h in enumerate(heads, start=2):
    cell = ws.cell(row=9, column=i, value=h)
    cell.font, cell.fill, cell.border = HDR_F, HDR_B, BOX
    cell.alignment = Alignment(horizontal="center", wrap_text=True)

segs = (rfm.groupby("segment").monetary.sum().sort_values(ascending=False).index.tolist())
for i, seg in enumerate(segs, start=10):
    ws.cell(row=i, column=2, value=seg)
    ws.cell(row=i, column=3, value=f'=COUNTIF({D["segment"]},$B{i})').number_format = "#,##0"
    ws.cell(row=i, column=4, value=f'=C{i}/COUNTA({D["CustomerID"]})').number_format = "0.0%"
    ws.cell(row=i, column=5, value=f'=SUMIF({D["segment"]},$B{i},{D["monetary"]})').number_format = '"£"#,##0'
    ws.cell(row=i, column=6, value=f'=E{i}/SUM({D["monetary"]})').number_format = "0.0%"
    ws.cell(row=i, column=7, value=f'=AVERAGEIF({D["segment"]},$B{i},{D["recency"]})').number_format = "0"
    ws.cell(row=i, column=8, value=f'=AVERAGEIF({D["segment"]},$B{i},{D["frequency"]})').number_format = "0.0"
    ws.cell(row=i, column=9, value=f'=AVERAGEIF({D["segment"]},$B{i},{D["monetary"]})').number_format = '"£"#,##0'
    for cc in range(2, 10):
        ws.cell(row=i, column=cc).border = BOX
last = 9 + len(segs)
ws.cell(row=last + 1, column=2, value="TOTAL").font = Font(bold=True)
ws.cell(row=last + 1, column=3, value=f"=SUM(C10:C{last})").font = Font(bold=True)
ws.cell(row=last + 1, column=5, value=f"=SUM(E10:E{last})").font = Font(bold=True)
ws.cell(row=last + 1, column=5).number_format = '"£"#,##0'
ws.conditional_formatting.add(f"E10:E{last}",
    DataBarRule(start_type="num", start_value=0, end_type="max", color="FC8019"))

ch = BarChart(); ch.type = "bar"; ch.style = 2
ch.title = "Revenue by RFM segment"
ch.add_data(Reference(ws, min_col=5, min_row=9, max_row=last), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=2, min_row=10, max_row=last))
ch.height, ch.width, ch.legend = 9, 12, None
ch.x_axis.delete = False; ch.y_axis.delete = False
ch.x_axis.tickLblPos = "nextTo"
for s in ch.series:
    s.graphicalProperties = GraphicalProperties(solidFill="FC8019")
    s.graphicalProperties.line = LineProperties(solidFill="FC8019")
ws.add_chart(ch, "B20")

ws["K8"] = ("=\"Champions are \"&TEXT(C10/COUNTA(" + D["CustomerID"] + "),\"0%\")&\" of customers and \"&TEXT(F10,\"0%\")"
            "&\" of revenue. The win-back pool (At Risk + Hibernating) holds \"&"
            f"TEXT((SUMIF({D['segment']},\"At Risk (high value)\",{D['monetary']})"
            f"+SUMIF({D['segment']},\"Hibernating\",{D['monetary']}))/SUM({D['monetary']}),\"0.0%\")&\" of revenue.\"")
ws["K8"].font = Font(size=10, bold=True, color="B5452C")
ws["K8"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("K8:P11")

m = wb.create_sheet("Method")
m["B2"] = "Data and method"
m["B2"].font = Font(size=16, bold=True)
rows = [
    ("Source", dq["source"]),
    ("Raw rows", f'{dq["rows_in"]:,}'),
    ("Cancelled invoices dropped", f'{dq["drops"]["cancelled_invoices"]:,}'),
    ("Non-positive quantity", f'{dq["drops"]["non_positive_quantity"]:,}'),
    ("Non-positive price", f'{dq["drops"]["non_positive_price"]:,}'),
    ("Duplicate rows", f'{dq["drops"]["duplicate_rows"]:,}'),
    ("Guest lines (no customer ID)", f'{dq["drops"]["missing_customer_id"]:,} — excluded from RFM, '
                                     f'{dq["guest_revenue_pct"]}% of revenue'),
    ("Rows analysed", f'{dq["rows_out_transactions"]:,}'),
    ("Snapshot date for recency", dq["snapshot_date"]),
    ("Scoring", "Quintiles 1-5 via RANK + qcut; 5 is always the desirable end"),
    ("Segment rule", "Champions R>=4 & F>=4; Loyal R>=3 & F>=3; At Risk R<=2 & M>=4; etc."),
    ("Integrity", "all checks PASS" if dq["integrity_passed"] else "FAIL"),
]
for i, (k, v) in enumerate(rows, start=4):
    m.cell(row=i, column=2, value=k).font = Font(bold=True)
    m.cell(row=i, column=3, value=v)
m.column_dimensions["B"].width = 32
m.column_dimensions["C"].width = 74
m.sheet_view.showGridLines = False

out = ROOT / "output" / "Customer_RFM_Summary.xlsx"
wb.save(out)
print(f"saved {out} ({out.stat().st_size/1e6:.2f} MB)")
