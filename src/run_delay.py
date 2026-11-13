"""Run one delay measurement from the command line.

Example:
    python src/run_delay.py --cload 4 --slew 50
"""
import argparse

from measure import measure_delay


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cload", type=float, required=True, help="output load in fF")
    parser.add_argument("--slew", type=float, required=True, help="input slew in ps")
    args = parser.parse_args()
    tphl, tplh = measure_delay(args.cload, args.slew)
    print(f"load={args.cload} fF  slew={args.slew} ps  tphl={tphl:.2f} ps  tplh={tplh:.2f} ps")


if __name__ == "__main__":
    main()
