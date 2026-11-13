"""Sweep input slew and output load, then write the delay table to CSV.

Example:
    python src/characterize.py
"""
import csv
from pathlib import Path

from measure import measure_delay

CLOADS_FF = [1, 2, 4, 8]
SLEWS_PS = [10, 50, 100]
OUT_CSV = Path(__file__).resolve().parent.parent / "results" / "delay_table.csv"


def main():
    OUT_CSV.parent.mkdir(exist_ok=True)
    rows = []
    for slew in SLEWS_PS:
        for cload in CLOADS_FF:
            tphl, tplh = measure_delay(cload, slew)
            rows.append({"slew_ps": slew, "cload_ff": cload,
                         "tphl_ps": round(tphl, 3), "tplh_ps": round(tplh, 3)})
            print(f"slew={slew:>4} ps  load={cload:>3} fF  tphl={tphl:8.2f}  tplh={tplh:8.2f}")
    with OUT_CSV.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["slew_ps", "cload_ff", "tphl_ps", "tplh_ps"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {OUT_CSV.relative_to(OUT_CSV.parent.parent)}")


if __name__ == "__main__":
    main()
