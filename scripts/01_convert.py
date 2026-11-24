"""01_convert.py — UCI Online Retail II workbook -> one CSV (streaming, low memory)."""
from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "online_retail_II.xlsx"
OUT = ROOT / "data" / "raw" / "transactions.csv"

wb = load_workbook(SRC, read_only=True, data_only=True)
with OUT.open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate",
                "Price", "CustomerID", "Country"])
    total = 0
    for name in wb.sheetnames:
        n = 0
        for i, row in enumerate(wb[name].iter_rows(values_only=True)):
            if i == 0 or row[0] is None:
                continue
            w.writerow(list(row[:8]))
            n += 1
        print(f"  {name}: {n:,} rows", flush=True)
        total += n
print(f"total: {total:,} -> {OUT.name}")
wb.close()
