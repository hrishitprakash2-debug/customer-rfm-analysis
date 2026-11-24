"""03_run_queries.py — run every query in sql/queries/ and export results."""
from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
con = sqlite3.connect(ROOT / "data" / "rfm.db")
OUT = ROOT / "output" / "sql_results"; OUT.mkdir(parents=True, exist_ok=True)
files = sorted((ROOT / "sql" / "queries").glob("*.sql"))
md = ["# Query results", ""]
fails = 0
for f in files:
    sql = f.read_text(encoding="utf-8")
    try:
        df = pd.read_sql_query(sql, con)
    except Exception as e:
        fails += 1; print("FAIL", f.stem, e); continue
    df.to_csv(OUT / f"{f.stem}.csv", index=False, encoding="utf-8")
    print(f"  {f.stem:<32} rows={len(df):>3} cols={df.shape[1]:>2}")
    md += [f"## {f.stem}", "", sql.splitlines()[0].replace("-- ", ""), "",
           df.head(10).to_markdown(index=False), ""]
con.close()
(ROOT / "output" / "sql_findings.md").write_text("\n".join(md), encoding="utf-8")
print(f"\n{len(files)-fails}/{len(files)} queries OK")
