"""Plot delay vs. output load for each input slew.

Example:
    python src/plot_results.py
"""
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display needed
import matplotlib.pyplot as plt  # noqa: E402

RESULTS = Path(__file__).resolve().parent.parent / "results"


def load_rows(path):
    with path.open() as f:
        return list(csv.DictReader(f))


def main():
    rows = load_rows(RESULTS / "delay_table.csv")
    by_slew = defaultdict(list)
    for r in rows:
        by_slew[int(r["slew_ps"])].append(r)

    fig, ax = plt.subplots(figsize=(6, 4))
    for slew, group in sorted(by_slew.items()):
        group.sort(key=lambda r: int(r["cload_ff"]))
        loads = [int(r["cload_ff"]) for r in group]
        avg = [(float(r["tphl_ps"]) + float(r["tplh_ps"])) / 2 for r in group]
        ax.plot(loads, avg, marker="o", label=f"input slew {slew} ps")
    ax.set_xlabel("Output load (fF)")
    ax.set_ylabel("Propagation delay, average of tphl and tplh (ps)")
    ax.set_title("CMOS inverter delay vs. load (generic 180 nm model)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    out = RESULTS / "delay_vs_load.png"
    fig.savefig(out, dpi=150)
    print(f"saved {out.name}")


if __name__ == "__main__":
    main()
